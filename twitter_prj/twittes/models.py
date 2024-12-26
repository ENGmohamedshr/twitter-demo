
from email.mime import image
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.db import models

from accounts.models import User
# Create your models here.

def post_media_directory_path(instance, filename):
    
    return f'{instance.id}/{filename}'

class Post(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    
    text = models.TextField()
    
    img = models.ImageField(upload_to=f'media/imgs/{post_media_directory_path}',
                            blank=True,null=True)
    
    video = models.FileField(upload_to=f'media/videos/{post_media_directory_path}',
                            blank=True, null=True,
                            validators=[FileExtensionValidator(allowed_extensions=['mp4','mkv','mov','avi'])])
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        if not self.text and not self.img and not self.video:
            raise ValidationError('the post must contain at least text or image or video')
        
    
    class Meta:
        ordering =['-created_at']
        
    def __str__(self):
        return f'{self.text} by {self.user} '


class Comment(models.Model):
    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    post = models.ForeignKey(Post , related_name='comments' , on_delete=models.CASCADE)
    comment = models.CharField(max_length=300)
    
    created_at = models.DateTimeField(auto_now_add=True)
    

    
    
    
    def __str__(self):
        return f'{self.comment} on {self.post} by{self.user}'


class CommentReply(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment , on_delete=models.CASCADE , related_name='replyes')
    reply = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.reply} by {self.user} on {self.comment}'

class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    content_type = models.ForeignKey(ContentType , models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_obj = GenericForeignKey('content_type','object_id')
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        unique_together  =('user','content_type','object_id')
        
    def __str__(self) -> str:
        return f'Liked by {self.user.username} on {self.content_obj}'



class Bookmarks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user','post'],name='user_post_unique')
        ]
        
    def __str__(self):
        return f"{self.post} booked by {self.user} at {self.created_at}"