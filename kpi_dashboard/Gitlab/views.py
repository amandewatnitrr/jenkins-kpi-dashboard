from django.shortcuts import render
from .models import Gitlab
import requests

def get_gitlab_version(url, private_token):
    try:
        response = requests.get(
            f"{url.rstrip('/')}/api/v4/version",
            headers={'Private-Token': private_token},
            timeout=10
        )
        response.raise_for_status()
        gitlab_info = response.json()
    except requests.RequestException as e:
        print(f"Error retrieving GitLab version: {e}")
        return 'N/A', 'Not Working'

    version = gitlab_info.get('version', 'N/A')
    return version, 'Working'

def Gitlab_view(request):
    # Fetch data from the model
    gitlab_instance = Gitlab.objects.first()  # Assuming you want the first GitLab instance

    # Replace these values with your GitLab server URL and Private Access Token
    gitlab_url = gitlab_instance.url
    private_token = 'your_private_access_token'

    # Get GitLab version and status
    version, status = get_gitlab_version(gitlab_url, private_token)

    # Update GitLab model in the database
    gitlab_instance.version = version
    gitlab_instance.status = status
    gitlab_instance.save()

    # Prepare data for template
    context = {
        'gitlab_url': gitlab_url,
        'Developers': '1000',  # You can update this based on your actual data
        'status': status,
        'Version': version,
        'Projects': '600',  # You can update this based on your actual data
    }

    # Pass data to the template
    return render(request, "Gitlab/Gitlab.html", context)
