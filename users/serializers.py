from django.utils import timezone
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Кастомный сериализатор для получения JWT токена.

    Добавляет email пользователя в payload токена
    и обновляет last_login после успешного входа.
    """
    @classmethod
    def get_token(cls, user):
        """
        Генерирует токен с добавленным полем email.

        Parameters
        ----------
        user : User
            Пользователь, для которого создается токен.

        Returns
        -------
        RefreshToken
            JWT токен пользователя.
        """
        token = super().get_token(user)

        token["email"] = user.email

        return token

    def validate(self, attrs):
        """
        Валидирует логин и пароль, обновляет last_login.

        Parameters
        ----------
        attrs : dict
            Входные данные (email и password).

        Returns
        -------
        dict
            Данные токена (access и refresh).
        """
        data = super().validate(attrs)
        self.user.last_login = timezone.now()
        self.user.save()
        return data