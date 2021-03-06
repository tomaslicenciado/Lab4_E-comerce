# Generated by Django 3.2.6 on 2021-09-07 02:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saledetail',
            name='product',
        ),
        migrations.RemoveField(
            model_name='saledetail',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='saledetail',
            name='subtotal',
        ),
        migrations.AlterField(
            model_name='sale',
            name='delivery_cost',
            field=models.FloatField(default=0, verbose_name='Costo de envío'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='pay_method',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='sales.paymethod', verbose_name='Forma de pago'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='subtotal',
            field=models.FloatField(default=0, verbose_name='Sub total'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='total',
            field=models.FloatField(default=0, verbose_name='Total'),
        ),
    ]
