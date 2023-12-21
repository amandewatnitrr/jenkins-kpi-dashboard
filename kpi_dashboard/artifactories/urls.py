from django.urls import path
from . import views

urlpatterns = [

    path('artifactories/', views.artifactories, name='artifactories')
]