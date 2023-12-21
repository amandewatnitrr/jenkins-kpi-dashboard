from django.shortcuts import render
from django.http import HttpResponse

def artifactories(request):
    artifactories = [
        {
            'id':1,
            'name':'BLR',
            'url':'http://localhost:8081/',
            'status':'Working'
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
            'status':'Failure'
        },
    ]
    context = {
        'artifactories':artifactories,
    }
    return render(request,"artifactories/artifactories.html",context)

# Create your views here.
