from django.contrib import admin
from .models import MSP, UserProfile,Client,Device,Incident,Severity
# Register your models here.
admin.site.register(MSP)
# admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Client)
admin.site.register(Device)
admin.site.register(Incident)
admin.site.register(Severity)