# apps/users/views.py
from django.shortcuts import render, redirect
from .models import UserProfile, Role
from django.http import HttpResponseForbidden

def role_required(role_name):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.userprofile.role.name != role_name:
                return HttpResponseForbidden("You don't have permission to view this page.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

@role_required('Technician')
def incident_detail(request, incident_id):
    # Fetch and display incident details
    ...
