# Generated by Django 4.2.5 on 2023-12-25 15:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_alter_restaurant_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_number', models.PositiveIntegerField()),
                ('pic', models.ImageField(upload_to='SubAdmin_pics/')),
                ('restaurant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.restaurant')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'django_SubAdmin',
            },
        ),
    ]
