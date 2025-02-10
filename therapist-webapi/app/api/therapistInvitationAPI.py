
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import logging
from app.serializers import TherapistInvitationSerializer
from app.service.therapistInvitationService import TherapistInitationService
from therapist_webapi.authentication import APIKeyAuthentication

from therapist_webapi.utils import WebInfo

class TherapistInvitationAPI(APIView):
    authentication_classes = [APIKeyAuthentication]
    permission_classes = [AllowAny]
    
    
    logger = logging.getLogger(__name__)
    invitationService = TherapistInitationService()

    def post(self, request):
        web = WebInfo(request)
        try:
            to_return = []
            data = request.data
            obj = self.invitationService.send(data, web)
            return  Response(TherapistInvitationSerializer(obj, many=False).data, status=status.HTTP_200_OK)

        except Exception as e:
            self.logger.error("error", e)
            return Response({'result': {'message':f'An error happened {str(e)}.'}}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        web = WebInfo(request)
        try:
            to_return = []
            data = request.data
            search = request.GET.get('uuid', None)
            index = request.GET.get('index', 1)
            page = request.GET.get('page', 25)
            obj = self.invitationService.find(search, index, page, web)
            return  Response(TherapistInvitationSerializer(obj, many=False).data, status=status.HTTP_200_OK)

        except Exception as e:
            self.logger.error("error", e)
            if isinstance(e, ValueError):
                return Response({'result': {'message':f'Validation: {str(e)}.'}}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'result': {'message':f'An error happened: {str(e)}.'}}, status=status.HTTP_400_BAD_REQUEST)
