from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import PortalUser

class PortalUserJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token.get("user_id")
            return PortalUser.objects.get(id=user_id)
        except PortalUser.DoesNotExist:
            raise AuthenticationFailed("User not found")