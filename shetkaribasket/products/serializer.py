from rest_framework.serializers import HyperlinkedModelSerializer, ImageField
from .models import Product


class ProductSerializer(HyperlinkedModelSerializer):
    product_image = ImageField(max_length=None, allow_empty_file=False, required=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'unit', 'discount', 'is_available',
                  'date_created', 'date_updated', 'product_image']
