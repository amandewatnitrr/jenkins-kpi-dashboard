from django.shortcuts import render
from django.http import HttpResponse

def homepage(request):

    gitlab_details = {
        'gitlab_url':'https://gitlab-gxp.company.com',
        'Developers':'1000',
        'status':'Failure',
        'Version':'14.10.5-ee',
        'Projects':'600',
    }

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
    artifactories = [
        {
            'id': 1,
            'name': 'BLR',
            'url': 'http://localhost:8081/',
            'status': 'Working'
        },
        {
            'id': 2,
            'name': 'US',
            'url': 'http://localhost:8082/',
            'status': 'Warning'
        },
        {
            'id': 3,
            'name': 'EU',
            'url': 'http://localhost:8083/',
            'status': 'Failure'
        },
    ]

    context = {
        'gitlab_details':gitlab_details,
        'jenkins_server_details':jenkins_server_details,
        'artifactories':artifactories,
    }
    return render(request,"homepage/homepage.html",context)

# Create your views here.
