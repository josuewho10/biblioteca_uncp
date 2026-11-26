from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permite que solo el propietario del objeto pueda editarlo.
    Cualquier usuario puede leerlo (RF4).
    """
    def has_object_permission(self, request, view, obj):
        # Permitir métodos de solo lectura (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # El objeto debe tener un atributo 'usuario' (para Préstamos)
        if hasattr(obj, 'usuario'):
            return obj.usuario == request.user
        
        return False


class PuedeCrearPrestamo(permissions.BasePermission):
    """
    Permiso personalizado para verificar si se puede crear un préstamo (RF4).
    (La lógica pesada está en el serializer, este es un filtro rápido).
    """
    def has_permission(self, request, view):
        # Solo bibliotecarios y admins pueden crear préstamos
        if request.method == 'POST':
            return request.user.is_staff or request.user.tipo in ['bibliotecario', 'admin']
        return True