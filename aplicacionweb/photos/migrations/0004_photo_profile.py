# Generated by Django 3.2.6 on 2024-06-17 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20240615_1518'),
        ('photos', '0003_alter_photo_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='profile',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='profile_photos', to='users.profile'),
            preserve_default=False,
        ),
    ]
