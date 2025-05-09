
from datetime import timedelta
from django.db.models.query import Q
from django.db import transaction
from django.utils import timezone
from django.core.paginator import Paginator
from app.models import Therapist_Invitation
from django.contrib.auth.models import User
from app.service.messageService import MessageWebService
from therapist_webapi.settings import REGISTRY_WEBAPP
from therapist_webapi.utils import WebInfo, decrypt_secure_uuid, generate_secure_uuid, is_uuid4


class TherapistInitationService:
    
    messageService = MessageWebService()
    
    @transaction.atomic
    def send(self, data, web:WebInfo):
        if 'first_name' not in data: raise ValueError('First name is required')
        if 'last_name' not in data: raise ValueError('Last name is required')
        # if 'npi' not in data: raise ValueError('NPI is required')
        # if 'email' not in data: raise ValueError('Email is required')
        if 'phone' not in data: raise ValueError('Phone is required')
        if 'company_id' not in data: raise ValueError('Company is required')
        if 'user_id' not in data: raise ValueError('User id is required')
        if not User.objects.filter(id=data.get('user_id', None), is_staff=1).exists(): 
            raise ValueError('Validation: User ID is invalid. Contact to the administrator')

        company_id = data.get('company_id', None)
        
        obj = Therapist_Invitation.objects.create(
            uuid=generate_secure_uuid({'company_id':company_id}),
            user_id=data.get('user_id', None),
            first_name=data.get('first_name', None),
            last_name=data.get('last_name', None),
            npi=data.get('npi', None),
            phone=data.get('phone', None),
            email=data.get('email', None),
            company_id=company_id,
            sent_at=timezone.now(),
            expires_at=timezone.now() + timedelta(days=7),
            created_at=timezone.now(),
            created_by=web.get_username(),
            )
        
        obj.url = f'{REGISTRY_WEBAPP}?uuid='+ str(obj.uuid)
        obj.save()
        
        app_name = "CampusPT App"
        com_name = "Campus Physical Therapy"

        template = f"""
Hi {obj.first_name} {obj.last_name},

You are invited to join {app_name} as a therapist! Click the link below to complete your enrollment and start managing your patients.

Enroll Now [{obj.url}]

If you have any questions, feel free to reach out.

Best,
{com_name}
            """
        self.messageService.send_message(company_id, "TEXT", obj.phone, "Enrollment", template, "usr_therapist_api")
        
        return obj
        
        
    def find(self, search, index:int, size:int, web:WebInfo):
        if search and search.strip() != '':
            if search: 
                obj = Therapist_Invitation.objects.filter(uuid=search).first()
                print(obj)
                if not obj: raise ValueError('Invalid UUID')
                return obj
            # return Paginator(Therapist_Invitation.objects.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(npi__icontains=search)), size).get_page(index)
            else:
                raise ValueError('UUID required')
        # return Paginator(Therapist_Invitation.objects.all(), size).get_page(index)
            