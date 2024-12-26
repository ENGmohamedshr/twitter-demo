from rest_framework.mixins import  RetrieveModelMixin, CreateModelMixin , DestroyModelMixin
from rest_framework.generics import ListCreateAPIView , RetrieveUpdateDestroyAPIView,GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status as st
from rest_framework.response import Response
from twittes.permissions import CanEditCommentOrReply
from .models import (Post,
                    Comment, 
                    CommentReply,
                    Like,
                    Bookmarks)
from .serializers import (PostSerializer , 
                        CommentReplySerializer ,
                        CommentSerializer ,
                        LikeSerializer,BookmarkSerializer)





class PostListCreateApiView(ListCreateAPIView):
    queryset =  Post.objects.prefetch_related('comments','user')
    serializer_class = PostSerializer
    
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user = user)
        
        
    def get_serializer_context(self):
        return {'request':self.request}
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]
    
    
class PostRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.select_related('user__profile').prefetch_related('comments')
    serializer_class = PostSerializer
    
    def get_permissions(self):
        if self.request.method == 'get':
            return [AllowAny()]
        else:
            return [CanEditCommentOrReply()]
        
    
    def get_serializer_context(self):
        return {'request':self.request}




class CommentListCreateAPIView(ListCreateAPIView):
    
    serializer_class = CommentSerializer
    
    
    def get_queryset(self):
        post_id = self.kwargs['post_id']
        posts = Comment.objects.filter(post=post_id).prefetch_related('replyes','user')
        return posts
    
    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post =  Post.objects.get(id= post_id)
        serializer.save(user = self.request.user , post = post)
        
        

class CommentRetrieveUpdateDeleteAPIview(RetrieveUpdateDestroyAPIView):
    queryset =  Comment.objects.all()
    serializer_class =  CommentSerializer
    
    
    def get_permissions(self):
        if self.request.method == 'get':
            return [AllowAny()]
        else:
            return [CanEditCommentOrReply()]
        
        
    def get_serializer_context(self):
        
        return {'request':self.request} 
    
    
class CommentReplyListCreateAPIView(ListCreateAPIView):
    queryset =  CommentReply.objects.all()
    serializer_class =  CommentReplySerializer
    
    def perform_create(self, serializer):
        comment_id = self.kwargs['comment_id']
        comment = Comment.objects.get(id= comment_id)
        
        serializer.save(user = self.request.user , comment=comment)
        
    
class CommentReplyRetrieveUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = CommentReply.objects.all()
    serializer_class = CommentReplySerializer
    
    def get_queryset(self):
        comment = Comment.objects.get(id = self.kwargs['comment_id'])
        replyes = CommentReply.objects.filter(comment= comment)
        return super().get_queryset()
    
    def get_permissions(self):
        if self.request.method == 'get':
            return [AllowAny()]
        else:
            return [CanEditCommentOrReply()]
        
    
    def get_serializer_context(self):
        return {'request':self.request}
        

class BookmarkListAPIView(ListAPIView):
    queryset = Bookmarks.objects.all()
    serializer_class = BookmarkSerializer
    
    def get_queryset(self):
        user = self.request.user
        qs = Bookmarks.objects.filter(user= user)
        
        return qs 

class BookmarkRetrieveCreateDestoryAPIView(GenericAPIView,
                                RetrieveModelMixin,
                                CreateModelMixin,
                                DestroyModelMixin
                                ):
    
    
    serializer_class =  BookmarkSerializer
    
    def get(self, request , *args, **kwargs):
        user = request.user
        post_id = kwargs['post_id']
        
        try:
            post = Post.objects.get(id= post_id)
        except Post.DoesNotExist:
            return Response(
                {
                    'detail':"Post Does Not Exist"
                },
                status= st.HTTP_404_NOT_FOUND
            )
        bookmark = get_object_or_404(Bookmarks , user = user ,post = post)
        serializer =  self.get_serializer( bookmark)
        return Response(serializer.data , status=st.HTTP_200_OK)
    
    
    def post(self, request, *args, **kwargs):
        user = request.user 
        post_id = kwargs['post_id']
        
        post = get_object_or_404(Post, id = post_id)
        
        bookmark = {
            "user" : user.id,
            "post":post.id
        }
        serializer = self.get_serializer(data = bookmark)
        
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data , status=st.HTTP_201_CREATED)
            except IntegrityError as e :
                return Response(
                    {
                        'detail':"this bookmark is already saved before "
                    },
                    status=st.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(serializer.errors , status=st.HTTP_400_BAD_REQUEST)
        
    
    def delete(self,request,*args, **kwargs):
        
        user = request.user
        post_id = kwargs['post_id']
        post = get_object_or_404(Post, id = post_id)
        
        bookmark = get_object_or_404(Bookmarks , user = user , post=post)
        
        bookmark.delete()
        
        return Response(
            {
                'detail':"Bookmark is already Deleted"
            },
            status=st.HTTP_204_NO_CONTENT
        )
