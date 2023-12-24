from django.db import models
import uuid

# Create your models here.

class jenkins_servers(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    server_url = models.CharField(max_length=200)
    server_up_time = models.CharField(max_length=200)
    response_time = models.CharField(max_length=200)
    network_latency = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    def __str__(self):
        return self.name
