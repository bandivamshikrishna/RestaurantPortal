from django.shortcuts import render,HttpResponseRedirect,redirect
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import login,logout,authenticate,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RestaurantForm
from .models import Restaurant
from django.contrib.auth.models import Group,User
from subadmin.models import Food,SubAdmin
from subadmin.forms import SubAdminForm,SubAdminUpdateForm
from customer.forms import CustomerCUForm
from core.forms import UserForm,UserUpdateForm
import matplotlib
import matplotlib.pyplot as plt,io,urllib, base64,numpy as np


# Create your views here.
def home(request):
    restaurants = Restaurant.objects.all()
    breakfast = Food.objects.filter(category='BreakFast')[0] if len(Food.objects.filter(category='BreakFast')) > 0 else ''
    lunch =  Food.objects.filter(category='Lunch')[0] if len(Food.objects.filter(category='Lunch')) > 0 else ''
    dinner = Food.objects.filter(category='Dinner')[0] if len(Food.objects.filter(category='Dinner')) > 0 else ''
    context = {
            'restaurants':restaurants,
            'breakfast':breakfast,
            'lunch':lunch,
            'dinner':dinner,
    }
    return render(request,'core/home.html',context=context)




def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            auth_form = AuthenticationForm(request=request,data=request.POST)
            if auth_form.is_valid():
                username = auth_form.cleaned_data.get('username')
                password = auth_form.cleaned_data.get('password')
                user = authenticate(username=username,password=password)
                if user is not None:
                    login(request,user)
                    return HttpResponseRedirect('/getusergroup/')
        else:
            auth_form = AuthenticationForm()
        return render(request,'core/login.html',{'authform':auth_form})
    else:
        return HttpResponseRedirect('/getusergroup/')
    

@login_required(login_url='login')
def get_usergroup(request):
    if request.user.groups.filter(name='CUSTOMER').exists():
        return redirect('customer-dashboard')
    if request.user.groups.filter(name='SUBADMIN').exists():
        return HttpResponseRedirect('/subadmin/dashboard/')
    elif request.user.groups.filter(name='CHEF').exists():
        return redirect('chef-dashboard')
    elif request.user.is_superuser:
        return HttpResponseRedirect('/admindashboard/')
    return HttpResponseRedirect('/login/')



@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')





@login_required(login_url='login')
def user_change_password(request):
    if request.method == 'POST':
        password_form = PasswordChangeForm(user=request.user,data=request.POST)
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request,password_form.user)
            messages.add_message(request,messages.SUCCESS,'Password Changed SuccessFully.')
            if request.user.groups.filter(name='SUBADMIN').exists():
                return redirect('subadmin-edit-profile')
            # elif request.user.groups.filter(name='CHEF').exists():
            #     return redirect('chef-edit-profile')
    else:
        password_form = PasswordChangeForm(user=request.user)

    if request.user.groups.filter(name='SUBADMIN').exists():
        user = 'subadmin'
        base_file = 'subadmin/base.html'
    # elif request.user.groups.filter(name='CHEF').exists(): 
    #     user = 'chef'
    #     base_file = 'chef/base.html'
    elif request.user.groups.filter(name='CUSTOMER').exists():
        user = 'customer'
        base_file = 'customer/base.html'
    return render(request,'core/changepassword.html',{'passwordform':password_form,'user':user,'basefile':base_file})



@login_required(login_url='login')
def user_edit_profile(request):
    if request.user.groups.filter(name='SUBADMIN').exists():
        user_type = 'subadmin'
        base_file = 'subadmin/base.html'
        user = request.user.subadmin
        specific_form_name = SubAdminUpdateForm
        user_form_name = UserUpdateForm
    elif request.user.groups.filter(name='CUSTOMER').exists():
        user_type = 'customer'
        base_file = 'customer/base.html'
        user = request.user.customer
        specific_form_name = CustomerCUForm
        user_form_name = UserUpdateForm
    
    if request.method == 'POST':
        specific_form = specific_form_name(request.POST,request.FILES,instance=user)
        user_form = user_form_name(request.POST,instance=request.user)

        if specific_form.is_valid() and user_form.is_valid():
            user = user_form.save()
            specific_user = specific_form.save(commit=False)
            specific_user.user = user
            specific_user.save()
            messages.add_message(request,messages.SUCCESS,'Profile Updated SuccessFully.')
            return redirect('user-edit-profile')
            
    context = {
        'basefile' : base_file,
        'specificform' : specific_form_name(instance=user),
        'userform' : user_form_name(instance=request.user)
    }

    return render(request,'core/editprofile.html',context=context)



@login_required(login_url='login') 
def admin_dashboard(request):
    return render(request,'admin/dashboard.html')



@login_required(login_url='login')
def admin_add_restaurant(request):
    if request.method=='POST':
        restaurant_form = RestaurantForm(request.POST,request.FILES)
        if restaurant_form.is_valid():
            restaurant_form.save()
            messages.add_message(request,messages.SUCCESS,'Restaurant Added SuccessFully..')
            restaurant_form = RestaurantForm()
    else:
        restaurant_form = RestaurantForm()
    return render(request,'admin/addrestaurant.html',{'restaurantform':restaurant_form})


@login_required(login_url='login')
def admin_view_restaurant(request):
    restaurants = Restaurant.objects.all()
    return render(request,'admin/viewrestaurant.html',{'restaurants':restaurants})


@login_required(login_url='login')
def admin_edit_restaurant(request,id):
    restaurant_instance = Restaurant.objects.get(id=id)
    if request.method == 'POST':
        restaurant_form = RestaurantForm(request.POST,request.FILES,instance=restaurant_instance)
        if restaurant_form.is_valid():
            restaurant_form.save()
            messages.add_message(request,messages.INFO,'Restaurant Updated SuccessFully.')
            return HttpResponseRedirect('/adminviewrestaurant/')
    else:
        restaurant_form = RestaurantForm(instance=restaurant_instance)
    return render(request,'admin/editrestaurant.html',{'restaurantform':restaurant_form})


@login_required(login_url='login')
def admin_delete_restaurant(request,id):
    restaurant_instance = Restaurant.objects.get(id=id)
    subadmin_instance = SubAdmin.objects.filter(restaurant_id=id)
    restaurant_instance.delete()
    subadmin_instance.delete()
    messages.add_message(request,messages.WARNING,'Restaurant deleted SuccessFully.')
    return HttpResponseRedirect('/adminviewrestaurant/')


@login_required(login_url='login')
def admin_add_subadmins(request):
    if request.method == 'POST':
        subadmin_user_form = UserForm(request.POST)
        subadmin_form = SubAdminForm(request.POST,request.FILES)
        if subadmin_form.is_valid() and subadmin_user_form.is_valid():
            restaurant_name = subadmin_form.cleaned_data.get('restaurant')
            restaurant = Restaurant.objects.get(name=restaurant_name)
            user = subadmin_user_form.save()
            sub_admin = subadmin_form.save(commit=False)
            sub_admin.user = user
            sub_admin.restaurant = restaurant
            sub_admin.save()
            sub_admin_group,group_created = Group.objects.get_or_create(name='SUBADMIN')
            user.groups.add(sub_admin_group)
            messages.add_message(request,messages.SUCCESS,'User Created SuccessFully.')
            subadmin_form = SubAdminForm()
            subadmin_user_form = UserForm()
    else:
        subadmin_form = SubAdminForm()
        subadmin_user_form = UserForm()
    return render(request,'admin/addsubadmins.html',{'subadminform':subadmin_form,'subadminuserform':subadmin_user_form})


@login_required(login_url='login')
def admin_view_subadmins(request):
    sub_admins = SubAdmin.objects.all()
    return render(request,'admin/viewsubadmins.html',{'subadmins':sub_admins})



@login_required(login_url='login')
def admin_delete_subadmins(request,id):
    subadmin = SubAdmin.objects.get(id=id)
    user = User.objects.get(id=subadmin.user_id)
    subadmin.delete()
    user.delete()
    messages.add_message(request,messages.WARNING,'Sub Admin deleted SuccessFully.')
    return HttpResponseRedirect('/adminviewsubadmins/')



@login_required(login_url='login')
def admin_view_requests(request): 
    return render(request,'admin/viewrequests.html')



@login_required(login_url='login')
def admin_reports(request):
    matplotlib.use('Agg')
    plt.plot(range(10))
    fig = plt.gcf()
    #convert graph into dtring buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri =  urllib.parse.quote(string)
    return render(request,'admin/reports.html',{'data':uri})