# Generated by Django 3.1.2 on 2020-12-06 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='is_delivered',
            field=models.BooleanField(default=False),
        ),
    ]