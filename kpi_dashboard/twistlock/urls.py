from django.urls import path
from . import views

urlpatterns = [
    path('twistlock/', views.twistlock_view, name='twistlock')
]