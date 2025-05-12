from itsdangerous import URLSafeTimedSerializer
from django.conf import settings

def generate_verification_token(email):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    return serializer.dumps(email, salt='email-verification')

def confirm_verification_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        email = serializer.loads(token, salt='email-verification', max_age=expiration)
    except Exception:
        return None
    return email