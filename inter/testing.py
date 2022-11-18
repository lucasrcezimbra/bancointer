import random
from uuid import uuid4

from faker import Faker

from inter import Client, Inter, Operation, Payment

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
        self.pay_barcode_data = {
            'quantidadeAprovadores': faker.pyint(),
            'dataAgendamento': faker.date(),
            'statusPagamento': 'AGUARDANDO_APROVACAO',
            'codigoTransacao': str(uuid4()),
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

    def pay_barcode(self, barcode, value, due_date, payment_date=None):
        """
        Retorna dados fakes simulando a resposta do endpoint real.
        Sobreescreva `client.pay_barcode_data` para customizar o retorno.

        >>> from datetime import date
        >>>
        >>> client = ClientFake()
        >>>
        >>> client.pay_barcode_data = {'custom': True}
        >>> client.pay_barcode('0123...', '1.99', date.today(), payment_date=date.today())
        {'custom': True}
        """
        return self.pay_barcode_data


class InterFake(Inter):
    def __init__(self, *args, **kwargs):
        client = ClientFake()
        self.balance = faker.pydecimal(right_digits=2)
        self.pay_barcode_data = Payment.from_data(client.pay_barcode_data)

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
        ...     date=date(2022, 10, 24),
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

    def pay_barcode(self, barcode, value, due_date, payment_date=None):
        """
        Retorna dados fakes simulando a resposta do client real.
        Sobreescreva `InterFake.pay_barcode_data` para customizar o retorno.

        >>> from datetime import date
        >>> from uuid import uuid4
        >>> from inter import Payment
        >>>
        >>> inter = InterFake()
        >>>
        >>> payment = Payment(
        ...     approvers_number=1,
        ...     scheduled_date=date(2022, 11, 18),
        ...     status=Payment.DONE,
        ...     transaction_id='tr4ns4ct10n_1d'
        ... )
        >>>
        >>> inter.pay_barcode_data = payment
        >>> inter.pay_barcode('', '1.99', date.today(), date.today())
        ... # doctest: +NORMALIZE_WHITESPACE
        Payment(approvers_number=1,
                scheduled_date=datetime.date(2022, 11, 18),
                status='REALIZADO',
                transaction_id='tr4ns4ct10n_1d')
        """
        return self.pay_barcode_data
