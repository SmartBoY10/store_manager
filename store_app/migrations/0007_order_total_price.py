# Generated by Django 3.0.4 on 2022-02-27 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0006_auto_20220227_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.PositiveIntegerField(default=0, verbose_name='Общая сумма'),
        ),
    ]