from django.urls import include, path
from rest_framework import routers
from .views import OrdersViewSet

router = routers.DefaultRouter()
router.register("", OrdersViewSet, basename="orders-page")

urlpatterns = [
    path("", include(router.urls)),
]
