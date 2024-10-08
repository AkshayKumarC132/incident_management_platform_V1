from rest_framework import serializers
from .models import *
import math

class RegisterSerializer(serializers.Serializer):
    username=serializers.CharField()
    first_name=serializers.CharField(default="")
    last_name=serializers.CharField(default="")
    email=serializers.EmailField()
    password=serializers.CharField()
    msp = serializers.PrimaryKeyRelatedField(queryset=MSP.objects.all())  # Use PrimaryKeyRelatedField

class MSPSerializer(serializers.ModelSerializer):
    class Meta:
        model = MSP
        fields = ['id', 'name']  # Replace 'name' with the actual field you want to display

class LoginSerialzier(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class MSPSerializer(serializers.ModelSerializer):
    class Meta:
        model = MSP
        fields = '__all__'
        
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'  # This will include all fields in the model
        
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'  # This will include all fields in the model
        
class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = '__all__'  # This will include all fields in the model
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Handle NaN for predicted_resolution_time
        predicted_resolution_time = representation.get('predicted_resolution_time', None)
        if isinstance(predicted_resolution_time, float) and math.isnan(predicted_resolution_time):
            representation['predicted_resolution_time'] = None  # or a default value, e.g., -1.0
        return representation
        