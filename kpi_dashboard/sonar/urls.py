from django.urls import path
from . import views

urlpatterns = [

    path('sonarqube/', views.sonar_view, name='sonarqube')
]