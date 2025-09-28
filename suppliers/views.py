
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from suppliers.models import Node, Product
from suppliers import serializers
from suppliers.permissions import IsActiveEmployee

@extend_schema_view(
    destroy=extend_schema(
        description="Удаление поставщиков через API запрещено.",
        responses={405: OpenApiResponse(description="Method Not Allowed")},
    )
)
class SupplierViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с узлами сети поставок (Node).

    Attributes
    ----------
    queryset : QuerySet
        Все объекты Node с предвыборкой связанных продуктов (`prefetch_related("products")`).
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
    - Используется для CRUD-операций через DRF с поддержкой фильтрации, поиска и сортировки.
    - Для оптимизации запросов используется `prefetch_related` для связанных продуктов.
    - Удаление поставщиков через API запрещено: метод `destroy` возвращает статус 405 (Method Not Allowed).
    """
    queryset = Node.objects.prefetch_related("products").all()
    serializer_class = serializers.NodeSerializer
    permission_classes = [IsAuthenticated, IsActiveEmployee]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["country"]
    search_fields = ["name"]
    ordering_fields = ["name", "country"]

    def destroy(self, request, *args, **kwargs):
        return Response(
            {"detail": "Удаление поставщиков через API запрещено."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с продуктами (Product).

    Attributes
    ----------
    queryset : QuerySet
        Все объекты Product.
    serializer_class : Serializer
        Сериализатор для модели Product (ProductSerializer).
    permission_classes : list
        Разрешения: доступ только для аутентифицированных и активных пользователей.
    filter_backends : list
        Фильтры, применяемые к запросам (DjangoFilterBackend).
    filterset_fields : list
        Поля для фильтрации (`owner`).

    Notes
    -----
    Используется для CRUD-операций с продуктами через DRF.
    """
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAuthenticated, IsActiveEmployee]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['owner']
