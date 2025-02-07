
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import logging

from therapist_webapi.utils import WebInfo

class TherapistAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    logger = logging.getLogger(__name__)
    

    def post(self, request):
        web = WebInfo(request)
        company_id = int(request.COOKIES['company'])
        try:
            to_return = []
            data = request.data
            
            return  Response(to_return, status=status.HTTP_200_OK)

        except Exception as e:
            self.logger.error("error", e)
            return Response({'result': {'message':f'An error happened {str(e)}.'}}, status=status.HTTP_400_BAD_REQUEST)