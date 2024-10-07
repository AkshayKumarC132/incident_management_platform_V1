from django.core.management.base import BaseCommand
from users.models import Incident, Device, Severity, Client, MSP
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Load sample incident data into the database'

    def handle(self, *args, **kwargs):
        # Create sample MSPs with realistic names
        msps = [
            {'name': 'Tech Solutions Inc.'},
            {'name': 'Network Innovations LLC'},
            {'name': 'CyberGuard Services'},
            {'name': 'CloudOps Partners'},
            {'name': 'DataSecure Corp.'},
            {'name': 'IT Wizards'},
            {'name': 'SysAdmin Experts'},
            {'name': 'Digital Shield'},
            {'name': 'Smart Networks'},
            {'name': 'TechSavvy Solutions'},
        ]

        msp_objects = []
        for msp_data in msps:
            msp, created = MSP.objects.get_or_create(name=msp_data['name'])
            msp_objects.append(msp)

        # Create sample clients linked to an MSP
        clients = [
            {'name': 'Acme Corp.'},
            {'name': 'Global Industries'},
            {'name': 'Future Tech'},
            {'name': 'Innovative Solutions'},
            {'name': 'NextGen Systems'},
            {'name': 'Eco-Friendly Enterprises'},
            {'name': 'HealthPlus Services'},
            {'name': 'Finance Group'},
            {'name': 'Retail Dynamics'},
            {'name': 'Travel Smart Co.'},
        ]

        client_objects = []
        for client_data in clients:
            msp = random.choice(msp_objects)
            client, created = Client.objects.get_or_create(
                name=client_data['name'], 
                msp=msp
            )
            client_objects.append(client)

        # Sample devices with realistic types
        devices = [
            {'name': f'Router {i}', 'device_type': 'Router'} for i in range(1, 6)
        ] + [
            {'name': f'Switch {i}', 'device_type': 'Switch'} for i in range(1, 6)
        ] + [
            {'name': f'Firewall {i}', 'device_type': 'Firewall'} for i in range(1, 6)
        ] + [
            {'name': f'Server {i}', 'device_type': 'Server'} for i in range(1, 6)
        ] + [
            {'name': f'Access Point {i}', 'device_type': 'Access Point'} for i in range(1, 6)
        ]

        # Create devices if they do not exist
        for device_data in devices:
            client = random.choice(client_objects)
            Device.objects.get_or_create(
                name=device_data['name'], 
                device_type=device_data['device_type'],
                client=client
            )

        severities = ['Low', 'Medium', 'High', 'Critical']
        num_of_incidents = 500

        for i in range(num_of_incidents):
            severity_level = random.choice(severities)
            severity, created = Severity.objects.get_or_create(level=severity_level)

            device = random.choice(Device.objects.all())

            # Generate a more detailed incident description
            descriptions = [
                f'Network outage affecting {device.name}.',
                f'Security breach detected on {device.name}.',
                f'Maintenance required for {device.name}.',
                f'Performance issues reported on {device.name}.',
                f'Configuration error found on {device.name}.'
            ]
            
            inc = Incident.objects.create(
                title=f'Incident #{i + 1}: Issue with {device.name}',
                description=random.choice(descriptions),
                device=device,
                severity=severity,
                resolved=random.choice([True, False]),
                created_at=datetime.now() - timedelta(days=random.randint(0, 30)),
                recommended_solution='Investigate and resolve based on severity level.',
                predicted_resolution_time=random.uniform(0.5, 4.0)  # Random prediction time between 0.5 to 4 hours
            )
            
            print(f'Created: {inc.title}')

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {num_of_incidents} sample incidents.'))