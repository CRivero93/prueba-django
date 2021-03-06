# Generated by Django 3.0 on 2020-03-07 10:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0005_auto_20200305_1902'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='room_number',
        ),
        migrations.AlterField(
            model_name='guest',
            name='phone',
            field=models.CharField(max_length=9, validators=[django.core.validators.RegexValidator(message="El teléfono debe tener el formato: '655223344'.", regex='^\\d{9}$')]),
        ),
    ]
