# Generated by Django 4.0.4 on 2022-05-15 03:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_alter_comment_commenter_alter_comment_listing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='value',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='winner',
        ),
        migrations.AddField(
            model_name='bid',
            name='bid',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10, validators=[django.core.validators.MinValueValidator(1)]),
            preserve_default=False,
        ),
    ]
