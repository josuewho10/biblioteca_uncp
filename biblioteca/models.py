from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Usuario(AbstractUser):
    """Modelo personalizado de usuario (RF3)"""
    TIPO_USUARIO = (
        ('estudiante', 'Estudiante'),
        ('docente', 'Docente'),
        ('investigador', 'Investigador'),
        ('bibliotecario', 'Bibliotecario'),
        ('admin', 'Administrador'),
    )
    tipo = models.CharField(max_length=20, choices=TIPO_USUARIO, default='estudiante')
    carrera = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_tipo_display()})"


class Autor(models.Model):
    """Autor de libros (parte del RF1 - nested serialization)"""
    nombre = models.CharField(max_length=150)
    nacionalidad = models.CharField(max_length=100, blank=True, null=True)
    biografia = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    """Libro del catálogo (RF1)"""
    isbn = models.CharField(max_length=20, unique=True)
    titulo = models.CharField(max_length=255)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='libros')
    editorial = models.CharField(max_length=150)
    anio = models.IntegerField()
    categoria = models.CharField(max_length=100)
    stock = models.PositiveIntegerField(default=0)
    ubicacion = models.CharField(
        max_length=100, 
        help_text="Ej: Estante 3, Piso 2"
    )

    def __str__(self):
        return self.titulo

    @property
    def disponible(self):
        """Campo calculado RF1: disponible si stock > 0"""
        return self.stock > 0


class Prestamo(models.Model):
    """Préstamo de libros (RF2)"""
    ESTADO_CHOICES = (
        ('activo', 'Activo'),
        ('devuelto', 'Devuelto'),
        ('vencido', 'Vencido'),
    )
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name='prestamos'
    )
    libro = models.ForeignKey(
        Libro, on_delete=models.CASCADE, related_name='prestamos'
    )
    fecha_prestamo = models.DateField(auto_now_add=True)
    fecha_devolucion = models.DateField()
    estado = models.CharField(
        max_length=20, choices=ESTADO_CHOICES, default='activo'
    )

    def __str__(self):
        return f"Préstamo #{self.id} - {self.libro.titulo} ({self.usuario.username})"

    @property
    def dias_restantes(self):
        """Campo calculado RF2: días restantes para devolver"""
        delta = self.fecha_devolucion - timezone.now().date()
        return max(0, delta.days)

    @property
    def multa(self):
        """Campo calculado RF2: S/ 2.00 por día de retraso"""
        hoy = timezone.now().date()
        if hoy > self.fecha_devolucion and self.estado != 'devuelto':
            dias_vencidos = (hoy - self.fecha_devolucion).days
            return dias_vencidos * 2.00
        return 0.00

    def save(self, *args, **kwargs):
        """Actualiza automáticamente el estado a 'vencido'"""
        if self.estado == 'activo' and timezone.now().date() > self.fecha_devolucion:
            self.estado = 'vencido'
        super().save(*args, **kwargs)
