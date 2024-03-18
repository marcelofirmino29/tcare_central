from django import forms
from django.core.exceptions import ValidationError

def validate_cpf(value):
    cpf = ''.join(filter(str.isdigit, value))  # Remover caracteres não numéricos do CPF
    if len(cpf) != 11:
        raise ValidationError('CPF deve conter 11 dígitos.')
    if cpf == cpf[::-1]:
        raise ValidationError('CPF inválido: todos os números são iguais.')
    
    # Cálculo do dígito verificador
    total = 0
    for i in range(9):
        total += int(cpf[i]) * (10 - i)
    remainder = total % 11
    if remainder < 2:
        digito1 = 0
    else:
        digito1 = 11 - remainder
    
    total = 0
    for i in range(10):
        total += int(cpf[i]) * (11 - i)
    remainder = total % 11
    if remainder < 2:
        digito2 = 0
    else:
        digito2 = 11 - remainder
    
    # Verificar se os dígitos calculados coincidem com os dígitos do CPF
    if digito1 != int(cpf[9]) or digito2 != int(cpf[10]):
        raise ValidationError('CPF inválido.')
    
    return value

# class PessoaForm(forms.Form):
#     cpf = forms.CharField(max_length=14, validators=[validate_cpf], label='CPF')
