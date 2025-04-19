from django.db import models

# Create your models here.
class CalendlyEvent(models.Model):
    event_name = models.CharField(max_length=255)
    event_start_time = models.DateTimeField()
    invitee_name = models.CharField(max_length=255)
    invitee_email = models.EmailField()
    def __str__(self):
        return f"{self.event_name} - {self.invitee_name}"