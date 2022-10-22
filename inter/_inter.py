from decimal import Decimal

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
