

from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User,Profile,SignUpEmailVerficationToken

@receiver(post_save , sender =  User)
def createUserProfile(sender, instance , created , *args, **kwargs):
    if created:
        Profile.objects.create(user = instance)
        


@receiver(post_save , sender =  User)
def verifyUserEmail(sender, instance , created , *args, **kwargs):
    print(created)

    if created:
        
        token = SignUpEmailVerficationToken.objects.create(user = instance)
        token.save()
        
    
        url = f'http://localhost:8000/api/accounts/user/verify-email/{token.token}/'
        
        send_mail(
            subject='Verify Email'.capitalize(),
            message=f'Verify your email by click on the link below: {url}',
            from_email=settings.DEFAULT_FROM_EMAIL, 
            recipient_list=[instance.email]
        )
     
    
