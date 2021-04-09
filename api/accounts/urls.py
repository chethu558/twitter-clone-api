from django.contrib import admin
from django.urls import path,include

from rest_framework.routers import DefaultRouter

#import views
from .import views

router = DefaultRouter()
router.register(r'', views.UserViewSet)

urlpatterns = [
    path('authenticate/', views.Authenticate.as_view(), name="authenticate"),
    path('countrycodes/', views.country_codes, name="contry_codes"),
    path('get_otp/', views.SendOtp.as_view(), name="get-otp"),
    # path('resend_otp/otp/', views.SendOtpAgain.as_view(), name="resend-otp"),
    path('verify/otp/', views.ValidateOTP.as_view(), name="verify-otp"),
    path('create_account/', views.create_account, name="create-account"),
    path('logout/<int:id>/', views.signout, name="create-account"),
    path('verify_token/', views.verify_token, name="verify-token")
]