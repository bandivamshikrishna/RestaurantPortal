from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from matplotlib import table
from .forms import FoodForm,TableForm,SubAdminUpdateForm
from core.forms import UserUpdateForm,UserForm
from .models import Food,Table
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import Group,User
from restUsers.forms import RestUsersCUForm
from restUsers.models import RestUsers
from customer.models import CustomerTableOrders,CustomerFoodOrders

# Create your views here.
@login_required(login_url='login')
def subadmin_dashboard(request):
    request.session['restaurant_id'] = request.user.subadmin.restaurant.id
    return render(request,'subadmin/dashboard.html')


@login_required(login_url='login')
def subadmin_add_table(request):
    if request.method == 'POST':
        table_form = TableForm(request.POST,request.FILES)
        if table_form.is_valid():
            table_no = table_form.cleaned_data.get('number')
            table_seater = table_form.cleaned_data.get('seater')
            table_pic = table_form.cleaned_data.get('pic')
            table = Table.objects.create(number=table_no,seater=table_seater,pic=table_pic,restaurant_id=request.session['restaurant_id'])
            messages.add_message(request,messages.SUCCESS,'Table Added SuccessFully.')
            table_form = TableForm()
    else:
        table_form = TableForm()
    return render(request,'subadmin/addtable.html',{'tableform':table_form})

@login_required(login_url='login')
def subadmin_view_tables(request):
    tables = Table.objects.all()
    return render(request,'subadmin/viewtables.html',{'tables':tables})


@login_required(login_url='login')
def subadmin_edit_table(request,id):
    table_instance = Table.objects.get(id=id)
    if request.method == 'POST':
        table_form = TableForm(request.POST,request.FILES,instance=table_instance)
        if table_form.is_valid():
            table_form.save()
            messages.add_message(request,messages.SUCCESS,'Updated Table SuccessFully.')
            return HttpResponseRedirect('/subadmin/viewtables/')
    else:
        table_form = TableForm(instance=table_instance)
    return render(request,'subadmin/edittable.html',{'tableform':table_form})



@login_required(login_url='login')
def subadmin_delete_table(request,id):
    table = Table.objects.get(id=id).delete()
    messages.add_message(request,messages.WARNING,'Table deleted SuccessFully.')
    return HttpResponseRedirect('/subadmin/viewtables/')


@login_required(login_url='login')
def subadmin_add_food(request):
    if request.method == 'POST':
        food_form = FoodForm(request.POST,request.FILES)
        if food_form.is_valid():
            fd_name = food_form.cleaned_data.get('name')
            fd_category = food_form.cleaned_data.get('category')
            fd_pic = food_form.cleaned_data.get('pic')
            fd_price = food_form.cleaned_data.get('price')
            Food.objects.create(name=fd_name,category=fd_category,pic=fd_pic,price=fd_price,restaurant_id=request.session['restaurant_id'])
            messages.add_message(request,messages.SUCCESS,'Food Added SuccessFully.')
            food_form = FoodForm()
    else:
        food_form = FoodForm()
    return render(request,'subadmin/addfood.html',{'foodform':food_form})


@login_required(login_url='login')
def subadmin_view_foods(request):
    foods = Food.objects.all()
    return render(request,'subadmin/viewfoods.html',{'foods':foods})


@login_required(login_url='login')
def subadmin_edit_food(request,id):
    food_instance = Food.objects.get(id=id)
    if request.method == 'POST':
        food_form = FoodForm(request.POST,request.FILES,instance=food_instance)
        if food_form.is_valid():
            food_form.save()
            messages.add_message(request,messages.SUCCESS,'Food Updated SuccessFully')
            return HttpResponseRedirect('/subadmin/viewfoods/')
    else:
        food_form = FoodForm(instance=food_instance)
    return render(request,'subadmin/editfood.html',{'foodform':food_form})


@login_required(login_url='login')
def subadmin_delete_food(request,id):
    food = Food.objects.get(id=id)
    food.delete()
    messages.add_message(request,messages.WARNING,'Food deleted SuccessFully.')
    return HttpResponseRedirect('/subadmin/viewfoods/')



@login_required(login_url='login')
def subadmin_add_restusers(request):
    if request.method == 'POST':
        ru_form = RestUsersCUForm(request.POST,request.FILES)
        user_form = UserForm(request.POST)
        if ru_form.is_valid() and user_form.is_valid():
            user = user_form.save()
            mobile_number = ru_form.cleaned_data.get('mobile_number')
            pic = ru_form.cleaned_data.get('pic')
            restaurant_id = request.user.subadmin.restaurant.id
            user_type = ru_form.cleaned_data.get('user_type')
            RestUsers.objects.create(mobile_number=mobile_number,pic=pic,approved=True,user_type=user_type,restaurant_id=restaurant_id,user_id=user.id)
            user_group,group_created = Group.objects.get_or_create(name=user_type.upper())
            user.groups.add(user_group)
            ru_form = RestUsersCUForm()
            user_form = UserForm()
    else:
        ru_form = RestUsersCUForm()
        user_form = UserForm()
    return render(request,'subadmin/addrestusers.html',{'ruform':ru_form,'userform':user_form})


@login_required(login_url='login')
def subadmin_view_users(request):
    rest_users = RestUsers.objects.filter(approved=True)
    return render(request,'subadmin/viewusers.html',{'restusers':rest_users})



@login_required(login_url='login')
def subadmin_delete_users(request,id):
    rest_user = RestUsers.objects.get(id=id)
    user = User.objects.get(id=rest_user.user_id)
    rest_user.delete()
    user.delete()
    messages.add_message(request,messages.SUCCESS,'Chef deleted SuccessFully.')
    return HttpResponseRedirect('/subadmin/viewusers/')



@login_required(login_url='login')
def subadmin_view_table_orders(request):
    tables = Table.objects.filter(restaurant_id=request.user.subadmin.restaurant.id)
    table_orders = [CustomerTableOrders.objects.filter(table_id=table.id) for table in tables]
    return render(request,'subadmin/viewtableorders.html')



@login_required(login_url='login')
def subadmin_view_food_deliveries(request):
    return render(request,'subadmin/viewfooddeliveries.html')





























