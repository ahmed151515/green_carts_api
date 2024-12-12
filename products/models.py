from django.db import models


class Products(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    stock = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=255, blank=True)
    image_url = models.URLField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    _image = models.ImageField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} (ID: {self.id})"
