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

        # Predefined device data based on the Device model
        device_data = [
            {"client": random.choice(client_objects), "name": "Router-1", "device_type": "Router", "ip_address": "192.168.1.1"},
            {"client": random.choice(client_objects), "name": "Router-2", "device_type": "Router", "ip_address": "192.168.1.2"},
            {"client": random.choice(client_objects), "name": "Switch-1", "device_type": "Switch", "ip_address": "192.168.1.3"},
            {"client": random.choice(client_objects), "name": "Switch-2", "device_type": "Switch", "ip_address": "192.168.1.4"},
            {"client": random.choice(client_objects), "name": "Firewall-1", "device_type": "Firewall", "ip_address": "192.168.1.5"},
            {"client": random.choice(client_objects), "name": "Server-1", "device_type": "Server", "ip_address": "192.168.1.6"},
            {"client": random.choice(client_objects), "name": "Server-2", "device_type": "Server", "ip_address": "192.168.1.7"},
            {"client": random.choice(client_objects), "name": "Access Point-1", "device_type": "Access Point", "ip_address": "192.168.1.8"},
            {"client": random.choice(client_objects), "name": "Access Point-2", "device_type": "Access Point", "ip_address": "192.168.1.9"},
        ]

        # Create devices in the database
        device_objects = []
        for device_info in device_data:
            device, created = Device.objects.get_or_create(
                name=device_info['name'],
                device_type=device_info['device_type'],
                client=device_info['client'],
                ip_address=device_info['ip_address']
            )
            device_objects.append(device)

        # Define severities with fixed IDs
        severities = {
            1: 'Low',
            2: 'Medium',
            3: 'High'
        }

        num_of_incidents = 500

        # Extensive incident data with 30 real-time examples
        incident_data = [
            {
                "title": "Network Outage in Main Office",
                "description": "A complete network outage has been reported in the main office affecting all employees. Immediate investigation required.",
                "solution": "Check router configurations and restart network devices.",
                "predicted_resolution_time": random.uniform(1.0, 3.0)
            },
            {
                "title": "Security Breach Detected",
                "description": "Suspicious activity detected on the firewall. Possible unauthorized access attempt.",
                "solution": "Review firewall logs and implement additional security measures.",
                "predicted_resolution_time": random.uniform(0.5, 2.0)
            },
            {
                "title": "Server Performance Degradation",
                "description": "The application server is experiencing performance issues leading to slow response times.",
                "solution": "Analyze server load and optimize resource allocation.",
                "predicted_resolution_time": random.uniform(0.5, 4.0)
            },
            {
                "title": "Configuration Error on Device",
                "description": "Configuration error found on the access point causing connectivity issues for users.",
                "solution": "Revert to previous configuration and test connectivity.",
                "predicted_resolution_time": random.uniform(0.5, 1.5)
            },
            {
                "title": "Malware Detected on Workstation",
                "description": "Malware has been detected on a workstation which may compromise sensitive data.",
                "solution": "Isolate the affected workstation and run a full antivirus scan.",
                "predicted_resolution_time": random.uniform(1.0, 2.5)
            },
            {
                "title": "Database Connection Timeout",
                "description": "The application is unable to connect to the database due to timeout errors.",
                "solution": "Check database server status and network connectivity.",
                "predicted_resolution_time": random.uniform(1.0, 2.0)
            },
            {
                "title": "Email Service Disruption",
                "description": "Users are unable to send or receive emails due to service disruption.",
                "solution": "Restart the email service and check for any server-side issues.",
                "predicted_resolution_time": random.uniform(0.5, 3.0)
            },
            {
                "title": "Data Loss Incident",
                "description": "Critical data loss reported by a user after a system update.",
                "solution": "Restore data from backups and investigate update logs.",
                "predicted_resolution_time": random.uniform(2.0, 5.0)
            },
            {
                "title": "Unauthorized Access Alert",
                "description": "An alert has been triggered due to unauthorized access attempts on sensitive files.",
                "solution": "Change access credentials and review security protocols.",
                "predicted_resolution_time": random.uniform(1.0, 3.0)
            },
            {
                "title": "VPN Connectivity Issues",
                "description": "Remote users are experiencing issues connecting to the VPN service.",
                "solution": "Check VPN server status and user configurations.",
                "predicted_resolution_time": random.uniform(1.0, 2.5)
            },
            {
                "title": "Backup Failure Notification",
                "description": "Scheduled backups have failed for multiple systems; immediate attention required.",
                "solution": "Investigate backup logs and retry backups manually if necessary.",
                "predicted_resolution_time": random.uniform(1.0, 3.0)
            },
            {
                "title": "Hardware Failure Detected",
                "description": f"Hardware failure detected on {random.choice(['Server-1', 'Router-2', 'Switch-3'])}. Immediate replacement needed.",
                "solution": f"Replace faulty hardware and restore services from backup systems.",
                "predicted_resolution_time": random.uniform(2.0, 4.0)
            },
            {
                "title": f"User Account Lockout",
                "description": f"User account {random.choice(['john.doe', 'jane.smith'])} has been locked out after multiple failed login attempts.",
                "solution": f"Unlock the account and review login attempts for suspicious activity.",
                "predicted_resolution_time": random.uniform(0.5, 1.5)
            },
            {
                "title": "Phishing Email Reported",
                "description": "A user has reported receiving a phishing email that attempts to steal credentials.",
                "solution": "Educate users on identifying phishing attempts and block sender.",
                "predicted_resolution_time": random.uniform(0.5, 1.5)
            },
            {
                "title": "Software Update Required",
                "description": "Critical software updates are pending for multiple systems.",
                "solution": "Schedule updates during off-peak hours to minimize disruption.",
                "predicted_resolution_time": random.uniform(1.0, 2.5)
            },
            {
                "title": "Network Latency Issues",
                "description": "Users are experiencing high latency when accessing internal applications.",
                "solution": "Investigate network traffic and optimize routing configurations.",
                "predicted_resolution_time": random.uniform(1.0, 3.0)
            },
            {
                "title": "File Server Unreachable",
                "description": "Users cannot access shared files on the file server due to connectivity issues.",
                "solution": "Check server status and restart services if needed.",
                "predicted_resolution_time": random.uniform(1.0, 2.0)
            },
            {
                "title": "Application Crash Reported",
                "description": f"The accounting application crashed unexpectedly during use by {random.choice(['John Doe', 'Jane Smith'])}.",
                "solution": f"Review application logs for errors and restart the application.",
                "predicted_resolution_time": random.uniform(1.5, 3.5)
            },
            {
                "title": "Printer Malfunction",
                "description": f"A printer in the {random.choice(['HR Department', 'Finance Department'])} is not responding.",
                "solution": f"Check printer connections and restart printer services.",
                "predicted_resolution_time": random.uniform(0.5, 1.5)
            },
            {
                "title": "SSL Certificate Expired",
                "description": f"The SSL certificate for {random.choice(['example.com', 'company.com'])} has expired.",
                "solution": f"Renew the SSL certificate immediately to avoid security risks.",
                "predicted_resolution_time": random.uniform(1.0, 2.0)
            },
            {
                "title": "Power Outage Reported",
                "description": f"A power outage has affected multiple workstations in the {random.choice(['Main Office', 'Branch Office'])}.",
                "solution": f"Ensure all critical systems are connected to UPS devices.",
                "predicted_resolution_time": random.uniform(2.0, 4.0)
            },
            {
                "title": "Data Migration Failure",
                "description": f"Data migration from legacy systems failed due to incompatible formats.",
                "solution": f"Review migration scripts and retry migration after adjustments.",
                "predicted_resolution_time": random.uniform(2.5, 5.0)
            },
            {
                "title": "Compliance Audit Findings",
                "description": "Recent compliance audit identified several areas needing immediate attention.",
                "solution": "Address findings as per compliance guidelines.",
                "predicted_resolution_time": random.uniform(2.0, 6.0),
            }
        ]

        for i in range(num_of_incidents):
            severity_id = random.choice(list(severities.keys()))  # Randomly select a severity ID
            severity_level = severities[severity_id]  # Get severity level by ID
            
            severity, created = Severity.objects.get_or_create(level=severity_level)

            # Assign a real Device instance instead of a string
            device = random.choice(device_objects)

            incident_info = random.choice(incident_data)

            inc = Incident.objects.create(
                title=f'Incident #{i + 1}: {incident_info["title"]}',
                description=incident_info["description"],
                device=device,
                severity=severity,
                resolved=random.choice([True, False]),
                created_at=datetime.now() - timedelta(days=random.randint(0, 30)),
                recommended_solution=incident_info.get("solution"),
                predicted_resolution_time=incident_info.get("predicted_resolution_time")
            )

            print(f'Created: {inc.title}')

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {num_of_incidents} sample incidents.'));