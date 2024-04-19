# Generated by Django 5.0.2 on 2024-03-05 02:15

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Especialidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Local',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('localizacao', models.CharField(choices=[('ala_a', 'Ala A'), ('ala_b', 'Ala B'), ('ala_c', 'Ala C'), ('ala_d', 'Ala D'), ('sala_de_emergencia', 'Sala de Emergência'), ('sala_de_cirurgia', 'Sala de Cirurgia'), ('sala_de_parto', 'Sala de Parto'), ('uti', 'UTI'), ('ambulatorio', 'Ambulatório'), ('laboratorio', 'Laboratório'), ('farmacia', 'Farmácia'), ('administracao', 'Administração')], max_length=30)),
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
                ('uuid_tag', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('status', models.CharField(choices=[('novo', 'Novo'), ('disponivel', 'Disponível'), ('indisponivel', 'Indisponível'), ('em_uso', 'Em Uso'), ('reservado', 'Reservado'), ('em_manutencao', 'Em Manutenção'), ('defeituoso', 'Defeituoso'), ('baixado', 'Baixado')], default='novo', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Objeto',
            fields=[
                ('monitorado_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.monitorado')),
                ('descricao', models.CharField(max_length=100)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            bases=('home.monitorado',),
        ),
        migrations.CreateModel(
            name='Pessoa',
            fields=[
                ('monitorado_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.monitorado')),
                ('nome', models.CharField(max_length=100)),
                ('cpf', models.CharField(max_length=14, unique=True)),
                ('genero', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')], max_length=1)),
                ('data_nascimento', models.DateField()),
                ('telefone', models.CharField(max_length=20)),
            ],
            bases=('home.monitorado',),
        ),
        migrations.CreateModel(
            name='Raspberry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid_rasp', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('local', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='home.local')),
            ],
        ),
        migrations.AddField(
            model_name='monitorado',
            name='tag_ble',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.tagble'),
        ),
        migrations.CreateModel(
            name='LeituraTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_leitura', models.DateTimeField(auto_now_add=True)),
                ('local', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='home.local')),
                ('monitorado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.monitorado')),
                ('raspberry', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.raspberry')),
                ('tag_ble', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.tagble')),
            ],
            options={
                'verbose_name_plural': 'Leituras de Tags',
            },
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('pessoa_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.pessoa')),
                ('matricula', models.CharField(max_length=20, unique=True)),
                ('salario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data_admissao', models.DateField()),
                ('status', models.CharField(choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')], default='ativo', max_length=10)),
                ('setor', models.CharField(max_length=100)),
            ],
            bases=('home.pessoa',),
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('pessoa_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.pessoa')),
                ('numero_quarto', models.IntegerField(blank=True, null=True)),
            ],
            bases=('home.pessoa',),
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('residencial', 'Residencial'), ('comercial', 'Comercial')], max_length=20)),
                ('cep', models.CharField(max_length=9)),
                ('logradouro', models.CharField(max_length=255)),
                ('numero', models.CharField(max_length=10)),
                ('bairro', models.CharField(max_length=100)),
                ('cidade', models.CharField(max_length=100)),
                ('uf', models.CharField(max_length=2)),
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
                ('paciente_acomp', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='home.paciente')),
            ],
            bases=('home.pessoa',),
        ),
        migrations.CreateModel(
            name='Visitante',
            fields=[
                ('pessoa_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.pessoa')),
                ('motivo_visita', models.CharField(max_length=100)),
                ('paciente_vis', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.paciente')),
            ],
            bases=('home.pessoa',),
        ),
        migrations.CreateModel(
            name='MedicoEspecialidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('especialidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.especialidade')),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.medico')),
            ],
        ),
    ]