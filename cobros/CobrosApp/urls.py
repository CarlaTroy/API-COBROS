from django.urls import path
from CobrosApp.Api.Course.views import CourseAV
urlpatterns = [
    path('courses/',CourseAV.as_view(),name='listado-cursos'),
]
