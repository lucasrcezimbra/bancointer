from datetime import date, datetime
from decimal import Decimal

from attrs import define

from inter._client import Client


class Inter:
    def __init__(self, client):
        self._client = client

    @classmethod
    def from_credentials(cls, client_id, client_secret, cert_path, key_path):
        return cls(client=Client(client_id, client_secret, cert_path, key_path))

    def get_balance(self, date=None):
        """
        Retorna o saldo disponível da conta em determinado dia.

        :param date: data do saldo
        :type date: :class:`datetime.date`

        :return: saldo disponível
        :rtype: :class:`decimal.Decimal`
        """
        return Decimal(str(self._client.get_balance(date)['disponivel']))

    def get_statement(self, start_date, end_date):
        """
        Busca extrato da conta referente as datas recebidas.

        :param start_date: data inicial do extrato
        :type start_date: :class:`datetime.date`
        :param end_date: data final do extrato
        :type end_date: :class:`datetime.date`

        :return: lista de operações do periodo
        :rtype: :class:`List[Operation]`
        """
        data = self._client.get_statements(start_date, end_date)['transacoes']
        return [Operation.from_data(d) for d in data]


@define
class Operation:
    PAYMENT = 'PAGAMENTO'
    PIX = 'PIX'

    CREDIT = 'C'
    DEBIT = 'D'

    date: date
    description: str
    title: str
    type: str
    value: Decimal

    @classmethod
    def from_data(cls, data):
        value = Decimal(str(data['valor']))
        value = (value * -1) if data['tipoOperacao'] == cls.DEBIT else value

        return cls(
            date=datetime.strptime(data['dataEntrada'], '%Y-%m-%d').date(),
            description=data['descricao'],
            title=data['titulo'],
            type=data['tipoTransacao'],
            value=value,
        )
