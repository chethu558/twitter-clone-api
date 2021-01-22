from django.contrib import admin

from .models import CustomUser, CountryCodes, OTP
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(CountryCodes)
admin.site.register(OTP)
