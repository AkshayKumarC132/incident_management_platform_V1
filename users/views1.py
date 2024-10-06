from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
import datetime
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


# created_at=datetime.datetime.now(utc)

class RegisterViewAPI(APIView):
    serializer_class= RegisterSerializer

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

            
            return Response({"message":'User registered successfully! Please log in.'},status=status.HTTP_200_OK)
        return Response({"message":serializer.error_messages},status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        msp_records = MSP.objects.all()
        serializer = MSPSerializer(msp_records, many=True)  # Use MSPSerializer
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class LoginViewAPI(CreateAPIView):
    serializer_class = LoginSerialzier

    @csrf_exempt
    def post(self,request):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            username  = serializer.data['username']
            password = serializer.data['password']
            
            # Authenticate the user
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return Response({'message':"User Login Successfull"},status=status.HTTP_200_OK)
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