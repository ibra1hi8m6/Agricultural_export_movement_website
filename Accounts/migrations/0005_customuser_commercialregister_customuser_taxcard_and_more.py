# Generated by Django 5.0.2 on 2024-05-05 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0004_alter_customuser_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='CommercialRegister',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='TaxCard',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='address',
            field=models.CharField(max_length=250, null=True),
        ),
    ]