from datetime import datetime
from decimal import Decimal

from inter import Inter
from inter._client import Client
from inter._inter import Operation


def test_init():
    client = object

    inter = Inter(client)

    assert inter._client == client


def test_from_credentials(faker, mocker):
    client_mock = mocker.patch('inter._inter.Client', autospec=True)
    client_id, client_secret = faker.pystr(), faker.pystr()
    cert_path, key_path = faker.file_path(), faker.file_path()

    inter = Inter.from_credentials(client_id, client_secret, cert_path, key_path)

    assert isinstance(inter._client, Client)
    client_mock.assert_called_once_with(client_id, client_secret, cert_path, key_path)


def test_get_balance(faker, mocker, balance_data):
    client = mocker.MagicMock(spec=Client)
    client.get_balance.return_value = balance_data

    inter = Inter(client)

    assert inter.get_balance() == Decimal(str(balance_data['disponivel']))


def test_get_balance_with_date(faker, mocker, balance_data):
    client_mock = mocker.MagicMock(spec=Client)
    client_mock.get_balance.return_value = balance_data
    date = faker.past_date()

    Inter(client_mock).get_balance(date)

    client_mock.get_balance.assert_called_once_with(date)


def test_get_statement(faker, mocker, statements_data):
    client_mock = mocker.MagicMock(spec=Client)
    client_mock.get_statements.return_value = statements_data
    start_date, end_date = faker.past_date(), faker.past_date()

    Inter(client_mock).get_statement(start_date, end_date)

    client_mock.get_statements.assert_called_once_with(start_date, end_date)


def test_get_statement_result(faker, mocker, statements_data):
    client_mock = mocker.MagicMock(spec=Client)
    client_mock.get_statements.return_value = statements_data

    statements = Inter(client_mock).get_statement(faker.past_date(), faker.past_date())

    assert isinstance(statements, list)
    statement, data = statements[0], statements_data['transacoes'][0]
    assert isinstance(statement, Operation)
    assert statement.date == datetime.strptime(data['dataEntrada'], '%Y-%m-%d').date()
    assert statement.type == data['tipoTransacao']
    assert statement.value == Decimal(str(data['valor']))
    assert statement.title == data['titulo']
    assert statement.description == data['descricao']
