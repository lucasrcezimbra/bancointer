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
        """
        Retorna dados fakes simulando a resposta do endpoint real.
        Sobreescreva `client.balance` para customizar o retorno.

        >>> client = ClientFake()
        >>>
        >>> client.balance = {'custom': 'balance'}
        >>> client.get_balance()
        {'custom': 'balance'}
        """
        return self.balance

    def get_statements(self, start_date, end_date):
        """
        Retorna dados fakes simulando a resposta do endpoint real.
        Sobreescreva `client.statements` para customizar o retorno.

        >>> from datetime import date
        >>>
        >>> client = ClientFake()
        >>>
        >>> client.statements = {'statements': 'custom'}
        >>> client.get_statements(date.today(), date.today())
        {'statements': 'custom'}
        """
        return self.statements
