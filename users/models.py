from django.db import models
from django.contrib.auth.models import User

class MSP(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    msp = models.ForeignKey(MSP, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username

# Client (Customer) Model associated with MSP
class Client(models.Model):
    name = models.CharField(max_length=255)
    # email = models.CharField(max_length=40)
    # phone = models.CharField(max_length=15)
    msp = models.ForeignKey(MSP, on_delete=models.CASCADE)  # Each client belongs to one MSP
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

# Device or Service Model associated with Client
class Device(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    device_type = models.CharField(max_length=50)  # e.g., "Server", "Router", etc.
    ip_address = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Severity(models.Model):
    level = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.level
    
# Incident Model linked to Device and Client
class Incident(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    severity = models.ForeignKey(Severity, on_delete=models.CASCADE)
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    recommended_solution = models.TextField(null=True, blank=True)  # Solution suggested by ML
    predicted_resolution_time = models.FloatField(null=True, blank=True)  # Predicted time (in hours)
    
    def __str__(self):
        return self.title
