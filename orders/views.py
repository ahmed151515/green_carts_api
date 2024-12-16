from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response

from products.models import Products
from .models import Orders, Items

from .serializers import OrdersSerializer, ItemsSerilaizer
from rest_framework import generics


#   cart
#  add items
# cart -> pending
# return to 1


class ItemViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ItemsSerilaizer

    def list(self, request, order_id):
        order = get_object_or_404(Orders, pk=order_id)
        items = Items.objects.filter(order=order)
        serializer = ItemsSerilaizer(items, many=True)
        return Response(serializer.data)

    def create(self, request):
        order = get_object_or_404(Orders, status="CART", user=request.user)
        product_id = request.data.get("product")
        quantity = int(request.data.get("quantity"))
        product = get_object_or_404(Products, pk=product_id)
        serilaizer = ItemsSerilaizer(
            data={
                "product": product.id,
                "quantity": quantity,
            }
        )
        if serilaizer.is_valid():
            order.total_price += product.price * quantity
            order.save()
            serilaizer.save(order=order, price=product.price)
            return Response(serilaizer.data, status=status.HTTP_201_CREATED)
        return Response(serilaizer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        order = get_object_or_404(Orders, user=request.user, status="CART")
        item = get_object_or_404(Items, pk=pk, order=order)
        serializer = ItemsSerilaizer(item)
        return Response(serializer.data)

    def update(self, request, pk):
        order = get_object_or_404(Orders, user=request.user, status="CART")
        item = get_object_or_404(Items, pk=pk, order=order)
        quantity = int(request.data.get("quantity"))
        serilaizer = ItemsSerilaizer(item, data={"quantity": quantity}, partial=True)
        if serilaizer.is_valid():
            if item.quantity < quantity:
                order.total_price += item.price * (quantity - item.quantity)
            else:
                order.total_price -= item.price * (item.quantity - quantity)
            order.save()
            serilaizer.save(quantity=quantity)
            return Response(serilaizer.data)
        return Response(serilaizer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        order = get_object_or_404(Orders, user=request.user, status="CART")
        item = get_object_or_404(Items, pk=pk, order=order)
        order.total_price -= item.price * item.quantity
        order.save()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartsList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrdersSerializer

    def get_queryset(self):
        return Orders.objects.filter(user=self.request.user, status="CART")


class OrdersCreate(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrdersSerializer

    def create(self, request, *args, **kwargs):
        order = get_object_or_404(Orders, user=request.user, status="CART")
        order.status = "PENDING"
        order.save()
        # payment here
        serializer = OrdersSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
