# Generated by Django 4.0.4 on 2022-05-10 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_listing_winner_alter_category_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('FG', 'Figurine'), ('HF', 'House Furnitures'), ('JW', 'Jewelry'), ('PT', 'Paiting'), ('PS', 'Plushie')], max_length=32),
        ),
    ]
