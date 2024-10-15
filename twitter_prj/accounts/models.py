
import os


from datetime import timedelta
from django.utils import timezone
from typing import Any
import uuid
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.deconstruct import deconstructible

# Create your models here.

class UserManger(BaseUserManager):
    
    
    def create_user(self , email , password =None ,**extra_fields ):
        
        if not email:
            raise ValueError('the email is reqired')
        
        if password == None:
            raise ValueError("password can't be None")
        
        if email and password:
            email = self.normalize_email(email)
            user = self.model(email=email ,**extra_fields)
            user.set_password(password)
            user.save()
            return user
        
    def create_superuser(self , email , password,**extra_fields):
        extra_fields.setdefault('is_staff' , True)
        extra_fields.setdefault('is_superuser' , True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    username  =models.CharField(verbose_name='username',max_length=100 ,  unique=True)
    email = models.EmailField(verbose_name='email', max_length=254 , unique=True)
    
    banned = models.BooleanField(default=False)
    
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(verbose_name='superuser status',default=False)

    is_active = models.BooleanField(default=True)
    pro_user = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
    
    objects =UserManger()
    
    def __str__(self) -> str:
        return self.email
    


@deconstructible
class GenerateProfilePic(object):
    
    def __init__(self) -> None:
        pass
    
    def __call__(self , instance , filename  ) -> Any:
        
        ext = filename.split('.')[-1]
        
        path = f'media/accounts/{instance.user.id}/images'
        name  = f'profile_img.{ext}'
        
        return os.path.join(path,name)
    
profile_img_path = GenerateProfilePic()

class Profile(models.Model):
    
    user = models.OneToOneField(User , on_delete=models.CASCADE , related_name='profile')
    
    first_name = models.CharField(verbose_name='first name' , max_length=250)
    last_name = models.CharField(verbose_name='last name' , max_length=250) 
    gender = models.CharField(verbose_name='Gender' , max_length=50 , blank=True )
    img  = models.ImageField(upload_to=profile_img_path)
    
    bio = models.TextField(verbose_name='Bio',max_length=500 , blank=True)
    
    def __str__(self) -> str:
        return self.user.username
    
    
    
    
class SignUpEmailVerficationToken(models.Model):
    user = models.ForeignKey( User,verbose_name=("user"), on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now=True)
    
    
    
    
class ChangePasswordToken(models.Model):
    token = models.UUIDField(default=uuid.uuid4 , unique=True)
    created_at = models.DateTimeField(auto_now=True)
    
    
    def is_valid(self):
        """Check if the token is still valid based on the created_at timestamp."""
        expiration_time = self.created_at + timedelta(minutes=15)  # Set your expiration duration
        return timezone.now() < expiration_time