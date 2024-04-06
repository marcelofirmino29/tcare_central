from django.contrib import admin
from home import models

@admin.register(models.TagBle)
class TagBleAdmin(admin.ModelAdmin):
    """
    Classe de administração para o modelo TagBle.
    """
    list_display = ('id', 'uuid_tag', 'status', 'show',)
    search_fields = ('uuid_tag',)


@admin.register(models.Raspberry)
class RaspberryAdmin(admin.ModelAdmin):
    """
    Classe de administração para o modelo Raspberry.
    """
    list_display = ('id', 'local')
    search_fields = ('local',)


@admin.register(models.LeituraTag)
class LeituraTagAdmin(admin.ModelAdmin):
    """
    Classe de administração para o modelo LeituraTag.
    """
    list_display = ('tag_ble', 'raspberry', 'data_leitura', 'monitorado', 'local')
    search_fields = ('tag_ble', 'raspberry', 'monitorado', 'local')


@admin.register(models.Local)
class LocalAdmin(admin.ModelAdmin):
    """
    Classe de administração para o modelo Local.
    """
    list_display = ('id','localizacao',)
    list_editable = ('localizacao',)

@admin.register(models.Tipo)
class TipoAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo')

@admin.register(models.Objeto)
class ObjetoAdmin(admin.ModelAdmin):
    """
    Classe de administração para o modelo Objeto.
    """
    list_display = ('id', 'descricao', 'tag_ble', 'valor')

@admin.register(models.Pessoa)
class PessoaAdmin(admin.ModelAdmin):
        list_display = ('id', 'nome', 'tipo','tag_ble','cpf', 'genero','local_atual','data_nascimento', 'email','telefone')


@admin.register(models.Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    """
    Classe de administração para o modelo Funcionario.
    """
    list_display = ('id','nome', 'tipo','tag_ble', 'cpf', 'genero', 'data_nascimento', 'telefone', 'email','matricula', 'salario', 'data_admissao', 'status', 'setor')
    list_editable = ('tipo',)


@admin.register(models.Paciente)
class PacienteAdmin(admin.ModelAdmin):
    """
    Classe de administração para o modelo Paciente.
    """
    list_display = ('id','nome', 'tipo', 'tag_ble','cpf', 'numero_quarto','local_atual','data_nascimento', 'email','telefone', )
    list_editable = ('tipo','numero_quarto')

@admin.register(models.Acompanhante)
class AcompanhanteAdmin(admin.ModelAdmin):
    """
    Classe de administração para o modelo Acompanhante.
    """
    list_display = ('id','nome', 'tipo', 'tag_ble', 'cpf', 'genero', 'data_nascimento', 'telefone','email', 'relacionamento', 'paciente_acomp')
    list_editable = ('tipo',)

@admin.register(models.Visitante)
class VisitanteAdmin(admin.ModelAdmin):
    """
    Classe de administração para o modelo Visitante.
    """
    list_display = ('nome', 'tag_ble', 'cpf', 'genero', 'data_nascimento','email', 'telefone', 'motivo_visita', 'paciente_vis')

"""
@admin.register(models.Endereco)
class EnderecoAdmin(admin.ModelAdmin):
   
    list_display = ('tipo', 'cep', 'logradouro', 'numero', 'bairro', 'cidade', 'uf', 'pessoa')

"""
@admin.register(models.Medico)
class MedicoAdmin(admin.ModelAdmin):
    """
    Classe de administração para o modelo Medico.
    """
    list_display = ('nome', 'tag_ble', 'cpf', 'genero','local_atual', 'data_nascimento', 'telefone', 'email','matricula', 'salario', 'data_admissao', 'status', 'setor', )


@admin.register(models.Enfermeiro)
class EnfermeiroAdmin(admin.ModelAdmin):
    """
    Classe de administração para o modelo Enfermeiro.
    """
    list_display = ('nome', 'tag_ble', 'cpf', 'genero','local_atual', 'data_nascimento', 'telefone', 'email','matricula', 'salario', 'data_admissao', 'status', 'setor', )
"""
Neste código:

Cada classe de administração é documentada com uma breve descrição do modelo correspondente.
A lista de campos de exibição (list_display) e campos de pesquisa (search_fields) são definidos para cada classe, especificando como os modelos devem ser exibidos e pesquisados na interface de administração do Django.
Essa documentação ajuda os desenvolvedores a entender o propósito de cada classe de administração e como ela está configurada para trabalhar com os modelos Django correspondentes.
"""