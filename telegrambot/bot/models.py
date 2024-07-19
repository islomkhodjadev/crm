from django.db import models

# Create your models here.
class Bot(models.Model):
    token = models.CharField(max_length=300)
    instructions = models.TextField()
    api = models.CharField(max_length=300)
    

