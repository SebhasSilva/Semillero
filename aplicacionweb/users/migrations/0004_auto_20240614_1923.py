# Generated by Django 3.2.6 on 2024-06-15 00:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0003_alter_photo_user'),
        ('users', '0003_auto_20240612_1324'),
    ]

    operations = [
        migrations.CreateModel(
            name='StreetPerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('birth_date', models.DateField()),
                ('birth_city', models.CharField(max_length=100)),
                ('alias', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='StreetPersonHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('changes', models.JSONField()),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('street_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.streetperson')),
            ],
        ),
        migrations.DeleteModel(
            name='Photo',
        ),
        migrations.AlterField(
            model_name='profile',
            name='photos',
            field=models.ManyToManyField(blank=True, to='photos.Photo'),
        ),
        migrations.AddField(
            model_name='streetperson',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
    ]
