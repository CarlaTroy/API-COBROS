import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission


class Command(BaseCommand):
    help = 'Creates read only default permission groups for users'

    def handle(self, *args, **options):
        GROUPS = ['group_admins', 'group_secretarys', 'group_students']
        for group in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)
            
        ## ASIGNADMOS A CADA GRUPO PERMISOS A DIFERENTES TABLAS
        MODELS = ['student', 'enrollement', 'course', 'cohorte', 'payment', 'user']
        PERMISSIONS = ['view', ] 
        group_admin, created = Group.objects.get_or_create(name='group_admins')
        for model in MODELS:
            for permission in PERMISSIONS:
                name = 'Can {} {}'.format(permission, model)
                print("Creating {}".format(name))

                try:
                    model_add_perm = Permission.objects.get(name=name)
                    group_admin.permissions.add(model_add_perm)
                except Permission.DoesNotExist:
                    logging.warning("ERROR EN GROUP_ADMIN SI NO EXISTE EL PERMISO")
            
        MODELS_SECRETARY=['payment','student','user','enrollement']
        PERMISSIONS_SECRETARY=['view', ]
        group_secretarys, created = Group.objects.get_or_create(name='group_secretarys')
        for model in MODELS_SECRETARY:
            for permission in PERMISSIONS_SECRETARY:
                name = 'Can {} {}'.format(permission, model)
                print("Creating {}".format(name))

                try:
                    model_add_perm = Permission.objects.get(name=name)
                    group_secretarys.permissions.add(model_add_perm)
                except Permission.DoesNotExist:
                    #logging.warning("Permission not found with name '{}'.".format(name))
                    logging.warning("ERROR EN GROUP_SECRETARY SI NO EXISTE EL PERMISO")
                
        MODELS_STUDENT=['payment','user','enrollement','student']
        PERMISSIONS_STUDEN=['view']
        group_students, created = Group.objects.get_or_create(name='group_students')
        for model in MODELS_STUDENT:
            for permission in PERMISSIONS_STUDEN:
                name = 'Can {} {}'.format(permission, model)
                print("Creating {}".format(name))

                try:
                    model_add_perm = Permission.objects.get(name=name)
                    group_students.permissions.add(model_add_perm)
                except Permission.DoesNotExist:
                    #logging.warning("Permission not found with name '{}'.".format(name))
                    logging.warning("ERROR EN GROUP_STUDENT SI NO EXISTE EL PERMISO")
        
        print("Created default group and permissions.")