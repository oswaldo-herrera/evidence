from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 
#from .views import user_login, user_register

app_name:'pruebayaab_app'

urlpatterns = [
    
    path('', views.landing, name='landing'),
    path('login/', auth_views.LoginView.as_view(template_name='pruebayaab/login.html'), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('formulario/', views.vista_formulario, name='formulario'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('prueba/', views.vista_prueba, name='prueba'),
    #path('dashboard/', views.dashboard_view, name='dashboard'), #SEGUN PARA EL TEMPLATE
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registrar_usuario, name='registro'),
    path('login/', views.login_view, name='login'),
]