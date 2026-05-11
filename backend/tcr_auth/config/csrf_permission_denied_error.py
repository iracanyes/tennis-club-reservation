from rest_framework.exceptions import PermissionDenied


class CSRFPermissionDeniedError(PermissionDenied):
    default_code = "csrf_permission_denied"

