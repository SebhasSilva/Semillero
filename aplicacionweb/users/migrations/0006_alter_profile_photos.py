# Generated by Django 3.2.6 on 2024-06-17 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0004_photo_profile'),
        ('users', '0005_auto_20240615_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photos',
            field=models.ManyToManyField(blank=True, related_name='profile_photos', to='photos.Photo'),
        ),
    ]