# apps/authentication/views.py
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import login  # Import login from django.contrib.auth
from django.conf import settings
from django.contrib.auth.models import User  # Import User model
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from .utils import prepare_django_request
import json
from pathlib import Path
from onelogin.saml2.settings import OneLogin_Saml2_Settings

def sso_login(request):
    req = prepare_django_request(request)

    try:
        BASE_DIR = Path(__file__).resolve().parent.parent
        SAML_PATH = BASE_DIR / 'settings.json'  # Correct path to the JSON file
        
        # Debugging output to verify path
        print(f"SAML settings path: {SAML_PATH}")

        # Check if the settings file exists
        if not SAML_PATH.is_file():
            return HttpResponse("Settings file not found.", status=404)

        # # Read the JSON settings
        # with open(SAML_PATH, 'r') as f:
        #     saml_settings_json = json.load(f)

        # # Pass the loaded JSON data to OneLogin_Saml2_Settings
        # saml_settings = OneLogin_Saml2_Settings(settings=saml_settings_json)
        print("SAML settings loaded successfully.")
        
        # Initialize OneLogin_Saml2_Auth with the loaded settings
        auth = OneLogin_Saml2_Auth(req, custom_base_path=str(BASE_DIR))  # Ensure correct base path
        return redirect(auth.login())
    
    except Exception as e:
        print(f"Error loading SAML settings: {e}")
        return HttpResponse("Error processing SAML login.", status=500)  # Return an error response

# def sso_acs(request):
#     req = prepare_django_request(request)
#     auth = OneLogin_Saml2_Auth(req, custom_base_path=str(settings.SAML_PATH))  # Ensure correct base path
#     auth.process_response()
    
#     if auth.is_authenticated():
#         user_email = auth.get_nameid()
#         user, created = User.objects.get_or_create(email=user_email)
#         login(request, user)  # Log in the user
#         return redirect('dashboard')  # Adjust the redirect to your dashboard
#     else:
#         return HttpResponse("SAML Authentication failed.", status=401)

def sso_acs(request):
    req = prepare_django_request(request)
    
    # Ensure that SAML_PATH is defined in your settings
    try:
        BASE_DIR = Path(__file__).resolve().parent.parent
        auth = OneLogin_Saml2_Auth(req, custom_base_path=str(BASE_DIR))
        auth.process_response()
        
        if auth.is_authenticated():
            user_email = auth.get_nameid()
            user, created = User.objects.get_or_create(email=user_email)
            login(request, user)  # Log in the user
            return redirect('dashboard')  # Adjust the redirect to your dashboard
        else:
            return HttpResponse("SAML Authentication failed.", status=401)
    
    except AttributeError as e:
        return HttpResponse(f"Configuration error: {str(e)}", status=500)
    except Exception as e:
        return HttpResponse(f"An error occurred during SAML processing: {str(e)}", status=500)