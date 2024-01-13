from datetime import datetime
from decimal import Decimal

from inter import Operation


def test_from_data(faker, mocker, statements_data):
    data = statements_data["transacoes"][0]

    statement = Operation.from_data(data)

    assert statement.date == datetime.strptime(data["dataEntrada"], "%Y-%m-%d").date()
    assert statement.type == data["tipoTransacao"]
    assert statement.value == Decimal(str(data["valor"]))
    assert statement.title == data["titulo"]
    assert statement.description == data["descricao"]


def test_from_data_negative_value_when_is_debit(faker, mocker, statements_data):
    data = statements_data["transacoes"][0]
    data["tipoOperacao"] = Operation.DEBIT

    statement = Operation.from_data(data)

    assert statement.value < 0
