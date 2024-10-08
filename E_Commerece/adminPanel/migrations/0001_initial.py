# Generated by Django 5.0.6 on 2024-05-27 08:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Product_name', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Product_price', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Product_image', models.TextField(blank=True, default=None, null=True)),
                ('Product_is_active', models.BooleanField(default=True)),
                ('Product_created_at', models.DateTimeField(auto_now_add=True)),
                ('Product_created_at_update', models.CharField(blank=True, default='None', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductdetailModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Productdetail_description', models.TextField(blank=True, default=None, null=True)),
                ('Productdetail_type', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Productdetail_colour', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('Productdetail_is_active', models.BooleanField(blank=True, default=True, null=True)),
                ('Productdetail_created_at', models.DateTimeField(auto_now_add=True)),
                ('Productdetail_created_at_update', models.CharField(blank=True, default='None', null=True)),
                ('Product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='adminPanel.productmodel')),
            ],
        ),
    ]
