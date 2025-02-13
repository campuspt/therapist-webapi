from datetime import datetime
import requests

from therapist_webapi.settings import REMINDERS_WEBAPI

class MessageWebService:
    
    
    
    def __init__(self):
        self.__api = REMINDERS_WEBAPI
        self.__version = "1.0.0"
        self.session = requests.Session()

    def send_message(self, company_id, reminder_type, to, title, text, username):
        url = self.__api + f'sent/new/{company_id}/{reminder_type}'
        r = requests.post(url, 
                         headers={'Content-Type':'application/x-www-form-urlencoded'}, 
                         data={'username':username, 'to': to, 'title':title, 'text':text})
        if r.status_code == 400:
            raise ValueError(r.content)
        if r.status_code == 404:
            raise ValueError('The endpoint has not been found, please report this error to the administrator.')
        if r.status_code == 500:
            raise ValueError(r.json()['message'])
        
        
        if r.status_code == 200:
                return r.json()['results']
        else:
            raise ValueError(r.content)