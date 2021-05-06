from django.contrib import admin
from .models import Tweet, Likes, Comments
# Register your models here.
admin.site.register(Tweet)
admin.site.register(Likes)
admin.site.register(Comments)   
