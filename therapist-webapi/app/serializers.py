from django.utils import timezone
from rest_framework import serializers

from app.models import Therapist_Invitation

class TherapistInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Therapist_Invitation
        fields = [
            'uuid', 'first_name', 'last_name', 'npi', 'email', 'phone', 'url', 'company_id', 'status', 'sent_at', 'expires_at', 'accepted_at', 'revoked_at'
        ]