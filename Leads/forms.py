from django import forms
from .models import Lead

LEAD_SOURCE_CHOICES = [
        ('Website', 'Website'),
        ('Social Media', 'Social Media'),
        ('Referral', 'Referral'),
        ('Event', 'Event'),
        ('Other', 'Other'),
    ]

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'email', 'phone_number', 'message','lead_source']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your message'}),
            'lead_source': forms.Select(attrs={'class': 'form-control'}),
        }