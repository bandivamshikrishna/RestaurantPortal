# Generated by Django 4.2.5 on 2023-12-28 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_customertableorders_table_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customertableorders',
            name='table_no',
        ),
    ]
