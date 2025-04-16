import requests
from django.conf import settings
from .models import ZohoAuth

def refresh_access_token():
    zoho = ZohoAuth.objects.latest('created_at')

    token_url = f"{settings.ZOHO_ACCOUNTS_URL}/oauth/v2/token"

    data = {
        "refresh_token": zoho.refresh_token,
        "client_id": settings.ZOHO_CLIENT_ID,
        "client_secret": settings.ZOHO_CLIENT_SECRET,
        "grant_type": "refresh_token",
    }
    response = requests.post(token_url, data=data)
    tokens = response.json()

    zoho.access_token = tokens.get("access_token")
    zoho.token_type = tokens.get("token_type")
    zoho.expires_in = tokens.get("expires_in")
    zoho.save()

    return zoho.access_token
