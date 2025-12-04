from django.test import TestCase # type: ignore
from django.urls import reverse # type: ignore
from django.contrib.auth.models import User # type: ignore

class MainViewIntegrationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='1234')

    def test_acceso_main_autenticado(self):
        self.client.login(username='admin', password='1234')
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bienvenido")
