from . import models
from django import forms
from django.core.exceptions import ValidationError
from home.validators import validate_cpf
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TagBleForm(forms.ModelForm):
    class Meta:
        model = models.TagBle
        fields = (
            'uuid_tag',
            'status',
        )

class PacienteForm(forms.ModelForm):
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
        )

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')

        validate_cpf(cpf)

        return cpf

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