# Generated by Django 3.2.6 on 2021-08-24 00:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopCart', '0003_auto_20210824_0008'),
        ('sales', '0003_remove_sale_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='address',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='shopCart.address', verbose_name='Dirección'),
        ),
    ]
