from django.urls import path
from .views import *

urlpatterns=[
    path('usuarios/', UsuariosView.as_view(), name='nombre'),
    path('psicologos/', PsicologosView.as_view(), name='nombre'),
    path('psicologos/<int:id>', PsicologosView.as_view(), name='psicologos_process'),
    path('citas/', CitasView.as_view(), name='nombre'),
    path('citas/<int:id>', CitasView.as_view(), name='nombre'),
    path('pacientes/', PacientesView.as_view(), name='nombre'),
    path('pacientes/<int:id>', PacientesView.as_view(), name='nombre'),
    path('ubicaciones/', UbicacionesView.as_view(), name='nombre'),
    path('recomendaciones/', RecomendacionesView.as_view(), name='nombre'),
    path('recomendaciones/<int:id>', RecomendacionesView.as_view(), name='nombre'),
    path('educacion/', EducacionesView.as_view(), name='nombre'),
    path('educacion/<int:id>', EducacionesView.as_view(), name='nombre')

]