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
    LOCAL_CHOICES = [
        ('ala_a', 'Ala A'),
        ('ala_b', 'Ala B'),
        ('ala_c', 'Ala C'),
        ('ala_d', 'Ala D'),
        ('sala_de_emergencia', 'Sala de Emergência'),
        ('sala_de_cirurgia', 'Sala de Cirurgia'),
        ('sala_de_parto', 'Sala de Parto'),
        ('uti', 'UTI'),
        ('ambulatorio', 'Ambulatório'),
        ('laboratorio', 'Laboratório'),
        ('farmacia', 'Farmácia'),
        ('administracao', 'Administração'),
    ]

    localizacao = models.CharField(
        max_length=30,
        choices=LOCAL_CHOICES,
    )

    def __str__(self) -> str:
        return str(self.localizacao)


class Raspberry(models.Model):
    uuid_rasp = models.UUIDField(default=uuid.uuid4, unique=True)
    local = models.ForeignKey(Local, on_delete=models.PROTECT, null=True)

    def __str__(self) -> str:
        return str(self.id)


class Monitorado(models.Model):
    tag_ble = models.OneToOneField(TagBle, on_delete=models.PROTECT, null=True, blank=True)

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

    def __str__(self) -> str:
        return f'{self.tag_ble, self.raspberry, self.data_leitura, self.monitorado, self.local}'

    class Meta:
        verbose_name_plural = 'Leituras de Tags'


class Objeto(Monitorado):
    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)


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
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    data_admissao = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ativo')
    setor = models.CharField(max_length=100)


class Recepcionista(Funcionario):
    pass


class Medico(Funcionario):
    pass


class Enfermeiro(Funcionario):
   pass
"""
class Especialidade(models.Model):
    descricao = models.CharField(max_length=50)

class MedicoEspecialidade(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    especialidade = models.ForeignKey(Especialidade, on_delete=models.CASCADE)
"""
"""
class Endereco(models.Model):
    TIPO_CHOICES = [
        ('residencial', 'Residencial'),
        ('comercial', 'Comercial'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    cep = models.CharField(max_length=9)  # Considerando formato 'XXXXX-XXX'
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)  # Considerando o código de 2 letras para a UF
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tipo}: {self.logradouro}, {self.numero}, {self.bairro}, {self.cidade} - {self.uf}"
"""   

"""
Este código define uma série de modelos em Django que representam diferentes entidades de um sistema. Aqui está uma visão geral do que acontece em cada seção:

Importações e Definição de Modelos:

O código começa importando models do Django e o módulo uuid.
Em seguida, são definidos vários modelos Django que representam diferentes entidades do sistema, como TagBle, Local, Raspberry, Monitorado, LeituraTag, Objeto, Pessoa, Paciente, Acompanhante, Visitante, Funcionario, Recepcionista, Medico, Enfermeiro, Especialidade, MedicoEspecialidade e Endereco.
Cada modelo possui campos que representam atributos da entidade correspondente, como nome, CPF, gênero, data de nascimento, etc. Além disso, existem campos relacionais como chaves estrangeiras e campos de muitos para muitos.
Herança de Modelos:

Alguns modelos, como Objeto, Pessoa, Recepcionista, Medico e Enfermeiro, herdam de Monitorado. Isso significa que eles têm todos os campos e métodos de Monitorado, além de campos e métodos adicionais específicos para cada subclasse.
Definição de Campos e Métodos:

Os modelos definem diferentes tipos de campos, como CharField, UUIDField, IntegerField, DecimalField, DateField, DateTimeField, etc., para armazenar diferentes tipos de dados.
Além disso, alguns modelos definem métodos especiais, como __str__, para retornar representações em string dos objetos.
Relacionamentos entre Modelos:

Os modelos estão interconectados por meio de chaves estrangeiras (ForeignKey) e chaves únicas (OneToOneField). Por exemplo, LeituraTag está relacionado com TagBle, Raspberry, Monitorado e Local.
Em resumo, este código define a estrutura de dados de um sistema em Django, representando diferentes entidades e seus relacionamentos. Esses modelos podem ser usados para persistir dados e realizar operações de banco de dados dentro de um aplicativo Django.
"""