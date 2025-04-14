from django.urls import path
from . import views

urlpatterns = [
    path('', views.lead_list, name='lead_list'),
    path('thanks/', views.thanks, name='thanks'),
]
