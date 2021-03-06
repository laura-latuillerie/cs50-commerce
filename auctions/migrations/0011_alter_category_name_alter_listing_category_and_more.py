# Generated by Django 4.0.4 on 2022-05-12 12:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('Figurine', 'Figurine'), ('House Furnitures', 'House Furnitures'), ('Jewelry', 'Jewelry'), ('Painting', 'Painting'), ('Plushie', 'Plushie')], max_length=32),
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(default='2', on_delete=django.db.models.deletion.SET_DEFAULT, to='auctions.category'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='watched_by',
            field=models.ManyToManyField(blank=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Watchlist',
        ),
    ]
