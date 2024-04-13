import os, sys
from pathlib import Path
from random import choice, randint, random
import django
from django.conf import settings

DJANGO_BASE_DIR = Path(__file__).parent.parent
NUMBER_OF_OBJECTS = 100

sys.path.append(str(DJANGO_BASE_DIR))
os.environ['DJANGO_SETTINGS_MODULE'] = 'central.settings'
settings.USE_TZ = False

django.setup()

if __name__ == '__main__':
    import faker
    from home.models import Funcionario, Tipo

    fake = faker.Faker('pt_BR')

    def create_pessoas(num_pessoas):
        for _ in range(num_pessoas):
           
            medico = Tipo.objects.get(id=3)
            enfermeiro = Tipo.objects.get(id=4)
            
            
            pessoa = Funcionario(
                nome=fake.name(),
                cpf=fake.unique.ssn(),  # Gera um número de CPF único
                genero=choice(['M', 'F', 'O']),
                data_nascimento=fake.date_of_birth(minimum_age=18, maximum_age=90),
                telefone=fake.phone_number(),
                email=fake.email(),
                matricula=fake.unique.ssn(),
                tipo=choice([medico,enfermeiro]),
            )
            pessoa.save()

    # Chame a função para criar as pessoas
    create_pessoas(NUMBER_OF_OBJECTS)
