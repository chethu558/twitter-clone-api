from django.contrib import admin

from .models import Users, CountryCodes, OTP, Profile
# Register your models here.

admin.site.register(Users)
admin.site.register(CountryCodes)
admin.site.register(OTP)
admin.site.register(Profile)
