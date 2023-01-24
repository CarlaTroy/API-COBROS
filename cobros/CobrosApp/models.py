from django.db import models

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