# Generated by Django 5.0.4 on 2024-05-09 05:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='medicineModel',
            fields=[
                ('medicine_id', models.CharField(default=None, max_length=60, primary_key=True, serialize=False)),
                ('medicine_name', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('medicine_price', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('medicine_quantity', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('medicine_mfg_date', models.DateField(blank=True, default=None, null=True)),
                ('medicine_expiry_date', models.DateField(blank=True, default=None, null=True)),
                ('medicine_mg', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('medicine_is_active', models.BooleanField(default=True)),
                ('medicine_created_at', models.DateTimeField(auto_now_add=True)),
                ('medicine_created_at_update', models.CharField(blank=True, default=None, max_length=100, null=True)),
            ],
            options={
                'db_table': 'medicinemodel_tb',
            },
        ),
        migrations.CreateModel(
            name='patienthistoryModel',
            fields=[
                ('patienthistory_id', models.CharField(default=None, max_length=60, primary_key=True, serialize=False)),
                ('patienthistory_name', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('patienthistory_doctor_name', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('patienthistory_diseases_description', models.TextField(blank=True, default=None, null=True)),
                ('patienthistory_medicine_name', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('patienthistory_mobile_no', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('patienthistory_price', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('patienthistory_quantity', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('patienthistory_remember_quantity', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('patienthistory_totalprice', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('patienthistory_is_active', models.BooleanField(default=True)),
                ('patienthistory_created_at', models.DateTimeField(auto_now_add=True)),
                ('patienthistory_created_at_update', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('medicine', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='adminpanelApp.medicinemodel')),
            ],
            options={
                'db_table': 'patienthistorymodel_tb',
            },
        ),
        migrations.CreateModel(
            name='sellmedicineModel',
            fields=[
                ('sellmedicine_id', models.CharField(default=None, max_length=60, primary_key=True, serialize=False)),
                ('sellmedicine_name', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('sellmedicine_price', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('sellmedicine_quantity', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('sellmedicine_remember_quantity', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('sellmedicine_is_active', models.BooleanField(default=True)),
                ('sellmedicine_created_at', models.DateTimeField(auto_now_add=True)),
                ('sellmedicine_created_at_update', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('medicine', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='adminpanelApp.medicinemodel')),
            ],
            options={
                'db_table': 'sellmedicinemodel_tb',
            },
        ),
    ]
