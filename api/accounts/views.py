import random 
import os
import requests
import re
from datetime import datetime
import time


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
    HTTP_200_OK,
    HTTP_202_ACCEPTED,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_302_FOUND
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
            return Response({'error': 'Provide all credintials.', 'code':4}, status=HTTP_200_OK)
        user = authenticate(username=username, password=password)
        if not user:
          return Response({'error': 'Invalid Credentials.', 'code':4}, status=HTTP_200_OK)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user':user.id, 'code':3}, status=HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_account(request):
    phone = str(request.data.get("phone"))
    user = User.objects.filter(phone__iexact = phone) 
    
    if user:
        return Response({"message":"User does exist with the phone number", "code":2}, status=HTTP_200_OK)   
    else:
        is_verified = is_phone_verified(phone=phone)
        if is_verified==False:
            return Response({"message":"Your phone number is not verified", "code":4}, status=HTTP_400_BAD_REQUEST)
        else:
            data = request.data
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"Data":serializer.data}, status=HTTP_200_OK)

            return Response({"Data":serializer.errors}, status=HTTP_200_OK)



class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = UserSerializer

@csrf_exempt
@api_view(['GET'])
def country_codes(request): #list the country codes
    codes = CountryCodes.objects.all()
    serializer = CountryCodesSerializer(codes, many=True)
    return Response(serializer.data)



#View to validate phone number
@method_decorator(csrf_exempt, name='dispatch')
class SendOtp(APIView): # function send otp
    permission_classes = [permissions.AllowAny]
    def post(self, request, format=None): 
        phone = request.data.get('phone')
        
        if not phone:
            return Response({'message':'Phone number required.', 'code':0}, status=HTTP_200_OK)

        elif not re.match('^\+?1?\d{9,15}$', phone):
            return Response({'message':'Invalid phone number.', 'code':1}, status=HTTP_200_OK)
       
        elif len(phone) != 10:
            return Response({'message':'Invalid phone number.', 'code':1}, status=HTTP_200_OK)

        else:
            phone = str(phone)
            user = User.objects.filter(phone__iexact = phone) #check if user exists with the phone
            if user.exists():
                return Response({'Res':'Phone number already exists.', 'code':4}, status=HTTP_200_OK)
            else:
                obj = OTP.objects.filter(phone__iexact=phone) #check if otp exists already delete it
                if obj.exists():
                    old = obj.first()
                    if old:
                       old.delete()
                       otp = send_otp(phone=phone)
                else:
                    otp = send_otp(phone=phone)
                
                if otp:
                    data = {'phone':phone, 'otp':otp}
                    serializer = PhoneOtp(data=data)
                    if serializer.is_valid():
                        serializer.save()  #save otp to database               
                        return Response({'message': "Hello, {} your otp is {}".format(phone, otp), 'code':2}, status=HTTP_202_ACCEPTED)
                    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)                
                else:
                    return Response({'message':'OTP can not be sent.', code:5}, status=HTTP_500_INTERNAL_SERVER_ERROR) 
                
        return Response({'message':'Something went wrong.', 'code':5}, status=HTTP_500_INTERNAL_SERVER_ERROR)


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
                sent_time = datetime.timestamp(old.created_at)
                current_time = time.time()
                time_diff = current_time - sent_time

                # print('sent time {}'.format(sent_time))
                # print('current time {}'.format(current_time))
                # print('time diff {}'.format(time_diff))

                if str(sent_otp)==str(old.otp) and time_diff<=600:    
                   obj.update(
                       verified = True
                   )
                   return Response({'message':'Valid otp', 'code':1}, status=HTTP_200_OK)
                else:
                   return Response({'message':'Invalid otp', 'code':0}, status=HTTP_200_OK)
        else:
            return Response({'message':'Please provide the otp', 'code':4}, status=HTTP_200_OK)

        return Response({'message':'Something went wrong', 'code':5}, status=HTTP_500_INTERNAL_SERVER_ERROR)


#Send otp
def send_otp(phone=None):
    otp = random.randint(99999,999999)
    if phone:
        #URL = "https://2factor.in/API/R1/?module=TRANS_SMS&apikey=1c3c9b6e-6a8f-11ea-9fa5-0200cd936042&to="+str(phone)+"&from=KMRCHE&templatename=Verify+OTP&var1="+str(phone)+"&var2="+str(otp)
        #if requests.get(URL):
        return otp
    
    return False 

def is_phone_verified(phone=None):
    obj = OTP.objects.filter(phone__iexact=phone)
    if obj.exists():
        obj = obj.first()
        if  obj.verified == True:
            return True
    return False
    
