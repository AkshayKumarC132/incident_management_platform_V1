from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from pytz import utc
from .serializers import *
from .models import *
from rest_framework import status
from django.contrib.auth.decorators import login_required
from rest_framework import generics, permissions
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import MSP
from .serializers import MSPSerializer
from rest_framework.views import APIView
from .ml_model import IncidentMLModel  # Assuming this is the ML integration part
from django.db.models import Avg,Count
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from datetime import datetime
from django.shortcuts import redirect



# created_at=datetime.datetime.now(utc)

class RegisterViewAPI(APIView):
    serializer_class= RegisterSerializer
    
    def get(self, request):
        # Fetch MSP records
        msp_records = MSP.objects.all()
        # Render the registration page with MSP records
        return render(request, 'register.html', {'msp_records': msp_records})

    @transaction.atomic()
    @csrf_exempt
    def post(self,request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            f_name = serializer.validated_data['first_name']
            l_name = serializer.validated_data['last_name']
            email = serializer.validated_data['email']
            pwd = serializer.validated_data['password']
            msp_id = serializer.validated_data['msp'].id  # Get the msp ID from the validated data
            # Create the user
            user = User.objects.create_user(
                username=username,
                email = email,
                first_name = f_name,
                last_name = l_name,
                password=pwd
                )
            
            # Ensure there is a default MSP
            default_msp = MSP.objects.get(id = msp_id)
            if default_msp:
                UserProfile.objects.create(user=user, msp=default_msp)

            
            # Redirect to a success page or login page after registration
            return render(request, 'registration_success.html')

        return Response({"message":serializer.error_messages},status=status.HTTP_400_BAD_REQUEST)
    
    # def get(self, request):
    #     msp_records = MSP.objects.all()
    #     serializer = MSPSerializer(msp_records, many=True)  # Use MSPSerializer
    #     print(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    
class LoginViewAPI(CreateAPIView):
    serializer_class = LoginSerialzier
    
    def get(self, request):
        # Render the login page
        return render(request, 'login.html')

    @csrf_exempt
    def post(self,request):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            username  = serializer.data['username']
            password = serializer.data['password']
            print(username,password)
            # Authenticate the user
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return render(request, 'dashboard.html')
            else:
                return Response({'message':"Invalid username or password"},status=status.HTTP_401_UNAUTHORIZED)



@method_decorator(login_required(login_url='/account/login/'), name='dispatch')
class MSPListView(generics.ListCreateAPIView):
    queryset = MSP.objects.all()  # Queryset to fetch all MSP instances
    serializer_class = MSPSerializer  # Serializer to convert queryset to JSON
    permission_classes = [permissions.IsAuthenticated]  # Ensure user is authenticated

@method_decorator(login_required(login_url='/account/login/'), name='dispatch')
class MSPDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MSP.objects.all()
    serializer_class = MSPSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
@method_decorator(login_required(login_url='/account/login/'), name='dispatch')
class ClientListView(generics.ListCreateAPIView):
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        msp_id = self.kwargs['msp_id']
        return Client.objects.filter(msp_id=msp_id)

@method_decorator(login_required(login_url='/account/login/'), name='dispatch')
class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        msp_id = self.kwargs['msp_id']
        return Client.objects.filter(msp_id=msp_id)
    
@method_decorator(login_required(login_url='/account/login/'), name='dispatch')
class DeviceListView(generics.ListCreateAPIView):
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        client_id = self.kwargs['client_id']
        return Device.objects.filter(client_id=client_id)

@method_decorator(login_required(login_url='/account/login/'), name='dispatch')
class DeviceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        client_id = self.kwargs['client_id']
        return Device.objects.filter(client_id=client_id)
    
    
@method_decorator(login_required(login_url='/account/login/'), name='dispatch')
class IncidentListView(generics.ListCreateAPIView):
    serializer_class = IncidentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        device_id = self.kwargs['device_id']
        return Incident.objects.filter(device_id=device_id)
    
    def perform_create(self, serializer):
        incident = serializer.save()
        ml_model = IncidentMLModel()

        try:
            ml_model.load_models()
            predicted_solution = ml_model.predict_solution(incident)
            predicted_time = ml_model.predict_time(incident)
        except Exception as e:
            print(f"Prediction error: {e}")
            predicted_solution = "No prediction available"
            predicted_time = 1.0  # Default resolution time

        incident.recommended_solution = predicted_solution
        incident.predicted_resolution_time = predicted_time
        incident.save()

        # Prepare the response data
        response_data = {
            "id": incident.id,
            "title": incident.title,
            "description": incident.description,
            "resolved": incident.resolved,
            "created_at": incident.created_at,
            "recommended_solution": incident.recommended_solution,
            "predicted_resolution_time": incident.predicted_resolution_time,
            "device": incident.device.id if incident.device else None,
            "severity": incident.severity,
            "device_type": incident.device.device_type if incident.device else None,  # Safely access device_type
        }

        # Clean response data to handle NaN
        cleaned_response = self.clean_response(response_data)

        return Response(cleaned_response)

    def clean_response(self, data):
        # Replace NaN with None or a default value
        return {key: (value if not isinstance(value, float) or not math.isnan(value) else None) 
                for key, value in data.items()}


@method_decorator(login_required(login_url='/account/login/'), name='dispatch')
class IncidentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IncidentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        device_id = self.kwargs['device_id']
        return Incident.objects.filter(device_id=device_id)
    
    def perform_create(self, serializer):
        incident = serializer.save()

        # Load the ML model
        ml_model = IncidentMLModel()
        try:
            ml_model.load_models()
        except Exception as e:
            print(f"Error loading models: {e}")
            return Response({'message': 'Error loading models'}, status=500)

        # Extract features from the incident
        features = ml_model.extract_features(incident)

        # Predict the solution and time based on the incident
        try:
            predicted_solution = ml_model.predict_solution(incident)
            predicted_time = ml_model.predict_time(incident)
        except Exception as e:
            print(f"Error predicting: {e}")
            predicted_solution = "Default solution based on severity"
            predicted_time = 2.0  # Default prediction in hours

        # Update the incident with predictions
        incident.recommended_solution = predicted_solution
        incident.predicted_resolution_time = predicted_time
        incident.save()

        # Prepare the response data
        response_data = {
            "id": incident.id,
            "title": incident.title,
            "description": incident.description,
            "resolved": incident.resolved,
            "created_at": incident.created_at,
            "recommended_solution": incident.recommended_solution,
            "predicted_resolution_time": incident.predicted_resolution_time,
            "device": incident.device.id if incident.device else None,
            "severity": incident.severity,
            "device_type": incident.device.device_type if incident.device else None,  # Safely access device_type
        }

        # Clean response data to handle NaN
        cleaned_response = self.clean_response(response_data)

        return Response(cleaned_response)

    def clean_response(self, data):
        # Replace NaN with None or a default value
        return {key: (value if not isinstance(value, float) or not math.isnan(value) else None) 
                for key, value in data.items()}
        
        

from django.core.paginator import Paginator
def dashboard_view(request):
    # Fetch all incidents and devices
    incident_list = Incident.objects.all()
    device_list = Device.objects.all()
    
    # Pagination for incidents
    incident_paginator = Paginator(incident_list, 50)  # Show 50 incidents per page
    incident_page_number = request.GET.get('incident_page')
    incident_page_obj = incident_paginator.get_page(incident_page_number)

    # Pagination for devices
    device_paginator = Paginator(device_list, 50)  # Show 50 devices per page
    device_page_number = request.GET.get('device_page')
    device_page_obj = device_paginator.get_page(device_page_number)

    # KPI calculations
    total_incidents = Incident.objects.count()
    resolved_incidents = Incident.objects.filter(resolved=True).count()
    unresolved_incidents = Incident.objects.filter(resolved=False).count()
    avg_resolution_time = Incident.objects.aggregate(Avg('predicted_resolution_time'))['predicted_resolution_time__avg'] or 0
    severity_counts = Incident.objects.values('severity__level').annotate(count=Count('id'))

    context = {
        'total_incidents': total_incidents,
        'resolved_incidents': resolved_incidents,
        'unresolved_incidents': unresolved_incidents,
        'avg_resolution_time': avg_resolution_time,
        'incident_page_obj': incident_page_obj,
        'device_page_obj': device_page_obj,
        'severity_counts': severity_counts,
    }

    return render(request, 'dashboard.html', context)

def generate_custom_report(request):
    # Fetch severity levels and device types (unique values from Device model)
    severities = Severity.objects.all()
    device_types = Device.objects.values_list('device_type', flat=True).distinct()  # Get unique device types

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        severity = request.POST.get('severity')
        device_type = request.POST.get('device_type')
        resolved = request.POST.get('resolved')
        
        # Convert string dates to datetime objects
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
        
        # Set end_date to the end of the day
        end_date_obj = end_date_obj.replace(hour=23, minute=59, second=59, microsecond=999999)

        # Debugging information
        print(f"Filtering incidents from {start_date_obj} to {end_date_obj}, severity: {severity}, device_type: {device_type}, resolved: {resolved}")

        # Filter incidents
        incidents = Incident.objects.filter(
            created_at__range=[start_date_obj, end_date_obj]
        )

        if severity != 'all':
            incidents = incidents.filter(severity__level=severity)  # Use severity level for filtering
        if device_type != 'all':
            incidents = incidents.filter(device__device_type=device_type)
        if resolved == 'resolved':
            incidents = incidents.filter(resolved=True)
        elif resolved == 'unresolved':
            incidents = incidents.filter(resolved=False)

        # Convert incidents to DataFrame for further processing (optional)
        df = pd.DataFrame(list(incidents.values()))

        # Check if the user requested an export
        if 'export_csv' in request.POST:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="custom_report.csv"'
            df.to_csv(path_or_buf=response, index=False)
            return response

        # Return filtered incidents and render the report template
        context = {
            'incidents': incidents,
            'report_data': df.to_dict('records'),  # Optional, for displaying in a table
            'severities': severities,
            'device_types': device_types,
        }
        print(context)
        return render(request, 'custom_report_results.html', context)

    # For GET requests, render the initial form with available options
    return render(request, 'custom_report.html', {
        'severities': severities,
        'device_types': device_types,
    })