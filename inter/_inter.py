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
        :rtype: List[:class:`Operation`]
        """
        data = self._client.get_statements(start_date, end_date)['transacoes']
        return [Operation.from_data(d) for d in data]


@define
class Operation:
    PAYMENT = 'PAGAMENTO'
    PIX = 'PIX'
    TYPES = (PAYMENT, PIX)

    CREDIT = 'C'
    DEBIT = 'D'

    date: date
    "Data da operação"

    description: str
    "Descrição da Operação"

    title: str
    "Título da Operação"

    type: str
    "Tipo da operação. Exemplo: :attr:`PAYMENT`, :attr:`PIX`, etc."

    value: Decimal
    "Valor da operação. Positivo se for crédito, negativo se for débito"

    @classmethod
    def from_data(cls, data):
        """
        Transforma dados retornados da API em um objeto :class:`Operation`.

        :param data: dicionário com dados de uma operação
        :type data: `dict`

        :return: Operação
        :rtype: :class:`Operation`
        """
        value = Decimal(str(data['valor']))
        value = (value * -1) if data['tipoOperacao'] == cls.DEBIT else value

        return cls(
            date=datetime.strptime(data['dataEntrada'], '%Y-%m-%d').date(),
            description=data['descricao'],
            title=data['titulo'],
            type=data['tipoTransacao'],
            value=value,
        )
