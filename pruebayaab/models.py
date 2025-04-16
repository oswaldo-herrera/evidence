from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#Para categoria
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)  # Corrección aquí
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha automática

    def __str__(self):
        return self.nombre

#Para producto
class Producto(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField()
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)  # Relación con Categoría
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    
#Tareas
class Tarea(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_curso', 'En Curso'),
        ('completada', 'Completada'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_vencimiento = models.DateTimeField(null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo
    
class Evento(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_evento = models.DateTimeField()
    
    def __str__(self):
        return self.nombre
