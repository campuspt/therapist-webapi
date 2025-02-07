"""
Definition of urls for therapist_webapi.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from app.api.therapistInvitationAPI import TherapistInvitationAPI


urlpatterns = [
    path('api/therapist/invitations', TherapistInvitationAPI.as_view(), name='invitations'),
]
