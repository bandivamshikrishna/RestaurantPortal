from random import choices
from django.db import models
from django.contrib.auth.models import User
from core.models import Restaurant

# Create your models here.

userTypes = (('receptionist','receptionist'),('barer','barer'),('chef','chef'))
class RestUsers(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    restaurant = models.OneToOneField(Restaurant,on_delete=models.CASCADE)
    mobile_number = models.PositiveSmallIntegerField()
    pic = models.ImageField(upload_to='RestUsers/Profile_Pics/')
    resume = models.FileField(upload_to='RestUsers/Resumes/')
    approved = models.BooleanField(default=False)
    user_type = models.CharField(max_length=100,choices=userTypes)

    class Meta:
        db_table = 'django_RestUsers'