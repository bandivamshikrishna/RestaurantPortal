from django.db import models
from core.models import Restaurant
from django.contrib.auth.models import User

# Create your models here.
class Table(models.Model):
    number = models.PositiveSmallIntegerField(unique=True)
    seater = models.PositiveSmallIntegerField()
    pic = models.ImageField(upload_to='Table_Pics/')
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)

    class Meta:
        db_table = 'django_table'


categories = (('BreakFast','BreakFast'),('Lunch','Lunch'),('Dinner','Dinner'))
class Food(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100,choices=categories)
    pic = models.ImageField(upload_to='Food_Pics/')
    price = models.PositiveSmallIntegerField()
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)

    class Meta:
        db_table = 'django_food'


class SubAdmin(models.Model):
    restaurant = models.OneToOneField(Restaurant,on_delete=models.CASCADE)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    mobile_number = models.PositiveIntegerField()
    pic = models.ImageField(upload_to='SubAdmin_pics/')

    class Meta:
        db_table = 'django_SubAdmin'