from rest_framework import serializers
from .models import Usuario, Autor, Libro, Prestamo

# ==========================================
# RF1: SERIALIZADORES PARA LIBROS Y AUTORES
# ==========================================
class AutorSerializer(serializers.ModelSerializer):
    """Nested serialization para el autor"""
    class Meta:
        model = Autor
        fields = ['id', 'nombre', 'nacionalidad', 'biografia']

class LibroSerializer(serializers.ModelSerializer):
    """Serialización avanzada para Libros"""
    # Campo anidado (Nested): Muestra el autor completo en lugar del ID
    autor = AutorSerializer(read_only=True)
    
    # Campo calculado (RF1)
    disponible = serializers.BooleanField(read_only=True)
    
    # Campo hipervinculado (HATEOAS - RF1)
    url = serializers.HyperlinkedIdentityField(
        view_name='libro-detail', 
        lookup_field='pk'
    )

    class Meta:
        model = Libro
        fields = [
            'url', 'id', 'isbn', 'titulo', 'autor', 'editorial', 
            'anio', 'categoria', 'stock', 'ubicacion', 'disponible'
        ]
        read_only_fields = ['disponible', 'url']


# ==========================================
# RF3: SERIALIZADOR PARA USUARIOS
# ==========================================
class UsuarioSerializer(serializers.ModelSerializer):
    """Serialización diferenciada para usuarios"""
    # Campo readonly: Cuenta préstamos activos
    prestamos_activos = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'tipo', 'carrera', 
            'email', 'telefono', 'prestamos_activos'
        ]
        read_only_fields = ['prestamos_activos']

    def get_prestamos_activos(self, obj):
        """Cuenta cuántos préstamos activos tiene el usuario"""
        return obj.prestamos.filter(estado='activo').count()


# ==========================================
# RF2: SERIALIZADOR PARA PRÉSTAMOS
# ==========================================
class PrestamoSerializer(serializers.ModelSerializer):
    """Serialización con validaciones y campos calculados"""
    # Campos calculados (RF2)
    dias_restantes = serializers.IntegerField(read_only=True)
    multa = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Prestamo
        fields = [
            'id', 'usuario', 'libro', 'fecha_prestamo', 
            'fecha_devolucion', 'estado', 'dias_restantes', 'multa'
        ]
        read_only_fields = ['dias_restantes', 'multa', 'fecha_prestamo', 'estado']

    def validate(self, attrs):
        """Validaciones de negocio (RF2)"""
        usuario = attrs.get('usuario')
        libro = attrs.get('libro')

        # 1. Validar que el usuario no tenga más de 5 préstamos activos
        prestamos_activos = usuario.prestamos.filter(estado='activo').count()
        if prestamos_activos >= 5:
            raise serializers.ValidationError({
                "usuario": "El usuario ya tiene el máximo de 5 préstamos activos."
            })

        # 2. Validar que el libro tenga stock disponible
        if libro.stock <= 0:
            raise serializers.ValidationError({
                "libro": "El libro no tiene stock disponible."
            })

        return attrs