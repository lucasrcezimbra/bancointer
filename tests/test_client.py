from uuid import uuid4

import pytest
import responses
from responses import matchers

from inter import Client, InterAPIError, Scopes
from inter._client import URL


@pytest.fixture
def client(faker):
    client_id, client_secret = faker.pystr(), faker.pystr()
    cert_path, key_path = faker.file_path(), faker.file_path()
    return Client(client_id, client_secret, cert_path, key_path)


def test_init(faker):
    client_id, client_secret = faker.pystr(), faker.pystr()
    cert_path, key_path = faker.file_path(), faker.file_path()

    client = Client(client_id, client_secret, cert_path, key_path)

    assert client.client_id == client_id
    assert client.client_secret == client_secret
    assert client.cert_path == cert_path
    assert client.key_path == key_path
    assert client.scopes == Scopes.all


def test_init_with_scopes(faker):
    scopes = [Scopes.READ_STATEMENTS]

    client = Client(
        client_id=faker.pystr(),
        client_secret=faker.pystr(),
        cert_path=faker.file_path(),
        key_path=faker.file_path(),
        scopes=scopes,
    )

    assert client.scopes == scopes


@responses.activate
def test_token(client):
    token = str(uuid4())

    responses.post(
        URL.AUTH,
        json={
            "access_token": token,
            "token_type": "Bearer",
            "expires_in": 3600,
            "scope": "extrato.read",
        },
        status=200,
        match=[
            matchers.urlencoded_params_matcher(
                {
                    "client_id": client.client_id,
                    "client_secret": client.client_secret,
                    "scope": "extrato.read pagamento-boleto.write",
                    "grant_type": "client_credentials",
                }
            ),
            matchers.request_kwargs_matcher(
                {"cert": (client.cert_path, client.key_path)}
            ),
        ],
    )

    assert client.token == token


def test_cached_token(client):
    token = str(uuid4())

    client._token = token

    assert client.token == token


def test_headers(client):
    token = str(uuid4())

    client._token = token

    assert client.headers == {"Authorization": f"Bearer {client.token}"}


def test_headers_account_number(client):
    token = str(uuid4())

    client._token = token
    client.account_number = "12321"

    assert client.headers == {
        "Authorization": f"Bearer {client.token}",
        "x-conta-corrente": "12321",
    }


@responses.activate
def test_get_statements(faker, client, statements_data):
    client._token = uuid4()
    start, end = faker.past_date(), faker.past_date()

    responses.get(
        URL.STATEMENTS,
        json=statements_data,
        status=200,
        match=[
            matchers.query_param_matcher(
                {
                    "dataInicio": start.strftime("%Y-%m-%d"),
                    "dataFim": end.strftime("%Y-%m-%d"),
                }
            ),
            matchers.header_matcher(client.headers),
            matchers.request_kwargs_matcher(
                {"cert": (client.cert_path, client.key_path)}
            ),
        ],
    )

    assert client.get_statements(start, end) == statements_data


@responses.activate
def test_get_balance(faker, client, balance_data):
    client._token = uuid4()

    responses.get(
        URL.BALANCE,
        json=balance_data,
        status=200,
        match=[
            matchers.header_matcher(client.headers),
            matchers.request_kwargs_matcher(
                {"cert": (client.cert_path, client.key_path)}
            ),
        ],
    )

    assert client.get_balance() == balance_data


@responses.activate
def test_get_balance_with_date(faker, client, balance_data):
    client._token = uuid4()
    date = faker.past_date()

    responses.get(
        URL.BALANCE,
        json=balance_data,
        status=200,
        match=[
            matchers.query_param_matcher({"dataSaldo": date.strftime("%Y-%m-%d")}),
            matchers.header_matcher(client.headers),
            matchers.request_kwargs_matcher(
                {"cert": (client.cert_path, client.key_path)}
            ),
        ],
    )

    assert client.get_balance(date) == balance_data


@responses.activate
def test_pay_barcode(faker, client, pay_barcode_data):
    client._token = uuid4()
    barcode, value, due_date = "01234", faker.pydecimal(), faker.future_date()

    responses.post(
        URL.PAYMENTS,
        json=pay_barcode_data,
        status=200,
        match=[
            matchers.json_params_matcher(
                {
                    "codBarraLinhaDigitavel": barcode,
                    "valorPagar": str(value),
                    "dataVencimento": due_date.strftime("%Y-%m-%d"),
                    "dataPagamento": None,
                }
            ),
            matchers.header_matcher(client.headers),
            matchers.request_kwargs_matcher(
                {"cert": (client.cert_path, client.key_path)}
            ),
        ],
    )

    assert client.pay_barcode(barcode, value, due_date) == pay_barcode_data


@responses.activate
def test_pay_barcode_future(faker, client, pay_barcode_data):
    client._token = uuid4()
    barcode, value = "01234", faker.pydecimal()
    due_date, payment_date = faker.future_date(), faker.future_date()

    responses.post(
        URL.PAYMENTS,
        json=pay_barcode_data,
        status=200,
        match=[
            matchers.json_params_matcher(
                {
                    "codBarraLinhaDigitavel": barcode,
                    "valorPagar": str(value),
                    "dataVencimento": due_date.strftime("%Y-%m-%d"),
                    "dataPagamento": payment_date.strftime("%Y-%m-%d"),
                }
            ),
            matchers.header_matcher(client.headers),
            matchers.request_kwargs_matcher(
                {"cert": (client.cert_path, client.key_path)}
            ),
        ],
    )

    assert (
        client.pay_barcode(barcode, value, due_date, payment_date) == pay_barcode_data
    )


@responses.activate
def test_get_balance_raises_on_non_200(client):
    client._token = uuid4()

    responses.get(
        URL.BALANCE,
        json={"title": "Unauthorized", "detail": "invalid token"},
        status=401,
    )

    with pytest.raises(InterAPIError) as exc:
        client.get_balance()

    assert exc.value.status_code == 401
    assert exc.value.payload["detail"] == "invalid token"


@responses.activate
def test_token_raises_on_non_200(client):
    responses.post(
        URL.AUTH,
        json={"error": "invalid_client"},
        status=400,
    )

    with pytest.raises(InterAPIError) as exc:
        _ = client.token

    assert exc.value.status_code == 400


def test_raises_on_redirect(mocker, client, mock_token):
    response = mocker.Mock()
    response.status_code = 302
    response.json.side_effect = ValueError("no json")
    response.text = "redirect"
    mocker.patch("inter._client.requests.get", return_value=response)
    with pytest.raises(InterAPIError) as exc:
        client.get_balance()
    assert exc.value.status_code == 302
    assert exc.value.payload == "redirect"
