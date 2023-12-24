from django.db import models
import uuid

# Create your models here.

class jenkins_servers(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    server_url = models.CharField(max_length=200)
    server_up_time = models.CharField(max_length=200,blank=True,null=True)
    response_time = models.CharField(max_length=200,blank=True,null=True)
    network_latency = models.CharField(max_length=200,blank=True,null=True)
    status = models.CharField(max_length=200,blank=True,null=True)
    def __str__(self):
        return self.server_url
