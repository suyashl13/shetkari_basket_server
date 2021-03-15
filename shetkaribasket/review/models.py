from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from ..orders.models import Cart


# Create your models here.
class Review(models.Model):
    review_cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    comment = models.TextField(max_length=255)

    def __str__(self):
        return f"Review for CART {self.review_cart.pk} (BY : {self.review_cart.user_owner.name})"