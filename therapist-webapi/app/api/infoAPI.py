
from django.utils import timezone
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import logging

class InfoAPI(APIView):
    permission_classes = [AllowAny]  # Only allow authenticated users
    
    logger = logging.getLogger(__name__)
    
    current = timezone.now()

    def get(self, request):
        return  Response({'result': {'company':'Campus Physical Therapy Inc.', 'status' : 'RUNNING', 'lastLaunch': self.current.strftime('%Y-%m-%d %H:%M:%S')}}, status=status.HTTP_200_OK)