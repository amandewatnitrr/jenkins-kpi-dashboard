from django.shortcuts import render
from .models import jenkins_servers
import jenkins
import requests

import requests
import jenkins

def get_jenkins_server_details(server_url, username, password):
    # Disable SSL certificate verification (not recommended for production)
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

    # Create a Jenkins server instance
    server = jenkins.Jenkins(server_url, username=username, password=password, timeout=10)

    # Get server details using the Jenkins API with SSL verification disabled
    try:
        response = requests.get(
            f"{server_url.rstrip('/')}/crumbIssuer/api/json",
            auth=(username, password),
            timeout=10,
            verify=False  # Disable SSL verification
        )
        response.raise_for_status()
        server_info = response.json()
    except requests.RequestException as e:
        # Handle the exception (e.g., log the error)
        print(f"Error retrieving Jenkins server details: {e}")
        return 'N/A', 'N/A', 'N/A', 'Not Working'

    # Extract relevant information
    server_up_time = server_info.get('mode', 'N/A')
    response_time = server_info.get('quietingDown', 'N/A')
    network_latency = server_info.get('useSecurity', 'N/A')  # You may need to adjust this field
    status = 'Working' if server_info.get('mode', 'NORMAL') == 'NORMAL' else 'Not Working'

    return server_up_time, response_time, network_latency, status

def update_jenkins_server_details():
    # Fetch all Jenkins servers from the database
    jenkins_servers_list = jenkins_servers.objects.all()

    for server in jenkins_servers_list:
        # Get Jenkins server details from the API
        server_up_time, response_time, network_latency, status = get_jenkins_server_details(
            server.server_url,
            'your_jenkins_username',
            'your_jenkins_password'
        )

        # Update the database with the obtained details
        server.server_up_time = server_up_time
        server.response_time = response_time
        server.network_latency = network_latency
        server.status = status
        server.save()

def jenkins_servers_view(request):
    # Update Jenkins server details in the database
    update_jenkins_server_details()

    # Fetch data from the model
    queryset = jenkins_servers.objects.all()

    # Prepare data for template
    jenkins_server_details = [
        {
            'jenkins_url': server.server_url,
            'server_up_time': server.server_up_time,
            'response_time': server.response_time,
            'network_latency': server.network_latency,
            'status': server.status,
        }
        for server in queryset
    ]

    # Pass data to the template
    return render(
        request,
        "jenkins_servers/jenkins_servers.html",
        context={'jenkins_server_details': jenkins_server_details}
    )
