# Generated by Django 4.1.3 on 2023-01-21 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cc', '0014_alter_complaint_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='complaint',
            old_name='user',
            new_name='owner',
        ),
    ]
