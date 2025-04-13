# Donate-a-pytest

A pytest extension for sharing test cases.

## Installation

```bash
pip install donate-a-pytest
```

## Usage

### Donating Tests

To donate test cases for a function, use the `register_for_donation` decorator:

```python
from donate_a_pytest.decorators import register_for_donation

@register_for_donation
def my_function(param1, param2):
    # Your function implementation
    return result
```

This decorator does two things:
1. It returns the original function so it can be used normally
2. It creates a test function named `test_my_function` that will be collected by pytest

The test function will automatically run all test cases found for `my_function`.

### Supported Output Types

The framework supports any output type, not just dictionaries. You can return:

- Basic types (int, float, str, bool)
- Collections (lists, tuples, dictionaries)
- None values
- Any other serializable type

Here's an example with different return types:

```python
@register_for_donation
def process_data(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a + b  # Returns an integer
    elif isinstance(a, str) and isinstance(b, str):
        return a + " " + b  # Returns a string
    elif isinstance(a, list) and isinstance(b, list):
        return a + b  # Returns a list
    elif isinstance(a, dict) and isinstance(b, dict):
        return {**a, **b}  # Returns a dictionary
    return None  # Returns None
```

### Running Donated Tests

You can run all tests marked with the `donate` marker using the provided CLI:

```bash
# Run all donated tests in the current directory
donate-pytest

# Run with verbose output
donate-pytest -v

# Specify a directory to search for tests
donate-pytest -d path/to/tests

# Stop on first failure
donate-pytest -f
```

### Programmatic Usage

You can also run the tests programmatically:

```python
from donate_a_pytest import run_donated_tests

results = run_donated_tests(
    directory="path/to/tests",
    verbose=True,
    output_format="summary",
    failfast=False
)
print(f"Tests {'passed' if results['success'] else 'failed'}")
```

## Test Case Format

Test cases are stored in JSON or YAML files that match the function name. Each test case should include:

- `input`: A dictionary of input parameters for the function
- `output`: The expected output from the function (can be any type)
- `description` (optional): A description of the test case

Example JSON:
```json
[
  {
    "input": {"param1": "value1", "param2": 42},
    "output": "expected result",
    "description": "Test with string and integer parameters"
  },
  {
    "input": {"a": 1, "b": 2},
    "output": 3,
    "description": "Returns an integer"
  },
  {
    "input": {"a": [1, 2], "b": [3, 4]},
    "output": [1, 2, 3, 4],
    "description": "Returns a list"
  }
]
```

Example YAML:
```yaml
- input:
    param1: value1
    param2: 42
  output: expected result
  description: Test with string and integer parameters

- input:
    a: 1
    b: 2
  output: 3
  description: Returns an integer
```

## Contributing

### Running Tests

Before submitting a pull request or requesting changes, please ensure all unit tests pass. This helps maintain code quality and prevents regressions.

To run the tests:

```bash
# Run all tests
pytest

# Run only tests related to donated tests
pytest -m donate

# Run with coverage report
pytest --cov=donate_a_pytest

# Run a specific test file
pytest tests/test_decorator.py
```

The test suite includes:
- Unit tests for core functionality
- Integration tests for the decorators
- Tests for different output types
- Tests for CLI functionality

If you're adding new features, please include appropriate tests. The test coverage should remain above 90%.

### Continuous Integration

This project uses GitHub Actions for continuous integration. Every push and pull request triggers:

1. **Pre-commit checks** - Ensures code quality using the pre-commit hooks
2. **Tests** - Runs the test suite on multiple Python versions (3.8, 3.9, 3.10, 3.11)

You can see the CI workflow configuration in `.github/workflows/python-tests.yml`.

To run the same checks locally before committing:

```bash
# Install pre-commit hooks
pre-commit install

# Run pre-commit checks manually
pre-commit run --all-files
```

### Test Data

When working with test data, you can add examples to the `tests/test_data` directory. This helps verify that your changes work correctly with different types of inputs and outputs.

## License

[MIT License](LICENSE)
