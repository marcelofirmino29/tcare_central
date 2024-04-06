from . import models
from django import forms
from django.core.exceptions import ValidationError
from home.validators import validate_cpf
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import uuid
from django.contrib.auth.forms import AuthenticationForm
from .models import Funcionario

class TagBleForm(forms.ModelForm):
    class Meta:
        model = models.TagBle
        fields = (
            'uuid_tag',
            'status',
        )
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
        widgets = {
            'uuid_tag': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(choices=CHOICES, attrs={'class': 'form-select'}),
        }

    
class PacienteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Defina um valor padrão para o campo 'tipo' aqui
        self.fields['tipo'].initial = 1


    class Meta:
        model = models.Paciente
        fields = (
            'nome',
            'cpf',
            'genero',
            'data_nascimento',
            'email',
            'telefone',
            'numero_quarto',
            'tag_ble',
            'tipo',
        )
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 123.456.789-00'}),
            'genero': forms.Select(attrs={'class': 'form-select'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: (99) 99999-9999'}),
            'numero_quarto': forms.TextInput(attrs={'class': 'form-control'}),
            'tag_ble': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),

        }


    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        print (f'passei no clean {cpf}')
        validate_cpf(cpf)



        return cpf


class AcompanhanteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Defina um valor padrão para o campo 'tipo' aqui
        self.fields['tipo'].initial = 2

        
    class Meta:
        model = models.Acompanhante
        fields = (
            'nome',
            'cpf',
            'genero',
            'data_nascimento',
            'telefone',
            'email',
            'paciente_acomp',
            'relacionamento',
            'tag_ble',
            'tipo',
        )

        widgets = {
            'tag_ble': forms.TextInput(attrs={'class': 'form-control'}),
            'relacionamento': forms.TextInput(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 123.456.789-00'}),
            'genero': forms.Select(attrs={'class': 'form-select'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: (99) 99999-9999'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'paciente_acomp': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
        }
        
        
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        print (f'passei no clean {cpf}')
            
        try:
            validate_cpf(cpf)
        except ValidationError as e:
            raise ValidationError(e.messages)  # Levanta a exceção novamente com as mensagens de erro

        return cpf


#TODO Fazer o cadastro de visitante


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome', 'cpf', 'genero', 'data_nascimento', 'telefone', 'email', 'matricula', 'salario', 'data_admissao', 'status', 'setor', 'tipo', 'tag_ble']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Adicionando classes Bootstrap aos widgets dos campos
        self.fields['nome'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'Nome'})
        self.fields['cpf'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'CPF'})
        self.fields['genero'].widget.attrs.update({'class': 'form-select mb-3'})
        self.fields['data_nascimento'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'Data de Nascimento'})
        self.fields['telefone'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'Telefone'})
        self.fields['email'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'E-mail'})
        self.fields['matricula'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'Matrícula'})
        self.fields['salario'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'Salário'})
        self.fields['data_admissao'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'Data de Admissão'})
        self.fields['status'].widget.attrs.update({'class': 'form-select mb-3'})
        self.fields['setor'].widget.attrs.update({'class': 'form-control mb-3'})
        self.fields['tipo'].widget.attrs.update({'class': 'form-select mb-3'})
        self.fields['tag_ble'].widget.attrs.update({'class': 'form-select mb-3'})

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
        return instance


class RegistroForm(UserCreationForm):
    
    first_name = forms.CharField(
        required=True,
        min_length=3,
    )
    last_name = forms.CharField(
        required=True, 
    )

    email = forms.EmailField(
        required=True,
    )
    
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 
            'username', 'password1', 'password2',
        )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
           self.add_error('email', ValidationError('Email já cadastrado',code='invalid'))

        return email
    

class BootstrapAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})  # Adiciona a classe form-control do Bootstrap

            # Se quiser adicionar classes adicionais para campos específicos, você pode fazer algo como:
            if field_name == 'username':
                field.widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'Nome de usuário'})
            elif field_name == 'password':
                field.widget.attrs.update({'class': 'form-control', 'placeholder': 'Senha'})
