# Generated by Django 3.1.2 on 2020-12-05 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_auto_20201205_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='payment_method',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
    ]