from rest_framework.permissions import BasePermission


class IsActiveEmployee(BasePermission):
    """
    Разрешение, позволяющее доступ только активным пользователям.

    Methods
    -------
    has_permission(request, view)
        Проверяет, что текущий пользователь активен.

    Returns
    -------
    bool
        True, если пользователь активен, иначе False.
    """
    def has_permission(self, request, view):
        return request.user.is_active
