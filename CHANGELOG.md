# Changelog

## Unreleased
- Switch from Coveralls to Codecov for coverage reporting [#23](https://github.com/lucasrcezimbra/bancointer/issues/23)

## 0.1.0 (2023-01-09)
- Add support to multiple accounts through the x-conta-corrente header [#26](https://github.com/lucasrcezimbra/bancointer/pull/26). Thanks @jeanwainer


## 0.0.9 (2023-08-28)
- Unpin dependencies
- Fix pre-commit hooks


## 0.0.8 (2022-12-14)
- Fix barcode payment


## 0.0.7 (2022-11-18)
- Add barcode payment [#14](https://github.com/lucasrcezimbra/bancointer/issues/14)
  * `Inter.pay_barcode` and `Client.pay_barcode`
- Add Scopes
- Fix pre-commit
- Reorganize docs


## 0.0.6 (2022-10-25)
- Improve `Inter.__init__`
- Fix tests


## 0.0.5 (2022-10-24)
- Add fake classes for testing


## 0.0.4 (2022-10-23)
- Add High Level API
- Fix Read the Docs
- Fix Coveralls


## 0.0.3 (2022-10-15)
- Add Inter.get_balance
- Improve docs


## 0.0.2 (2022-10-15)
- Fix build


## 0.0.1 (2022-10-15)
- First PyPI version
    * authentication and get_statements
