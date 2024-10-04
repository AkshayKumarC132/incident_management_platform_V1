# urls.py
from django.urls import path
from .views1 import *

urlpatterns = [
    # path('', views.home, name='home'), 
    # path('register/',views.register,name='Register'),
    # path('login/', views.custom_login_view, name='login'),
    # path('msps/', list_msps, name='list_msps'),
    # path('msps/create/', views.create_msp, name='create_msp'),
    # path('msps/<int:msp_id>/', views.get_msp, name='get_msp'),

    # path('msps/<int:msp_id>/clients/', views.list_clients, name='list_clients'),
    # path('msps/<int:msp_id>/clients/create/', views.create_client, name='create_client'),

    # path('clients/<int:client_id>/devices/', views.list_devices, name='list_devices'),
    # path('clients/<int:client_id>/devices/create/', views.create_device, name='create_device'),

    # path('devices/<int:device_id>/incidents/', views.list_incidents, name='list_incidents'),
    # path('devices/<int:device_id>/incidents/create/', views.create_incident, name='create_incident'),
    
    
    path('signup',RegisterViewAPI.as_view(),name='Signup Page'),
    path('login',LoginViewAPI.as_view(),name='Login'),
    
    path('msp/', MSPListView.as_view(), name='msp-list'),  # List of all MSPS
    path('msp/<int:pk>/', MSPDetailView.as_view(), name='msp-detail'),  # Detail view for specific MSP
    
    path('msp/<int:msp_id>/clients/', ClientListView.as_view(), name='client-list-create'),  # List and create clients for a specific MSP
    path('msp/<int:msp_id>/clients/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),  # Retrieve, update, delete a specific client
    
    path('clients/<int:client_id>/devices/', DeviceListView.as_view(), name='device-list-create'),  # List and create devices for a specific client
    path('clients/<int:client_id>/devices/<int:pk>/', DeviceDetailView.as_view(), name='device-detail'),  # Retrieve, update, delete a specific device
    
    path('devices/<int:device_id>/incidents/', IncidentListView.as_view(), name='incident-list-create'),  # List and create incidents for a specific device
    path('devices/<int:device_id>/incidents/<int:pk>/', IncidentDetailView.as_view(), name='incident-detail'),  # Retrieve, update, delete a specific incident
]
