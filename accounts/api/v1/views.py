from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView
from rest_framework.authtoken.models import Token
from .serializers import (RegistrationSerializer, CustomAuthTokenSerializer, 
                          CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer, 
                          CustomTokenVerifySerializer, UserProfileSerializer)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomTokenObtainPairSerializer

from django.core.mail import send_mail
from django.urls import reverse
from .utils import generate_verification_token

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import confirm_verification_token
from ...models import User

class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'email':serializer.validated_data['email']
            }
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
    def post(self, request, *args,**kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id':user.pk,
            'email':user.email
        })
        
        
class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        request.user.auth_token.delete()
        return Response (status=status.HTTP_204_NO_CONTENT)
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

class CustomTokenVerifyView(TokenVerifyView):
    serializer_class = CustomTokenVerifySerializer
    
    
def send_verification_email(user):
    token = generate_verification_token(user.email)
    verification_link = f"http://127.0.0.1:8000/api/accounts/verify-email/?token={token}"
    send_mail(
        'Verify your email',
        f'Click the link to verify your account: {verification_link}',
        'from@example.com',
        [user.email],
        fail_silently=False,
    )
    
class VerifyEmailView(APIView):
    def get(self, request):
        token = request.GET.get('token')
        email = confirm_verification_token(token)
        if not email:
            return Response({'error': 'Invalid or expired token'}, status=400)
        try:
            user = User.objects.get(email=email)
            user.is_verified = True
            user.save()
            return Response({'message': 'Email verified successfully'}, status=200)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user