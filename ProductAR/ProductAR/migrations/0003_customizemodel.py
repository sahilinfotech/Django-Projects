# Generated by Django 5.0.3 on 2024-03-27 09:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProductAR', '0002_delete_customizemodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='customizeModel',
            fields=[
                ('customize_id', models.CharField(default=None, max_length=60, primary_key=True, serialize=False)),
                ('customize_image', models.TextField(blank=True, default=None, null=True)),
                ('customize_video_path', models.TextField(blank=True, default=None, null=True)),
                ('customize_video_download_link', models.TextField(blank=True, default=None, null=True)),
                ('customize_created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='ProductAR.usermodel')),
            ],
            options={
                'db_table': 'customizemodel_tb',
            },
        ),
    ]
