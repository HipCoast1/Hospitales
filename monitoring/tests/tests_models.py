from django.test import TestCase # type: ignore
from monitoring.models import Zona

class ZonaModelTest(TestCase):
    def test_creacion_zona(self):
        zona = Zona.objects.create(nombre="Pediatría", tipo="1")
        self.assertEqual(zona.nombre, "Pediatría")
        self.assertEqual(Zona.objects.count(), 1)

