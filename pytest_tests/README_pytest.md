# Section B: `pytest`

## Introduction to `pytest`
`pytest` is a popular third-party testing framework for Python. It simplifies test writing and execution, providing rich features and a clean syntax.

## Key Concepts

### Test Functions
In `pytest`, test functions are regular Python functions that you mark as tests using the `@pytest.mark` decorator. Test functions do not need to be part of a test case class.

### Test Discovery
`pytest` automatically discovers and runs test functions based on naming conventions and markers. Test files should be named with the `test_` prefix.

### Assertions
`pytest` uses Python's native `assert` statements for assertions. This means you can use any assert statement, and `pytest` will report the result.

### Fixtures
Fixtures are reusable setup code that can be shared across multiple test functions. They are defined using the `@pytest.fixture` decorator.

### Plugins
`pytest` supports a wide range of plugins that extend its functionality, such as test parametrization, coverage reporting, and more.

## Writing Tests
1. Import the `pytest` module.
2. Write test functions and use the `@pytest.mark` decorator to mark them as tests.
3. Use standard Python `assert` statements for assertions.

## Running Tests
To run `pytest` tests, simply use the `pytest` command followed by the test file or directory. Common commands include:
- `pytest` to discover and run all tests in the current directory and subdirectories.
- `pytest test_file.py` to run tests in a specific file.
- `pytest -k test_name` to run tests with a specific name.
