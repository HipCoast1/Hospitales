from django.test import TestCase # type: ignore
from django.urls import reverse # type: ignore
from django.contrib.auth.models import User # type: ignore
from monitoring.models import Zona, Cliente, Empleado

class AuthAndAnalisisTest(TestCase):
    """Pruebas unitarias y de integración para login, registro, logout y analisis"""

    def setUp(self):
        self.user = User.objects.create_user(username='usuario', password='1234')
        self.admin = User.objects.create_superuser(username='admin', password='1234', email='a@a.com')

    # ---------- LOGIN ----------
    def test_login_correcto(self):
        response = self.client.post(reverse('login'), {'username': 'usuario', 'password': '1234'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main'))

    def test_login_incorrecto(self):
        response = self.client.post(reverse('login'), {'username': 'usuario', 'password': 'wrong'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Usuario o contraseña incorrectos")

    # ---------- LOGOUT ----------
    def test_logout(self):
        self.client.login(username='usuario', password='1234')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

    # ---------- REGISTRO ----------
    def test_registro_exitoso(self):
        data = {
            'username': 'nuevo',
            'email': 'nuevo@test.com',
            'password1': 'abc12345',
            'password2': 'abc12345',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='nuevo').exists())

    def test_registro_contraseñas_distintas(self):
        data = {'username': 'fallido', 'password1': '123', 'password2': '456'}
        response = self.client.post(reverse('register'), data)
        self.assertContains(response, "Las contraseñas no coinciden")

    def test_registro_usuario_duplicado(self):
        data = {'username': 'usuario', 'password1': '1234', 'password2': '1234'}
        response = self.client.post(reverse('register'), data)
        self.assertContains(response, "El nombre de usuario ya existe")

    # ---------- ANÁLISIS ----------
    def test_analisis_view_con_datos(self):
        self.client.login(username='admin', password='1234')

        zona = Zona.objects.create(nombre="Zona 1", tipo=1, identificador="z1")
        Cliente.objects.create(nombre="Juan", apellido1="Perez", documento="1", correo="a@a.com",
                               tipo_documento=1, tipo_enfermedad="Cardiaca",
                               zona_asignada=zona, identificador="c1")
        Empleado.objects.create(nombre="Ana", apellido1="Lopez", cargo="Enfermera",
                                zona_asignada=zona, identificador="e1")

        response = self.client.get(reverse('analisis'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Zonas registradas")
        self.assertContains(response, "Clientes")
        self.assertContains(response, "Empleados")

    def test_analisis_view_sin_login_redirige(self):
        response = self.client.get(reverse('analisis'))
        self.assertRedirects(response, reverse('login'))
