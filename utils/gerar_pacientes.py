import os, sys
from pathlib import Path
from random import choice, randint, random
import django
from django.conf import settings

DJANGO_BASE_DIR = Path(__file__).parent.parent
NUMBER_OF_OBJECTS = 1000

sys.path.append(str(DJANGO_BASE_DIR))
os.environ['DJANGO_SETTINGS_MODULE'] = 'central.settings'
settings.USE_TZ = False

django.setup()

if __name__ == '__main__':
    import faker
    from home.models import Paciente

    fake = faker.Faker('pt_BR')

    def create_pacientes(num_pacientes):
        for _ in range(num_pacientes):
            paciente = Paciente(
                nome=fake.name(),
                cpf=fake.unique.ssn(),  # Gera um número de CPF único
                genero=choice(['M', 'F', 'O']),
                data_nascimento=fake.date_of_birth(minimum_age=18, maximum_age=90),
                telefone=fake.phone_number(),
                email=fake.email(),
                numero_quarto=randint(1, 100) if random() > 0.5 else None
            )
            paciente.save()

    # Chame a função para criar os pacientes
    create_pacientes(1000)
