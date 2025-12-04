from django.test import TestCase # type: ignore
from django.urls import reverse # type: ignore
from django.contrib.auth.models import User # type: ignore
from monitoring.models import Zona, Cliente, Empleado

class MainViewSystemTest(TestCase):
    """Pruebas de sistema para verificar la vista principal (main)."""

    def setUp(self):
        # Crear usuario normal y admin
        self.user = User.objects.create_user(username='user', password='1234')
        self.admin = User.objects.create_superuser(username='admin', password='admin123')

        # Crear algunos datos de ejemplo
        self.zona = Zona.objects.create(nombre="Urgencias", tipo=1)
        self.cliente = Cliente.objects.create(
            nombre="Juan", apellido1="Pérez", documento="12345678",
            tipo_documento=1, tipo_enfermedad="Cardíaca", zona_asignada=self.zona
        )
        self.empleado = Empleado.objects.create(
            nombre="Carlos", apellido1="Gómez", cargo="Doctor", zona_asignada=self.zona
        )

    def test_main_context_data(self):
        """Verifica que los totales se envían correctamente al contexto."""
        self.client.login(username='user', password='1234')
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bienvenido")
        self.assertIn('total_zonas', response.context)
        self.assertIn('total_clientes', response.context)
        self.assertIn('total_empleados', response.context)
        self.assertEqual(response.context['total_zonas'], 1)
        self.assertEqual(response.context['total_clientes'], 1)
        self.assertEqual(response.context['total_empleados'], 1)

    def test_main_view_user_normal(self):
        """Un usuario normal debe ver 'Quiénes somos' y no el botón Admin."""
        self.client.login(username='user', password='1234')
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Quiénes somos")
        self.assertNotContains(response, "Panel Admin")

    def test_main_view_admin(self):
        """Un superusuario debe ver el Panel Admin (puede también ver Quiénes somos)."""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Panel Admin")