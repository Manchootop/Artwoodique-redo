# Generated by Django 4.2.6 on 2023-11-01 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_product_discount_price_alter_product_label_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='like',
            field=models.IntegerField(default=0),
        ),
    ]