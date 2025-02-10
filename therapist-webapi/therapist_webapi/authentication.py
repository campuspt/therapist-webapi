from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
from therapist_webapi.settings import API_SECRET_KEY

class APIKeyAuthentication(BaseAuthentication):
    
    def authenticate(self, request):
        api_key = request.headers.get('X-API-KEY')
        print(api_key)
        print(API_SECRET_KEY)
        if api_key != API_SECRET_KEY: raise AuthenticationFailed('Invalid API key')
        
        return (AnonymousUser(), None)  # You can return a user object here if needed