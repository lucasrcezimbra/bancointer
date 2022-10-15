import requests


class URL:
    BASE = 'https://cdpj.partners.bancointer.com.br/'
    AUTH = BASE + 'oauth/v2/token'


class Inter:
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
