# Generated by Django 5.0.2 on 2024-04-04 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_tipo_remove_pessoa_tipo_monitorado_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='local',
            name='localizacao',
            field=models.CharField(max_length=30),
        ),
    ]
