from decimal import Decimal
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
    
class Tipe_Pay(models.Model):
    name=models.CharField(max_length=100,unique=True)
    codigo=models.CharField(max_length=100,unique=True)
    def __str__(self) :
        return self.name
    
class Status_Pay(models.Model):
    name=models.CharField(max_length=100,unique=True)
    codigo=models.CharField(max_length=100,unique=True)
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
    
class Enrollement(models.Model):
    student=models.ForeignKey(Student,on_delete=models.RESTRICT,related_name='studentlist')
    cohorte=models.ForeignKey(Cohorte,on_delete=models.RESTRICT,related_name='cohortelist')
    tipe_pay=models.ForeignKey(Tipe_Pay,on_delete=models.RESTRICT,related_name='tipopagolist')
    cuotas =models.PositiveIntegerField(max_length=10)
    day_limite =models.PositiveIntegerField(max_length=4)
    cash =models.PositiveIntegerField(max_length=10)
    discount = models.PositiveIntegerField(max_length=3)
    updated_on=models.DateTimeField(auto_now=True)
    created_on=models.DateTimeField(auto_now_add=True)
    def __str__(self) :
        return str(self.student.name+" "+self.cohorte.name) 
    
class Payment(models.Model):
    amount=models.DecimalField(max_digits=20, decimal_places=2,default=Decimal(0.00))
    date_pay=models.DateField(max_length=250)
    date_limit=models.DateField(max_length=250)
    status_pay=models.ForeignKey(Status_Pay,on_delete=models.RESTRICT,related_name='statuslist')
    enrollement=models.ForeignKey(Enrollement,on_delete=models.RESTRICT,related_name='enrrollementlist')
    updated_on=models.DateTimeField(auto_now=True)
    created_on=models.DateTimeField(auto_now_add=True)
    def __str__(self) :
        return str(self.amount) 