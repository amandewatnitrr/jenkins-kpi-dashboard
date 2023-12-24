from django.shortcuts import render
from .models import Artifactories  # Import the model

def artifactories_view(request):
    # Fetch data from the model
    artifactories = Artifactories.objects.all()

    # Prepare data for template
    artifactories_data = [
        {
            'id': art.id,
            'name': art.name,
            'url': art.url,
            'status': art.status,
        }
        for art in artifactories
    ]

    # Pass data to the template
    context = {
        'artifactories': artifactories_data,
    }
    return render(request, "artifactories/artifactories.html", context)
