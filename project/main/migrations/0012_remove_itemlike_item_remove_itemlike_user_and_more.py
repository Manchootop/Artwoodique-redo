# Generated by Django 4.2.6 on 2024-04-13 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_remove_wishlist_item_wishlist_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemlike',
            name='item',
        ),
        migrations.RemoveField(
            model_name='itemlike',
            name='user',
        ),
        migrations.DeleteModel(
            name='Subscriber',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='item',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='user',
        ),
        migrations.DeleteModel(
            name='ItemLike',
        ),
        migrations.DeleteModel(
            name='WishList',
        ),
    ]