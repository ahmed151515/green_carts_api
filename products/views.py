from django.shortcuts import render
from rest_framework import viewsets
# from rest_framework import permissions
from .models import Products
from .serializers import ProductsSerializer

class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]