from urllib import request
from rest_framework import serializers

from .models import Post , Comment , CommentReply , Like,Bookmarks

from rest_framework.validators import UniqueTogetherValidator


    
    
class CommentReplySerializer(serializers.ModelSerializer):
    
    class Meta:
        model =  CommentReply
        fields = '__all__'
        read_only_fields = ['user','comment']
        
    def validate(self, attrs):
        if not attrs.get('reply'):
            return  serializers.ValidationError('reply can not be blank')
        else :
            return attrs 
    
    
    def update(self, instance, validated_data):
        
        request  = self.context.get('request')
        user  = request.user
        
        if instance.user != user :
            return serializers.ValidationError({'error':'you are not allowed to update this comment'})
        
        
        for key , val in validated_data.items():
            setattr(instance , key , val)
        
        instance.save()
        return instance
    
class LikeSerializer(serializers.Serializer):
    class Meta:
        model = Like
        fields = '__all__'
        
        

class CommentSerializer(serializers.ModelSerializer):
    replyes = CommentReplySerializer(many = True)
    class Meta:
        model= Comment
        exclude = ['post']
        read_only_fields = ['user', 'created_at','replyes']
    
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = {
            'userName':instance.user.username,
            'firstName':instance.user.first_name,
            'lastName':instance.user.last_name,
        }
        representation['replyes'] = instance.replyes.count()
        
        return representation
    
    def validate(self, attrs):
        if not attrs.get('comment'):
            return  serializers.ValidationError('text can not be blank')
        else :
            return attrs 
    
    def update(self, instance, validated_data):
        
        request  = self.context.get('request')
        user  = request.user
        
        if instance.user != user :
            return serializers.ValidationError({'error':'you are not allowed to update this comment'})
        
        
        for key , val in validated_data.items():
            setattr(instance , key , val)
        
        instance.save()
        return instance
    

class PostSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name = 'post_details', read_only= True)
    # comments = CommentSerializer(many =True,read_only = True)
    class Meta:
        model= Post
        fields = ['id','url','user', 'text','img','video','created_at','comments']
        read_only_fields = ['user', 'created_at']
        
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        representation['user'] = {
            'userName':instance.user.username,
            'firstName':instance.user.profile.first_name,
            'lastName':instance.user.profile.last_name,
        }
        representation['comments'] = instance.comments.all().count()
        return representation
        
    
    def validate(self, data):
        if not data.get('text') and not data.get('img') and not data.get('video'):
            raise serializers.ValidationError('the post must contain at least text or image or video')
        return data
    

    
    def update(self, instance, validated_data):
        
        request = self.context.get('request')
        
        user = request.user
        if instance.user != user :
            raise serializers.ValidationError({'error':'you are not allowed to update this Post'.capitalize()})
        
        for key, val in validated_data.items():
            setattr(instance , key, val)
            
        
        instance.save()
        
        return instance


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmarks
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Bookmarks.objects.all(),
                fields=['user','post']
                ,message="this bookmark is saved before"
            )
        ]
        
   