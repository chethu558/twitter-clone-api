from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import authentication_classes, permission_classes

from .models import CustomUser, CountryCodes, OTP

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=CustomUser
        extra_kwargs = {'password':{'write_only':True}}
        fields = ('username', 'phone', 'password', 'email', 'is_active', 'is_staff', 'is_superuser')
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
            instance.save()
            return instance

        

    def update(self, instance, validated_data):
        for key, value in validated_data.item():
            if key == 'password':
                instance.set_password(value)
            else:
                setattr(instance, key, value)
        instance.save()
        return instance

class CountryCodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryCodes
        fields = ['code']


class PhoneOtp(serializers.ModelSerializer):
    #phone = serializers. 
    class Meta:
        model = OTP
        fields = ['phone', 'otp']

        def create(self, validated_data):
            otp = super(PhoneOtp, self).create(validated_data)
            otp.save()
            return True

