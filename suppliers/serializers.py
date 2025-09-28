from rest_framework import serializers
from suppliers.models import Node, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class NodeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Node.

    Parameters
    ----------
    model : Node
        Модель, которую сериализует данный класс.
    fields : str or list
        Поля модели, которые включены в сериализацию.
    read_only_fields : tuple
        Поля, доступные только для чтения.

    Notes
    -----
    Используется для CRUD-операций через DRF.
    """
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Node
        fields = [
            'id', 'name', 'email', 'country', 'city',
            'street', 'house_number', 'supplier', 'debt',
            'created_at', 'level', 'products'
        ]
        read_only_fields = ("debt",  'created_at', 'level')

