from django.urls import path
from . import views

urlpatterns = [

    path('artifactories/', views.artifactories_view, name='artifactories')
]