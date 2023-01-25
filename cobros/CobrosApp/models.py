from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Course(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=250)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    def __str__(self) :
        return self.name
    
class Cohorte(models.Model):
    name=models.CharField(max_length=100)
    date_init=models.DateField(max_length=250)
    date_end=models.DateField(max_length=250)
    cost_effective =models.DecimalField(max_digits=19, decimal_places=2)
    cost_credit =models.DecimalField(max_digits=19, decimal_places=2)
    course = models.ForeignKey(Course,on_delete=models.RESTRICT,related_name='courselist')
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    def __str__(self) :
        return self.name
    
class Student(models.Model):
    name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    identification=models.CharField(max_length=11)
    cell_phone =models.CharField(max_length=15)
    address =models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.RESTRICT,related_name='userlist')
    updated_on=models.DateTimeField(auto_now=True)
    created_on=models.DateTimeField(auto_now_add=True)
    def __str__(self) :
        return self.name 