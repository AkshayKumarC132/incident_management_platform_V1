# apps/users/models.py
from django.db import models
from django.contrib.auth.models import User

class Tenant(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Role(models.Model):
    name = models.CharField(max_length=255)
    permissions = models.JSONField()  # Custom permissions
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
