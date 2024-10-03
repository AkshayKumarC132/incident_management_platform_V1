# apps/incidents/urls.py
from django.urls import path
from .views import incident_detail

urlpatterns = [
    path('detail/<int:incident_id>/', incident_detail, name='incident_detail'),
]
