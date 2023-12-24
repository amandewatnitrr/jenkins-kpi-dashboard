from django.shortcuts import render
from .models import jenkins_servers  # Import the model

def jenkins_servers_view(request):
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
