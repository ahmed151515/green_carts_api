from rest_framework import serializers
from .models import Orders, Items


class OrdersSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(many=True, queryset=Items.objects.all())

    class Meta:
        model = Orders
        fields = "__all__"
        read_only_fields = ["order_date", "status"]


class ItemsSerilaizer(serializers.ModelSerializer):

    class Meta:
        model = Items
        fields = "__all__"
        # read_only_fields = "__all__"
