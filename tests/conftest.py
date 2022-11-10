from uuid import uuid4

import pytest


@pytest.fixture
def statements_data():
    return {
        'transacoes': [
            {
                'dataEntrada': '2022-09-11',
                'tipoTransacao': 'PIX',
                'tipoOperacao': 'C',
                'valor': '123.45',
                'titulo': 'Pix recebido',
                'descricao': 'PIX RECEBIDO - Cp :12345678-EMPRESA TECNOLOGIA LTDA',
            },
            {
                'dataEntrada': '2022-09-10',
                'tipoTransacao': 'PAGAMENTO',
                'tipoOperacao': 'D',
                'valor': '1122.33',
                'titulo': 'Pagamento efetuado',
                'descricao': 'PAGAMENTO DARF - ',
            },
            {
                'dataEntrada': '2022-09-15',
                'tipoTransacao': 'PIX',
                'tipoOperacao': 'D',
                'valor': '3322.11',
                'titulo': 'Pix enviado ',
                'descricao': 'PIX ENVIADO - Cp :12345678-EMPRESA TECNOLOGIA LTDA',
            }
        ]
    }


@pytest.fixture
def balance_data():
    return {'disponivel': 1234.56}


@pytest.fixture
def pay_barcode_data(faker):
    return {
        'quantidadeAprovadores': 1,
        'dataAgendamento': faker.date(),
        'statusPagamento': 'AGUARDANDO_APROVACAO',
        'codigoTransacao': str(uuid4()),
    }
