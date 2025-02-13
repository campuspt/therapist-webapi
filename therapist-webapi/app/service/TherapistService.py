
from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone
from app.api.geoService import GEOService
from app.models import Contact, Email, Location, Therapist, Therapist_Attribute, Therapist_Contact, Therapist_Email, Therapist_Invitation, Therapist_Location, Therapist_Signature


class TherapistService:
    
    geoService = GEOService()
    
    @transaction.atomic       
    def new_therapist(self, data,company_id, search, uuid):
        # Run validations
            self.__validate(data)
            
            if not uuid: raise ValueError('You are not auhorized')
            
            i = self.__get_valid_invitation(uuid)
            
            ta = Therapist_Attribute.objects.filter(value=i.npi).first()
            user = User.objects.filter(username=data.get('username', None)).first()
            therapist = None
            if not ta:
                # Create therapist
                therapist = Therapist.objects.create(
                    name=data.get('firstName'),
                    last_name=data.get('lastName'),
                    title=data.get('title'),
                    company_id=company_id,
                    user_id=user.id
                    )
                # Create therapist attribute NPI
                npi = att_ptlicense=Therapist_Attribute.objects.create(
                    type='NPI',
                    value=data.get('npi'),
                    therapist=therapist,
                    )
                # Create therapist attribute PT License
                license = att_ptlicense=Therapist_Attribute.objects.create(
                    type='STATE_LICENSE',
                    value=data.get('license'),
                    therapist=therapist,
                    )
                # Therapist Location
                location = Therapist_Location.objects.create(
                    therapist_id = therapist.id,
                    location_id = Location.objects.create(
                        address=data.get('practiceAddress', None),
                        zip_code=data.get('zip', None),
                        appartment=data.get('appartment', ''),
                        city=self.geoService.find_city_by_zip(data.get('zip', None)),
                        ).location_id,
                        is_primary=True
                    )
                
                # Therapist Contact
                contact = Therapist_Contact.objects.create(
                    therapist_id = therapist.id,
                    contact_id = Contact.objects.create(
                        contact_name=data.get('firstName') + ' ' + data.get('lastName'),
                        phone_number=data.get('phone', None),
                        ).contact_id,
                        is_primary=True
                    )
                
                # Therapist Email
                email = Therapist_Email.objects.create(
                    therapist_id = therapist.id,
                    email_id = Email.objects.create(value=data.get('email', None)).email_id,
                        is_primary=True
                    )
                
                # Therapist Email
                signature = Therapist_Signature.objects.create(
                    therapist_id=therapist.id,
                    signature=data.get('signature', None),
                    is_primary=True
                    )
                
                fax = None
                
                # Fax Information
                if data.get('fax', None):
                   fax = Therapist_Contact.objects.create(
                        therapist_id = therapist.id,
                        contact_id = Contact.objects.create(
                            contact_name=data.get('firstName') + ' ' + data.get('lastName'),
                            phone_number=data.get('fax', None),
                            is_fax=True
                            ).contact_id,
                            is_primary=True
                        )
                   

                user.set_password(data.get('password', None))
                user.save()
                
                i.accepted_at = timezone.now()
                i.update_at = timezone.now()
                i.updated_by = user.username
                i.accepted_at = timezone.now()
                i.status = 'accepted'
                i.save()
                
                return therapist
            else:
                # Create therapist
                therapist = ta.therapist
                Therapist.objects.filter(therapist=therapist).update(
                    name=data.get('firstName'),
                    last_name=data.get('lastName'),
                    title=data.get('title'),
                    company_id=company_id,
                    user_id=user.id
                    )
                # Create therapist attribute NPI
                npi = att_ptlicense=Therapist_Attribute.objects.filter(type='NPI', therapist=therapist).update(
                    value=data.get('npi'),
                    therapist=therapist,
                    )
                # Create therapist attribute PT License
                license = att_ptlicense=Therapist_Attribute.objects.filter(type='STATE_LICENSE', therapist=therapist).update(
                    value=data.get('license'),
                    therapist=therapist,
                    )
                # Therapist Location
                Therapist_Location.objects.filter(therapist_id = therapist.id,active=True, is_primary=True).update(active=False)
                location = Therapist_Location.objects.create(
                    therapist_id = therapist.id,
                    location_id = Location.objects.create(
                        address=data.get('practiceAddress', None),
                        zip_code=data.get('zip', None),
                        appartment=data.get('appartment', ''),
                        city=self.geoService.find_city_by_zip(data.get('zip', None)),
                        ).location_id,
                        is_primary=True
                    )
                
                # Therapist Contact
                Therapist_Contact.objects.filter(therapist_id = therapist.id,active=True, is_primary=True).update(active=False)
                contact = Therapist_Contact.objects.create(
                    therapist_id = therapist.id,
                    contact_id = Contact.objects.create(
                        contact_name=data.get('firstName') + ' ' + data.get('lastName'),
                        phone_number=data.get('phone', None),
                        ).contact_id,
                        is_primary=True
                    )
                
                # Therapist Email
                Therapist_Email.objects.filter(therapist_id = therapist.id,active=True, is_primary=True).update(active=False)
                email = Therapist_Email.objects.create(
                    therapist_id = therapist.id,
                    email_id = Email.objects.create(value=data.get('email', None)).email_id,
                        is_primary=True
                    )
                
                # Therapist Email
                Therapist_Signature.objects.filter(therapist_id = therapist.id,active=True, is_primary=True).update(active=False)
                signature = Therapist_Signature.objects.create(
                    therapist_id=therapist.id,
                    signature=data.get('signature', None),
                    is_primary=True
                    )
                
                fax = None
                
                # Fax Information
                if data.get('fax', None):
                   Therapist_Contact.objects.filter(therapist_id = therapist.id,active=True, is_primary=True).update(active=False)
                   fax = Therapist_Contact.objects.create(
                        therapist_id = therapist.id,
                        contact_id = Contact.objects.create(
                            contact_name=data.get('firstName') + ' ' + data.get('lastName'),
                            phone_number=data.get('fax', None),
                            is_fax=True
                            ).contact_id,
                            is_primary=True
                        )
                   

                user.set_password(data.get('password', None))
                user.save()
                
                i.accepted_at = timezone.now()
                i.update_at = timezone.now()
                i.updated_by = user.username
                i.accepted_at = timezone.now()
                i.status = 'accepted'
                i.save()
                
                return therapist

    # def find_by_uuid(self, search, company_id):
    #     if search:
    #         ta = Therapist_Attribute.objects.filter(value=search, active=1, visible=1, therapist__active=1).first() 
    #         if not ta:
    #             return []
    #         else:
    #             return ta.therapist
            
    #     return Therapist.objects.filter(active=1)

    def find_by_uuid(self, uuid):
        inv = self.__get_valid_invitation(uuid)
        return Therapist.objects.filter(active=1,user_id=inv.user_id).first()
        
    def __get_valid_invitation(self, uuid):
        i = Therapist_Invitation.objects.filter(uuid = uuid).first()
        if not i: raise ValueError('You are not auhorized')
        if i.status in ['accepted', 'revoked']: raise ValueError('This resource is not available')
        if i.status in ['expired'] or i.expires_at < timezone.now(): raise ValueError('This resource expired')
        return i

    def __validate(self, data):
        if not data.get('username', None) or data.get('username', None).strip() == '': 
            raise ValueError('Validation: Username is required. Contact to the administrator')
        if not User.objects.filter(username=data.get('username', None), is_staff=1).exists(): 
            raise ValueError('Validation: Username is invalid. Contact to the administrator')
        if not data.get('firstName', None) or data.get('firstName', None).strip() == '': 
            raise ValueError('Validation: First name is required')
        if not data.get('lastName', None) or data.get('lastName', None).strip() == '': 
            raise ValueError('Validation: Last name is required')
        if not data.get('title', None) or data.get('title', None).strip() == '': 
            raise ValueError('Validation: Title is required')
        if not data.get('npi', None) or data.get('npi', None).strip() == '': 
            raise ValueError('Validation: NPI is required')
        if not data.get('license', None) or data.get('license', None).strip() == '': 
            raise ValueError('Validation: License is required')
        if not data.get('practiceAddress', None) or data.get('practiceAddress', None).strip() == '': 
            raise ValueError('Validation: Address is required')
        if not data.get('zip', None) or data.get('zip', None).strip() == '': 
            raise ValueError('Validation: Zip code is required')
        if not data.get('phone', None) or data.get('phone', None).strip() == '': 
            raise ValueError('Validation: Email is required')
        if not data.get('email', None) or data.get('email', None).strip() == '': 
            raise ValueError('Validation: Email is required')
        if not data.get('password', None) or data.get('password', None).strip() == '' or len(data.get('password', None)) < 8: 
            raise ValueError('Validation: Invalid password')
        if not data.get('signature', None) or data.get('signature', None).strip() == '' or len(data.get('signature', None)) < 10: 
            raise ValueError('Validation: A valid signature is required')