from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import Orders
from products.models import Products
from .serializers import OrdersSerializer

# Create your views here.


class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):

        product = get_object_or_404(
            Products, id=serializer.validated_data["product_id"].id
        )

        if product.stock < serializer.validated_data["quantity"]:
            return Response(
                {"error": "Insufficient stock available for this product."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        total_price = product.price * serializer.validated_data["quantity"]
        product.stock -= serializer.validated_data["quantity"]
        product.save()

        serializer.save(total_price=total_price, user_id=self.request.user)
