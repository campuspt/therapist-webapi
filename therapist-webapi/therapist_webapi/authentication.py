from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
import logging

class APIKeyAuthentication(BaseAuthentication):
    logger = logging.getLogger(__name__)
    
    def authenticate(self, request):
        api_key = request.headers.get('X-API-KEY')
        client_ip = self.get_client_ip(request)

        # Check API key
        if api_key != settings.API_SECRET_KEY:
            self.logger.warning(f'Unauthorized API key attempt from {client_ip}')
            raise AuthenticationFailed('Invalid API key')

        # Check if the IP is allowed
        if client_ip not in settings.ALLOWED_API_IPS:
            self.logger.warning(f'Unauthorized IP attempt: {client_ip}')
            raise AuthenticationFailed(f'Unauthorized IP: {client_ip}')

        return (AnonymousUser(), None)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]  # First IP in list
        return request.META.get('REMOTE_ADDR')
