from django.shortcuts import render
from .models import Gitlab
import requests

def get_gitlab_server_details(url, username, password):
    # Disable SSL certificate verification (not recommended for production)
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

    # Make a request to the GitLab API to fetch server details
    try:
        response = requests.get(
            f"{url.rstrip('/')}/api/v4/version",
            auth=(username, password),
            timeout=10,
            verify=False  # Disable SSL verification
        )
        response.raise_for_status()
        gitlab_info = response.json()
    except requests.RequestException as e:
        # Handle the exception (e.g., log the error)
        print(f"Error retrieving GitLab server details: {e}")
        return 'N/A', 'Not Working'

    # Extract relevant information
    version = gitlab_info.get('version', 'N/A')
    status = 'Working' if response.status_code == 200 else 'Not Working'

    return version, status

def Gitlab_view(request):
    # Fetch data from the model
    gitlab_instance = Gitlab.objects.first()  # Assuming you want the first GitLab instance

    # Get GitLab server details from the API
    version, status = get_gitlab_server_details(gitlab_instance.url, 'your_gitlab_username', 'your_gitlab_password')

    # Prepare data for template
    context = {
        'gitlab_url': gitlab_instance.url,
        'Developers': '1000',  # You can update this based on your actual data
        'status': status,
        'Version': version,
        'Projects': '600',  # You can update this based on your actual data
    }

    # Pass data to the template
    return render(request, "Gitlab/Gitlab.html", context)
