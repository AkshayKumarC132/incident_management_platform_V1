# views.py

from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import MSP, Client, Device, Incident,Severity, UserProfile
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

# Home view (rendering an HTML page)
def home(request):
    return render(request, 'home.html')  # Render the home template


# Register view with template rendering for registration
@require_http_methods(["POST", "GET"])
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken!')
            return redirect('register')

        # Create the user
        user = User.objects.create_user(username=username, password=password)
        messages.success(request, 'User registered successfully!')

        # Ensure there is a default MSP
        default_msp = MSP.objects.first()
        if default_msp:
            UserProfile.objects.create(user=user, msp=default_msp)

        messages.success(request, 'User registered successfully! Please log in.')
        return redirect('login')
    
    # Render registration page
    return render(request, 'registration.html')


# Login view with template rendering for authentication
@require_http_methods(["POST", "GET"])
def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home after successful login
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    # Render login page
    return render(request, 'login.html')
# Fetch the list of MSPs
# List all MSPs
@login_required
@require_http_methods(["GET"])
def list_msps(request):
    msps = MSP.objects.all()
    return render(request, 'msps.html', {'msps': msps})  # Create a list_msps.html template

# Add a new MSP
@login_required
@require_http_methods(["POST", "GET"])
def create_msp(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            msp = MSP.objects.create(name=name)
            messages.success(request, 'MSP created successfully!')
            return redirect('list_msps')  # Redirect to the list of MSPs
        else:
            messages.error(request, 'Invalid data!')
    
    return render(request, 'create_msps.html')  # Create a create_msp.html template
# Get MSP details
# Get MSP details
@login_required
@require_http_methods(["GET"])
def get_msp(request, msp_id):
    msp = get_object_or_404(MSP, id=msp_id)
    return render(request, 'get_msps.html', {'msp': msp})  # Create a get_msp.html template

# Fetch clients of an MSP
# Fetch clients of an MSP
@login_required
@require_http_methods(["GET"])
def list_clients(request, msp_id):
    clients = Client.objects.filter(msp_id=msp_id)
    return render(request, 'clients.html', {'clients': clients, 'msp_id': msp_id})  # Create a list_clients.html template


# Add a new client under an MSP
@login_required
@require_http_methods(["POST"])
@csrf_exempt
def create_client(request, msp_id):
    name = request.POST.get('name')
    msp = get_object_or_404(MSP, id=msp_id)
    if name:
        client = Client.objects.create(name=name, msp=msp)
        return JsonResponse({'id': client.id, 'name': client.name, 'created_at': client.created_at})
    else:
        return JsonResponse({'error': 'Invalid data'}, status=400)

# Fetch devices of a client
@login_required
@require_http_methods(["GET"])
@csrf_exempt
def list_devices(request, client_id):
    devices = Device.objects.filter(client_id=client_id).values('id', 'name', 'device_type', 'ip_address', 'created_at')
    return JsonResponse(list(devices), safe=False)

# Add a new device under a client
@login_required
@require_http_methods(["POST"])
@csrf_exempt
def create_device(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    name = request.POST.get('name')
    device_type = request.POST.get('device_type')
    ip_address = request.POST.get('ip_address', None)

    if name and device_type:
        device = Device.objects.create(client=client, name=name, device_type=device_type, ip_address=ip_address)
        return JsonResponse({'id': device.id, 'name': device.name, 'device_type': device.device_type, 'created_at': device.created_at})
    else:
        return JsonResponse({'error': 'Invalid data'}, status=400)

# Fetch incidents of a device
@login_required
@require_http_methods(["GET"])
@csrf_exempt
def list_incidents(request, device_id):
    incidents = Incident.objects.filter(device_id=device_id).values('id', 'title', 'description', 'severity_id', 'resolved', 'created_at')
    return JsonResponse(list(incidents), safe=False)

# Add a new incident under a device
@login_required
@require_http_methods(["POST"])
@csrf_exempt
def create_incident(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    title = request.POST.get('title')
    description = request.POST.get('description')
    severity_id = request.POST.get('severity_id')

    if title and description and severity_id:
        severity = get_object_or_404(Severity, id=severity_id)
        incident = Incident.objects.create(device=device, title=title, description=description, severity=severity)
        return JsonResponse({'id': incident.id, 'title': incident.title, 'description': incident.description, 'resolved': incident.resolved, 'created_at': incident.created_at})
    else:
        return JsonResponse({'error': 'Invalid data'}, status=400)
