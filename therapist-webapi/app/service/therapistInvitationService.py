
from datetime import timedelta
from django.db.models.query import Q
from django.db import transaction
from django.utils import timezone
from django.core.paginator import Paginator
from app.models import Therapist_Invitation
from therapist_webapi.utils import WebInfo, is_uuid4


class TherapistInitationService:
    
    
    @transaction.atomic
    def send(self, data, web:WebInfo):
        if 'first_name' not in data: raise ValueError('First name is required')
        if 'last_name' not in data: raise ValueError('Last name is required')
        if 'npi' not in data: raise ValueError('NPI is required')
        # if 'email' not in data: raise ValueError('Email is required')
        if 'phone' not in data: raise ValueError('Phone is required')
        if 'company_id' not in data: raise ValueError('Company is required')
        

        
        obj = Therapist_Invitation.objects.create(
            first_name=data.get('first_name', None),
            last_name=data.get('last_name', None),
            npi=data.get('npi', None),
            # email=data.get('email', None),
            phone=data.get('phone', None),
            email=data.get('email', None),
            company_id=data.get('company_id', None),
            sent_at=timezone.now(),
            expires_at=timezone.now() + timedelta(days=7),
            created_at=timezone.now(),
            created_by=web.get_username(),
            )
        
        obj.url = 'https://therapistregistry.campusphysicaltherapy.com?uuid='+ str(obj.uuid)
        obj.save()
        return obj
        
        
    def find(self, search, index:int, size:int, web:WebInfo):
        if search and search.strip() != '':
            if is_uuid4(search): return Paginator([Therapist_Invitation.objects.filter(uuid=search).first()], size).get_page(1)
            return Paginator(Therapist_Invitation.objects.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(npi__icontains=search)), size).get_page(index)
        
        return Paginator(Therapist_Invitation.objects.all(), size).get_page(index)
            