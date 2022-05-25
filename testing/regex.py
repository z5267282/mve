import re
import sys

class Test:
    def __init__(self, description, input_data, expected):
        self.description = description
        self.input_data = input_data
        self.expected = expected
    
    def check(self, pattern):
        if bool(pattern.fullmatch(self.input_data)) != self.expected:
            print(f"failed test: {self.description}", file=sys.stderr)
            sys.exit(1)

        print(f"passed test: {self.description}")

    def test_all(tests, pattern, name):
        for t in tests:
            t.check(pattern)
        print(f'\npassed all tests in suite: {name}\n')

    def test_good_bad(name, pattern, good_tests, bad_tests):
        Test.test_all(good_tests, pattern, f'good {name}')
        Test.test_all(bad_tests, pattern, f'bad {name}')

def time_tests():
    RE_END_TIME = r'-?[0-9]+|([0-9]+-)+[0-9]+'
    pattern = re.compile(RE_END_TIME)

    good_tests = [
        Test('positive integer', '3', True),
        Test('negative integer', '-1', True),
        Test('leading 0 minute and second', '01-02', True),
        Test('no leading 0 minute and second', '1-2', True),
    ]

    bad_tests = [
        Test('trailing dash', '01-', False),
        Test('decimal points', '1.2', False),
        Test('letters', 'fish 3', False),
    ]

    Test.test_good_bad('time', pattern, good_tests, bad_tests)

def name_tests():
    RE_NAME = r'[a-zA-Z0-9 ]+'
    pattern = re.compile(RE_NAME)

    good_tests = [
        Test('good name', 'hello 123', True)
    ]

    bad_tests = [
        Test('bad name', 'hello-123', False)
    ]

    Test.test_good_bad('name', pattern, good_tests, bad_tests)

def main():
    time_tests()
    name_tests()

if __name__ == '__main__':
    main()
