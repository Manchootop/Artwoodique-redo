# Generated by Django 4.2.6 on 2024-04-13 19:47

import django.core.validators
from django.db import migrations, models
import project.accounts.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_rename_first_name_artwoodiqueuserprofile_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='artwoodiqueuserprofile',
            name='username',
            field=models.CharField(default='mancho', max_length=30, unique=True, validators=[django.core.validators.MinLengthValidator(2), project.accounts.models.validate_only_letters]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='artwoodiqueuserprofile',
            name='name',
            field=models.CharField(blank=True, max_length=30, null=True, validators=[django.core.validators.MinLengthValidator(2), project.accounts.models.validate_only_letters]),
        ),
    ]