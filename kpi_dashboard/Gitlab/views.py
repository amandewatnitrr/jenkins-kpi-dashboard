from django.shortcuts import render
from django.http import HttpResponse

def Gitlab(request):

    context = {
        'gitlab_url':'https://gitlab-gxp.company.com',
        'Developers':'1000',
        'status':'Failure',
        'Version':'14.10.5-ee',
        'Projects':'600',
    }
    return render(request,"Gitlab/Gitlab.html",context)

# Create your views here.
