from django.db import models
from django.contrib.auth import get_user_model 

class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), unique=True, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=30, default='匿名')
    zipcode = models.CharField(max_length=8, default='')
    prefecture = models.CharField(max_length=6, default='')
    city = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=30, default='')
