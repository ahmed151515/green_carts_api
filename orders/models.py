from django.db import models


class Orders(models.Model):

    # product = models.ForeignKey("products.Products", on_delete=models.CASCADE)
    # quantity = models.IntegerField()
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, default=0
    )
    user = models.ForeignKey("customers.Customer", on_delete=models.CASCADE, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"Order {self.id} - Status: {self.status}"


# class Carts(models.Model):

#     # product = models.ForeignKey("products.Products", on_delete=models.CASCADE)
#     # quantity = models.IntegerField()
#     total_price = models.DecimalField(
#         max_digits=10, decimal_places=2, blank=True, null=True
#     )
#     user = models.ForeignKey("customers.Customer", on_delete=models.CASCADE, blank=True)
#     order_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Order {self.id} - Status: {self.status}"


class Items(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("products.Products", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Item {self.id} - Order: {self.order.id}, Product: {self.product}"
