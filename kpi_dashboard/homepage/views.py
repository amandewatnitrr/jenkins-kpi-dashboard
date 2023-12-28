# views.py in the homepage app

from django.shortcuts import render
from django.http import HttpResponse

from artifactories.models import Artifactories
from Gitlab.models import Gitlab
from jenkins_servers.models import jenkins_servers

def homepage_view(request):
    # Fetch data from models
    artifactories_data = Artifactories.objects.all()
    gitlab_data = Gitlab.objects.all()
    jenkins_servers_data = jenkins_servers.objects.all()

    # Prepare data for the template
    context = {
        'artifactories': artifactories_data,
        'gitlab_data': gitlab_data,
        'jenkins_server_details': jenkins_servers_data,
    }

    # Pass data to the template
    return render(request, "homepage/homepage.html", context)
