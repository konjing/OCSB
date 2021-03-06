# Generated by Django 3.2.12 on 2022-04-08 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brix',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brix_value', models.DecimalField(decimal_places=1, max_digits=4, verbose_name='ค่าบริกซ์')),
                ('spcific_gravity', models.DecimalField(decimal_places=5, max_digits=6, verbose_name='spcific gravity at 20 C/20 C')),
            ],
            options={
                'verbose_name': 'Brix',
                'verbose_name_plural': 'Brixs',
                'db_table': '',
                'managed': True,
            },
        ),
    ]
