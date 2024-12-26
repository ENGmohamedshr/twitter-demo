

from django.conf import settings
from django.core.mail import send_mail
from django.db.migrations import serializer
from django.shortcuts import get_object_or_404, render
from rest_framework import mixins, status as st, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *


from .serializers import ChangePasswordSerializer, ForgetPasswordSerializer, ProfileSerializer, SignUpSerializer, UserSerializer

# Create your views here.



class UserViewApi(viewsets.GenericViewSet):
    
    serializer_class = UserSerializer
    
    @action(detail=False , methods=['post'],url_path='sign-up')
    def signUp(self, request , *args, **kwargs):
        try:
            
            serializer = SignUpSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data , status=st.HTTP_201_CREATED)
            else:
                return Response(serializer.errors , status=st.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':str(e)}, status=st.HTTP_400_BAD_REQUEST)
        
    
    
    @action(detail=False , methods=['post'] , url_path='forget-password')
    def forget_password(self , request ,*args, **kwargs):
        serializer = ForgetPasswordSerializer(data =request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            user = get_object_or_404(User , email = email)
            token = ChangePasswordToken()
            token.save()
            
            
            url = f'http://localhost:8000/api/accounts/user/change-password/{user.username}/{token.token}'
            
            
            if user and token:
                send_mail(
                    subject='change password'.capitalize(),
                    message=f'Click on Link to change Your Password : {url}',
                    from_email=settings.DEFAULT_FROM_EMAIL, 
                    recipient_list=[user.email]
                )
                return Response({'message':'check your Email'.capitalize()},status=st.HTTP_200_OK)
            else:
                return Response({'error':'user not Found'.capitalize()},st.HTTP_400_BAD_REQUEST)   
        else:
            return Response(serializer.errors)   





class ProfileViewApi(viewsets.ViewSet):
    
    authentication_classes = [TokenAuthentication]
    
    lookup_field = 'username'
    
    
    def retrieve(self,request, username =None,*args, **kwargs):
        
        
        
        try:
            profile = Profile.objects.get(user__username = username)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data , status=st.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error':str(e)} , status=st.HTTP_400_BAD_REQUEST)
        
        
    
    
    @action(detail=True , methods=['put','patch'])
    def editProfile(self,request,*args, **kwargs):
        
        try:
            serializer = ProfileSerializer(data =request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data , status=st.HTTP_200_OK)
            else :
                return Response(serializer.errors)
            
        except Exception as e:
            return Response({'error':str(e)} , status=st.HTTP_400_BAD_REQUEST)
        
        
    
            
        
class EmailVerficationView(APIView):
    
    def get (self, request , token):
        verfication_token = get_object_or_404(SignUpEmailVerficationToken,token =token)
        user = verfication_token.user 
        user.is_email_verified= True
        
        user.save()
        verfication_token.delete()
        
        return Response({'message':'Email was verified successfully'.capitalize()},status=st.HTTP_200_OK)
    
    
class ChangePasswordView(APIView):
    
    def post(self, request , username,token , *args, **kwargs):
        
        token = get_object_or_404(ChangePasswordToken , token = token)
        
        user = get_object_or_404(User , username = username)
        
        if not token.is_valid():
            return Response({'error ':'invalid or expired token'})
        
        
        serializer =  ChangePasswordSerializer(data = request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password1']
            
            user.set_password(password)
            user.save()
            
            return Response({'message':'password Changed'} , st.HTTP_200_OK)
        else:
            return Response(serializer.errors)

        
            
        
        
        
        