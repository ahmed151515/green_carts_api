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

    # def list(self, request, order_id):
    #     order = get_object_or_404(Orders, pk=order_id)
    #     items = Items.objects.filter(order=order)
    #     serializer = ItemsSerilaizer(items, many=True)
    #     return Response(serializer.data)

    def create(self, request):
        """
        Create a new item in the user's cart.

        This method retrieves an existing order with status "CART" for the
        authenticated user, adds a new product to the order with the specified
        quantity, updates the total price of the order, and saves the item.

        Args:
            request (Request): The HTTP request object containing the user and
                               data for the new item (product ID and quantity).

        Returns:
            Response: A Response object containing the serialized data of the
                      created item and a status code of 201 if successful, or
                      the serializer errors and a status code of 400 if invalid.
        """
        product_id = request.data.get("product")
        quantity = int(request.data.get("quantity"))
        order = get_object_or_404(Orders, status="CART", user=request.user)
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
        """
        Retrieve a specific item from the user's cart.

        Args:
            request (Request): The HTTP request object containing user information.
            pk (int): The primary key of the item to retrieve.

        Returns:
            Response: A Response object containing the serialized item data.

        Raises:
            Http404: If the order with status "CART" for the user or the item with the given pk in the order is not found.
        """
        order = get_object_or_404(Orders, user=request.user, status="CART")
        item = get_object_or_404(Items, pk=pk, order=order)
        serializer = ItemsSerilaizer(item)
        return Response(serializer.data)

    def update(self, request, pk):
        """
        Update the quantity of an item in the user's cart.

        Args:
            request (Request): The HTTP request object containing user and data.
            pk (int): The primary key of the item to be updated.

        Returns:
            Response: A Response object containing the serialized item data if successful,
                      or the serializer errors with a 400 status code if validation fails.

        Raises:
            Http404: If the order or item does not exist.
        """
        quantity = int(request.data.get("quantity"))
        order = get_object_or_404(Orders, user=request.user, status="CART")
        item = get_object_or_404(Items, pk=pk, order=order)
        serilaizer = ItemsSerilaizer(item, data={"quantity": quantity}, partial=True)
        if serilaizer.is_valid():
            # if item.quantity < quantity:

            order.total_price += item.price * (quantity - item.quantity)
            # else:
            # order.total_price -= item.price * (item.quantity - quantity)
            order.save()
            serilaizer.save(quantity=quantity)
            return Response(serilaizer.data)
        return Response(serilaizer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        """
        Delete an item from the user's cart and update the total price of the order.

        Args:
            request (Request): The HTTP request object.
            pk (int): The primary key of the item to be deleted.

        Returns:
            Response: An HTTP response with status 204 (No Content) indicating the item was successfully deleted.
        """
        order = get_object_or_404(Orders, user=request.user, status="CART")
        item = get_object_or_404(Items, pk=pk, order=order)
        order.total_price -= item.price * item.quantity
        item.delete()
        order.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartsList(generics.ListAPIView):
    """
    CartsList is a view that provides a list of orders with the status "CART" for the authenticated user.

    Attributes:
        permission_classes (list): A list of permission classes that the user must pass to access the view.
        serializer_class (class): The serializer class used to serialize the orders.

    Methods:
        get_queryset(self):
            Returns a queryset of orders filtered by the authenticated user and status "CART".
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrdersSerializer

    def get_queryset(self):
        return Orders.objects.filter(user=self.request.user, status="CART")


class OrdersCreate(generics.CreateAPIView):
    """
    API view for creating an order.

    This view handles the creation of an order for an authenticated user. It changes the status of the order from "CART" to "PENDING" and saves it. The order is then serialized and returned in the response.

    Attributes:
        permission_classes (list): A list of permission classes that the user must satisfy to access this view.
        serializer_class (OrdersSerializer): The serializer class used for serializing the order data.

    Methods:
        create(request, *args, **kwargs):
            Handles the creation of an order. Changes the order status to "PENDING" and saves it. Returns the serialized order data in the response.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrdersSerializer

    def create(self, request, *args, **kwargs):
        """
        Handles the creation of an order.

        This method retrieves an order with the status "CART" for the current user,
        updates its status to "PENDING", and saves the order. It then serializes
        the order and returns the serialized data in the response with a status
        code of 201 (Created).

        Args:
            request (Request): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A Response object containing the serialized order data and
            a status code of 201 (Created).
        """
        order = get_object_or_404(Orders, user=request.user, status="CART")
        order.status = "PENDING"
        # payment here
        order.save()
        neworder = Orders.objects.create(user=request.user, status="CART")
        neworder.save()
        serializer = OrdersSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
