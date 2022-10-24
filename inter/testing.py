import random

from faker import Faker

from inter import Client, Inter, Operation

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


class InterFake(Inter):
    def __init__(self):
        self.balance = faker.pydecimal(right_digits=2)

    def get_balance(self, date=None):
        """
        Retorna dados fakes simulando a resposta do client real.
        Sobreescreva `InterFake.balance` para customizar o retorno.

        >>> from decimal import Decimal
        >>>
        >>> inter = InterFake()
        >>>
        >>> inter.balance = Decimal('1000.99')
        >>> inter.get_balance()
        Decimal('1000.99')
        """
        return self.balance

    def get_statement(self, start_date, end_date):
        """
        Retorna dados fakes simulando a resposta do client real.
        Sobreescreva `InterFake.statement` para customizar o retorno.

        >>> from decimal import Decimal
        >>> from datetime import date
        >>> from inter import Operation
        >>>
        >>> inter = InterFake()
        >>>
        >>> operation = Operation(
        ...     date=date.today(),
        ...     description='Descrição da Operação',
        ...     title='Pagamento efetuado',
        ...     type=Operation.PIX,
        ...     value=Decimal('123.45'),
        ... )
        >>>
        >>> inter.statement = [operation]
        >>> inter.get_statement(date.today(), date.today())  # doctest: +NORMALIZE_WHITESPACE
        [Operation(date=datetime.date(2022, 10, 24),
                   description='Descrição da Operação',
                   title='Pagamento efetuado',
                   type='PIX',
                   value=Decimal('123.45'))]
        """
        return self.statement
