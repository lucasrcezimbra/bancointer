from datetime import datetime
from decimal import Decimal

from inter import Inter
from inter._client import Client
from inter._inter import Operation
from inter.testing import ClientFake


def test_init():
    client = ClientFake()

    inter = Inter(client=client)

    assert inter._client == client


def test_init_from_credentials(faker, mocker):
    client_mock = mocker.patch('inter._inter.Client', autospec=True)
    client_id, client_secret = faker.pystr(), faker.pystr()
    cert_path, key_path = faker.file_path(), faker.file_path()

    inter = Inter(
        client_id=client_id,
        client_secret=client_secret,
        cert_path=cert_path,
        key_path=key_path,
    )

    assert isinstance(inter._client, Client)
    client_mock.assert_called_once_with(client_id, client_secret, cert_path, key_path)


def test_get_balance(faker, mocker):
    client = ClientFake()
    balance_data = client.balance

    inter = Inter(client=client)

    assert inter.get_balance() == Decimal(str(balance_data['disponivel']))


def test_get_balance_with_date(faker, mocker, balance_data):
    client = ClientFake()
    get_balance_spy = mocker.spy(client, 'get_balance')
    date = faker.past_date()

    Inter(client=client).get_balance(date)

    get_balance_spy.assert_called_once_with(date)


def test_get_statement(faker, mocker, statements_data):
    client_mock = mocker.MagicMock(spec=Client)
    start_date, end_date = faker.past_date(), faker.past_date()

    Inter(client=client_mock).get_statement(start_date, end_date)

    client_mock.get_statements.assert_called_once_with(start_date, end_date)


def test_get_statement_result(faker, mocker):
    client = ClientFake()
    client.statements['transacoes'][0]['tipoOperacao'] = 'C'
    statements_data = client.statements

    statement = Inter(client=client).get_statement(faker.past_date(), faker.past_date())

    assert isinstance(statement, list)
    operation, data = statement[0], statements_data['transacoes'][0]
    assert isinstance(operation, Operation)
    assert operation.date == datetime.strptime(data['dataEntrada'], '%Y-%m-%d').date()
    assert operation.type == data['tipoTransacao']
    assert operation.value == Decimal(data['valor'])
    assert operation.title == data['titulo']
    assert operation.description == data['descricao']
