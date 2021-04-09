from django.contrib import admin
from django.urls import path,include

from . import views

from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'',views.index)

urlpatterns = [
    path('', views.index, name="index"),
    path('account/', include('api.accounts.urls')),
    path('posts/', include('api.posts.urls')),
]