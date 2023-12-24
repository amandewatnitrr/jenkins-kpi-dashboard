from django.urls import path
from . import views

urlpatterns = [

    path('jenkins_serves/', views.jenkins_servers_view, name='jenkins_servers')
]