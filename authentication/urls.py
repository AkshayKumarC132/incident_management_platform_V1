# apps/authentication/urls.py
from django.urls import path
from .views import sso_login, sso_acs

urlpatterns = [
    path('login/', sso_login, name='sso_login'),  # URL for SSO login
    path('acs/', sso_acs, name='sso_acs'),  # URL for SSO Assertion Consumer Service
]
