"""
URL configuration for RestaurantPoratal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('login/',views.user_login,name='login'),
    path('getusergroup/',views.get_usergroup,name='get-usergroup'),
    path('userchangepassword/',views.user_change_password,name='user-change-password'),
    path('usereditprofile/',views.user_edit_profile,name='user-edit-profile'),
    path('logout/',views.user_logout,name='logout'),


    path('admindashboard/',views.admin_dashboard,name='admin-dashboard'),

    path('adminaddrestaurant/',views.admin_add_restaurant,name='admin-add-restaurant'),
    path('adminviewrestaurant/',views.admin_view_restaurant,name='admin-view-restaurant'),
    path('admineditrestaurant/<int:id>/',views.admin_edit_restaurant,name='admin-edit-restaurant'),
    path('admindeleterestaurant/<int:id>/',views.admin_delete_restaurant,name='admin-delete-restaurant'),


    path('adminaddsubadmins/',views.admin_add_subadmins,name='admin-add-subadmins'),
    path('adminviewsubadmins/',views.admin_view_subadmins,name='admin-view-subadmins'),
    path('admindeletesubadmins/<int:id>/',views.admin_delete_subadmins,name='admin-delete-subadmins'),

    path('adminreports/',views.admin_reports,name='admin-reports'),
    path('adminviewrequests/',views.admin_view_requests,name='admin-view-reports'),

  

    path('subadmin/',include('subadmin.urls')),
    path('customer/',include('customer.urls')),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
