from django.urls import path
from CobrosApp.Api.Course.views import CourseAV,CourseDetail
from CobrosApp.Api.Cohorte.views import CohorteAV
from CobrosApp.Api.Cohorte.views import CohorteDetail
urlpatterns = [
    path('courses/',CourseAV.as_view(),name='listado-cursos'),
    path('courses/<int:pk>',CourseDetail.as_view(),name='detalle-cursos'),
    path('cohortes/',CohorteAV.as_view(),name='listado-cohortes'),
    path('cohortes/<int:pk>',CohorteDetail.as_view(),name='detalle-cohortes'),
]
