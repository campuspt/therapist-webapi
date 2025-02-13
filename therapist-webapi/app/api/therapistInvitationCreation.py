
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import logging
from app.serializers import TherapistInvitationSerializer
from app.service.therapistInvitationService import TherapistInitationService
from therapist_webapi.authentication import APIKeyAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from therapist_webapi.utils import WebInfo

class TherapistInvitationCreationAPI(APIView):
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
