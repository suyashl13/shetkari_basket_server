# Generated by Django 3.1.4 on 2021-07-28 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_cart_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
