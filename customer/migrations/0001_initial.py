# Generated by Django 4.2.5 on 2023-12-28 12:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('subadmin', '0004_subadmin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_number', models.PositiveSmallIntegerField()),
                ('pic', models.ImageField(upload_to='Customer/Profile_Pics')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'django_customer',
            },
        ),
        migrations.CreateModel(
            name='CustomerTableOrders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('check_in', models.DateTimeField()),
                ('check_out', models.DateTimeField()),
                ('table_no', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
                ('food', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='subadmin.food')),
                ('table', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='subadmin.table')),
            ],
            options={
                'db_table': 'django_CustomerTableOrders',
            },
        ),
        migrations.CreateModel(
            name='CustomerFoodOrders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('checked', models.BooleanField(default=False)),
                ('quantity', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8)], default=0)),
                ('total_price', models.PositiveSmallIntegerField()),
                ('address1', models.CharField(max_length=400)),
                ('address2', models.CharField(max_length=400)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subadmin.food')),
            ],
            options={
                'db_table': 'django_CustomerFoodOrders',
            },
        ),
    ]
