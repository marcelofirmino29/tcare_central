from django.db import models
import uuid

class TagBle(models.Model):
    uuid_tag = models.UUIDField(default=uuid.uuid4, unique=True)
    show = models.BooleanField(default=True)
    
    CHOICES = [
        ('novo', 'Novo'),
        ('disponivel', 'Disponível'),
        ('indisponivel', 'Indisponível'),
        ('em_uso', 'Em Uso'),
        ('reservado', 'Reservado'),
        ('em_manutencao', 'Em Manutenção'),
        ('defeituoso', 'Defeituoso'),
        ('baixado', 'Baixado'),
    ]

    status = models.CharField(
        max_length=20,
        choices=CHOICES,
        default='novo',
    )

    def __str__(self) -> str:
        return str(self.id)


class Local(models.Model):
    # LOCAL_CHOICES = [
    #     ('ala_a', 'Ala A'),
    #     ('ala_b', 'Ala B'),
    #     ('ala_c', 'Ala C'),
    #     ('ala_d', 'Ala D'),
    #     ('sala_de_emergencia', 'Sala de Emergência'),
    #     ('sala_de_cirurgia', 'Sala de Cirurgia'),
    #     ('sala_de_parto', 'Sala de Parto'),
    #     ('uti', 'UTI'),
    #     ('ambulatorio', 'Ambulatório'),
    #     ('laboratorio', 'Laboratório'),
    #     ('farmacia', 'Farmácia'),
    #     ('administracao', 'Administração'),
    # ]

    localizacao = models.CharField(
        max_length=30,
        #choices=LOCAL_CHOICES,
    )

    def __str__(self) -> str:
        return str(self.localizacao)


class Raspberry(models.Model):
    uuid_rasp = models.UUIDField(default=uuid.uuid4, unique=True)
    local = models.ForeignKey(Local, on_delete=models.PROTECT, null=True)

    def __str__(self) -> str:
        return str(self.id)

class Tipo(models.Model):
    # MONITORADO_CHOICES = [
    #     ('paciente','Paciente'),
    #     ('medico','Médico'),
    #     ('enfermeiro','Enfermeiro'),
    #     ('acompanhante','Acompanhante'),
    #     ('visitante','Visitante'),
    #     ('objeto','Objeto'),


    # ]
    tipo = models.CharField(
        max_length=20, 
        #choices=MONITORADO_CHOICES,
        )

    def __str__(self) -> str:
        return str(self.tipo)

class Monitorado(models.Model):
    tag_ble = models.OneToOneField(TagBle, on_delete=models.PROTECT, null=True, blank=True)
    local_atual = models.ForeignKey(Local, on_delete=models.PROTECT, null=True, blank=True, default=13) #default 13 = recepção
    tipo = models.ForeignKey(Tipo, on_delete=models.PROTECT, null=True, blank=False)
    

    def nome_ou_descricao(self, obj):
        if hasattr(obj, 'objeto'):
            return obj.objeto.descricao
        elif hasattr(obj, 'pessoa'):
            return obj.pessoa.nome
        else:
            return "N/A"

    def __str__(self) -> str:
        return self.nome_ou_descricao(self)

    nome_ou_descricao.short_description = 'Nome ou Descrição'


class LeituraTag(models.Model):
    tag_ble = models.ForeignKey(TagBle, on_delete=models.PROTECT)
    raspberry = models.ForeignKey(Raspberry, on_delete=models.PROTECT)
    monitorado = models.ForeignKey(Monitorado, on_delete=models.PROTECT )
    data_leitura = models.DateTimeField(auto_now_add=True)
    local = models.ForeignKey(Local, on_delete=models.PROTECT,default=1)

    def get_leitura_como_array(self):
        return [
            self.tag_ble_id,
            self.raspberry_id,
            self.data_leitura,
            self.monitorado_id,
            self.local_id
        ]
    def __str__(self) -> str:
        return f'{self.tag_ble, self.raspberry, self.data_leitura, self.monitorado, self.local}'
    

    class Meta:
        verbose_name_plural = 'Leituras de Tags'


class Objeto(Monitorado):
    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = 'objeto'


class Pessoa(Monitorado):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]


    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)  # Considerando formato 'XXX.XXX.XXX-XX'
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=20)  # Considerando formato com DDD e número
    email = models.EmailField(max_length=80)

    def __str__(self):
        return self.nome


class Paciente(Pessoa):
    numero_quarto = models.IntegerField(blank=True, null=True)



class Acompanhante(Pessoa):
    relacionamento = models.CharField(max_length=100)
    paciente_acomp = models.OneToOneField(Paciente, on_delete=models.PROTECT)
    


class Visitante(Pessoa):
    motivo_visita = models.CharField(max_length=100)
    paciente_vis = models.ForeignKey(Paciente, on_delete=models.PROTECT)


class Funcionario(Pessoa):
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
    ]



    matricula = models.CharField(max_length=20, unique=True)
    #salario = models.DecimalField(max_digits=10, decimal_places=2) #TODO Remover campos de salário e data_admissão
    #data_admissao = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ativo')
    setor = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.nome} ({self.tipo})"
    


class Recepcionista(Funcionario):
    ...


class Medico(Funcionario):
    ...

class Enfermeiro(Funcionario):
    ...
