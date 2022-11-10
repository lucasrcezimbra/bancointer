import requests


class URL:
    BASE = 'https://cdpj.partners.bancointer.com.br/'
    AUTH = BASE + 'oauth/v2/token'
    STATEMENTS = BASE + 'banking/v2/extrato'
    BALANCE = BASE + 'banking/v2/saldo'


class Scopes:
    READ_STATEMENTS = 'extrato.read'
    "Consulta de saldo e extrato"

    WRITE_PAYMENT = 'pagamento-boleto.write'
    "Pagamento de boletos"

    all = (READ_STATEMENTS, WRITE_PAYMENT)


class Client:
    """
    Inicializa utilizando as credenciais.

    :param client_id: Client ID
    :type client_id: :class:`str`

    :param client_secret: Client Secret
    :type client_secret: :class:`str`

    :param cert_path: Caminho do arquivo de certificado
    :type cert_path: :class:`str`

    :param key_path: Caminho do arquivo de chave
    :type key_path: :class:`str`

    :param scopes: Iterável contendo os :class:`Scopes` necessários
    :type scopes: :class:`Iterable`
    """
    def __init__(self, client_id, client_secret, cert_path, key_path, scopes=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.cert_path = cert_path
        self.key_path = key_path
        self.scopes = scopes or Scopes.all
        self._token = None

    def _get_token(self):
        response = requests.post(
            URL.AUTH,
            data={
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'scope': ' '.join(self.scopes),
                'grant_type': 'client_credentials',
            },
            cert=(self.cert_path, self.key_path),
        )
        return response.json()['access_token']

    @property
    def token(self):
        if not self._token:
            self._token = self._get_token()
        return self._token

    @property
    def headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    def get_balance(self, date=None):
        params = {}

        if date:
            params['dataSaldo'] = date.strftime('%Y-%m-%d')

        response = requests.get(
            URL.BALANCE,
            params=params,
            headers=self.headers,
            cert=(self.cert_path, self.key_path),
        )
        return response.json()

    def get_statements(self, start_date, end_date):
        response = requests.get(
            URL.STATEMENTS,
            params={
                'dataInicio': start_date.strftime('%Y-%m-%d'),
                'dataFim': end_date.strftime('%Y-%m-%d'),
            },
            headers=self.headers,
            cert=(self.cert_path, self.key_path),
        )
        return response.json()
