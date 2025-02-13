from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
import logging
import ipaddress

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
        if not self.is_ip_allowed(client_ip):
            self.logger.warning(f'Unauthorized IP attempt: {client_ip}')
            raise AuthenticationFailed(f'Unauthorized IP: {client_ip}')

        return (AnonymousUser(), None)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]  # First IP in list
        return request.META.get('REMOTE_ADDR')
    
    def is_ip_allowed(self, client_ip):
        client_ip_obj = ipaddress.ip_address(client_ip)
        for allowed in settings.ALLOWED_API_IPS:
            try:
                if '/' in allowed:  # Check if it's a subnet
                    if client_ip_obj in ipaddress.ip_network(allowed, strict=False):
                        return True
                elif client_ip == allowed:  # Exact match for single IP
                    return True
            except ValueError:
                self.logger.warning(f'Invalid IP format in settings: {allowed}')
        return False