from django.shortcuts import render
from django.http import HttpResponse

def jenkins_servers(request):

    jenkins_server_details = [
        {
            'jenkins_url':'https://jenkins-gxp.company.com',
            'server_up_time':'99.99%',
            'response_time':'0.5s',
            'network_latency':'0.5s',
            'status':'Working'
        },
        {
            'jenkins_url': 'https://jenkins-gxp.company.com',
            'server_up_time': '99.99%',
            'response_time': '0.5s',
            'network_latency': '0.5s',
            'status': 'Warning'
        },
        {
            'jenkins_url': 'https://jenkins-gxp.company.com',
            'server_up_time': '99.99%',
            'response_time': '0.5s',
            'network_latency': '0.5s',
            'status': 'Failure'
        }
    ]
    return render(request,"jenkins_servers/jenkins_servers.html",context={'jenkins_server_details':jenkins_server_details})

# Create your views here.
