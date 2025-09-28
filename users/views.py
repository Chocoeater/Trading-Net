from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import MyTokenObtainPairSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    """
    Вью для получения JWT токенов пользователя.

    Использует кастомный сериализатор MyTokenObtainPairSerializer,
    который добавляет email в payload токена и обновляет last_login.

    Attributes
    ----------
    serializer_class : MyTokenObtainPairSerializer
        Сериализатор для токена.
    permission_classes : list
        Список разрешений (AllowAny).
    """
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]