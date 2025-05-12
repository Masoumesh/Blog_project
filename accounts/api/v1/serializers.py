from rest_framework import serializers
from ...models import User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import (TokenObtainPairSerializer, 
                                                TokenRefreshSerializer, TokenVerifySerializer)
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'password', 'password1']
        
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password1'):
            raise serializers.ValidationError({'detail':'password doesnt match'})
        try:
            validate_password(attrs.get('password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password':list(e.messages)})
            
        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data.pop('password1',None)
        return User.objects.create_user(**validated_data)


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_("Email"), 
        write_only=True)
    password = serializers.CharField(
        label=_("Password"), 
        style={'input_type': 'password'}, 
        trim_whitespace=False,
        write_only=True
        )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), 
                                email=email, password=password)

            if not user:
                msg = _('Access denied: wrong email or password.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Both "email" and "password" are required.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['first_name'] = user.first_name
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['email'] = self.user.email
        data['first_name'] = self.user.first_name
        return data

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data['message'] = "Token refreshed successfully"

        return data
    
class CustomTokenVerifySerializer(TokenVerifySerializer):
    def validate(self, attrs):
        try:
            token = UntypedToken(attrs['token'])
        except TokenError as e:
            raise InvalidToken(e.args[0])
        
        # Add custom success message
        return {"message": "Token is valid"}
    

from rest_framework import serializers
from .models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'is_verified']
        read_only_fields = ['email', 'is_verified']