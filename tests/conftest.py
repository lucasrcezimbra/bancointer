import pytest


@pytest.fixture
def statements_data():
    return {
        'transacoes': [
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
