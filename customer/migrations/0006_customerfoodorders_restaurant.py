# Generated by Django 4.2.5 on 2023-12-29 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_delete_subadmin'),
        ('customer', '0005_remove_customerfoodorders_checked_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerfoodorders',
            name='restaurant',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='core.restaurant'),
            preserve_default=False,
        ),
    ]
