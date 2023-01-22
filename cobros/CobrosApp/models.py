from django.db import models

# Create your models here.
class Course(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=250)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)