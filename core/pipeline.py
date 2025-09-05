from social_core.exceptions import AuthForbidden
from .models import AllowedUser

def allow_only_whitelisted(strategy, details, **kwargs):
    email = details.get('email')
    if not email: 
        raise AuthForbidden('google-oauth2')
    try:
        AllowedUser.objects.get(email__iexact=email, is_active=True)
    except AllowedUser.DoesNotExist:
        # Not approved
        raise AuthForbidden('google-oauth2')