from django.utils import timezone
from rest_framework import serializers

from app.models import Therapist, Therapist_Attribute, Therapist_Contact, Therapist_Email, Therapist_Invitation, Therapist_Location, Therapist_Signature

class TherapistInvitationSerializer(serializers.ModelSerializer):
    
    username = serializers.SerializerMethodField()
    
    class Meta:
        model = Therapist_Invitation
        fields = [
            'uuid', 'first_name', 'last_name', 'npi', 'email', 'phone','username', 'url', 'company_id', 'status', 'sent_at', 'expires_at', 'accepted_at', 'revoked_at'
        ]
        
    
    def get_username(self, obj): return  obj.username

class TherapistAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Therapist_Attribute
        fields = [
            'id', 'type', 'value', 'active','created_at', 'created_by', 'update_at', 'updated_by'
        ]
        
class TherapistLocationSerializer(serializers.ModelSerializer):

    address = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    # state = serializers.SerializerMethodField()
    # state_code = serializers.SerializerMethodField()
    zip_code = serializers.SerializerMethodField()
    appartment = serializers.SerializerMethodField()

    class Meta:
        model = Therapist_Location
        fields = [
            'id', 'is_primary','address','city', 'zip_code','appartment','active','created_at', 'created_by', 'update_at', 'updated_by'
        ]
        
    def get_address(self, obj): return  obj.location.address
    def get_city(self, obj): return  obj.location.city.name
    # def get_state(self, obj): return  obj.location.city.state.name
    # def get_state_code(self, obj): return  obj.location.city.state.abbreviation
    def get_zip_code(self, obj): return  obj.location.zip_code
    def get_appartment(self, obj): return  obj.location.appartment
    
        
class TherapistContactSerializer(serializers.ModelSerializer):

    contact_name = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    is_fax = serializers.SerializerMethodField()

    class Meta:
        model = Therapist_Contact
        fields = [
            'id', 'is_primary','contact_name','phone_number','is_fax','active','created_at', 'created_by', 'update_at', 'updated_by'
        ]

    def get_contact_name(self, obj): return  obj.contact.contact_name
    def get_phone_number(self, obj): return  obj.contact.phone_number
    def get_is_fax(self, obj): return  obj.contact.is_fax
        
        
class TherapistEmailSerializer(serializers.ModelSerializer):

    email = serializers.SerializerMethodField()

    class Meta:
        model = Therapist_Email
        fields = [
            'id', 'is_primary','email','active','created_at', 'created_by', 'update_at', 'updated_by'
        ]

    def get_email(self, obj): return  obj.email.value
        
class TherapistSignatureSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Therapist_Signature
        fields = [
            'id', 'is_primary','signature','active','created_at', 'created_by', 'update_at', 'updated_by'
        ]

    def get_email(self, obj): return  obj.email.value
        
class TherapistSerializer(serializers.ModelSerializer):

    
    emails = serializers.SerializerMethodField()
    contacts = serializers.SerializerMethodField()
    locations = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()
    signatures = serializers.SerializerMethodField()

    class Meta:
        model = Therapist
        fields = [
            'id', 'name', 'last_name', 'title', 'company_id', 'emails', 'contacts', 'locations', 'attributes', 'signatures','created_at', 'created_by', 'update_at', 'updated_by'
        ]
        
    
    def get_emails(self, obj): return  TherapistEmailSerializer(obj.emails, many=True).data
    def get_contacts(self, obj): return  TherapistContactSerializer(obj.contacts, many=True).data
    def get_locations(self, obj): return  TherapistLocationSerializer(obj.locations, many=True).data
    def get_attributes(self, obj): return  TherapistAttributeSerializer(obj.attributes, many=True).data
    def get_signatures(self, obj): return  TherapistSignatureSerializer(obj.signatures, many=True).data