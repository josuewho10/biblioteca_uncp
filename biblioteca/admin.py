from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Autor, Libro, Prestamo


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'tipo', 'carrera', 'is_staff')
    list_filter = ('tipo', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Información UNCP', {'fields': ('tipo', 'carrera', 'telefono')}),
    )


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nacionalidad')
    search_fields = ('nombre',)


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'isbn', 'autor', 'categoria', 'stock', 'disponible')
    list_filter = ('categoria', 'anio')
    search_fields = ('titulo', 'isbn', 'autor__nombre')


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'libro', 'fecha_prestamo', 'fecha_devolucion', 'estado')
    list_filter = ('estado',)