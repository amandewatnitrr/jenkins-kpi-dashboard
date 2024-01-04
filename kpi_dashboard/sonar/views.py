from django.shortcuts import render
from .models import SonarQube
import requests
import json

def sonar_view(request):
    sonar_instance = SonarQube.objects.first()  # Assuming there's only one SonarQube instance in the database

    if sonar_instance:
        sonar_url = sonar_instance.url
        sonar_username = sonar_instance.username
        sonar_password = sonar_instance.password

        # Make API request to get server information
        info_url = f"{sonar_url}/api/system/info"
        auth = (sonar_username, sonar_password)

        try:
            response = requests.get(info_url, auth=auth)
            response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
            data = response.json()

            sonar_instance.health = data.get('status', 'Bad')
            sonar_instance.version = data.get('version', 'Unknown')  # Add version field to SonarQube model
            # You can fetch and save other details like edition, etc. here

            sonar_instance.save()

            context = {
                'sonar_instance': sonar_instance,
            }

            return render(request, "sonar/sonar.html", context)

        except requests.exceptions.RequestException as e:
            # Handle exceptions, log the error, or provide default values
            context = {
                'sonar_instance': SonarQube(health='Bad', version='Unknown'),  # Use default values for health and version
                'error_message': f'Failed to fetch SonarQube details. {str(e)}',
            }
            return render(request, "sonar/sonar.html", context)

    # Handle the case where no SonarQube instance is found
    context = {
        'sonar_instance': SonarQube(health='Bad', version='Unknown'),  # Use default values for health and version
        'error_message': 'No SonarQube instance found in the database.',
    }
    return render(request, "sonar/sonar.html", context)
