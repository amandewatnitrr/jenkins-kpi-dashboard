from django.shortcuts import render
from .models import Gitlab  # Import the model

def Gitlab_view(request):
    # Fetch data from the model
    gitlab_instance = Gitlab.objects.first()  # Assuming you want the first Gitlab instance

    # Prepare data for template
    context = {
        'gitlab_url': gitlab_instance.url,
        'Developers': '1000',
        'status': gitlab_instance.status,
        'Version': gitlab_instance.version,
        'Projects': '600',
    }

    # Pass data to the template
    return render(request, "Gitlab/Gitlab.html", context)
