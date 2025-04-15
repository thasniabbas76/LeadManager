from django.urls import path
from . import views

urlpatterns = [
    path('', views.lead_form, name='lead_form'),
    path('thanks/', views.thanks, name='thanks'),
    path('lead_list/', views.lead_list, name='lead_list'),
    path('zoho/auth/',views.zoho_auth, name='zoho_auth'),
    path('oauth2callback/',views.zoho_callback, name='zoho_callback'),
]
