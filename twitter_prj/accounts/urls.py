from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import EmailVerficationView, UserViewApi,ChangePasswordView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router= DefaultRouter()
router.register(r'user' , UserViewApi , basename='users')

urlpatterns = [
    path('user/verify-email/<uuid:token>/',EmailVerficationView.as_view(),name='verify_email'),
    path('user/change-password/<str:username>/<uuid:token>/',ChangePasswordView.as_view()),
        path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns+= router.urls