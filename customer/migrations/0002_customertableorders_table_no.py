# Generated by Django 4.2.5 on 2023-12-28 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customertableorders',
            name='table_no',
            field=models.PositiveIntegerField(null=True),
        ),
    ]