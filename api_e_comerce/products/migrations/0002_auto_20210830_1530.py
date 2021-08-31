# Generated by Django 3.2.6 on 2021-08-30 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock_unit',
            field=models.IntegerField(default=0, verbose_name='Stock de unidades'),
        ),
        migrations.AlterField(
            model_name='product',
            name='unit_per_package',
            field=models.IntegerField(verbose_name='Unidades por bulto'),
        ),
    ]