from django.test import TestCase # type: ignore
from django.urls import reverse # type: ignore
from django.contrib.auth.models import User # type: ignore
from monitoring.models import Zona, Cliente, Empleado

class CRUDIntegrationTest(TestCase):
    """Pruebas de integración para vistas CRUD de zonas, clientes y empleados"""

    def setUp(self):
        # Crear superusuario para acceder al panel
        self.admin = User.objects.create_superuser(username="admin", password="1234", email="admin@test.com")
        self.client.login(username="admin", password="1234")

        # Crear zona base para relacionar clientes y empleados
        self.zona = Zona.objects.create(nombre="Zona Test", tipo=1)

    # ---------- ZONAS ----------
    def test_agregar_zona(self):
        response = self.client.post(reverse("agregar_zona"), {"nombre": "Nueva Zona", "tipo": "1"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Zona.objects.filter(nombre="Nueva Zona").exists())

    def test_editar_zona(self):
        response = self.client.post(reverse("editar_zona", args=[self.zona.id]), {"nombre": "Zona Editada", "tipo": "2"})
        self.zona.refresh_from_db()
        self.assertEqual(self.zona.nombre, "Zona Editada")

    def test_eliminar_zona(self):
        response = self.client.get(reverse("eliminar_zona", args=[self.zona.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Zona.objects.filter(id=self.zona.id).exists())

    # ---------- CLIENTES ----------
    def test_agregar_cliente(self):
        data = {
            "nombre": "Juan",
            "apellido1": "Pérez",
            "documento": "12345",
            "correo": "juan@test.com",
            "tipo_documento": 1,
            "tipo_enfermedad": "Cardiaca",
            "zona_asignada": self.zona.id
        }
        response = self.client.post(reverse("agregar_cliente"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Cliente.objects.filter(nombre="Juan").exists())

    def test_editar_cliente(self):
        cliente = Cliente.objects.create(
            nombre="Maria", apellido1="Lopez", documento="999", correo="maria@test.com",
            tipo_documento=1, tipo_enfermedad="Respiratoria", zona_asignada=self.zona, identificador="abc123"
        )
        response = self.client.post(reverse("editar_cliente", args=[cliente.id]), {
            "nombre": "Maria Editada",
            "apellido1": "Lopez",
            "documento": "999",
            "correo": "maria@test.com",
            "tipo_documento": "dni",
            "tipo_enfermedad": "Neurológica",
            "zona_asignada": self.zona.id
        })
        cliente.refresh_from_db()
        self.assertEqual(cliente.nombre, "Maria Editada")

    def test_eliminar_cliente(self):
        cliente = Cliente.objects.create(
            nombre="Carlos", apellido1="Ramírez", documento="333", correo="carlos@test.com",
            tipo_documento=1, tipo_enfermedad="Visual", zona_asignada=self.zona, identificador="def456"
        )
        response = self.client.get(reverse("eliminar_cliente", args=[cliente.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Cliente.objects.filter(id=cliente.id).exists())

    # ---------- EMPLEADOS ----------
    def test_agregar_empleado(self):
        data = {
            "nombre": "Pedro",
            "apellido1": "Soto",
            "cargo": "Enfermero",
            "zona_asignada": self.zona.id
        }
        response = self.client.post(reverse("agregar_empleado"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Empleado.objects.filter(nombre="Pedro").exists())

    def test_editar_empleado(self):
        empleado = Empleado.objects.create(
            nombre="Laura", apellido1="Torres", cargo="Doctora",
            zona_asignada=self.zona, identificador="ghi789"
        )
        response = self.client.post(reverse("editar_empleado", args=[empleado.id]), {
            "nombre": "Laura Editada",
            "apellido1": "Torres",
            "cargo": "Especialista",
            "zona_asignada": self.zona.id
        })
        empleado.refresh_from_db()
        self.assertEqual(empleado.nombre, "Laura Editada")

    def test_eliminar_empleado(self):
        empleado = Empleado.objects.create(
            nombre="Diego", apellido1="Vera", cargo="Paramédico",
            zona_asignada=self.zona, identificador="xyz123"
        )
        response = self.client.get(reverse("eliminar_empleado", args=[empleado.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Empleado.objects.filter(id=empleado.id).exists())
