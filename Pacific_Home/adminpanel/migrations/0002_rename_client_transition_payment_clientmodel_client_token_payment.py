# Generated by Django 4.2.5 on 2023-12-06 06:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clientmodel',
            old_name='client_transition_payment',
            new_name='client_token_payment',
        ),
    ]
