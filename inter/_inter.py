from inter._client import Client


class Inter:
    def __init__(self, client):
        self._client = client

    @classmethod
    def from_credentials(cls, client_id, client_secret, cert_path, key_path):
        return cls(client=Client(client_id, client_secret, cert_path, key_path))
