from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import  logout
from django.contrib.auth.models import User
from .forms import Formularioyaab
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import FormularioRegistro
from django.http import HttpResponseRedirect
#CATEGORIA >>>
from .models import Categoria
from .forms import CategoriaForm
#Excel
import pandas as pd
from django.http import HttpResponse
#PDF
from django.template.loader import get_template
from xhtml2pdf import pisa
#PRODUCTO >>>
from .models import Producto
from .forms import ProductoForm
#producto graficas
from django.db.models import Sum, F
import json
from django.db.models import Count
from django.http import JsonResponse
from django.db.models import Q
from django.utils.timezone import make_aware, is_naive
import pytz
from django.views.decorators.http import require_POST


#tareass
from rest_framework import generics
from .models import Tarea
from .serializers import TareaSerializer
from rest_framework.permissions import IsAuthenticated

from django.views.generic import CreateView, DeleteView, TemplateView, UpdateView

from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .forms import TareaForm  #formulario de Tarea:)
from django.urls import reverse_lazy


#TABLERO
from django.views.decorators.csrf import csrf_exempt
#calendario
from. models import Evento
from datetime import datetime



#def vista_formulario(request): #solicito esta respuesta para el usuario
    
    #if request.method == 'POST':
     #   form = Formularioyaab(request.POST)
      #  if form.is_valid():
       #     nombre = form.cleaned_data['nombre']
        #    email = form.cleaned_data['email']
         #   mensaje = form.cleaned_data['mensaje']
          #  telefonico = form.cleaned_data['telefonico']
            #Enviar una respuesta al usuario
        #return render(request, 'pruebayaab/mensaje.html', {'nombre': nombre})

    #else:
     #   form = Formularioyaab()
    #print(form)
    #return render (request, 'pruebayaab/formulario.html', {'form': form})
def vista_prueba(request):
    prueba={'texto':'hola'}
    return render (request, 'pruebayaab/prueba.html', prueba)

def vista_formulario(request):
    if request.method == "POST":
        form = Formularioyaab(request.POST)
        if form.is_valid():
            # Guardar los datos en la base de datos o procesarlos 
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            mensaje = form.cleaned_data['mensaje']
            telefono = form.cleaned_data['telefono']

            # Voy a enviar mensaje
            print(f"Nombre: {nombre}, Email: {email}, Mensaje: {mensaje}, Teléfono: {telefono}")

           # return redirect('pruebayaab_app:formulario')  # Aqui solo va regresar después de enviar el formulario
        return render (request, 'pruebayaab/formulario.html', {'form': form})

    else:
        form = Formularioyaab()

    return render(request, 'pruebayaab/formulario.html', {'form': form})

   # return redirect('pruebayaab_app:formulario')

def landing(request):
    return render(request, 'pruebayaab/landing.html')

#def es_superuser(user):
 #   return user.is_superuser

@login_required
def dashboard(request):
    return render(request, 'pruebayaab/dashboard_template.html')
#@user_passes_test(es_superuser, login_url='/')
#def dashboard(request):
 #   if not request.user.is_superuser:
  #      return redirect('landing')
   # return render(request, 'pruebayaab/dashboard_template.html') #cambie esto del dashboard !!GGGGG


def login_view(request):
    if request.method == "POST":
        login_input = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=login_input, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard") #redirigir al dashboard
        else:
            messages.error(request, "Usuario o contraseña incorrecta.")
    return render(request, "pruebayaab/registration/login.html")



def logout_view(request):
    logout(request)
    return redirect("login") #redirige al login despues del logout

def dashboard_view(request):
    return render(request, 'pruebayaab/dashboard_template.html')

def registrar_usuario(request):
    if request.method == 'POST':
        form = FormularioRegistro(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # Guarda el usuario pero no lo commitea aún
            user.set_password(form.cleaned_data['password']) # Hashea la contraseña
            user.save() # Guarda el usuario definitivamente
            messages.success(request, 'Usuario registrado exitosamente.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
    else:
        form = FormularioRegistro()
    return render(request, 'registro.html', {'form': form})

#def registrar_usuario(request):
 #   if request.method == 'POST':
  #      form = FormularioRegistro(request.POST)  # Formulario con datos del POST
   #     if form.is_valid():
    #        # ... lógica para guardar el usuario ...
     #       return redirect('login')  # Redirige a la página de login
      #  else:
            # El formulario no es válido, se volverá a mostrar con errores.
       #     pass # No es necesario hacer nada aquí explícitamente, Django lo maneja.

    #else:  # Si es una petición GET (primera vez que se carga el formulario)
     #   form = FormularioRegistro()  # Formulario vacío

    #return render(request, 'registro.html', {'form': form})  # 'form' es clave
   

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')  # Redirige a la página de login, o la URL que prefieras.
    return render(request, 'pruebayaab/confirmar_logout.html')

#>>>>>>>>Crear las funciones para listar,agregar,editar y eliminar categorías:<<<<<<<

# Listar Categorías
def listar_categorias(request):
    categorias = Categoria.objects.all()

    nombre = request.GET.get('nombre', '')
    descripcion = request.GET.get('descripcion', '')

    if nombre:
        categorias = categorias.filter(nombre__icontains=nombre)
    if descripcion:
        categorias = categorias.filter(descripcion__icontains=descripcion)


    return render(request, 'pruebayaab/lista.html', {'categorias': categorias})

# Crear una nueva Categoría
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'pruebayaab/form.html', {'form': form})

# Editar una Categoría existente
def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('listar_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'pruebayaab/form.html', {'form': form})

# Eliminar una Categoría
def eliminar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        categoria.delete()
        return redirect('listar_categorias')
    return render(request, 'pruebayaab/confirmar_eliminacion.html', {'categoria': categoria}) #confirmar_eliminacion es para CATEGORIAS

#EXPORTAR CATEGORIAS 

def exportar_categorias_excel(request):
    categorias = Categoria.objects.all().values('nombre', 'descripcion', 'fecha_creacion')
    df = pd.DataFrame(categorias)

    # utilizo 'fecha_creacion' a timezone-naive  para convertir
    df['fecha_creacion'] = pd.to_datetime(df['fecha_creacion']).dt.tz_localize(None)

    #el response para archivo Excel
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="categorias.xlsx"'

    # Escribimos el DataFrame al archivo Excel
    with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Categorías')

    return response


def exportar_categorias_pdf(request):
    categorias = Categoria.objects.all()
    template = get_template('pruebayaab/exportar_categorias_pdf.html')
    html = template.render({'categorias': categorias})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="categorias.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error al generar PDF", status=500)

    return response


#>>>>>>>>VISTA PRODUCTO<<<<<<<<
# Listar productos
def lista_productos(request):
    productos = Producto.objects.all()

    nombre = request.GET.get('nombre', '')
    descripcion = request.GET.get('descripcion', '')
    categoria = request.GET.get('categoria', '')

 #filtros
    if nombre:
        productos = productos.filter(nombre__icontains=nombre)
    if descripcion:
        productos = productos.filter(descripcion__icontains=descripcion)
    if categoria:
        productos = productos.filter(categoria__nombre__icontains=categoria)
    
    return render(request, 'pruebayaab/lista_productos.html', {'productos': productos})
    
    
# Crear producto
def crear_producto(request):
    categorias = Categoria.objects.all() # obtengo categorias
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
      
    return render(request, 'pruebayaab/formulario_producto.html', {'form': form, 'categorias': categorias})

# Editar producto
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    categorias = Categoria.objects.all() # obtengo las categoias
    
    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'pruebayaab/formulario_producto.html', {'form': form, 'categorias': categorias, 'producto': producto })

# Eliminar producto
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == "POST":
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'pruebayaab/eliminar_producto.html', {'producto': producto}) #Este html si es para PRODUCTOS

#Exportar Productos>>>
def exportar_productos_excel(request):
    productos = Producto.objects.all().values(
        'nombre', 'descripcion', 'costo', 'stock', 
        'categoria__nombre', 'fecha_creacion', 
        'fecha_actualizacion', 'disponible'
    )
    
    df = pd.DataFrame(productos)

    # Convertimos fechas a timezone-naive para evitar errores
    df['fecha_creacion'] = pd.to_datetime(df['fecha_creacion']).dt.tz_localize(None)
    df['fecha_actualizacion'] = pd.to_datetime(df['fecha_actualizacion']).dt.tz_localize(None)

    # Configurar response para Excel
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="productos.xlsx"'

    # Escribir DataFrame al response usando ExcelWriter
    with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Productos')

    return response


def exportar_productos_pdf(request):
    productos = Producto.objects.all()
    template = get_template('pruebayaab/exportar_productos_pdf.html')
    html = template.render({'productos': productos})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="productos.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error al generar PDF", status=500)

    return response

# Grafica Productos :) >>>>>
def graficas_productos(request):
    productos_disponibles = Producto.objects.filter(disponible=True).count()
    productos_no_disponibles = Producto.objects.filter(disponible=False).count()
    total_productos = Producto.objects.count()

    valor_total_productos = Producto.objects.aggregate(total=Sum('costo'))['total'] or 0

    return render(request, 'pruebayaab/graficas_productos.html', {
        'productos_disponibles': productos_disponibles,
        'productos_no_disponibles': productos_no_disponibles,
        'total_productos': total_productos,
        'valor_total_productos': valor_total_productos
    })

# Grafica lineal Categorias - stock total :) >>>>>
def categorias_productos_api(request):
    categorias = Categoria.objects.all()
    data = {
        "categorias": [categoria.nombre for categoria in categorias],  
        "totales": [Producto.objects.filter(categoria=categoria).count() for categoria in categorias]
    }
    return JsonResponse(data)


# Vista para listar y crear tareas (solo tareas del usuario logueado)
class TareaList(CreateView):
    model = Tarea
    template_name = "pruebayaab/tareas.html"
    form_class = TareaForm
    success_url = reverse_lazy('pruebayaab_app:tarea_list_create')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Filtramos las tareas según el estado
        tareas_pendientes = Tarea.objects.filter(usuario=self.request.user, estado='pendiente')
        tareas_en_curso = Tarea.objects.filter(usuario=self.request.user, estado='en_curso')
        tareas_completadas = Tarea.objects.filter(usuario=self.request.user, estado='completada')

        context['tareas_pendientes'] = tareas_pendientes
        context['tareas_en_curso'] = tareas_en_curso
        context['tareas_completadas'] = tareas_completadas
        return context


#Tablero>>>
@csrf_exempt
def actualizar_estado_tarea(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        tarea_id = data.get('task_id')
        nuevo_estado = data.get('estado')  # Cambié 'column' por 'estado' para mantener la coherencia
        
        # Verificamos que la tarea exista
        try:
            tarea = Tarea.objects.get(id=tarea_id, usuario=request.user)
            tarea.estado = nuevo_estado  # Actualizamos el estado
            tarea.save()
            return JsonResponse({'status': 'success'})
        except Tarea.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Tarea no encontrada'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=400)

#EVENTOS>>>>
def calendario(request):
    return render(request, 'pruebayaab/calendario.html')
""""
def obtener_eventos(request):
    eventos = Evento.objects.all()
    eventos_json = [
        {
            "title": evento.nombre,
            "start": evento.fecha_evento.strftime('%Y-%m-%dT%H:%M:%S'),
            "description": evento.descripcion
        }
        for evento in eventos
    ]
    return JsonResponse(eventos_json, safe=False)
    """
""""
@csrf_exempt
def crear_evento(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre = data.get('nombre')
            descripcion = data.get('descripcion')
            fecha_evento = datetime.strptime(data.get('fecha'), '%Y-%m-%dT%H:%M')  # Cambiado a 'fecha'

            evento = Evento.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                fecha_evento=fecha_evento
            )
            return JsonResponse({"success": True, "message": "Evento creado", "id": evento.id}, status=201)

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)
"""
@csrf_exempt
def crear_evento(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Datos recibidos:", data)  # 🔍 Ver qué llega realmente

            nombre = data.get('nombre')
            descripcion = data.get('descripcion')
            fecha_str = data.get('fecha')

            if not fecha_str:  # 🚨 Si no hay fecha, manda error
                return JsonResponse({"success": False, "error": "No se recibió la fecha"}, status=400)

            print(f"Nombre: {nombre}, Descripción: {descripcion}, Fecha: {fecha_str}")

            # Convierte la fecha recibida en un objeto datetime naive (sin zona horaria)
            fecha_evento = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')

            # Define la zona horaria (en este caso la de México)
            tz = pytz.timezone('America/Mexico_City')

            # Localiza la fecha en la zona horaria correcta
            fecha_evento = tz.localize(fecha_evento)

            # Crea el evento en la base de datos
            evento = Evento.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                fecha_evento=fecha_evento
            )

            return JsonResponse({"success": True, "message": "Evento creado", "id": evento.id}, status=201)

        except Exception as e:
            print("Error en la creación del evento:", e)
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)

def obtener_eventos(request):
    eventos = Evento.objects.all().values("id", "nombre", "descripcion", "fecha_evento")
    eventos_lista = [
        {
            "id": evento["id"],
            "title": evento["nombre"],  # FullCalendar usa "title"
            "start": evento["fecha_evento"].strftime('%Y-%m-%dT%H:%M:%S'),
            "description": evento["descripcion"]
        }
        for evento in eventos
    ]
    return JsonResponse(eventos_lista, safe=False)