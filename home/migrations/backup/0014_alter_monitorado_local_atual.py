# Generated by Django 5.0.2 on 2024-04-09 14:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_alter_monitorado_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitorado',
            name='local_atual',
            field=models.ForeignKey(blank=True, default=13, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.local'),
        ),
    ]
