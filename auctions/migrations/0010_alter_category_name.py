# Generated by Django 4.0.4 on 2022-05-11 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('Choose', 'Choose'), ('Figurine', 'Figurine'), ('House Furnitures', 'House Furnitures'), ('Jewelry', 'Jewelry'), ('Painting', 'Painting'), ('Plushie', 'Plushie')], max_length=32),
        ),
    ]