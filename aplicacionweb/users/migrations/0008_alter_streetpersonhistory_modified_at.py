# Generated by Django 3.2.6 on 2024-09-23 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20240923_0903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streetpersonhistory',
            name='modified_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]