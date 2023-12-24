from django.db import models
import uuid
# Create your models here.
class Gitlab(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200,null=True)
    url = models.CharField(max_length=200,null=True)
    version = models.CharField(max_length=200,null=True)
    status = models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.name