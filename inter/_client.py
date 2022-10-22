import requests


class URL:
    BASE = 'https://cdpj.partners.bancointer.com.br/'
    AUTH = BASE + 'oauth/v2/token'
    STATEMENTS = BASE + 'banking/v2/extrato'
    BALANCE = BASE + 'banking/v2/saldo'


class Client:
    def __init__(self, client_id, client_secret, cert_path, key_path):
        self.client_id = client_id
        self.client_secret = client_secret
        self.cert_path = cert_path
        self.key_path = key_path
        self._token = None

    def _get_token(self):
        response = requests.post(
            URL.AUTH,
            data={
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'scope': 'extrato.read',
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
