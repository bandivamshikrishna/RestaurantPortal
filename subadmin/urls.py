from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/',views.subadmin_dashboard,name='subadmin-dashboard'),

    path('addtable/',views.subadmin_add_table,name='subadmin-add-table'),
    path('viewtables/',views.subadmin_view_tables,name='subadmin-view-tables'),
    path('edittable/<int:id>/',views.subadmin_edit_table,name='subadmin-edit-table'),
    path('deletetable/<int:id>/',views.subadmin_delete_table,name='subadmin-delete-table'),


    path('addfood/',views.subadmin_add_food,name='subadmin-add-food'),
    path('viewfoods/',views.subadmin_view_foods,name='subadmin-view-foods'),
    path('editfood/<int:id>/',views.subadmin_edit_food,name='subadmin-edit-food'),
    path('deletefood/<int:id>/',views.subadmin_delete_food,name='subadmin-delete-food'),


    path('addrestUsers/',views.subadmin_add_restusers,name='subadmin-add-rest-users'),
    path('viewusers/',views.subadmin_view_users,name='subadmin-view-users'),
    path('deleteusers/<int:id>/',views.subadmin_delete_users,name='subadmin-delete-users'),

    path('viewtableorders/',views.subadmin_view_table_orders,name='subadmin-view-table-orders'),
    path('viewfooddeliveries/',views.subadmin_view_food_deliveries,name='subadmin-view-food-deliveries'),

    # path('editprofile/',views.subadmin_edit_profile,name='subadmin-edit-profile'),

]
