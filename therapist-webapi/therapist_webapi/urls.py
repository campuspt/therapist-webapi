"""
Definition of urls for therapist_webapi.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from app.api.authenticationAPI import exchange_uuid_for_token
from app.api.infoAPI import InfoAPI
from app.api.therapistAPI import TherapistAPI
from app.api.therapistInvitationAPI import TherapistInvitationAPI
from app.api.therapistInvitationCreation import TherapistInvitationCreationAPI


urlpatterns = [
    path('api/auth/', exchange_uuid_for_token, name='auth'),
    path('api/therapist/invitations/creation', TherapistInvitationCreationAPI.as_view(), name='invitations'),
    path('api/therapist/invitations', TherapistInvitationAPI.as_view(), name='invitations'),
    path('api/therapist/registry', TherapistAPI.as_view(), name='therapist'),
    path('api/info', InfoAPI.as_view(), name='info'),
]
