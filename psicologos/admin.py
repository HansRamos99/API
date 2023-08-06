from django.contrib import admin
from .models import *

admin.site.register(Usuario)
# Register your models here.
admin.site.register(Psicologo)
admin.site.register(Paciente)
admin.site.register(Cita)
admin.site.register(Educacion)
admin.site.register(Recomendacion)
admin.site.register(Ubicacion)