# Generated by Django 3.2.6 on 2024-10-08 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_streetperson_common_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='acepto_tratamiento',
            field=models.BooleanField(default=False, help_text='Indica si el usuario ha aceptado el tratamiento de sus datos personales.'),
        ),
    ]
