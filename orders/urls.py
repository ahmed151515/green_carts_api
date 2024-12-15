from django.urls import include, path
# from rest_framework import routers
from . import views

# router = routers.DefaultRouter()
# router.register("", OrdersViewSet, basename="orders-page")
# router.register("checkout/<int:order_id>/", ItemsViewSet, basename="checkout_page")

urlpatterns = [
    # # path("", include(router.urls)),
    # path("", OrdersViewSet.as_view({'get': 'list', 'post': 'create'}), name="orders-page"),
    # path("<int:pk>/", OrdersViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name="order-detail"),
    # path("checkout/<int:order_id>/", ItemsViewSet.as_view({'get': 'list'}), name="checkout-page"),
    path("", views.OrdersList.as_view(), name="orders-page"),
]
