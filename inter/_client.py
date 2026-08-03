import requests

DEFAULT_TIMEOUT = 30  # seconds (connect + read)


class URL:
    BASE = "https://cdpj.partners.bancointer.com.br/"
    AUTH = BASE + "oauth/v2/token"
    STATEMENTS = BASE + "banking/v2/extrato"
    BALANCE = BASE + "banking/v2/saldo"
    PAYMENTS = BASE + "banking/v2/pagamento"


class Scopes:
    READ_STATEMENTS = "extrato.read"
    "Consulta de saldo e extrato"

    WRITE_PAYMENT = "pagamento-boleto.write"
    "Pagamento de títulos com código de barra"

    all = (READ_STATEMENTS, WRITE_PAYMENT)


class InterAPIError(Exception):
    """Raised when Banco Inter responds with a non-success HTTP status."""

    def __init__(self, response):
        self.response = response
        self.status_code = response.status_code
        try:
            self.payload = response.json()
        except ValueError:
            self.payload = response.text
        super().__init__(f"Banco Inter API error {self.status_code}: {self.payload}")


def _ensure_success(response):
    if response.status_code != 200:
        raise InterAPIError(response)
    return response


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

    :param scopes: Iterável contendo os :class:`Scopes` necessários,
        defaults to :class:`Scopes.all`
    :type scopes: :class:`Iterable`, optional
    """

    def __init__(
        self,
        client_id,
        client_secret,
        cert_path,
        key_path,
        account_number=None,
        scopes=None,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.cert_path = cert_path
        self.key_path = key_path
        self.account_number = account_number
        self.scopes = scopes or Scopes.all
        self._token = None

    def _get_token(self):
        response = _ensure_success(
            requests.post(
                URL.AUTH,
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "scope": " ".join(self.scopes),
                    "grant_type": "client_credentials",
                },
                cert=(self.cert_path, self.key_path),
            timeout=DEFAULT_TIMEOUT,
            )
        )
        return response.json()["access_token"]

    @property
    def token(self):
        if not self._token:
            self._token = self._get_token()
        return self._token

    @property
    def headers(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        if self.account_number:
            headers["x-conta-corrente"] = self.account_number

        return headers

    def get_balance(self, date=None):
        params = {}

        if date:
            params["dataSaldo"] = date.strftime("%Y-%m-%d")

        response = _ensure_success(
            requests.get(
                URL.BALANCE,
                params=params,
                headers=self.headers,
                cert=(self.cert_path, self.key_path),
            timeout=DEFAULT_TIMEOUT,
            )
        )
        return response.json()

    def get_statements(self, start_date, end_date):
        response = _ensure_success(
            requests.get(
                URL.STATEMENTS,
                params={
                    "dataInicio": start_date.strftime("%Y-%m-%d"),
                    "dataFim": end_date.strftime("%Y-%m-%d"),
                },
                headers=self.headers,
                cert=(self.cert_path, self.key_path),
            timeout=DEFAULT_TIMEOUT,
            )
        )
        return response.json()

    def pay_barcode(self, barcode, value, due_date, payment_date=None):
        """
        Pagamento imediato ou agendado de títulos com código de barras.

        Necessita do :class:`Scopes.WRITE_PAYMENT`.

        Referência: https://developers.bancointer.com.br/reference/pagarboleto

        :param barcode: código de barras (somente números)
        :type barcode: :class:`str`

        :param value: valor do título
        :type value: :class:`str`

        :param due_date: data de vencimento
        :type due_date: :class:`datetime.date`

        :param payment_date: data de pagamento, se não informado, será o mesmo dia.
        :type payment_date: :class:`datetime.date`, opcional

        :return: resposta da API
        :rtype: :class:`dict`
        """
        response = _ensure_success(
            requests.post(
                URL.PAYMENTS,
                json={
                    "codBarraLinhaDigitavel": barcode,
                    "valorPagar": str(value),
                    "dataVencimento": due_date.strftime("%Y-%m-%d"),
                    "dataPagamento": (
                        payment_date.strftime("%Y-%m-%d") if payment_date else None
                    ),
                },
                headers=self.headers,
                cert=(self.cert_path, self.key_path),
            timeout=DEFAULT_TIMEOUT,
            )
        )
        return response.json()
