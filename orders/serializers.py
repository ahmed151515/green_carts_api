from rest_framework import serializers
from .models import Orders


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ["id", "product_id", "quantity", "order_date", "status", "total_price"]
        read_only_fields = ["order_date", "status"]
