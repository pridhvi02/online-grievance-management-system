# Generated by Django 4.1.3 on 2023-02-19 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cc', '0019_hod'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comp', to='cc.branch'),
        ),
    ]
