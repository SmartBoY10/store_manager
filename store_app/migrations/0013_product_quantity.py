# Generated by Django 3.0.4 on 2022-05-16 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0012_remove_product_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.PositiveIntegerField(default=0, verbose_name='Кол-во в складе'),
        ),
    ]
