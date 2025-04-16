from django.shortcuts import render, redirect
from .forms import LeadForm
from .models import Lead, ZohoAuth
import requests
from django.conf import settings
from django.http import JsonResponse
from .utils import refresh_access_token

def lead_form(request):
    if request.method =='POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save()
            token = refresh_access_token()
            headers ={
                'Authorization': f'Zoho-oauthtoken {token}',
                'Content-Type': 'application/json',
            }

            data = {
                "data": [
                    {
                        "Last_Name": lead.name or "Unknown",
                        "Email": lead.email,
                        "Phone": lead.phone_number,
                        "Description": lead.message,
                        "Company":"De'thas",
                        "Lead_Source": lead.lead_source,
                    }
                ]
            }
            response = requests.post(
                'https://www.zohoapis.in/crm/v2/Leads',
                headers=headers,
                json=data
            )
            print("Zoho response:", response.status_code, response.json())
            return redirect('thanks')
    else:
        form=LeadForm
    return render(request, 'lead_form.html',{'form':form})
def thanks(request):
    return render(request, 'thanks.html')

def lead_list(request):
    leads = Lead.objects.all()
    return render(request, 'lead_list.html', {'leads': leads})

def zoho_auth(request):
    auth_url = (
        f"{settings.ZOHO_ACCOUNTS_URL}/oauth/v2/auth?"
        f"scope={settings.ZOHO_SCOPE}&"
        f"client_id={settings.ZOHO_CLIENT_ID}&"
        f"response_type=code&"
        f"access_type=offline&"
        f"redirect_uri={settings.ZOHO_REDIRECT_URL}"
    )
    print("Redirect URI being sent:", settings.ZOHO_REDIRECT_URL)
    return redirect(auth_url)

def zoho_callback(request):
    code = request.GET.get('code')
    token_url =f"{settings.ZOHO_ACCOUNTS_URL}/oauth/v2/token"

    data ={
        "grant_type" :"authorization_code",
        "client_id" : settings.ZOHO_CLIENT_ID,
        "client_secret" : settings.ZOHO_CLIENT_SECRET,
        "redirect_uri" : settings.ZOHO_REDIRECT_URL,
        "code" : code,
    }
    response = requests.post(token_url, data=data)
    

    tokens = response.json()
    ZohoAuth.objects.create(
        access_token=tokens.get("access_token"),
        refresh_token=tokens.get("refresh_token"),
        token_type=tokens.get("token_type"),
        expires_in=tokens.get("expires_in"),
    )

    return render(request, 'zoho_tokens.html', {'tokens': tokens})
def token_refresh(request):
        access_token = refresh_access_token()
        return JsonResponse({"access_token": access_token})
