from django.db import models
import uuid

class TagBle(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.id)

class Local(models.Model):
    descricao = models.CharField(max_length=100)

    def __str__(self) -> str:
        return str(self.descricao)

class Raspberry(models.Model):
    local = models.ForeignKey(Local, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return str(self.id)

class Monitorado(models.Model):
    tag_ble = models.OneToOneField(TagBle, on_delete=models.CASCADE, null=True, blank=True)

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
    tag_ble = models.ForeignKey(TagBle, on_delete=models.CASCADE)
    raspberry = models.ForeignKey(Raspberry, on_delete=models.CASCADE)
    monitorado = models.ForeignKey(Monitorado, on_delete=models.CASCADE )
    data_leitura = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.tag_ble, self.raspberry, self.data_leitura}'

    class Meta:
        verbose_name_plural = 'Leituras de Tags'







class Objeto(Monitorado):
    # Adicione campos específicos para a classe Objeto aqui
    descricao = models.CharField(max_length=100)

class Pessoa(Monitorado):
    # Adicione campos específicos para a classe Pessoa aqui
    nome = models.CharField(max_length=100)


class Paciente(Pessoa):
    # Adicione campos específicos para a classe Paciente aqui
    numero_quarto = models.IntegerField()

class Acompanhante(Pessoa):
    # Adicione campos específicos para a classe Acompanhante aqui
    relacionamento = models.CharField(max_length=100)
    paciente_acomp = models.ForeignKey(Paciente, on_delete=models.CASCADE)

class Visitante(Pessoa):
    # Adicione campos específicos para a classe Visitante aqui
    motivo_visita = models.CharField(max_length=100)
    paciente_vis = models.ForeignKey(Paciente, on_delete=models.CASCADE)

class Funcionario(Pessoa):
    # Adicione campos específicos para a classe Funcionario aqui
    matricula = models.CharField(max_length=11)

class Recepcionista(Funcionario):
    pass

class Medico(Funcionario):
    especialidade = models.CharField(max_length=100)
    # Adicione outros campos específicos para Médico, se houver

class Enfermeiro(Funcionario):
   pass

class Endereco(models.Model):
    cep = models.CharField(max_length=8)
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
