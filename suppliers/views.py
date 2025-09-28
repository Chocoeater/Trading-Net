
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from suppliers.models import Node, Product
from suppliers import serializers
from suppliers.permissions import IsActiveEmployee


class SupplierViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с узлами сети поставок (Node).

    Attributes
    ----------
    queryset : QuerySet
        Все объекты Node.
    serializer_class : Serializer
        Сериализатор для модели Node (NodeSerializer).
    permission_classes : list
        Список разрешений: только аутентифицированные и активные пользователи.
    filter_backends : list
        Фильтры, применяемые к запросам (фильтрация, поиск, сортировка).
    filterset_fields : list
        Поля для фильтрации (`country`).
    search_fields : list
        Поля для поиска (`name`).
    ordering_fields : list
        Поля для сортировки (`name`, `country`).

    Notes
    -----
    Используется для CRUD-операций через DRF с поддержкой фильтрации, поиска и сортировки.
    """
    queryset = Node.objects.all()
    serializer_class = serializers.NodeSerializer
    permission_classes = [IsAuthenticated, IsActiveEmployee]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["country"]
    search_fields = ["name"]
    ordering_fields = ["name", "country"]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAuthenticated, IsActiveEmployee]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['owner']