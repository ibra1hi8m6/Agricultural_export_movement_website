# Generated by Django 5.0.2 on 2024-02-26 06:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0002_productsnames'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductsNames',
            new_name='ProductsName',
        ),
    ]
