from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('main/', views.main_view, name='main'),
    path('analisis/', views.analisis_view, name='analisis'),
    path('logout/', views.logout_view, name='logout'),

    # --- PANEL ADMIN PERSONALIZADO ---
    path('panel/', views.admin_panel_view, name='admin_panel'),

    # --- CLIENTES ---
    path('panel/clientes/editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('panel/clientes/eliminar/<int:id>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('panel/clientes/agregar/', views.agregar_cliente, name='agregar_cliente'),

    # --- ZONAS ---
    path('panel/zonas/editar/<int:id>/', views.editar_zona, name='editar_zona'),
    path('panel/zonas/eliminar/<int:id>/', views.eliminar_zona, name='eliminar_zona'),
    path('panel/zonas/agregar/', views.agregar_zona, name='agregar_zona'),

    # --- EMPLEADOS ---
    path('panel/empleados/editar/<int:id>/', views.editar_empleado, name='editar_empleado'),
    path('panel/empleados/eliminar/<int:id>/', views.eliminar_empleado, name='eliminar_empleado'),
    path('panel/empleados/agregar/', views.agregar_empleado, name='agregar_empleado'),
]
