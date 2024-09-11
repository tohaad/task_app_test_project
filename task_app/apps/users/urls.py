from django.urls import path
from users.views import UserLoginAPIView, UserRegisterAPIView, UserLogoutAPIView, UserAuthenticationCheckAPIView

urlpatterns = [
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('register/', UserRegisterAPIView().as_view(), name='register'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout'),
    path('auth-check/', UserAuthenticationCheckAPIView.as_view(), name='auth-check')
]
