from django.urls import path
from . import views

urlpatterns = [

    path('Gitlab/', views.Gitlab_view, name='Gitlab')
]