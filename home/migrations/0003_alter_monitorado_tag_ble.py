# Generated by Django 5.0.2 on 2024-03-02 19:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_monitorado_tag_ble'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitorado',
            name='tag_ble',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.tagble', unique=True),
        ),
    ]