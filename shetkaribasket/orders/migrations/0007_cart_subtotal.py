# Generated by Django 3.1.2 on 2020-12-05 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20201205_0916'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='subtotal',
            field=models.CharField(default='', max_length=4),
        ),
    ]