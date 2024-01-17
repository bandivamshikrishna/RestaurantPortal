from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    pic = models.ImageField(upload_to='Restaurant_Pics/')

    class Meta:
        db_table = 'django_Restaurant'
    
    def __str__(self):
        return self.name


