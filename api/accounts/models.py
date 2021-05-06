from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator,  EmailValidator

# Create your models here.

class Users(AbstractUser):
    username = models.CharField(max_length=255, unique=True, null=True, blank=False)
    phone = models.CharField(max_length=10, unique=True, null=True, blank=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    email = models.EmailField(max_length=255, unique=True, null=True, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CountryCodes(models.Model):
    iso_codes = models.CharField(max_length=10, null=False, blank=False, default='IN')
    code = models.IntegerField(null=False, blank=False)
  
    def __str__(self):
        return str(self.code)



class OTP(models.Model):
    phone_reg = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Invalide phone number")
    phone = models.CharField(max_length=13, blank=False, null=False, unique=True, validators=[phone_reg])
    otp = models.CharField(max_length=6, blank=False, null=False, unique=False)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.phone)+'s otp'


class Profile(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    avatar = models.ImageField(default="default.jpg", upload_to="profile_pics")
    backgroung_img = models.ImageField(default="default.jpg", upload_to="background_pics")
    title = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=256, null=True)
    url = models.CharField(max_length=100, null=True)
    dob = models.DateField(auto_now=False, auto_now_add=False, null=True)
    location = models.CharField(max_length=100, null=True)

    
    def __str__(self):
        return self.user.phone + ' Profile'



@receiver(post_save, sender=Users)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Users)
def save_profile(sender, instance, **kwargs):
        instance.profile.save()






