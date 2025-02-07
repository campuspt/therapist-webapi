
import base64
import uuid
from django.utils import timezone
from app.models import Audit_Fields
from therapist_webapi.settings import DATABASES, ENCRYPT_KEY
from cryptography import fernet


def set_audit_creation(obj:Audit_Fields, username):
    obj.created_by = username
    obj.created_at = timezone.now()
    
def set_audit_update(obj:Audit_Fields, username):
    obj.updated_by = username
    obj.update_at = timezone.now()
        

def encrypt(cleartext: str) -> str:
  key = ENCRYPT_KEY
  f = fernet.Fernet(key)
  return f.encrypt(cleartext.encode()).decode()


def decrypt(ciphertext: str) -> str:
  key = ENCRYPT_KEY
  f = fernet.Fernet(key)
  return f.decrypt(ciphertext.encode()).decode()
    
def text_end_with(text:str, phrases:list):
    for word in phrases: 
        if text.endswith(word): return True
    return False

def text_start_with(text:str, phrases:list):
    for word in phrases: 
        if text.startswith(word): return True
    return False

def text_contains_with(text:str, phrases:list):
    for word in phrases: 
        if text.find(word) > -1: return True
    return False

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



def decode_base64_file(file_base64):
    format, imgstr = file_base64.split(';base64,') 
    ext = format.split('/')[-1]
    return base64.b64decode(imgstr), ext


def is_uuid4(string):
    try:
        val = uuid.UUID(string, version=4)
        return str(val) == string  # Ensures it's a valid UUID4 format
    except ValueError:
        return False

class WebInfo:
    def __init__(self, request) -> None:
        self.__userfullname = 'Anonymous' if not request.user.is_authenticated or not request.COOKIES.get('user') else request.COOKIES.get('user')
        self.__username = 'Anonymous' if request.user.username == '' else request.user.username
        self.is_staff = request.user.is_staff
        self.is_super = request.user.is_superuser 
        self.is_authenticated = request.user.is_authenticated
        self.__ip = get_client_ip(request)
        self.__agent = request.META.get('HTTP_USER_AGENT','Unknow')
        self.__company_id = int(request.COOKIES['company']) if 'company' in request.COOKIES else None
        self.__db_name = DATABASES['default']['NAME']
        self.__is_prod = not text_contains_with(self.__db_name.lower(), ['dev','test','prepro'])
        
    def set_company_id(self, company_id): self.__company_id = company_id
    
    def get_userfullname(self):
        return self.__userfullname
    
    def get_username(self):
        return self.__username
    
    def get_ip(self):
        return self.__ip
    
    def get_agent(self):
        return self.__agent
    
    def get_company_id(self):
        return self.__company_id
    
    def is_prod(self):
        return self.__is_prod
    
    def db_name(self):
        return self.__db_name
    
    def __str__(self) -> str:
        return f"""
        Username:{self.__username},\n
        Name:{self.__userfullname},\n
        Company:{self.__company_id},\n
        Is Staff:{self.is_staff},\n
        Is Super:{self.is_super},\n
        Is authenticated:{self.is_authenticated},\n
        IP:{self.__ip},\n
        Agent:{self.__agent},\n
        Db Name:{self.__db_name},\n
        Is prod:{self.__is_prod},\n
        """