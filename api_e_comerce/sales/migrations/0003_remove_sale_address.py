# Generated by Django 3.2.6 on 2021-08-24 00:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_alter_sale_client'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='address',
        ),
    ]
