from django.shortcuts import render, redirect
from django.contrib.auth import  logout
from django.contrib.auth.models import User
from .forms import Formularioyaab
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import FormularioRegistro


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
    return render(request, "pruebayaab/login.html")



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
   