# Generated by Django 3.2.6 on 2024-10-15 04:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_customuser_acepto_tratamiento'),
    ]

    operations = [
        migrations.CreateModel(
            name='FamilySearch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_name', models.CharField(max_length=100)),
                ('search_birth_date', models.DateField()),
                ('search_gender', models.CharField(max_length=10)),
                ('search_last_seen', models.DateField()),
                ('search_description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
