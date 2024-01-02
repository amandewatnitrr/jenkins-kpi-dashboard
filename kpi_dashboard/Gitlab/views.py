# views.py
from django.shortcuts import render
from .models import Gitlab
from celery import shared_task
import requests

@shared_task
def update_gitlab_data():
    gitlab_instance = Gitlab.objects.first()
    gitlab_url = gitlab_instance.url
    private_token = 'your_private_access_token'
    version, status = get_gitlab_version(gitlab_url, private_token)
    gitlab_instance.version = version
    gitlab_instance.status = status
    gitlab_instance.save()

@shared_task
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
    # Call the Celery task to update GitLab data asynchronously
    update_gitlab_data.delay()

    # Fetch data from the model for displaying in the template
    gitlab_instance = Gitlab.objects.first()
    gitlab_url = gitlab_instance.url
    version = gitlab_instance.version
    status = gitlab_instance.status

    context = {
        'gitlab_url': gitlab_url,
        'Developers': '1000',
        'status': status,
        'Version': version,
        'Projects': '600',
    }

    return render(request, "Gitlab/Gitlab.html", context)
