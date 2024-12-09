from rest_framework import serializers
from .models import Products

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = fields = [
            'id', 'name', 'description', 'price', 'stock', 
            'category', 'image', 'is_available', 
            'created_at', 'updated_at'
        ]