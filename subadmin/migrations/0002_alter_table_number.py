# Generated by Django 4.2.5 on 2023-12-26 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subadmin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='number',
            field=models.PositiveSmallIntegerField(unique=True),
        ),
    ]
