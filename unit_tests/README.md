# Section A: `unittest`

## Introduction to `unittest`
`unittest` is Python's built-in testing framework. It provides a test discovery mechanism and test execution framework, making it a powerful choice for writing unit tests.

## Key Concepts

### Test Case
A test case is the individual unit of testing in `unittest`. You create test cases by subclassing `unittest.TestCase`. Each test case is responsible for testing a specific aspect of your code.

### Test Fixture
A test fixture is the preparation needed to run a test case. You can set up fixtures using methods like `setUp()` and `tearDown()`. These methods are called before and after each test method in a test case.

### Test Method
A test method is a method within a test case that performs a specific test. Test method names must start with the word "test."

### Test Runner
A test runner is responsible for discovering and running test cases. You can use the `unittest.TextTestRunner` or other custom runners to execute your tests.

## Writing Tests
1. Import the `unittest` module.
2. Create a test case class by subclassing `unittest.TestCase`.
3. Write test methods within the test case class.
4. Use various assertion methods (e.g., `assertEqual`, `assertTrue`, `assertRaises`) to check expected outcomes.
5. Use fixtures like `setUp` and `tearDown` to set up and tear down resources needed for your tests.

## Running Tests
To run `unittest` tests, you can use the command line or an IDE with built-in test runners. Common CLI commands include:
- `python -m unittest test_module` to run all tests in a module.
        
    - In our example this would be `python -m unittest unit_tests/test_item.py` or
    - `python -m unittest unit_tests.test_item`
    
- `python -m unittest test_module.TestClass` to run all tests in a specific test class.

    - An example in our case would be `python -m unittest unit_tests.test_item_repository.TestItemRepository`
    
- `python -m unittest test_module.TestClass.test_method` to run a specific test method.