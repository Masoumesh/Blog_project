from django.urls import path, include
from . import views


# from rest_framework.authtoken.views import ObtainAuthToken

app_name = 'api-v1'

urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    # registration
    path('registration/',views.RegistrationApiView.as_view(),name = 'registration'),
    
    # login token
    path('token/login/', views.CustomTokenObtainPairView.as_view(),name='token-login'),
    path('token/logout/', views.CustomDiscardAuthToken.as_view(),name='token-logout'),
    # change password
    # reset password
    
    # login jwt
    path('jwt/create/', views.CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', views.CustomTokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', views.CustomTokenVerifyView.as_view(), name="jwt-verify"),
    
    path('verify-email/', views.VerifyEmailView.as_view(), name='verify-email'),
]
