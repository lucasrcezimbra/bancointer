# Banco Inter


[![PyPI](https://img.shields.io/pypi/v/bancointer.svg)](https://pypi.python.org/pypi/bancointer)
[![Coverage Status](https://coveralls.io/repos/github/lucasrcezimbra/bancointer/badge.svg?branch=master)](https://coveralls.io/github/lucasrcezimbra/bancointer?branch=master)
[![Documentation Status](https://readthedocs.org/projects/bancointer/badge/?version=latest)](https://bancointer.readthedocs.io/en/latest/?version=latest)

Client to consume Banco Inter APIs

* Documentation: https://bancointer.readthedocs.io.


## Installation

```bash
pip install bancointer
```


## How to Use

```python
from datetime import date

from inter import Inter


inter = Inter(
    "YOUR_CLIENT_ID",
    "YOUR_CLIENT_SECRET"
    '/path/to/certificado.crt',
    '/path/to/chave.key',
)

# get September/2022 statements
inter.get_statements(date(2022, 9, 1), date(2022, 9, 30))
```




## Contributing

Contributions are welcome, feel free to open an Issue or Pull Request.

Pull requests must be for the `develop` branch.

```
git clone https://github.com/lucasrcezimbra/bancointer
cd bancointer
git checkout develop
python -m venv .venv
source .venv/bin/activate
pip install .[test]
pre-commit install
pytest
```
