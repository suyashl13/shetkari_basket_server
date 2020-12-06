from django.db import models
from ..products.models import Product
from ..users.models import CustomUser


# Create your models here.
class Cart(models.Model):
    user_owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user_address = models.TextField(max_length=255, default="")

    is_delivered = models.BooleanField(default=False)
    delivered_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='employee_who_delivered', blank=True, null=True)

    date_time_created = models.DateTimeField(auto_now=True)
    date_time_updated = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, default="")
    subtotal = models.CharField(max_length=4, default="")
    order_status = models.CharField(max_length=12, default='Assigned')

    def __str__(self):
        return f"{self.user_owner.name} (CART ID : {str(self.pk)})"


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=9, default="1")

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user_phone = models.CharField(max_length=12)
    amount = models.CharField(max_length=8, default="0")

    date_time_created = models.DateTimeField(auto_now=True)
    date_time_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} (ORDER ID : {self.pk})"
