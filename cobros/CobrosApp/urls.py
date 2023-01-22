from django.urls import path
from CobrosApp.Api.Course.views import CourseAV,CourseDetail
urlpatterns = [
    path('courses/',CourseAV.as_view(),name='listado-cursos'),
    path('courses/<int:pk>',CourseDetail.as_view(),name='detalle-cursos'),
]
