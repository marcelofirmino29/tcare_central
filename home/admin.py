from django.contrib import admin
from home import models

@admin.register(models.TagBle)
class TagBleAdmin(admin.ModelAdmin):
    list_display = ('id','uuid', 'status')

@admin.register(models.Raspberry)
class RaspberryAdmin(admin.ModelAdmin):
    list_display = ('id','local')

@admin.register(models.LeituraTag)
class LeituraTagAdmin(admin.ModelAdmin):
    list_display = ('tag_ble','nome','local', 'raspberry', 'data_leitura')

    def nome(self,obj):
        return obj.monitorado
    
    def local(self, obj):
        return obj.raspberry.local

@admin.register(models.Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = ('descricao',)



@admin.register(models.Objeto)
class ObjetoAdmin(admin.ModelAdmin):
    list_display = ('id','descricao','tag_ble')


@admin.register(models.Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('id','nome','tag_ble',)

@admin.register(models.Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('id','nome','tag_ble',)

@admin.register(models.Acompanhante)
class AcompanhanteAdmin(admin.ModelAdmin):
    list_display = ('id','tag_ble','nome','relacionamento','paciente',)

    def paciente(self, obj):
        return obj.paciente_acomp.nome

@admin.register(models.Visitante)
class VisitanteAdmin(admin.ModelAdmin):
    list_display = ('id','nome','tag_ble',)

@admin.register(models.Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('id','cep','nome_pessoa')

    def nome_pessoa(self, obj):
        return obj.pessoa.nome

@admin.register(models.Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ('id','nome','tag_ble')


@admin.register(models.Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('id','nome','tag_ble')

