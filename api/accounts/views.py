import random 
import os
import requests 

from rest_framework import viewsets

from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
from django.db.models import Q

User = get_user_model()

#rest_framework
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework  import permissions
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)



from . models import CustomUser, CountryCodes, OTP
from .serializers import UserSerializer, CountryCodesSerializer, PhoneOtp


User = get_user_model()

#View to authenticate user
class Authenticate(APIView):
     permission_classes = [permissions.AllowAny]

     def post(self, request, format=None):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username  or not password:
            return Response({'error': 'Provide all credintials','status':HTTP_400_BAD_REQUEST})
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials', 'status':HTTP_404_NOT_FOUND})
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user':user.id})


class CreateUser(APIView):
    pass



class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = UserSerializer

@csrf_exempt
@api_view(['GET'])
def country_codes(request):
    codes = CountryCodes.objects.all()
    serializer = CountryCodesSerializer(codes, many=True)
    return JsonResponse(serializer.data, safe=False)



#View to validate phone number
@method_decorator(csrf_exempt, name='dispatch')
class SendOtp(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, format=None):
        phone = request.data.get('phone')
        
        if not phone:
            return Response({'Msg':'Phone number required'})

        else:
            phone = str(phone)
            user = User.objects.filter(phone__iexact = phone)
            if user.exists():
                return Response({'Res':'Phone number already exists'})
            else:
                otp = send_otp(phone=phone)
                if otp:
                    data = {'phone':phone, 'otp':otp}
                    serializer = PhoneOtp(data=data)
                    if serializer.is_valid():
                        serializer.save()                      
                        return Response({'Msg': "Hello, {} your otp is {}".format(phone, otp)})
                    return Response(serializer.errors, status=400)                
                else:
                    return Response({'Res':'OTP can not be sent'}) 
                
        return Response(status=500)

class SendOtpAgain(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, format=None):
        phone = request.data.get('phone')
        
        if not phone:
            return Response({'Msg':'Phone number required'})

        else:
            phone = str(phone)
            user = User.objects.filter(phone__iexact = phone)
            if user.exists():
                return Response({'Res':'Phone number already exists'})
            else:
                obj = OTP.objects.filter(phone__iexact=phone)
                if obj.exists():
                    old = obj.first()
                    if old:
                       old.delete()
                       otp = send_otp(phone)
                else:
                    otp = send_otp(phone)

                if otp:
                    data = {'phone':phone, 'otp':otp}
                    serializer = PhoneOtp(data=data)
                    if serializer.is_valid():
                        serializer.save()                      
                        return Response({'Msg': "Hello, {} your otp is {}".format(phone, otp)})
                    return Response(serializer.errors, status=400)                   
                else:
                    return Response({'Res':'OTP can not be sent'})                  
            return Response({'Msg':'Something went wrong'}) 

        return Response(status=500)


#View to validate phone otp
class ValidateOTP(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, format=None):
        phone = request.data.get('phone')
        sent_otp = request.data.get('sent_otp')

        if phone and sent_otp:
            obj = OTP.objects.filter(phone__iexact=phone)
            if obj.exists():
                old = obj.first()
                if str(sent_otp)==str(old.otp):
                    
                   obj.update(
                       verified = True
                   )
                   return Response({'Msg':'Valid otp'})
                else:
                   return Response({'Msg':'Invalid otp'})
        else:
            return Response({'Msg':'Please provide the otp'})

        return Response({'Msg':'Something went wrong'})


#Send otp
def send_otp(phone=None):
    otp = random.randint(99999,999999)
    if phone:
        # URL = "https://2factor.in/API/R1/?module=TRANS_SMS&apikey=1c3c9b6e-6a8f-11ea-9fa5-0200cd936042&to="+str(phone)+"&from=KMRCHE&templatename=Verify+OTP&var1="+str(phone)+"&var2="+str(otp)
        # if requests.get(URL):
        return otp
    
    return False