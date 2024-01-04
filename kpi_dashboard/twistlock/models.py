from django.db import models
import uuid
# Create your models here.
class Twistlock(models.Model):
    url = models.CharField(max_length=200,null=True)
    version = models.CharField(max_length=200,null=True)
    status = models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.url