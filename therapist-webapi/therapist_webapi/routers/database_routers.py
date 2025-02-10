
from ..settings import DATABASES

class CampusPTRouter:
    database_alias_name = 'campuspt_db'
    campuspt_tables = ['contact',
                       'location',
                       'email',
                       'city',
                       'State',
                       'country',
                       'country_states',
                       'therapist',
                       'therapist',
                       'therapist_attribute', 
                       'auth_user']

    def db_for_read(self, model, **hints):
        """
        Directs read operations for `Therapist_Attribute` to a specific database.
        """
        if model._meta.db_table in self.campuspt_tables:
            return self.database_alias_name  # Replace 'other_database' with the name of the database
        return None

    def db_for_write(self, model, **hints):
        """
        Directs write operations for `Therapist_Attribute` to a specific database.
        """
        if model._meta.db_table in self.campuspt_tables:
            return self.database_alias_name  # Replace 'other_database' with the name of the database
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == self.database_alias_name:
            return False  # No permitir migraciones en esta base de datos
        return None  # Usar el comportamiento por defecto