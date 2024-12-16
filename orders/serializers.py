from rest_framework import serializers


from products.models import Products
from .models import Orders, Items


# class CartsSerializer(serializers.ModelSerializer):
#     products_id = serializers.ListSerializer()

#     class Meta:
#         model = Orders
#         fields = "__all__"
#         read_only_fields = ["order_date", "status", "user", "total_price"]


class ItemsSerilaizer(serializers.ModelSerializer):

    class Meta:
        model = Items
        fields = "__all__"
        read_only_fields = ["order", "price"]

    def validate_quantity(self, value):
        if self.instance and self.instance.quantity == value:
            raise serializers.ValidationError("Quantity cannot be the same as the current value.")
        if value < 1:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value




class OrdersSerializer(serializers.ModelSerializer):
    items = ItemsSerilaizer(many=True, read_only=True)

    class Meta:
        model = Orders
        fields = "__all__"
        read_only_fields = ["order_date", "status", "user", "total_price"]
