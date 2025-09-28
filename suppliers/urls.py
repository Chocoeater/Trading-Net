from rest_framework.routers import DefaultRouter
from suppliers import views

from suppliers.apps import SuppliersConfig


app_name = SuppliersConfig.name

router = DefaultRouter()

router.register(r"nodes", views.SupplierViewSet, basename="nodes")
router.register(r"products", views.ProductViewSet, basename="products")

urlpatterns = [] + router.urls