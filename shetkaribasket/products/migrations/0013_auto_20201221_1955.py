# Generated by Django 3.1.2 on 2020-12-21 14:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_auto_20201221_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(help_text='*Per 250 Grams if unit is Gram.', validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
