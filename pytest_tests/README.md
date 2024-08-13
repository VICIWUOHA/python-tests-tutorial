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
Note: depending on the setup of your PYTHONPATH/IDE, you may get a no module names src error
to run these tests from your terminal, add `python -m` before all your commands below.
or better stil configure your IDE setup to allow such imports fromm src/

To run `pytest` tests, simply use the `pytest` command followed by the test file or directory. Common commands include:
- `pytest` to discover and run all tests in the current directory and subdirectories.
- `python -m pytest test_file.py` to run tests in a specific file.
- `pytest -k test_name` to run tests with a specific name/pattern.

Another beautiful use case of pytest is that it can also be used to run your unit test cases using the same commands above.

To see stdout messages in a verbose manner. In this case for our tests in /pytest_tests use ;
- `python -m pytest_tests -s -vvv`

running with -s alone gives you just log/prints to stdout.


#### OPTIONAL TESTS/ ENHANCEMENTS YOU CAN IMPLEMENT

1) Implement the skipped test - `test_reduce_nonexistent_item_from_cart`
2) Write a test that would fail if we try to add a -ve quantity to the cart.
Let's see What happens if we try to add an item with negative quantity to the cart? You can Modify the ShoppingCart.add_item code to handle that, also build a test for it.
3) Think of any other cases that may break if the code logic changes
4) We can also move the redundant add_item action in most test cases to our shopping cart fixture in [pytest_tests/conftest.py](https://github.com/VICIWUOHA/python-tests-tutorial/tree/main/pytest_tests/conftest.py)
5) The list goes on...


_Want more details ?? visit the [Offical pytest docs](https://docs.pytest.org/en/stable/contents.html)_.