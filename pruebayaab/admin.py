from django.contrib import admin
from .models import Categoria, Producto


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