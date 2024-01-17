from django.urls import path
from . import views

urlpatterns = [

    path('signup/',views.customer_sign_up,name='customer-singup'), 
    path('dashboard/',views.customer_dashboard,name='customer-dashboard'),
    # path('editprofile/',views.customer_edit_profile,name='customer-edit-profile'),


    path('booktable/<str:type>/',views.customer_book_table,name='customer-book-table'),
    path('viewtablebookings/<str:args>/',views.customer_view_table_bookings,name='customer-view-table-bookings'),
    path('viewtablefood/<str:args>/<int:id>/',views.customer_view_table_food,name='customer-view-table-food'),
    path('edittable/<str:args>/<int:id>/',views.customer_edit_table,name='customer-edit-table'),
    path('deletetable/<int:id>/',views.customer_delete_table,name='customer-delete-table'),


    path('orderfood/<str:args>/',views.customer_order_food,name='customer-order-food'),
    path('viewfoodorders/<str:args>/',views.customer_view_food_orders,name='customer-view-food-orders'),
    path('viewindividualfoods/<str:args>/<int:id>/',views.customer_view_individual_foods,name='customer-view-individual-foods')
]
