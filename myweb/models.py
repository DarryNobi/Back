from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

# Create your models here.
class Buser(AbstractUser):
    email=models.CharField(max_length=40,blank=True)
    first_name = models.CharField(max_length=20,blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    is_active=models.BooleanField(default=True,blank=True)
    is_staff=models.BooleanField(default=True,blank=True)
    is_superuser=models.BooleanField(default=False,blank=True)
    date_joined=models.DateTimeField(blank=True,default=timezone.now)
    usr_type=models.CharField(max_length=40,blank=True)
    contact_usr=models.CharField(max_length=20,blank=True)
    phone=models.CharField(max_length=20,blank=True)
    enterprise_name=models.CharField(max_length=20,blank=True)

    class Meta():
        permissions = (
            ("city_management", "市政管理"),
            ("agriculture_management", "农业管理"),
            ("forestry_management", "林业管理"),
            ("environment_management", "环境管理"),
            ("road_management", "道路管理"),
            ("settlement_observation", "沉降检测")
        )


class Module(models.Model):
    module_name=models.CharField(max_length=20,blank=True)
    image=models.CharField(max_length=40,blank=True)
    purpose=models.CharField(max_length=20,blank=True)
    create_time=models.DateTimeField(blank=True)
    modify_time=models.DateTimeField(blank=True)
    is_active=models.CharField(max_length=40,blank=True)


class Bmap(models.Model):
    map_name=models.CharField(max_length=20,blank=True)
    create_time=models.DateField(auto_now_add=True)
    #ReceiveTime = models.DateField(default=False, blank=True)
    satelite=models.CharField(max_length=20,blank=True)
    download_times=models.IntegerField(default=0)
    desc=models.TextField(max_length=500,default='Describe This Image')
    thumbnail_path=models.TextField(max_length=500,blank=True,default='')
    downloadfile=models.TextField(max_length=500,blank=True,default='')
    sourcefile=models.TextField(max_length=500,blank=True,default='')
    status=models.BooleanField(default=True,blank=True)
    imagry_type=models.CharField(max_length=20,default='二级影像',blank=True)
    IsUnit8=models.BooleanField(default=False)
