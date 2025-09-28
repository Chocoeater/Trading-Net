from django_filters import OrderingFilter
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from suppliers.models import Node
from suppliers import serializers
from suppliers.permissions import IsActiveEmployee

@extend_schema_view(
    list=extend_schema(
        summary="Список поставщиков",
        description="Получить список узлов сети поставок (Node) с поддержкой фильтрации, поиска и сортировки.",
        parameters=[
            OpenApiParameter(name="country", description="Фильтр по стране", required=False, type=str),
            OpenApiParameter(name="search", description="Поиск по имени", required=False, type=str),
            OpenApiParameter(name="ordering", description="Сортировка по `name` или `country`", required=False, type=str),
        ],
        responses={200: serializers.NodeSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Получить поставщика",
        description="Возвращает данные одного узла сети поставок по ID.",
        responses={200: serializers.NodeSerializer},
    ),
    create=extend_schema(
        summary="Создать поставщика",
        description="Создает новый узел сети поставок.",
        request=serializers.NodeSerializer,
        responses={201: serializers.NodeSerializer},
    ),
    update=extend_schema(
        summary="Обновить поставщика",
        description="Полностью обновляет данные поставщика по ID.",
        request=serializers.NodeSerializer,
        responses={200: serializers.NodeSerializer},
    ),
    partial_update=extend_schema(
        summary="Частично обновить поставщика",
        description="Частично обновляет данные поставщика по ID.",
        request=serializers.NodeSerializer,
        responses={200: serializers.NodeSerializer},
    ),
    destroy=extend_schema(
        summary="Удалить поставщика",
        description="Удаляет узел сети поставок по ID.",
        responses={204: OpenApiResponse(description="Удалено успешно")},
    ),
)
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