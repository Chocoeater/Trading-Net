from rest_framework import serializers
from suppliers.models import Node


class NodeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Node.

    Parameters
    ----------
    model : Node
        Модель, которую сериализует данный класс.
    fields : str or list
        Поля модели, которые включены в сериализацию. В данном случае `"__all__"`.
    read_only_fields : tuple
        Поля, доступные только для чтения. Здесь `debt` нельзя менять через API.

    Notes
    -----
    Используется для CRUD-операций через DRF.
    """
    class Meta:
        model = Node
        fields = "__all__"
        read_only_fields = ("debt",)