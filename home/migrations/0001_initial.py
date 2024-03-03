# Generated by Django 5.0.2 on 2024-03-02 19:16

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Local',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Monitorado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TagBle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Objeto',
            fields=[
                ('monitorado_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.monitorado')),
                ('descricao', models.CharField(max_length=100)),
            ],
            bases=('home.monitorado',),
        ),
        migrations.CreateModel(
            name='Pessoa',
            fields=[
                ('monitorado_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.monitorado')),
                ('nome', models.CharField(max_length=100)),
            ],
            bases=('home.monitorado',),
        ),
        migrations.CreateModel(
            name='Raspberry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('local', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.local')),
            ],
        ),
        migrations.AddField(
            model_name='monitorado',
            name='tag_ble',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.tagble'),
        ),
        migrations.CreateModel(
            name='LeituraTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_leitura', models.DateTimeField(auto_now_add=True)),
                ('monitorado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.monitorado')),
                ('raspberry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.raspberry')),
                ('tag_ble', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.tagble')),
            ],
            options={
                'verbose_name_plural': 'Leituras de Tags',
            },
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('pessoa_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.pessoa')),
                ('matricula', models.CharField(max_length=11)),
            ],
            bases=('home.pessoa',),
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('pessoa_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.pessoa')),
                ('numero_quarto', models.IntegerField()),
            ],
            bases=('home.pessoa',),
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cep', models.CharField(max_length=8)),
                ('pessoa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.pessoa')),
            ],
        ),
        migrations.CreateModel(
            name='Enfermeiro',
            fields=[
                ('funcionario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.funcionario')),
            ],
            bases=('home.funcionario',),
        ),
        migrations.CreateModel(
            name='Medico',
            fields=[
                ('funcionario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.funcionario')),
                ('especialidade', models.CharField(max_length=100)),
            ],
            bases=('home.funcionario',),
        ),
        migrations.CreateModel(
            name='Recepcionista',
            fields=[
                ('funcionario_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.funcionario')),
            ],
            bases=('home.funcionario',),
        ),
        migrations.CreateModel(
            name='Acompanhante',
            fields=[
                ('pessoa_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.pessoa')),
                ('relacionamento', models.CharField(max_length=100)),
                ('paciente_acomp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.paciente')),
            ],
            bases=('home.pessoa',),
        ),
        migrations.CreateModel(
            name='Visitante',
            fields=[
                ('pessoa_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.pessoa')),
                ('motivo_visita', models.CharField(max_length=100)),
                ('paciente_vis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.paciente')),
            ],
            bases=('home.pessoa',),
        ),
    ]