from ast import arg
from typing import OrderedDict
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from core.forms import UserForm,UserUpdateForm
from core.models import Restaurant
import customer
from .forms import CustomerCUForm,CustomerTableOrdersForm
from django.contrib.auth.models import Group
from django.contrib.auth import login
from django.contrib import messages
from subadmin.models import Food, Table
from datetime import datetime
from datetime import date
from .models import CustomerTableOrders,CustomerFoodOrders
import re



# Create your views here.
def customer_sign_up(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        customer_form = CustomerCUForm(request.POST,request.FILES)
        if user_form.is_valid() and customer_form.is_valid():
            user = user_form.save()
            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()
            customer_group,group_created = Group.objects.get_or_create(name='CUSTOMER')
            user.groups.add(customer_group)
            login(request,user)
            return redirect('customer-dashboard')           
    else:
        user_form,customer_form = UserForm(),CustomerCUForm()
    return render(request,'customer/signup.html',{'userform':user_form,'customerform':customer_form})



@login_required(login_url='login')
def customer_dashboard(request):
    return render(request,'customer/dashboard.html')



@login_required(login_url='login')
def customer_book_table(request,type):
    if request.method == 'POST' and type!='foodyes':
        id = int(type)
        table_form = CustomerTableOrdersForm(request.POST)
        table = Table.objects.get(id=id)
        if table_form.is_valid():
            check_in = table_form.cleaned_data.get('check_in')
            check_out = table_form.cleaned_data.get('check_out')
            request.session['table_id'] = table.id
            request.session['check_in'] = str(check_in)
            request.session['check_out'] = str(check_out)
            return render(request,'customer/booktable.html',{'type':'foodmenu','table':table})
        return render(request,'customer/booktable.html',{'table':table,'type':'booking table','tableform':table_form})
    elif request.method == 'POST' and type == 'foodyes':
        all_food_ids = request.POST.getlist('food_Ids[]')
        all_food_quantities = request.POST.getlist('food_quantity[]')
        temp_food_quantities = all_food_quantities

        for i in reversed(range(len(temp_food_quantities))):
            if temp_food_quantities[i] == '':
                all_food_quantities.pop(i)
                all_food_ids.pop(i)
        

        table_id = request.session['table_id']
        check_in_str = request.session['check_in']
        check_out_str = request.session['check_out']
        check_in = datetime.fromisoformat(check_in_str)
        check_out = datetime.fromisoformat(check_out_str)
        customer_id = request.user.customer.id
        date = datetime.now()
        CustomerTableOrders.objects.create(date=date,customer_id=customer_id,table_id=table_id,check_in=check_in,check_out=check_out,food_ids=all_food_ids,food_quantities=all_food_quantities)
        return redirect('customer-dashboard')
    else:
        if type == 'restaurant':
            restaurants = Restaurant.objects.all()
            return render(request,'customer/booktable.html',{'restaurants':restaurants,'type':'restaurant'})
        elif type == 'foodyes':
            restaurant_id = request.session['restauant_id']
            foods = Food.objects.filter(restaurant_id=restaurant_id)
            return render(request,'customer/booktable.html',{'foods':foods,'type':'foodyes'})
        elif type == 'foodno':
            table_id = request.session['table_id']
            check_in_str = request.session['check_in']
            check_out_str = request.session['check_out']
            check_in = datetime.fromisoformat(check_in_str)
            check_out = datetime.fromisoformat(check_out_str)
            customer_id = request.user.customer.id
            date = datetime.now()
            CustomerTableOrders.objects.create(date=date,customer_id=customer_id,table_id=table_id,check_in=check_in,check_out=check_out)
            return redirect('customer-dashboard')
        else:
            id = int(type)
            if Table.objects.filter(restaurant_id=id).exists():
                request.session['restauant_id'] = id
                tables = Table.objects.filter(restaurant_id=id)
                return render(request,'customer/booktable.html',{'tables':tables,'type':'table'})
            elif Table.objects.filter(id=id).exists():
                table = Table.objects.get(id=id)
                table_form = CustomerTableOrdersForm()
                return render(request,'customer/booktable.html',{'table':table,'type':'booking table','tableform':table_form})
            else:
                restaurants = Restaurant.objects.all()
                return render(request,'customer/booktable.html',{'restaurants':restaurants,'type':'restaurant'})



@login_required(login_url='login')
def customer_view_table_bookings(request,args):
    # today = str(date.today())
    # today = today.split('-')
    # today = datetime(int(today[0]), int(today[1]), int(today[2]))
    if args == 'new':
        table_orders_new = CustomerTableOrders.objects.filter(customer_id=request.user.customer.id,check_in__gte=datetime.today()).order_by('check_in')
        context = {
            'tableorders' : table_orders_new,
            'args':args,
        }
    else:
        table_orders_old = CustomerTableOrders.objects.filter(customer_id=request.user.customer.id,check_in__lte=datetime.today()).order_by('check_in')
        context = {
            'tableorders' : table_orders_old,
            'args' : args,
        }
    return render(request,'customer/viewtablebookings.html',context=context)


class FoodItems:
    def __init__(self,id,tno,name,quantity,price,totalprice):
        self.id = id
        self.tno = tno 
        self.name = name
        self.quantity = quantity
        self.price = price
        self.totalprice = totalprice



@login_required(login_url='login')
def customer_view_table_food(request,args,id):
    order = CustomerTableOrders.objects.get(id=id)
    if request.method == 'POST':
        food_ids = request.POST.getlist("food_Ids[]")
        food_quantities = request.POST.getlist("food_Quantities[]")
        temp_food_quantities = food_quantities
        for i in reversed(range(len(temp_food_quantities))):
            if temp_food_quantities[i] == '0':
                food_quantities.pop(i)
                food_ids.pop(i)

        order.food_ids = food_ids
        order.food_quantities = food_quantities

        order.save(update_fields=['food_ids','food_quantities'])
        return redirect('customer-dashboard')
    table_no = order.table.number
    food_ids = re.sub(r'^\[|\]$', '',order.food_ids)
    food_quantities = re.sub(r'^\[|\]$', '',order.food_quantities)
    total_price = 0
    foods = []
    if len(food_ids) > 0:
        food_ids = food_ids.replace('\'','').split(',')
        food_quantities = food_quantities.replace('\'','').split(',')
        for iter,value in enumerate(food_ids):
            food = Food.objects.get(id=value)
            fd_name = food.name
            fd_quantity = food_quantities[iter]
            fd_price = food.price
            fd_totalprice = int(food.price) * int(fd_quantity)
            food_item = FoodItems(value,table_no,fd_name,fd_quantity,fd_price,fd_totalprice)
            foods.append(food_item)
            total_price +=fd_totalprice
    return render(request,'customer/viewtablefood.html',{'foods':foods,'args':args,'totalprice':total_price})



@login_required(login_url='login')
def customer_edit_table(request,args,id):
    if args == 'change-table':
        order_id = int(request.session['order_id'])
        order = CustomerTableOrders.objects.get(id=order_id)
        tables = Table.objects.filter(restaurant_id=order.table.restaurant.id)
        return render(request,'customer/edittable.html',{'tables':tables,'type':args})
    elif request.method == 'POST':
        order_id = int(request.session['order_id'])
        order = CustomerTableOrders.objects.get(id=id)
        table_form = CustomerTableOrdersForm(request.POST,instance=order)
        if table_form.is_valid():
            check_in = table_form.cleaned_data.get('check_in')
            check_out = table_form.cleaned_data.get('check_out')
            table_id = request.POST.get('table.id')
            order.table_id = table_id
            order.date = datetime.now()
            order.check_in = check_in
            order.check_out = check_out
            order.save(update_fields=['date','check_in','check_out','table_id'])
            return redirect('customer-dashboard')
    
    elif args == 'order-id':
        order_id = id
        order = CustomerTableOrders.objects.get(id=id)
        table_form = CustomerTableOrdersForm(instance=order)
        request.session['order_id'] = order_id
        return render(request,'customer/edittable.html',{'tableform':table_form,'ordertable':order})
    elif args == 'table-id':
        table_id = id
        order_id = int(request.session['order_id'])
        order = CustomerTableOrders.objects.get(id=order_id)
        order.table_id = table_id
        table_form = CustomerTableOrdersForm(instance=order)
        return render(request,'customer/edittable.html',{'tableform':table_form,'ordertable':order})



@login_required(login_url='login')
def customer_delete_table(request,id):
    order = CustomerTableOrders.objects.get(id=id)
    order.delete()
    return redirect("/customer/viewtablebookings/new/")



@login_required(login_url='login')
def customer_order_food(request,args):
    if request.method == 'POST':
        food_ids = request.POST.getlist('food_Ids[]')
        food_quantities = request.POST.getlist('food_quantity[]')
        addr1 = re.sub(r'^\[|\]$', '',request.POST['address1'])
        addr2 = re.sub(r'^\[|\]$', '',request.POST['address2'])
        temp_food_quantities = food_quantities
        total_price = 0
        for i in reversed(range(len(temp_food_quantities))):
            if temp_food_quantities[i] == '':
                food_quantities.pop(i)
                food_ids.pop(i)
        
        for iter,value in enumerate(food_ids):
            food = Food.objects.get(id=value)
            total_price += (food.price * int(food_quantities[iter]))
        
        restaurant_id = request.session['restauant_id']
        date = datetime.now()
        customer_id = request.user.customer.id

        CustomerFoodOrders.objects.create(date=date,customer_id=customer_id,address1=addr1,address2=addr2,total_price=total_price,food_ids=food_ids,food_quantities=food_quantities,restaurant_id=restaurant_id)
        return redirect('customer-dashboard')
    else:
        if args == 'restaurants':
            restaurants = Restaurant.objects.all()
            return render(request,'customer/orderfood.html',{'args':args,'restaurants':restaurants})
        else:
            restaurant_id = int(args)
            request.session['restauant_id'] = restaurant_id
            if Food.objects.filter(restaurant_id=restaurant_id).exists():
                foods = Food.objects.filter(restaurant_id=restaurant_id)
                return render(request,'customer/orderfood.html',{'args':'orderfood','foods':foods})


class ViewFoodOrders():
    def __init__(self,orderID,restaurant,foods,food_quantities,address,total_price):
        self.orderID = orderID
        self.restaurant = restaurant
        self.foods = foods
        self.food_quantities = food_quantities
        self.address = address
        self.total_price = total_price
        

@login_required(login_url='login')
def customer_view_food_orders(request,args):
    today = str(date.today())
    today = today.split('-')
    today = datetime(int(today[0]), int(today[1]), int(today[2]))
    overall_foods = []
    if args == 'new':
        foodorders = CustomerFoodOrders.objects.filter(customer_id=request.user.customer.id,date__gte=today)
    else:
        foodorders = CustomerFoodOrders.objects.filter(customer_id=request.user.customer.id,date__lte=today)
    for food in foodorders:
        order_id = food.id
        restaurant = Restaurant.objects.get(id=food.restaurant_id)
        restaurant = restaurant.name + "\n"+restaurant.address
        food_ids = re.sub(r'^\[|\]$', '',food.food_ids)
        food_quantities = re.sub(r'^\[|\]$', '',food.food_quantities)
        food_ids = food_ids.replace('\'','').split(',')
        food_quantities = food_quantities.replace('\'','').split(',')
        food_names = [Food.objects.get(id=food_ids[i]).name for i in range(len(food_ids)) if Food.objects.filter(id=food_ids[i]).exists()]
        address = food.address1 + ", " + food.address2
        total_price = food.total_price

        viewfoodorder = ViewFoodOrders(order_id,restaurant,food_names,food_quantities,address,total_price)
        overall_foods.append(viewfoodorder)

    context = {
        'args' : args,
        'foodorders': overall_foods,
    }
    return render(request,'customer/viewfoodorders.html',context=context)


@login_required(login_url='login')
def customer_view_individual_foods(request,args,id):
    order = CustomerFoodOrders.objects.get(id=id)
    if request.method == 'POST':
        food_ids = request.POST.getlist("food_Ids[]")
        food_quantities = request.POST.getlist("food_Quantities[]")
        temp_food_quantities = food_quantities
        for i in reversed(range(len(temp_food_quantities))):
            if temp_food_quantities[i] == '0':
                food_quantities.pop(i)
                food_ids.pop(i)
        
        order.food_ids = food_ids
        order.food_quantities = food_quantities

        order.save(update_fields=['food_ids','food_quantities'])
        return redirect('customer-dashboard')
    
    food_ids = re.sub(r'^\[|\]$', '',order.food_ids)
    food_quantities = re.sub(r'^\[|\]$', '',order.food_quantities)
    food_ids = food_ids.replace('\'','').split(',')
    food_quantities = food_quantities.replace('\'','').split(',')
    overall_foods = []
    total_price = 0
    for i in range(len(food_ids)):
        food = Food.objects.get(id=food_ids[i])
        fd_name = food.name
        fd_quantity = food_quantities[i]
        fd_price = food.price
        fd_total_price = int(food.price) * int(fd_quantity)
        food_item = FoodItems(food.id,0,fd_name,fd_quantity,fd_price,fd_total_price)
        overall_foods.append(food_item)
        total_price += fd_total_price

    context = {
        'args': args,
        'foodorders': overall_foods,
        'totalprice': total_price
    }
    return render(request,'customer/viewindividualfoods.html',context=context)
































































# @login_required(login_url='login')
# def customer_edit_profile(request):
#     user_form = UserUpdateForm(instance=request.user)
#     customercu_form = CustomerCUForm(instance=request.user.customer)
#     if request.method == 'POST':
#         customercu_form = CustomerCUForm(request.POST,request.FILES,instance=request.user.customer)
#         user_form = UserUpdateForm(request.POST,instance=request.user)
#         if customercu_form.is_valid() and user_form.is_valid():
#             user = user_form.save()
#             customer = customercu_form.save(commit=False)
#             customer.user = user
#             customer.save()
#             messages.add_message(request,messages.SUCCESS,'Profile Updated SuccessFully.')
#             return redirect('customer-edit-profile')
#     return render(request,'customer/editprofile.html',{'userform':user_form,'customercuform':customercu_form})
