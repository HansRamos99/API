from django.db import models
from django.contrib.gis.db import *

# Create your models here.



class Usuario(models.Model):
    PSICOLOGO='PS'
    PACIENTE='PA'

    TIPO_DE_USUARIO=[(PSICOLOGO, 'psicologo'),(PACIENTE, 'paciente')]

    correo=models.EmailField()
    contrasenia=models.CharField(max_length=25)
    tipo_de_usuario=models.CharField(max_length=2, choices=TIPO_DE_USUARIO)


class Psicologo(models.Model):
    NORTE='NO'
    SUR='SU'
    CENTRO='CE'
    SAMBORONDON='SA'
    DAULE='DA'
    SECTOR=[(NORTE,'Norte'),(SUR,'Sur'),(CENTRO,'Centro'),(SAMBORONDON,'Samborondon'),(DAULE,'Daule')]

    nombre= models.CharField(max_length=50)
    categoria=models.CharField(max_length=100)
    descripcion=models.TextField()
    sector=models.CharField(max_length=2, choices=SECTOR)


class Paciente(models.Model):
    nombre=models.CharField(max_length=50)
    descripcion=models.TextField()


class Cita(models.Model):
    inicio_cita=models.DateTimeField()
    fin_cita=models.DateTimeField()
    psicologo=models.ForeignKey("Psicologo",on_delete=models.CASCADE)
    paciente=models.ForeignKey("Paciente", on_delete=models.CASCADE,null=True, blank=True)

class Educacion(models.Model):
    universidad=models.CharField(max_length=50)
    titulo=models.CharField(max_length=50)
    psicologo=models.ForeignKey('Psicologo',on_delete=models.CASCADE)

class Recomendacion(models.Model):
    recomendacion=models.CharField(max_length=150, default='Recomendacion')
    paciente=models.ForeignKey('Paciente',on_delete=models.CASCADE)

class Ubicacion(models.Model):
    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    psicologo=models.ForeignKey('Psicologo',on_delete=models.CASCADE)
