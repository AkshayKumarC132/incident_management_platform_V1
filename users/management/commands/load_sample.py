from django.core.management.base import BaseCommand
from users.models import Incident, Device, Severity, Client, MSP  # Import MSP
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Load sample incident data into the database'

    def handle(self, *args, **kwargs):
        # Create sample MSPs
        msps = [
            {'name': 'MSP A'},
            {'name': 'MSP B'},
            {'name': 'MSP C'},
            {'name': 'MSP D'},
            {'name': 'MSP E'},
            {'name': 'MSP F'},
            {'name': 'MSP G'},
            {'name': 'MSP H'},
            {'name': 'MSP I'},
            {'name': 'MSP J'},
            {'name': 'MSP K'},
            {'name': 'MSP L'},
        ]

        msp_objects = []
        for msp_data in msps:
            msp, created = MSP.objects.get_or_create(name=msp_data['name'])
            msp_objects.append(msp)  # Store created MSPs

        # Create sample clients, ensuring they are linked to an MSP
        clients = [
            {'name': 'Client A'},
            {'name': 'Client B'},
            {'name': 'Client C'},
            {'name': 'Client D'},
            {'name': 'Client E'},
            {'name': 'Client F'},
            {'name': 'Client G'},
            {'name': 'Client H'},
            {'name': 'Client I'},
            {'name': 'Client J'},
            {'name': 'Client K'},
            {'name': 'Client L'},
        ]

        client_objects = []
        for client_data in clients:
            # Randomly assign an MSP to each client
            msp = random.choice(msp_objects)
            client, created = Client.objects.get_or_create(
                name=client_data['name'], 
                msp=msp  # Ensure to assign the MSP
            )
            client_objects.append(client)

        # Sample devices to ensure device instances exist
        devices = [
            {'name': 'Router A', 'device_type': 'Router'},
            {'name': 'Switch B', 'device_type': 'Switch'},
            {'name': 'Firewall C', 'device_type': 'Firewall'},
            {'name': 'Server D', 'device_type': 'Server'},
            {'name': 'Access Point E', 'device_type': 'Access Point'},
            {'name': 'NAS F', 'device_type': 'NAS'},
            {'name': 'Printer G', 'device_type': 'Printer'},
            {'name': 'Laptop H', 'device_type': 'Laptop'},
            {'name': 'Desktop I', 'device_type': 'Desktop'},
            {'name': 'Tablet J', 'device_type': 'Tablet'},
            {'name': 'Router K', 'device_type': 'Router'},
            {'name': 'Switch L', 'device_type': 'Switch'},
            {'name': 'Firewall M', 'device_type': 'Firewall'},
            {'name': 'Server N', 'device_type': 'Server'},
            {'name': 'Access Point O', 'device_type': 'Access Point'},
            {'name': 'NAS P', 'device_type': 'NAS'},
            {'name': 'Printer Q', 'device_type': 'Printer'},
            {'name': 'Laptop R', 'device_type': 'Laptop'},
            {'name': 'Desktop S', 'device_type': 'Desktop'},
            {'name': 'Tablet T', 'device_type': 'Tablet'},
        ]

        # Create devices if they do not exist
        for device_data in devices:
            # Randomly assign a client to each device
            client = random.choice(client_objects)
            Device.objects.get_or_create(
                name=device_data['name'], 
                device_type=device_data['device_type'],
                client=client  # Assign the client
            )

        severities = ['Low', 'Medium', 'High']
        num_of_incidents = 2000  # Increase the number of incidents for testing

        for i in range(num_of_incidents):
            severity_level = random.choice(severities)

            # Ensure the severity exists or create it
            severity, created = Severity.objects.get_or_create(level=severity_level)

            # Randomly select a device
            device = random.choice(Device.objects.all())

            # Create a new incident
            inc = Incident.objects.create(
                title=f'Sample Incident {i + 1} for {device.name}',
                description=f'Description of the incident related to {device.name}.',
                device=device,
                severity=severity,
                resolved=random.choice([True, False]),  # Randomly resolve incidents
                created_at=datetime.now() - timedelta(days=random.randint(1, 30)),  # Random date within the last 30 days
                recommended_solution='Default solution based on severity',
                predicted_resolution_time=random.uniform(1.0, 5.0)  # Random prediction time between 1 to 5 hours
            )
            print(inc.title)

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {num_of_incidents} sample incidents.'))
