# Generated by Django 5.0.4 on 2024-05-16 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanelApp', '0005_patientmedicinemodel_patientmedicine_mg'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicinemodel',
            name='medicine_remember_quantity',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]
