# Generated by Django 3.2.6 on 2024-06-27 22:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0005_photo_visible'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacialLandmarks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('photo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='landmarks', to='photos.photo')),
            ],
        ),
    ]
