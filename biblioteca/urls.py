from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LibroViewSet, PrestamoViewSet, UsuarioViewSet

# El router genera automáticamente las URLs
router = DefaultRouter()
router.register(r'libros', LibroViewSet, basename='libro')
router.register(r'prestamos', PrestamoViewSet, basename='prestamo')
router.register(r'usuarios', UsuarioViewSet, basename='usuario')

urlpatterns = [
    path('', include(router.urls)),
]