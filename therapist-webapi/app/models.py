"""
Definition of models.
"""

import uuid
from django.db import models
from django.utils import timezone

        
class Audit_Fields(models.Model):
    created_at = models.DateTimeField(default=timezone.now())
    created_by = models.CharField(max_length=25)
    update_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=25, blank=True, null=True)
    class Meta:
         abstract = True

class Country(models.Model):
    
    class Meta:
            db_table = "country"
            ordering = ['name']
    
    country_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=45)
    
    def __str__(self) -> str:
      return self.name + " (" + self.code + ")"

# Country model, mapping to manage country catalogs.
class State(models.Model):
    
    class Meta:
            db_table = "country_states"
            ordering = ['name']
    
    state_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    abbreviation = models.CharField(max_length=2)
    capital = models.CharField(max_length=45)
    incorporation_date = models.DateField(auto_now_add=True)
    timezone = models.CharField(max_length=45)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
      return self.name + " (" + self.abbreviation + ")"

# City model, mapping to manage cities catalogs.
class City(models.Model):
    
    class Meta:
            db_table = "city"
            ordering = ['name']
    
    city_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    population = models.IntegerField()
    location_latitude = models.DecimalField(decimal_places=0, max_digits=9)
    location_longitude = models.DecimalField(decimal_places=0, max_digits=9)
    
    def __str__(self) -> str:
      return self.name + " (" + self.state.name + ")"

class Location(models.Model):
    
    class Meta:
            db_table = "location"
    
    location_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=250)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=5)
    appartment = models.CharField(max_length=100, blank=True)
    
    def __str__(self) -> str:
      return self.address + ' ' + self.city.name + ', '   + self.city.state.name

# Location model, mapping to manage locations.
class Contact(models.Model):
    
    class Meta:
            db_table = "contact"
            ordering = ['contact_name']
    
    contact_id = models.AutoField(primary_key=True)
    contact_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=14)
    ext = models.CharField(max_length=4, blank=True, null=True)
    is_fax = models.BooleanField(default=False)
    
    def __str__(self) -> str:
      return self.phone_number + " (" + self.contact_name + ")"
  
    def get_clean_number(self) -> str:
        return self.phone_number.replace(' ','').replace(')','').replace('(','').replace('-','') 

class Email(models.Model):
      email_id = models.AutoField(primary_key=True)
      value = models.CharField(max_length=100)
      
      class Meta:
            db_table = "email"
            ordering = ['value']
            
class Therapist(Audit_Fields):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    user_id = models.IntegerField()
    company_id = models.IntegerField()
    active = models.BooleanField(default=True)
        
    class Meta:
            db_table = "therapist"
            
    def __str__(self) -> str:
      return "{} ({}) - {}".format(self.name,self.title, 'ACTIVE' if self.active else 'INACTIVE')
  
class Therapist_Attribute(Audit_Fields):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=25)
    value = models.CharField(max_length=250)
    therapist = models.ForeignKey(Therapist, on_delete=models.DO_NOTHING)
    active = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)
        
    class Meta:
            db_table = "therapist_attribute"
            
    def __str__(self) -> str:
      return "{} ({}={})/{} - {}".format(self.therapist.name,self.name,self.value,self.type, 'ACTIVE' if self.active else 'INACTIVE')
  
class Therapist_Location(Audit_Fields):
    id = models.AutoField(primary_key=True)
    therapist = models.ForeignKey(Therapist, on_delete=models.DO_NOTHING)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    active = models.BooleanField(default=True)
    is_primary = models.BooleanField(default=False)
    visible = models.BooleanField(default=True)
        
class Therapist_Contact(Audit_Fields):
    id = models.AutoField(primary_key=True)
    therapist = models.ForeignKey(Therapist, on_delete=models.DO_NOTHING)
    contact = models.ForeignKey(Contact, on_delete=models.DO_NOTHING)
    active = models.BooleanField(default=True)
    is_primary = models.BooleanField(default=False)
    visible = models.BooleanField(default=True)
        
class Therapist_Email(Audit_Fields):
    id = models.AutoField(primary_key=True)
    therapist = models.ForeignKey(Therapist, on_delete=models.DO_NOTHING)
    email = models.ForeignKey(Email, on_delete=models.DO_NOTHING)
    active = models.BooleanField(default=True)
    is_primary = models.BooleanField(default=False)
    visible = models.BooleanField(default=True)
        
        
class Therapist_Invitation(Audit_Fields):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked'),
    ]
    
    models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    npi = models.CharField(max_length=15)
    email = models.CharField(max_length=250)
    phone = models.CharField(max_length=25)
    url = models.CharField(max_length=5000)
    company_id = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    sent_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    accepted_at = models.DateTimeField(null=True, blank=True)
    revoked_at = models.DateTimeField(null=True, blank=True)
    indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["phone"]),
            models.Index(fields=["status"]),
        ]