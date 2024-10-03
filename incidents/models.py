# apps/incidents/models.py
from django.db import models
from users.models import Tenant

class Incident(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    severity = models.CharField(max_length=50)
    resolved = models.BooleanField(default=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
