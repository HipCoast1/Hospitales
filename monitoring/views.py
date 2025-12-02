from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.contrib.auth import authenticate, login, logout # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.contrib import messages # type: ignore
from django.contrib.auth.decorators import user_passes_test # type: ignore
from django.db.models import Count # type: ignore
from .models import Zona, Cliente, Empleado
import uuid

# ------------------------------
# LOGIN
# ------------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, "Usuario o contraseña incorrectos")

    return render(request, 'monitoring/login.html')


# ------------------------------
# LOGOUT
# ------------------------------
def logout_view(request):
    logout(request)
    return redirect('login')


# ------------------------------
# REGISTRO
# ------------------------------
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya existe")
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            messages.success(request, "Usuario registrado correctamente.")
            return redirect('login')

    return render(request, 'monitoring/register.html')


# ------------------------------
# MAIN
# ------------------------------
def main_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'monitoring/main.html')


# ------------------------------
# ANÁLISIS (MEJORADO)
# ------------------------------
def analisis_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Totales generales
    total_zonas = Zona.objects.count()
    total_clientes = Cliente.objects.count()
    total_empleados = Empleado.objects.count()

    # ---- CLIENTES POR ZONA ----
    clientes_por_zona = (
        Cliente.objects.values('zona_asignada__nombre')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    clientes_por_zona_dict = {
        c['zona_asignada__nombre'] or 'Sin zona': c['total'] for c in clientes_por_zona
    }

    # ---- CLIENTES POR ENFERMEDAD ----
    clientes_por_enfermedad = (
        Cliente.objects.values('tipo_enfermedad')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    clientes_por_enfermedad_dict = {
        c['tipo_enfermedad'] or 'No especificado': c['total'] for c in clientes_por_enfermedad
    }

    # ---- EMPLEADOS POR ZONA ----
    empleados_por_zona = (
        Empleado.objects.values('zona_asignada__nombre')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    empleados_por_zona_dict = {
        e['zona_asignada__nombre'] or 'Sin zona': e['total'] for e in empleados_por_zona
    }

    # ---- EMPLEADOS POR CARGO ----
    empleados_por_cargo = (
        Empleado.objects.values('cargo')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    empleados_por_cargo_dict = {e['cargo']: e['total'] for e in empleados_por_cargo}

    context = {
        'total_zonas': total_zonas,
        'total_clientes': total_clientes,
        'total_empleados': total_empleados,
        'clientes_por_zona': clientes_por_zona_dict,
        'clientes_por_enfermedad': clientes_por_enfermedad_dict,
        'empleados_por_zona': empleados_por_zona_dict,
        'empleados_por_cargo': empleados_por_cargo_dict,
    }

    return render(request, 'monitoring/analisis.html', context)


# ------------------------------
# PANEL ADMIN
# ------------------------------
@user_passes_test(lambda u: u.is_superuser)
def admin_panel_view(request):
    clientes = Cliente.objects.all()
    zonas = Zona.objects.all()
    empleados = Empleado.objects.all()

    context = {
        'clientes': clientes,
        'zonas': zonas,
        'empleados': empleados,
        'total_clientes': clientes.count(),
        'total_zonas': zonas.count(),
        'total_empleados': empleados.count(),
    }
    return render(request, 'monitoring/admin.html', context)


# ------------------------------
# CRUD CLIENTES
# ------------------------------
@user_passes_test(lambda u: u.is_superuser)
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    cliente.delete()
    messages.success(request, f"Cliente '{cliente.nombre} {cliente.apellido1}' eliminado correctamente.")
    return redirect('admin_panel')


@user_passes_test(lambda u: u.is_superuser)
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    zonas = Zona.objects.all()

    if request.method == 'POST':
        cliente.nombre = request.POST.get('nombre')
        cliente.apellido1 = request.POST.get('apellido1')
        cliente.documento = request.POST.get('documento')
        cliente.correo = request.POST.get('correo')
        tipo_doc = request.POST.get('tipo_documento')
        cliente.tipo_documento = 1 if tipo_doc == 'dni' else 2
        cliente.tipo_enfermedad = request.POST.get('tipo_enfermedad')
        zona_id = request.POST.get('zona_asignada')
        cliente.zona_asignada = Zona.objects.get(id=zona_id) if zona_id else None
        cliente.save()
        messages.success(request, "Cliente actualizado correctamente.")
        return redirect('admin_panel')

    return render(request, 'monitoring/editar_cliente.html', {'cliente': cliente, 'zonas': zonas})


@user_passes_test(lambda u: u.is_superuser)
def agregar_cliente(request):
    zonas = Zona.objects.all()

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        apellido1 = request.POST.get("apellido1")
        documento = request.POST.get("documento")
        correo = request.POST.get("correo")
        tipo_documento = request.POST.get("tipo_documento")
        tipo_enfermedad = request.POST.get("tipo_enfermedad")
        zona_id = request.POST.get("zona_asignada")

        identificador = str(uuid.uuid4())[:8]
        zona = Zona.objects.get(id=zona_id) if zona_id else None

        Cliente.objects.create(
            nombre=nombre,
            apellido1=apellido1,
            documento=documento,
            correo=correo,
            tipo_documento=tipo_documento,
            tipo_enfermedad=tipo_enfermedad,
            zona_asignada=zona,
            identificador=identificador
        )

        messages.success(request, "✅ Cliente agregado correctamente.")
        return redirect("admin_panel")

    return render(request, "monitoring/agregar_cliente.html", {'zonas': zonas})


# ------------------------------
# CRUD ZONAS
# ------------------------------
@user_passes_test(lambda u: u.is_superuser)
def eliminar_zona(request, id):
    zona = get_object_or_404(Zona, id=id)
    zona.delete()
    return redirect('admin_panel')


@user_passes_test(lambda u: u.is_superuser)
def editar_zona(request, id):
    zona = get_object_or_404(Zona, id=id)
    if request.method == 'POST':
        zona.nombre = request.POST.get('nombre')
        zona.tipo = request.POST.get('tipo')
        zona.save()
        return redirect('admin_panel')
    return render(request, 'monitoring/editar_zona.html', {'zona': zona})


@user_passes_test(lambda u: u.is_superuser)
def agregar_zona(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        tipo = request.POST.get('tipo')

        if nombre and tipo:
            Zona.objects.create(nombre=nombre, tipo=tipo)
            messages.success(request, 'Zona agregada correctamente.')
            return redirect('admin_panel')
        else:
            messages.error(request, 'Todos los campos son obligatorios.')

    return render(request, 'monitoring/agregar_zona.html')


# ------------------------------
# CRUD EMPLEADOS
# ------------------------------
@user_passes_test(lambda u: u.is_superuser)
def eliminar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    empleado.delete()
    return redirect('admin_panel')


@user_passes_test(lambda u: u.is_superuser)
def editar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    zonas = Zona.objects.all()

    if request.method == 'POST':
        empleado.nombre = request.POST.get('nombre')
        empleado.apellido1 = request.POST.get('apellido1')
        empleado.cargo = request.POST.get('cargo')
        zona_id = request.POST.get('zona_asignada')
        empleado.zona_asignada = Zona.objects.get(id=zona_id) if zona_id else None
        empleado.save()
        messages.success(request, "Empleado actualizado correctamente.")
        return redirect('admin_panel')

    return render(request, 'monitoring/editar_empleado.html', {'empleado': empleado, 'zonas': zonas})


@user_passes_test(lambda u: u.is_superuser)
def agregar_empleado(request):
    zonas = Zona.objects.all()

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido1 = request.POST.get('apellido1')
        cargo = request.POST.get('cargo')
        zona_id = request.POST.get('zona_asignada')

        if nombre and apellido1 and cargo:
            identificador_unico = str(uuid.uuid4())[:8]
            zona = Zona.objects.get(id=zona_id) if zona_id else None

            Empleado.objects.create(
                nombre=nombre,
                apellido1=apellido1,
                cargo=cargo,
                identificador=identificador_unico,
                zona_asignada=zona
            )

            messages.success(request, 'Empleado agregado correctamente.')
            return redirect('admin_panel')
        else:
            messages.error(request, 'Todos los campos son obligatorios.')

    return render(request, 'monitoring/agregar_empleado.html', {'zonas': zonas})
