
import logging
from uszipcode import SearchEngine

from app.models import City, State

class GEOService:
    
    logger = logging.getLogger(__name__)
    
    def find_city_by_zip(self, code:str):
        if code is None: raise ValueError(f'You should enter a ZIP code')  
        with SearchEngine() as search:
                    result = search.by_zipcode(code)
                    if result is None:
                        self.logger.error(f'ZIP code not found {code}')
                        raise ValueError(f'ZIP code not found {code}')  
                    if result is not None:               
                        return City.objects.filter(name=result.major_city).first()
                    
    def find_states(self): return State.objects.all()