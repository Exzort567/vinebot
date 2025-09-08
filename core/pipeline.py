from social_core.exceptions import AuthForbidden
from .models import AllowedUser

def allow_only_whitelisted(strategy, details, **kwargs):
    email = details.get('email')
    print(f"[DEBUG] Pipeline check for email={email}")
    if not email: 
        print("[DEBUG] No email in details, forbidden")
        raise AuthForbidden('google-oauth2')
    try:
        user = AllowedUser.objects.get(email__iexact=email, is_active=True)
        print(f"[DEBUG] User allowed: {user.email}, role={user.role}")
    except AllowedUser.DoesNotExist:
        print(f"[DEBUG] User not found or inactive: {email}")
        raise AuthForbidden('google-oauth2')
