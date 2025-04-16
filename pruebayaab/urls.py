from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 
#from .views import user_login, user_register


app_name='pruebayaab_app'

urlpatterns = [
    
    path('', views.landing, name='landing'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('formulario/', views.vista_formulario, name='formulario'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('prueba/', views.vista_prueba, name='prueba'),
    #path('dashboard/', views.dashboard_view, name='dashboard'), #SEGUN PARA EL TEMPLATE
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registrar_usuario, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout_view'),

    #CATEGORIA
    path('categorias/', views.listar_categorias, name='listar_categorias'),
    path('categorias/nueva/', views.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:id>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:id>/', views.eliminar_categoria, name='eliminar_categoria'),
    #Exportar EXCEL y PDF
    path('categorias/exportar-excel/', views.exportar_categorias_excel, name='exportar_categorias_excel'),
    path('categorias/exportar-pdf/', views.exportar_categorias_pdf, name='exportar_categorias_pdf'),

    #PRODUCTO
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/nuevo/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    #Exportar EXCEL y PDF
    path('productos/exportar-excel/', views.exportar_productos_excel, name='exportar_productos_excel'),
    path('productos/exportar-pdf/', views.exportar_productos_pdf, name='exportar_productos_pdf'),
    #Grafica productos
     path('graficas/', views.graficas_productos, name='graficas_productos'),
     path('api/categorias-productos-api/', views.categorias_productos_api, name='categorias_productos_api'),

    # Ruta para listar y crear tareas (tareas del usuario logueado)
    path('tareas/', views.TareaList.as_view(), name='tarea_list_create'),
    #tablero
    path('tareas/actualizar/', views.actualizar_estado_tarea, name='actualizar_estado_tarea'),
    #calendario   
    path('calendario/', views.calendario, name='calendario'),
    path('crear-evento/', views.crear_evento, name='crear_evento'),
    path('eventos/', views.obtener_eventos, name='obtener_eventos'),
   
]