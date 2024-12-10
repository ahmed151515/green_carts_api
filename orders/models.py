from django.db import models

# Create your models here.


class Orders(models.Model):

    product_id = models.ForeignKey("products.Products", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Pending")
    user_id = models.ForeignKey("customers.Customer", on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.order_id
