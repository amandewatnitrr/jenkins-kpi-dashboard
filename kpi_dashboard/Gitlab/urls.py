from django.urls import path
from . import views

urlpatterns = [

    path('Gitlab/', views.Gitlab, name='Gitlab')
]