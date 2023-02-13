
from django.contrib import admin

from CobrosApp.models import Course,Cohorte,Student,Enrollement,Status_Pay,Tipe_Pay,Payment
from django.contrib.auth.models import Permission
# Register your models here.
# Register your models here.
#registrar el modelo en la aplicacion 
# Register your models here.
admin.site.register(Course)
admin.site.register(Cohorte)
admin.site.register(Student)
admin.site.register(Enrollement)
admin.site.register(Status_Pay)
admin.site.register(Tipe_Pay)
admin.site.register(Payment)
admin.site.register(Permission)
#admin.site.register(Profile)