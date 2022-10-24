import random

from faker import Faker

from inter import Client, Operation

faker = Faker()


def generate_operation_data():
    return {
        'dataEntrada': faker.date(),
        'tipoTransacao': random.choice(Operation.TYPES),
        'tipoOperacao': random.choice(('C', 'D')),
        'valor': str(faker.pyfloat(right_digits=2, positive=True)),
        'titulo': faker.sentence(),
        'descricao': faker.sentence(),
    }


class ClientFake(Client):
    def __init__(self, *args, **kwargs):
        self.balance = {'disponivel': faker.pyfloat(right_digits=2)}
        self.statements = {
            'transacoes': [generate_operation_data(), generate_operation_data()]
        }

    def get_balance(self, date=None):
        return self.balance

    def get_statements(self, start_date, end_date):
        return self.statements
