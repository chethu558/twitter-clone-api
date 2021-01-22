from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

from django.core.validators import RegexValidator,  EmailValidator

# Create your models here.

class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, default="User")
    phone = models.CharField(max_length=10, unique=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    email = models.EmailField(max_length=256, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CountryCodes(models.Model):
    code = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.code



class OTP(models.Model):
    phone_reg = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Invalide phone number")
    phone = models.CharField(max_length=13, blank=False, null=False, unique=True, validators=[phone_reg])
    otp = models.CharField(max_length=6, blank=False, null=False, unique=False)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return str(self.phone)+'s otp'






