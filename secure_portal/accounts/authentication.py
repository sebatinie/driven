from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from .models import APIKey


class ApiKeyAuthentication(BaseAuthentication):
    """Expects:  Authorization: ApiKey <key>"""
    keyword = "ApiKey"

    def authenticate(self, request):
        parts = get_authorization_header(request).split()

        # Not our scheme? Return None so DRF tries the next class.
        if not parts or parts[0].lower() != self.keyword.lower().encode():
            return None

        if len(parts) != 2:
            raise AuthenticationFailed("Invalid ApiKey header.")

        try:
            api_key = APIKey.objects.select_related("user").get(
                key=parts[1].decode(), is_active=True
            )
        except (APIKey.DoesNotExist, UnicodeError):
            raise AuthenticationFailed("Invalid API key.")

        return (api_key.user, api_key)    # (request.user, request.auth)

    def authenticate_header(self, request):
        return self.keyword               # makes DRF send 401 instead of 403