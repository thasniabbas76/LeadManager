from django.shortcuts import render, redirect
from .forms import LeadForm
from .models import Lead

def lead_list(request):
    if request.method =='POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lead_list')
    else:
        form = LeadForm()
    return render(request, 'lead_list.html',{'form':form})
def thanks(request):
    return render(request, 'thanks.html')