from django.urls import path
from CobrosApp.Api.Course.views import CourseAV,CourseDetail
from CobrosApp.Api.Cohorte.views import CohorteAV
from CobrosApp.Api.Cohorte.views import CohorteDetail
from CobrosApp.Api.Enrollement.views import EnrollementAV, EnrollementDetail
from CobrosApp.Api.Payment.views import PaymentAV, getAllByPaymentsEnrrollementId
from CobrosApp.Api.Student.views import StudentAV
from CobrosApp.Api.Student.views import StudentDetail
from CobrosApp.Api.Tipe_pay.views import TypePayseAV
urlpatterns = [
    path('courses/',CourseAV.as_view(),name='listado-cursos'),
    path('courses/<int:pk>',CourseDetail.as_view(),name='detalle-cursos'),
    
    path('cohortes/',CohorteAV.as_view(),name='listado-cohortes'),
    path('cohortes/<int:pk>',CohorteDetail.as_view(),name='listado-cohortes'),
    
    path('students/',StudentAV.as_view(),name='listado-students'),
    path('students/<int:pk>',StudentDetail.as_view(),name='detalle-students'),
    
    path('enrollements/',EnrollementAV.as_view(),name='listado-matriculas'),
    path('enrollements/<int:pk>',EnrollementDetail.as_view(),name='detalle-matricula'),
    
    path('payments/',PaymentAV.as_view(),name='listado-pagos'),
    path('payments/enrollement/<int:pk>',getAllByPaymentsEnrrollementId,name='obtener-todos-pagos-estudainte'),
    path('payments/<int:pk>',EnrollementDetail.as_view(),name='detalle-matricula'),
    
    path('type-pays/',TypePayseAV.as_view(),name='listado-tipo-pagos'),
    
    path('status-pays/',TypePayseAV.as_view(),name='listado-estados-pagos'),
]
