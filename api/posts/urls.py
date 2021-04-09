from django.contrib import admin
from django.urls import path,include

from rest_framework.routers import DefaultRouter

#import views
from .import views

router = DefaultRouter()
#router.register(r'', views.UserViewSet)

urlpatterns = [
    path('tweet/', views.Tweets.as_view(), name="tweet"),
]