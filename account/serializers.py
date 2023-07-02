from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = vendorregistration
        fields = ['email','password']


class VerifyOtpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    class Meta:
            model = vendorregistration
            fields = ['email','otp']


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = vendorregistration
        fields =['email','password']



class SendPasswordResetEmailSerializer(serializers.ModelSerializer):  
    class Meta:
        model = vendorregistration
        fields = ['email']



class UserPasswordResetSerializar(serializers.Serializer):
    
    password = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    
    class Meta:
        model = vendorregistration
        fields = ['otp','password','password2']
        

class VendorProfileSerializer(serializers.ModelSerializer):  
    class Meta:
        model = VendorProfile
        fields = ['vendor','name','profile_picture','age','city','working_or_studying']  

class VendorArtworkSerializer(serializers.ModelSerializer):  
    class Meta:
        model = VendorArtwork
        fields = ['vendor', 'Art_image','themes','price','medium']

class usersSerializer(serializers.ModelSerializer):  
    class Meta:
        model = users
        fields = ['panting', 'name','email','mobile_number','Address']   