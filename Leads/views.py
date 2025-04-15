from django.shortcuts import render, redirect
from .forms import LeadForm
from .models import Lead
import requests
from django.conf import settings

def lead_form(request):
    if request.method =='POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lead_form')
    else:
        form = LeadForm()
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
        f"redirect_url={settings.ZOHO_REDIRECT_URL}"
    )
    return redirect(auth_url)

def zoho_callback(request):
    code = request.GET.get('code')
    token_url =f"{settings.ZOHO_ACCOUNTS_URL}/oauth/v2/token"

    data ={
        "grand_type" :"authorization_code",
        "client_id" : settings.ZOHO_CLIENT_ID,
        "client_secret" : settings.ZOHO_CLIENT_SECRET,
        "redirect_url" : settings.ZOHO_REDIRECT_URI,
        "code" : code,
    }
    response = requests.post(token_url, data=data)
    tokens = response.json()

    return render(request, 'zoho_tokens.html', {'tokens': tokens})
