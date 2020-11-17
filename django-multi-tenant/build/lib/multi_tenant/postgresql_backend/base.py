import django.db.utils
import psycopg2
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from tenant_schemas.postgresql_backend.base import \
    DatabaseWrapper as TenantDatabaseWrapper
from tenant_schemas.postgresql_backend.base import (FakeTenant,
                                                    _check_schema_name)
from tenant_schemas.utils import get_limit_set_calls, get_public_schema_name

EXTRA_SEARCH_PATHS = getattr(settings, 'PG_EXTRA_SEARCH_PATHS', [])


class DatabaseWrapper(TenantDatabaseWrapper):

    def _cursor(self, name=None):
        """
        Here it happens. We hope every Django db operation using PostgreSQL
        must go through this to get the cursor handle. We change the path.
        """
        if name:
            # Only supported and required by Django 1.11 (server-side cursor)
            cursor = super(DatabaseWrapper, self)._cursor(name=name)
        else:
            cursor = super(DatabaseWrapper, self)._cursor()

        # optionally limit the number of executions - under load, the execution
        # of `set search_path` can be quite time consuming
        if (not get_limit_set_calls()) or not self.search_path_set:
            # Actual search_path modification for the cursor. Database will
            # search schemata from left to right when looking for the object
            # (table, index, sequence, etc.).
            if not self.schema_name:
                raise ImproperlyConfigured("Database schema not set. Did you forget "
                                           "to call set_schema() or set_tenant()?")
            _check_schema_name(self.schema_name)
            public_schema_name = get_public_schema_name()
            search_paths = []

            if self.schema_name == public_schema_name:
                search_paths = [public_schema_name]
            else:
                if self.include_public_schema:
                    search_paths = [self.schema_name, public_schema_name]
                else:
                    search_paths = [self.schema_name]

                if not isinstance(self.tenant, FakeTenant) and not self.tenant.is_leading():
                    if len(search_paths) > 1:
                        search_paths.insert(1, self.tenant.tenant.schema_name)
                    else:
                        search_paths.append(self.tenant.tenant.schema_name)

            search_paths.extend(EXTRA_SEARCH_PATHS)

            if name:
                # Named cursor can only be used once
                cursor_for_search_path = self.connection.cursor()
            else:
                # Reuse
                cursor_for_search_path = cursor

            # In the event that an error already happened in this transaction and we are going
            # to rollback we should just ignore database error when setting the search_path
            # if the next instruction is not a rollback it will just fail also, so
            # we do not have to worry that it's not the good one
            try:
                cursor_for_search_path.execute('SET search_path = {0}'.format(','.join(search_paths)))
            except (django.db.utils.DatabaseError, psycopg2.InternalError):
                self.search_path_set = False
            else:
                self.search_path_set = True

            if name:
                cursor_for_search_path.close()

        return cursor
