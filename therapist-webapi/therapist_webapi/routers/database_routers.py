
from ..settings import DATABASES

class CampusPTRouter:
    database_alias_name = 'campuspt_db'
    campuspt_tables = ['contact','location','email','city','country_states','country']

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
        """
        Ensures migrations for `Therapist_Attribute` occur only in the correct database.
        """
        if model_name in self.campuspt_tables:
            return db == self.database_alias_name  # Make sure migrations are only applied to 'other_database'
        return None
