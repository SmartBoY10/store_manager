# Generated by Django 3.0.4 on 2022-03-02 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storage',
            name='quantity_of_product',
        ),
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.PositiveIntegerField(default=0, verbose_name='Кол-во в складе'),
        ),
    ]
