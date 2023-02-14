from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from UserApp.api.auth_web.views import  listar_grupos_view, listar_usuarios_view, login_view, registration_view,logout_view, usuario_id_view
urlpatterns = [
    #path('login/',obtain_auth_token,name='login'),
    path('login/',login_view,name='login'),
    path('register/',registration_view,name='registro'),
    path('logout/',logout_view,name='logout'),
    path('users/',listar_usuarios_view,name='usuarios'),
    path('grupos/',listar_grupos_view,name='grupos'),
    path('users/<int:pk>',usuario_id_view,name='usuario-id'), 
    #path('users/<int:pk>',usuarios_update_id_view,name='actualizar-usuario-id'), 
]
