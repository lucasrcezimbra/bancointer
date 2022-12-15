from datetime import datetime

from inter import Payment


def test_from_data(faker, mocker, pay_barcode_data):
    data = pay_barcode_data

    payment = Payment.from_data(data)

    assert payment.approvers_number == data['quantidadeAprovadores']
    assert payment.scheduled_date == datetime.strptime(data['dataAgendamento'], '%Y-%m-%d').date()
    assert payment.status == data['statusPagamento']
    assert payment.transaction_id == data['codigoTransacao']


def test_from_data_without_scheduled_date(faker, mocker, pay_barcode_data):
    data = pay_barcode_data

    del data['dataAgendamento']
    payment = Payment.from_data(data)

    assert payment.scheduled_date is None
