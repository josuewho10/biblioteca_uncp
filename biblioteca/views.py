from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import Libro, Prestamo, Usuario
from .serializers import LibroSerializer, PrestamoSerializer, UsuarioSerializer
from .permissions import IsOwnerOrReadOnly, PuedeCrearPrestamo


class LibroViewSet(viewsets.ModelViewSet):
    """
    RF1: ViewSet completo para Libros con filtrado y búsqueda.
    """
    queryset = Libro.objects.select_related('autor').all()
    serializer_class = LibroSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # RF5: Filtrado y Búsqueda
    filterset_fields = ['categoria', 'anio', 'stock']
    search_fields = ['titulo', 'autor__nombre', 'isbn']
    ordering_fields = ['anio', 'titulo', 'stock']
    ordering = ['titulo'] # Orden por defecto


class PrestamoViewSet(viewsets.ModelViewSet):
    """
    RF2: ViewSet para Préstamos con endpoints personalizados.
    """
    queryset = Prestamo.objects.select_related('usuario', 'libro').all()
    serializer_class = PrestamoSerializer
    permission_classes = [IsAuthenticated, PuedeCrearPrestamo, IsOwnerOrReadOnly]

    def get_queryset(self):
        """Optimización: Bibliotecarios ven todo, usuarios solo los suyos"""
        user = self.request.user
        if user.is_staff or user.tipo in ['bibliotecario', 'admin']:
            return Prestamo.objects.all()
        return Prestamo.objects.filter(usuario=user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def devolver(self, request, pk=None):
        """Endpoint personalizado: Marcar préstamo como devuelto"""
        prestamo = self.get_object()
        
        if prestamo.estado == 'devuelto':
            return Response({"error": "Este préstamo ya fue devuelto."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Actualizar estado y devolver stock
        prestamo.estado = 'devuelto'
        prestamo.save()
        
        prestamo.libro.stock += 1
        prestamo.libro.save()
        
        serializer = self.get_serializer(prestamo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def vencidos(self, request):
        """Endpoint personalizado: Listar préstamos vencidos"""
        hoy = timezone.now().date()
        # Buscamos préstamos activos cuya fecha de devolución ya pasó
        prestamos_vencidos = Prestamo.objects.filter(
            estado='activo', 
            fecha_devolucion__lt=hoy
        )
        serializer = self.get_serializer(prestamos_vencidos, many=True)
        return Response(serializer.data)


class UsuarioViewSet(viewsets.ReadOnlyModelViewSet):
    """
    RF3: ViewSet de solo lectura para Usuarios.
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def perfil(self, request):
        """Endpoint personalizado: Obtener perfil del usuario autenticado"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)