# Incident Management Platform

This is an Incident Management Platform designed for MSPs and MSSPs, featuring SSO integration, user management, and incident tracking. 

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- Single Sign-On (SSO) authentication using SAML
- Role-based access control
- Incident management and tracking
- User and team management

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your machine.
- Git installed on your machine.
- A virtual environment manager (optional, but recommended).

## Installation

Follow these steps to get your development environment set up:

1. **Clone the repository:**

   Open your terminal and run:

   ```bash
   git clone https://github.com/yourusername/incident_management_platform_V1.git
   cd incident_management_platform_V1

## Setting up a Virtual Environment (Optional but Recommended)

2. Creating a virtual environment isolates your project dependencies and prevents conflicts with other Python projects.
### Activating the Virtual Environment 

   ```bash
   venv\Scripts\activate
   ```

#### For macOS/Linux:
```bash
   source venv/bin/activate
```
## Installing Dependencies

After activating your virtual environment, install the required dependencies using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

## Running the Development Server

Start the Django development server:
```bash
python manage.py runserver
```

The application will be accessible at `http://127.0.0.1:8000/`.