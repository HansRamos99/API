from django.shortcuts import render
from django.views import View
from .models import *
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.response import Response
from datetime import datetime

import os
from django.core.cache import cache
import time
import redis
redis_instance = redis.StrictRedis(host='127.0.0.1', port=6379, db=1)

import environ

env = environ.Env()
environ.Env.read_env()

USAR_REDIS= env("USAR_REDIS") == "true" or env("USAR_REDIS") == "True" 


# Create your views here.

class UsuariosView(View):
    def get (self, request):
        clave = 'usuarios'

        start_time = time.time()
        
        if(redis_instance.exists(clave)):
            print("se mando por redis")
            datos = redis_instance.get(clave)
            datos = json.loads(datos.decode('utf-8'))

            end_time = time.time ()
            duration = end_time - start_time
            print ('\n Total time: {:.3f} ms'.format(duration * 1000.0))

            return JsonResponse(datos)
         
        usuarios=list(Usuario.objects.values())

        if len(usuarios)>0:
            datos={'mensaje': 'exito', 'usuarios': usuarios}
            
        else:
            datos={'mensaje': 'Usuarios no encontrados'}

        print("se mando por sql")

        end_time = time.time ()
        duration = end_time - start_time
        print ('\n Total time: {:.3f} ms'.format(duration * 1000.0))

        return JsonResponse(datos)


class PsicologosView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request,id=0):
        if(id>0):
            psicologos=list(Psicologo.objects.filter(id=id).values())
            print(psicologos)
            if (len(psicologos)>0):
                psicologo=psicologos[0]
                datos={'mensaje': 'exito', 'psicologo': psicologo}
            else:
                datos={'mensaje': 'psicologo no encontrado'}
            return JsonResponse(datos)

        else:
            psicologos=list(Psicologo.objects.values())
            if len(psicologos)>0:
                datos={'mensaje': 'exito', 'psicologos': psicologos}
            else:
                datos={'mensaje': 'psicologos no encontrados'}
            return JsonResponse(datos)

    def post(self, request):
        jd=json.loads(request.body)
        Psicologo.objects.create(nombre=jd['nombre'], categoria=jd['categoria'], descripcion=jd['descripcion'], sector=jd['sector'])
        datos={'mensaje':'Exito'}
        return JsonResponse(datos)

    def put(self, request, id):
        jd=json.loads(request.body)
        otro=json.loads(jd)
        print(type(otro))
        print(otro)
        psicologos=list(Psicologo.objects.filter(id=id).values())
        print("luego de buscardd")

        if (len(psicologos)>0):
            psic=Psicologo.objects.get(id=id)
            psic.nombre=otro['nombre']
            psic.categoria=otro['categoria']
            psic.descripcion=otro['descripcion']
            psic.sector=otro['sector']
            psic.save()
            datos={'mensaje':'exito'}
        else:
            datos={'mensaje': 'cita no encontrada'}
        return JsonResponse(datos)

    def delete(self, request, id):
        citas=list(Psicologo.objects.filter(id=id).values())
        if (len(citas)>0):
            Psicologo.objects.filter(id=id).delete()
            datos={'mensaje': 'exito'}

        else:
            datos={'mensaje': 'No se pudo eliminar'}
        return JsonResponse(datos)

class PacientesView(View):

    def get(self, request,id=0):

        if(id>0):
            pacientes=list(Paciente.objects.filter(id=id).values())
       
            if (len(pacientes)>0):
                paciente=pacientes[0]
                datos={'mensaje': 'exito', 'paciente': paciente}
            else:
                datos={'mensaje': 'paciente no encontrado'}
            return JsonResponse(datos)
        else:
            pacientes=list(Paciente.objects.values())
            if len(pacientes)>0:
                datos={'mensaje': 'exito', 'psicologos': pacientes}
            else:
                datos={'mensaje': 'pacientes no encontrados'}
            return JsonResponse(datos)


def actualizar_citas():
    citas=list(Cita.objects.values())
    for cita in citas:
                cita["inicio_cita"] = cita["inicio_cita"].strftime('%Y-%m-%dT%H:%M:%SZ')
                cita["fin_cita"] = cita["fin_cita"].strftime('%Y-%m-%dT%H:%M:%SZ')

    datos={'mensaje': 'exito', 'cita': citas}
    redis_instance.set("citas", json.dumps(datos))


class CitasView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if(id>0):
            citas=list(Cita.objects.filter(id=id).values())
        
            if (len(citas)>0):
                cita=citas[0]
                datos={'mensaje': 'exito', 'cita': cita}
            else:
                datos={'mensaje': 'cita no encontrada'}
            return JsonResponse(datos)
        
        else:
            print("variable de entorno USAR_REDIS ---> "+str(USAR_REDIS))

            if(redis_instance.exists('citas') and USAR_REDIS):
                print("usando redis")
                datos = redis_instance.get('citas')
                datos = json.loads(datos.decode('utf-8'))

                return JsonResponse(datos)

            citas=list(Cita.objects.values())
        
            if len(citas)>0:
                datos={'mensaje': 'exito', 'citas': citas}
            else:
                datos={'mensaje': 'citas no encontrados'}
            return JsonResponse(datos)
 
    def post(self, request):

        jd=json.loads(request.body)
        
        psic=Psicologo.objects.filter(id=jd['psicologo_id']).first()
        pac=Paciente.objects.filter(id=jd['paciente_id']).first()
        Cita.objects.create(inicio_cita=datetime.strptime(jd['inicio_cita'], '%Y-%m-%dT%H:%M:%SZ'), fin_cita=datetime.strptime(jd['fin_cita'],'%Y-%m-%dT%H:%M:%SZ'),psicologo=psic, paciente=pac)
        datos={'mensaje':'Exito'}
        actualizar_citas()
       
        return JsonResponse(datos)     
     
    #Para el put se necesitan los valores inicio_cita, fin_cita, y el id de un paciente 
    def put(self, request, id):
        jd=json.loads(request.body)
        citas=list(Cita.objects.filter(id=id).values())
        if (len(citas)>0):
            cita=Cita.objects.get(id=id)
            pac=Paciente.objects.filter(id=jd['paciente_id']).first()
            cita.paciente=pac
            cita.save()
            datos={'mensaje':'exito'}
        else:
            datos={'mensaje': 'cita no encontrada'}

        actualizar_citas()
        return JsonResponse(datos)

    def delete(self, request, id):
        citas=list(Cita.objects.filter(id=id).values())
        if (len(citas)>0):
            Cita.objects.filter(id=id).delete()
            datos={'mensaje': 'exito'}

        else:
            datos={'mensaje': 'No se pudo eliminar'}

        actualizar_citas()
        return JsonResponse(datos)

class RecomendacionesView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if(id>0):
            citas=list(Recomendacion.objects.filter(id=id).values())
        
            if (len(citas)>0):
                cita=citas[0]
                datos={'mensaje': 'exito', 'cita': cita}
            else:
                datos={'mensaje': 'Recomendacion no encontrada'}
            return JsonResponse(datos)


        citas=list(Recomendacion.objects.values())
        if len(citas)>0:
            datos={'mensaje': 'exito', 'recomendaciones': citas}
        else:
            datos={'mensaje': 'Recomendaciones no encontrados'}
        return JsonResponse(datos)

    def post(self, request):

        jd=json.loads(request.body)
        pac=Paciente.objects.filter(id=jd['paciente_id']).first()
        recomendacion=jd['recomendacion']
        Recomendacion.objects.create(recomendacion=recomendacion, paciente=pac)
        datos={'mensaje':'Exito'}
        return JsonResponse(datos)  

    def put(self, request, id):
        jd=json.loads(request.body)
        citas=list(Recomendacion.objects.filter(id=id).values())
        if (len(citas)>0):
            cita=Recomendacion.objects.get(id=id)
            cita.recomendacion=jd['recomendacion']
            cita.save()
            datos={'mensaje':'exito'}
        else:
            datos={'mensaje': 'cita no encontrada'}
        return JsonResponse(datos)

    def delete(self, request, id=0):
        print(id)
        citas=list(Recomendacion.objects.filter(id=id).values())
        if (len(citas)>0):
            Recomendacion.objects.filter(id=id).delete()
            datos={'mensaje': 'exito'}
        else:
            datos={'mensaje': 'No se pudo eliminar'}
        return JsonResponse(datos)

class UbicacionesView(View):

    def get(self, request):
        citas=list(Ubicacion.objects.values())
        if len(citas)>0:
            datos={'mensaje': 'exito', 'ubicaciones': citas}
        else:
            datos={'mensaje': 'Ubicaciones no encontrados'}
        return JsonResponse(datos)

class EducacionesView(View):
    def get(self, request,id=0):
        if(id==0):
            citas=list(Educacion.objects.values())
            if len(citas)>0:
                datos={'mensaje': 'exito', 'titulos': citas}
            else:
                datos={'mensaje': 'No encontramos titulos'}
            return JsonResponse(datos)
        else:
        
            educaciones=list(Educacion.objects.filter(psicologo_id=id).values())
            if(len(educaciones)>0):
                datos={'mensaje': 'exito', 'titulos': educaciones}
            else:
                datos={'mensaje': 'No encontramos titulos'}
            return JsonResponse(datos)


