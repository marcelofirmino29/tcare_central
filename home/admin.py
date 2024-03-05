from django.contrib import admin
from home import models

@admin.register(models.TagBle)
class TagBleAdmin(admin.ModelAdmin):
    list_display = ('id','uuid_tag', 'status')
    search_fields = ('uuid_tag',)


@admin.register(models.Raspberry)
class RaspberryAdmin(admin.ModelAdmin):
    list_display = ('id','local')
    search_fields = ('local',)



@admin.register(models.LeituraTag)
class LeituraTagAdmin(admin.ModelAdmin):
    list_display = ('tag_ble', 'raspberry', 'data_leitura', 'monitorado', 'local')
    search_fields = ('tag_ble', 'raspberry', 'monitorado', 'local')

    #def nome(self,obj):
    #    return obj.monitorado
    
   # def local(self, obj):
     #   return obj.raspberry.local

@admin.register(models.Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = ('localizacao',)



@admin.register(models.Objeto)
class ObjetoAdmin(admin.ModelAdmin):
    list_display = ('id','descricao','tag_ble','valor')


class PessoaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'genero', 'data_nascimento', 'telefone','tag_ble')
    search_fields = ('nome', 'cpf')


@admin.register(models.Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tag_ble','cpf', 'genero', 'data_nascimento', 'telefone', 'matricula', 'salario', 'data_admissao', 'status', 'setor')

@admin.register(models.Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'genero', 'data_nascimento', 'telefone', 'numero_quarto')

@admin.register(models.Acompanhante)
class AcompanhanteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tag_ble','cpf', 'genero', 'data_nascimento', 'telefone', 'relacionamento', 'paciente_acomp')

    def paciente(self, obj):
        return obj.paciente_acomp.nome

@admin.register(models.Visitante)
class VisitanteAdmin(admin.ModelAdmin):
    list_display = ('nome','tag_ble', 'cpf', 'genero', 'data_nascimento', 'telefone', 'motivo_visita', 'paciente_vis')

@admin.register(models.Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'cep', 'logradouro', 'numero', 'bairro', 'cidade', 'uf', 'pessoa')

    #def nome_pessoa(self, obj):
      #  return obj.pessoa.nome


@admin.register(models.Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('nome','tag_ble', 'cpf', 'genero', 'data_nascimento', 'telefone', 'matricula', 'salario', 'data_admissao', 'status', 'setor', 'especialidade')

