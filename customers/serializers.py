from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Customer
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "password",
            "address",
            "phone_number",
        ]

    def create(self, validated_data):
        return Customer.objects.create_user(**validated_data)
