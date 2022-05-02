# Generated by Django 3.2.12 on 2022-04-29 04:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_ocsb', '0009_auto_20220419_0615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='syrupusage',
            name='syrup_brix',
            field=models.DecimalField(decimal_places=2, max_digits=4, validators=[django.core.validators.MinValueValidator(57), django.core.validators.MaxValueValidator(100)], verbose_name='ค่าบริกซ์น้ำเชื่อม'),
        ),
    ]
