
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
import json
import logging
from app.models import Therapist, Therapist_Attribute

from therapist_webapi.utils import WebInfo

class TherapistAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    logger = logging.getLogger(__name__)
    

    def post(self, request):
        web = WebInfo(request)
        company_id = int(request.COOKIES['company'])
        try:
            to_return = []
            search=request.GET.get('search', None)
            data = request.data
            
            th = Therapist_Attribute.objects.filter(value=search).first()
            if not th:
                th = Therapist.objects.create(
                    name=data.get('first_name'),
                    last_name=data.get('last_name'),
                    title=data.get('title'),
                    user_id=User
                    )
            
            return  Response(to_return, status=status.HTTP_200_OK)

        except Exception as e:
            self.logger.error("error", e)
            return Response({'result': {'message':f'An error happened {str(e)}.'}}, status=status.HTTP_400_BAD_REQUEST)