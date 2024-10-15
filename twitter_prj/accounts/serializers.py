import email
import re
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.Serializer):
    
    class Meta:
        model = User
        exclude = ['password','is_active']
        
        

class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 250)
    email = serializers.EmailField()
    password = serializers.CharField(write_only =True)
    
    def validate_username(self ,value):
        pattern =r'^[a-z0-9]+(_[a-z-0-9]+)*$'
        
        if not re.match(pattern,value):
            raise ValueError("can't accept spaces of special characters")
        
        return value
    
    def create(self , validated_data):
        user =User(username = validated_data['username'],
                   email = validated_data['email'])
        
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    class Meta:
        model = User
        fields = ['username','email','password']

class ProfileSerializer(serializers.Serializer):
    class Meta:
        model = Profile
        fields = '__all__'
        
        
        

class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    class Meta:
        model = User 
        fields = ['email']
        
        
class ChangePasswordSerializer(serializers.Serializer):
    
    password1 = serializers.CharField(write_only = True)
    password2 = serializers.CharField(write_only = True)
    
    def validate(self, data):
        
        if data.get('password1') != data.get('password2'):
            raise serializers.ValidationError("password doesn't match".capitalize())
            
        return data