from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from django.utils import timezone
from app.models import Therapist_Invitation
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django_ratelimit.decorators import ratelimit
from django.contrib.auth.models import User

from therapist_webapi.settings import USER_ADMIN

@ratelimit(key='ip', rate='5/m', method='POST', block=True)
@api_view(['POST'])
def exchange_uuid_for_token(request):
    uuid_code = request.data.get('uuid')

    invitation = get_object_or_404(Therapist_Invitation, uuid=uuid_code)

    if invitation.status  != 'pending' or invitation.expires_at < timezone.now():
        return Response({"error": "Invalid or expired invitation"}, status=400)

    user = User.objects.using('default').get(username=USER_ADMIN)

    # Generate a token (JWT)
    refresh = RefreshToken.for_user(user)  # You may want to associate with a user
    access_token = str(refresh.access_token)

    # Mark the invitation as used
    invitation.is_used = True
    invitation.save()

    return Response({"access_token": access_token})
