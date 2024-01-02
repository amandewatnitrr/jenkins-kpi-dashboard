from django.db import models

class SonarQube(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    username = models.CharField(max_length=255,blank=True)
    password = models.CharField(max_length=255,blank=True)# Added field for total number of projects
    health = models.CharField(max_length=255,blank=True) # Added field for health
    version = models.CharField(max_length=255,blank=True) # Added field for version

    def __str__(self):
        return self.name
