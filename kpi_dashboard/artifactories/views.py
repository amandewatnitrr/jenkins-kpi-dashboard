from django.shortcuts import render
from .models import Artifactories
import requests

def artifactories_view(request):
    # Fetch data from the model
    artifactories = Artifactories.objects.all()

    # Prepare data for template
    artifactories_data = []

    for art in artifactories:
        # Make a request to check the status
        try:
            response = requests.head(art.url, timeout=5)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            status = 'Working'
        except requests.RequestException as e:
            status = 'Failure'

        # Update the status in the database
        art.status = status
        art.save()

        # Append data to the list
        artifactories_data.append({
            'id': art.id,
            'name': art.name,
            'url': art.url,
            'status': status,
        })

    # Pass data to the template
    context = {
        'artifactories': artifactories_data,
    }
    return render(request, "artifactories/artifactories.html", context)
