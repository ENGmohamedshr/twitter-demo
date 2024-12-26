from django.urls import path,include
from rest_framework.routers import DefaultRouter 
from . import views

urlpatterns = [
    path('',views.PostListCreateApiView.as_view()),
    path('<int:pk>/' , views.PostRetrieveUpdateDestroyApiView.as_view(), name='post_details'),
    path('<int:post_id>/comment/',views.CommentListCreateAPIView.as_view()),
    path('<int:post_id>/comment/<int:pk>/',views.CommentRetrieveUpdateDeleteAPIview.as_view()),
    path('<int:post_id>/comment/<int:comment_id>/reply/',views.CommentReplyListCreateAPIView.as_view()),
    path('<int:post_id>/comment/<int:comment_id>/reply/<int:pk>/',views.CommentReplyRetrieveUpdateDeleteAPIView.as_view()),
    path('bookmarks/', views.BookmarkListAPIView.as_view(), name ="list_bookmark"),
    path('bookmarks/<int:post_id>/', views.BookmarkRetrieveCreateDestoryAPIView.as_view(), name ="retrive_bookmark"),
]