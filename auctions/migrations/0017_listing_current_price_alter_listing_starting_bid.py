# Generated by Django 4.0.4 on 2022-05-15 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_alter_bid_listing_alter_bid_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='current_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='listing',
            name='starting_bid',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
