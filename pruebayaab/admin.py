from django.contrib import admin
from .models import Categoria, Producto, Tarea, Evento


# Register your models here.
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display =('nombre', 'descripcion', 'fecha_creacion')
    search_fields = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'costo', 'stock', 'categoria', 'fecha_creacion', 'fecha_actualizacion', 'disponible')
    search_fields = ('nombre', 'categoria__nombre')  # Permite buscar por nombre y categoría
    list_filter = ('categoria', 'disponible')  # Agrega filtros en la vista de admin

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'estado', 'fecha_vencimiento', 'usuario')  # Campos visibles en la lista
    search_fields = ('titulo', 'usuario__username')  # Búsqueda por título y usuario
    list_filter = ('estado', 'fecha_vencimiento')  # Filtros para facilitar la búsqueda

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'fecha_evento')  # Campos visibles en la lista
    search_fields = ('nombre', 'descripcion')  # Permite buscar por nombre y descripción
    list_filter = ('fecha_evento',)  # Filtro por fecha de evento