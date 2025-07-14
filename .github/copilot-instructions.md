# GitHub Copilot Instructions for bancointer

This file provides GitHub Copilot with repository-specific guidelines, code conventions, and best practices for the `bancointer` project - a Python client library for consuming Banco Inter APIs.

## Repository Overview

### Architecture
- **Two-tier API design**: High-level `Inter` class and low-level `Client` class
- **Data models**: `Operation` and `Payment` classes for bank transaction data
- **Testing utilities**: Fake implementations provided in `inter.testing` module
- **Domain**: Brazilian banking APIs with OAuth2 authentication and certificate-based security

### Core Components
- `inter._client.Client`: Low-level HTTP client for Banco Inter APIs
- `inter._inter.Inter`: High-level interface with convenience methods
- `inter._inter.Operation`: Bank transaction/statement data model
- `inter._inter.Payment`: Payment transaction data model
- `inter.testing`: Testing utilities with fake implementations

## Code Conventions

### Python Style
- **Line length**: 99 characters (configured in `.flake8`)
- **Formatter**: Black (configured in pre-commit hooks)
- **Linter**: Ruff (configured in pre-commit hooks)
- **Import style**: Explicit imports with `# noqa` comments when needed
- **Python versions**: Support 3.7+ (see `pyproject.toml`)

### Class Design
- Use `attrs.define` decorator for data classes (e.g., `Operation`, `Payment`)
- Use regular classes for service/client classes
- Define constants as class attributes in `ALL_CAPS`
- Group related constants in classes (e.g., `Scopes`, `URL`)

### Documentation
- **Docstring style**: Sphinx format with detailed parameter documentation
- **Type annotations**: Use only for attrs fields.
- **Parameter documentation**: Include `:param name:`, `:type name:`, `:return:`, `:rtype:`
- **Language**: Mix of English and Portuguese (Portuguese for banking domain terms)

### Example class structure:
```python
@define
class DataModel:
    """Brief description.

    :param field: Description
    :type field: Type
    """
    field: Type
    "Field description"

class ServiceClass:
    """
    Service description.

    :param param: Parameter description
    :type param: Type
    """

    def method(self, param: Type) -> ReturnType:
        """
        Method description.

        :param param: Parameter description
        :type param: Type
        :return: Return description
        :rtype: ReturnType
        """
```

## Testing Standards

### Framework and Tools
- **Test framework**: pytest with additional plugins (faker, mock, responses)
- **Fake implementations**: Use classes from `inter.testing` for mocking
- **Test data**: Use `faker` library for generating realistic test data
- **HTTP mocking**: Use `responses` library for API call mocking

### Test Structure
- Tests are organized in `tests/` directory
- One test file per main module: `test_client.py`, `test_inter.py`, etc.
- Use descriptive test function names: `test_<action>_<expected_result>`
- Fixtures are defined in `conftest.py`

### Testing Patterns
```python
# Use fake implementations for integration-style tests
def test_with_fake_client():
    client = ClientFake()
    inter = Inter(client=client)
    result = inter.get_balance()
    assert result == client.balance

# Use mocking for unit tests
def test_with_mocking(mocker):
    client_mock = mocker.patch("inter._inter.Client", autospec=True)
    # test implementation
```

## Development Workflow

### Pre-commit Setup
```bash
git clone https://github.com/lucasrcezimbra/bancointer
cd bancointer
git checkout develop
python -m venv .venv
source .venv/bin/activate
pip install .[test]
pre-commit install
pytest
```

### Code Quality Tools
- **Black**: Code formatting (automatically applied)
- **Ruff**: Linting and code analysis
- **Pre-commit**: Runs hooks for code quality checks
- **Coverage**: Test coverage measurement

## Banking Domain Guidelines

### Security Considerations
- **Never commit**: API credentials, certificates, or private keys
- **Authentication**: Uses OAuth2 with client credentials and mTLS certificates
- **Sensitive data**: Handle financial data with appropriate care
- **Testing**: Use fake data generators, never real banking data

### Banking Terminology
- `extrato`: Bank statement
- `saldo`: Account balance
- `pagamento`: Payment
- `boleto`: Brazilian payment slip/bill
- `codigo de barras`: Barcode (for bill payments)

### API Scopes
- `extrato.read`: Read statements and balance
- `pagamento-boleto.write`: Payment of bills with barcode

## Preferred Libraries and Dependencies

### Core Dependencies
- `attrs`: For data classes (use `@define` decorator)
- `requests`: For HTTP client functionality

### Development Dependencies
- `pytest`: Testing framework
- `faker`: Test data generation
- `responses`: HTTP response mocking
- `pre-commit`: Code quality automation

## Error Handling

### Patterns
- Use appropriate exception types for domain-specific errors
- Validate input parameters early in methods
- Provide clear error messages with context

## Contribution Guidelines

### Code Changes
- Make minimal, focused changes
- Ensure all tests pass before submitting PR
- Update documentation if adding new features
- Follow existing code patterns and conventions

### New Features
- Add comprehensive tests for new functionality
- Update relevant documentation
- Consider both high-level (`Inter`) and low-level (`Client`) APIs
- Provide fake implementations in `inter.testing` if applicable

### API Design
- Maintain backward compatibility when possible
- Use clear, descriptive method names
- Follow Python naming conventions (`snake_case`)
- Return appropriate data types (use data classes for structured data)

## Common Patterns

### Date Handling
```python
from datetime import date
# Use date objects for API parameters
start_date = date(2022, 9, 1)
end_date = date(2022, 9, 30)
```

### Data Class Creation
```python
@define
class BankData:
    amount: Decimal
    description: str
    date: date

    @classmethod
    def from_data(cls, data: dict):
        """Create instance from API response data."""
        return cls(
            amount=Decimal(data['valor']),
            description=data['descricao'],
            date=data['data']
        )
```

### Client Method Pattern
```python
def api_method(self, param: Type) -> ReturnType:
    """
    Method description.

    :param param: Parameter description
    :type param: Type
    :return: Return description
    :rtype: ReturnType
    """
    # Implementation with proper error handling
    response = self._client.make_request(param)
    return self._process_response(response)
```

When suggesting code, prioritize maintainability, security, and consistency with existing patterns.
