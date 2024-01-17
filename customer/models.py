from django.db import models
from django.contrib.auth.models import User
from core.models import Restaurant
from subadmin.models import Food,Table


# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    mobile_number = models.PositiveSmallIntegerField()
    pic = models.ImageField(upload_to='Customer/Profile_Pics')

    class Meta:
        db_table = 'django_customer'


class CustomerTableOrders(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    table = models.ForeignKey(Table,on_delete=models.CASCADE)
    food_ids = models.CharField(max_length=500,blank=False,null=True)
    food_quantities = models.CharField(max_length=500,blank=False,null=True)
    date = models.DateTimeField()
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()

    class Meta:
        db_table = 'django_CustomerTableOrders'


quantity = ((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8))
class CustomerFoodOrders(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    date = models.DateTimeField()
    food_ids = models.CharField(max_length=500)
    food_quantities = models.CharField(max_length=500)
    total_price = models.PositiveSmallIntegerField() 
    address1 = models.CharField(max_length=400)
    address2 = models.CharField(max_length=400)
    

    class Meta:
        db_table = 'django_CustomerFoodOrders'

