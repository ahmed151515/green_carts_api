from rest_framework import viewsets
# from rest_framework import permissions
from .models import Products
from .serializers import ProductsSerializer

class ProductsViewSet(viewsets.ModelViewSet):
    # queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Products.objects.all()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__iexact=category)
        return queryset