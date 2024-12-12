from os import getenv
from rest_framework import viewsets
from .permissions import IsAdminUserOrReadOnly
from .models import Products
from .serializers import ProductsSerializer
import cloudinary.uploader
import cloudinary

cloudinary.config(
    cloud_name=getenv("CLOUD_NAME"),
    api_key=getenv("API_KEY"),
    api_secret=getenv("API_SECRET"),
)


class ProductsViewSet(viewsets.ModelViewSet):
    # queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def get_queryset(self):
        queryset = Products.objects.all()
        category = self.request.query_params.get("category")
        if category:
            queryset = queryset.filter(category__iexact=category)
        return queryset

    def perform_create(self, serializer):
        image = serializer.validated_data.get("_image")
        uploaded_image = cloudinary.uploader.upload(image)
        serializer.save(image_url=uploaded_image["url"])
