from django.db import models

# ────────────────────────────────
# 🔹 MODELO: ZONA
# ────────────────────────────────
class Zona(models.Model):
    TIPOS_ZONA = [
        (1, 'Edificio'),
        (2, 'Planta'),
        (3, 'Pasillo'),
        (4, 'Habitación'),
        (5, 'Cama'),
        (6, 'Baño / Aseo'),
        (7, 'Zona genérica'),
    ]

    identificador = models.CharField(max_length=512, unique=True)
    nombre = models.CharField(max_length=50, unique=True)
    tipo = models.IntegerField(choices=TIPOS_ZONA, default=7)
    zona_padre = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subzonas')
    bloqueada = models.BooleanField(default=False)

    # Campos extra opcionales para análisis
    total_camas = models.PositiveIntegerField(default=0)
    camas_ocupadas = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"


# ────────────────────────────────
# 🔹 MODELO: CLIENTE
# ────────────────────────────────
class Cliente(models.Model):
    TIPO_DOC = [
        (1, 'DNI'),
        (2, 'Pasaporte'),
    ]

    TIPO_ENFERMEDAD = [
        ('ninguna', 'Ninguna'),
        ('cardiaca', 'Cardíaca'),
        ('respiratoria', 'Respiratoria'),
        ('neurologica', 'Neurológica'),
        ('diabetes', 'Diabetes'),
        ('otra', 'Otra'),
    ]

    identificador = models.CharField(max_length=512, unique=True)
    nombre = models.CharField(max_length=50)
    apellido1 = models.CharField(max_length=50)
    apellido2 = models.CharField(max_length=50, blank=True, null=True)
    documento = models.CharField(max_length=50, unique=True)
    tipo_documento = models.IntegerField(choices=TIPO_DOC, default=2)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    alta = models.BooleanField(default=True)
    zona_asignada = models.ForeignKey('Zona', null=True, blank=True, on_delete=models.SET_NULL, related_name='clientes')

    # ➕ Nuevo campo: tipo de enfermedad
    tipo_enfermedad = models.CharField(
        max_length=20,
        choices=TIPO_ENFERMEDAD,
        default='ninguna'
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido1}"


# ────────────────────────────────
# 🔹 MODELO: CONTACTO DE CLIENTE
# ────────────────────────────────
class Contacto(models.Model):
    RELACIONES = [
        (1, 'Otros'),
        (2, 'Hijo/a'),
        (3, 'Cónyuge'),
        (4, 'Padre/Madre'),
        (5, 'Hermano/a'),
        (6, 'Vecino/a'),
        (7, 'Amigo/a'),
        (8, 'Familiar'),
    ]

    identificador = models.CharField(max_length=512, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='contactos')
    nombre = models.CharField(max_length=50)
    apellido1 = models.CharField(max_length=50)
    apellido2 = models.CharField(max_length=50, blank=True, null=True)
    relacion = models.IntegerField(choices=RELACIONES, default=1)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_relacion_display()})"


# ────────────────────────────────
# 🔹 MODELO: EMPLEADO
# ────────────────────────────────
class Empleado(models.Model):
    identificador = models.CharField(max_length=512, unique=True)
    nombre = models.CharField(max_length=50)
    apellido1 = models.CharField(max_length=50)
    cargo = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    # ➕ Nuevo: Relación con zona
    zona_asignada = models.ForeignKey(
        Zona,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='empleados_asignados'
    )

    def __str__(self):
        zona = f" - {self.zona_asignada.nombre}" if self.zona_asignada else ""
        return f"{self.nombre} {self.apellido1} - {self.cargo}{zona}"
