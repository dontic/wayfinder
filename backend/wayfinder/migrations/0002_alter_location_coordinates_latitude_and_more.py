# Generated by Django 5.0 on 2023-12-30 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wayfinder', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='coordinates_latitude',
            field=models.DecimalField(decimal_places=17, max_digits=20),
        ),
        migrations.AlterField(
            model_name='location',
            name='coordinates_longitude',
            field=models.DecimalField(decimal_places=17, max_digits=20),
        ),
        migrations.AlterField(
            model_name='visit',
            name='arrival_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='visit',
            name='coordinates_latitude',
            field=models.DecimalField(decimal_places=17, max_digits=20),
        ),
        migrations.AlterField(
            model_name='visit',
            name='coordinates_longitude',
            field=models.DecimalField(decimal_places=17, max_digits=20),
        ),
    ]
