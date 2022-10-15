from uuid import uuid4

import pytest
import responses
from responses import matchers

from inter import URL, Inter


@pytest.fixture
def inter(faker):
    client_id, client_secret = faker.pystr(), faker.pystr()
    cert_path, key_path = faker.file_path(), faker.file_path()
    return Inter(client_id, client_secret, cert_path, key_path)


def test_init(faker):
    client_id, client_secret = faker.pystr(), faker.pystr()
    cert_path, key_path = faker.file_path(), faker.file_path()

    inter = Inter(client_id, client_secret, cert_path, key_path)

    assert inter.client_id == client_id
    assert inter.client_secret == client_secret
    assert inter.cert_path == cert_path
    assert inter.key_path == key_path


@responses.activate
def test_token(inter):
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
                    'client_id': inter.client_id,
                    'client_secret': inter.client_secret,
                    'scope': 'extrato.read',
                    'grant_type': 'client_credentials',
                }
            ),
            matchers.request_kwargs_matcher({'cert': (inter.cert_path, inter.key_path)})
        ],
    )

    assert inter.token == token


def test_cached_token(inter):
    token = str(uuid4())

    inter._token = token

    assert inter.token == token
