from tenant_schemas.middleware import BaseTenantMiddleware, TenantMiddleware
from tenant_schemas.utils import get_public_schema_name


class XHeaderTenantMiddleware(BaseTenantMiddleware):
    """
    Determines tenant by the value of the ``X-DTS-SCHEMA`` HTTP header.
    """
    def get_tenant(self, model, hostname, request):
        tenant = None

        schema_name = request.META.get('HTTP_X_DTS_SCHEMA', None)
        if schema_name:
            tenant = model.objects.get(schema_name=schema_name)

        if tenant is None:
            tenant = model.objects.get(schema_name=get_public_schema_name())

        return tenant
