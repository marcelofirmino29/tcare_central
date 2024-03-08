from django.test import TestCase

from django.test import TestCase
from models import Pessoa, Paciente


"""
DESCONSIDERAR, POR ORA
"""
class PessoaTestCase(TestCase):
    def setUp(self):
        Pessoa.objects.create(nome="João", cpf="123.456.789-00", genero="M", data_nascimento="1990-01-01", telefone="12345-6789")

    def test_pessoa_criada_com_sucesso(self):
        pessoa = Pessoa.objects.get(nome="João")
        self.assertEqual(pessoa.cpf, "123.456.789-00")
        self.assertEqual(pessoa.genero, "M")
        self.assertEqual(pessoa.telefone, "12345-6789")

class PacienteTestCase(TestCase):
    def setUp(self):
        Paciente.objects.create(nome="Maria", cpf="987.654.321-00", genero="F", data_nascimento="1980-01-01", telefone="98765-4321", numero_quarto=101)

    def test_paciente_criado_com_sucesso(self):
        paciente = Paciente.objects.get(nome="Maria")
        self.assertEqual(paciente.numero_quarto, 101)

