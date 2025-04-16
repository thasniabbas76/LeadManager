from django.db import models

# Create your models here.
LEAD_SOURCE_CHOICES = [
    ('Website', 'Website'),
    ('Social Media', 'Social Media'),
    ('Referral', 'Referral'),
    ('Event', 'Event'),
    ('Other', 'Other'),
]

class Lead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    lead_source = models.CharField(max_length=100, choices=LEAD_SOURCE_CHOICES, default='website')

    def __str__(self):
        return self.name

class ZohoAuth(models.Model):
    
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    expires_in = models.IntegerField()
    token_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ZohoAuth({self.access_token})"