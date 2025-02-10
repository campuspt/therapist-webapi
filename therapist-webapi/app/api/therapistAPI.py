
from app.serializers import TherapistSerializer
from app.service.TherapistService import TherapistService
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
import json
import logging
from app.models import Contact, Email, Location, Therapist, Therapist_Attribute, Therapist_Contact, Therapist_Email, Therapist_Location
from therapist_webapi.authentication import APIKeyAuthentication

from therapist_webapi.utils import WebInfo, decrypt_secure_uuid

class TherapistAPI(APIView):
    authentication_classes = [APIKeyAuthentication]
    permission_classes = [AllowAny]
    
    logger = logging.getLogger(__name__)
    therapistService = TherapistService()

    def post(self, request):
        web = WebInfo(request)
        
        try:
            to_return = []
            search=request.GET.get('search', None)
            uuid=request.GET.get('uuid', None)
            company_id=decrypt_secure_uuid(uuid).get('company_id', None)
            data = request.data
            result = self.therapistService.new_therapist(data, company_id, search, uuid)
            return  Response({'result': TherapistSerializer(result, many=False).data}, status=status.HTTP_200_OK)

        except Exception as e:
            self.logger.error("error", e)
            return Response({'result': {'message':f'An error happened {str(e)}.'}}, status=status.HTTP_400_BAD_REQUEST)
        
    
    def get(self, request):
        web = WebInfo(request)
        
        try:
            to_return = []
            uuid=request.GET.get('uuid', None)
            searchType=request.GET.get('searchType', None)
            if uuid:
                result = self.therapistService.find_by_uuid(uuid)
            # else:
            #     result = self.therapistService.find_by_username(search)
            return  Response({'result': TherapistSerializer(result, many=False).data}, status=status.HTTP_200_OK)

        except Exception as e:
            self.logger.error("error", e)
            return Response({'result': {'message':f'An error happened {str(e)}.'}}, status=status.HTTP_400_BAD_REQUEST)
        
    