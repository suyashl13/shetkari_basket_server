from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=30, unique=True)
    price = models.IntegerField(validators=[MinValueValidator(1)], help_text="*Per 250 Grams if unit is Gram.")

    UNIT_CHOICES = (
        ('Kg', 'Kg'),
        ('Gram', 'Gram'),
        ('Litre', 'Litre')
    )

    unit = models.CharField(max_length=8, default="", null=True, blank=True, choices=UNIT_CHOICES)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_available = models.BooleanField(blank=False, default=True)
    date_created = models.DateField(auto_now=True)
    date_updated = models.DateField(auto_now_add=True)
    product_image = models.ImageField(upload_to='products/', default="")

    def __str__(self):
        return f"{self.name} (Rs.{self.price}) (ID : {self.pk})"
