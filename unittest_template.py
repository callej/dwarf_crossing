import unittest
import fibonacci

# For info see: https://docs.python.org/3/library/unittest.html


def setUpModule():
    print(f'Run before any test in this module')

def tearDownModule():
    print(f'Run after last test in this module')


class TestFibGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print(f'Run before the first test in this class (TestFibGenerator) is run')

    @classmethod
    def tearDownClass(cls) -> None:
        print(f'Run after the last test in this class (TestFibGenerator) is run')

    def setUp(self) -> None:
        print(f'Run before each test in TestFibGenerator')

    def tearDown(self) -> None:
        print(f'Run after each test in TestFibGenerator')

    def test_case1(self):
        self.assertEqual(list(fibonacci.fibonacci_gen(-1)), [], "Should be []")  # add assertion here

    def test_case2(self):
        self.assertEqual(list(fibonacci.fibonacci_gen(0)), [])  # add assertion here

    def test_case3(self):
        self.assertEqual(list(fibonacci.fibonacci_gen(1)), [1])  # add assertion here

    def test_case4(self):
        self.assertEqual(list(fibonacci.fibonacci_gen(2)), [1, 1])  # add assertion here

    def test_case5(self):
        self.assertEqual(list(fibonacci.fibonacci_gen(3)), [1, 1, 2])  # add assertion here

    def test_case6(self):
        self.assertEqual(list(fibonacci.fibonacci_gen(4)), [1, 1, 2, 3])  # add assertion here

    def test_case7(self):
        self.assertEqual(list(fibonacci.fibonacci_gen(5)), [1, 1, 2, 3, 5])  # add assertion here

    def test_case8(self):
        self.assertEqual(list(fibonacci.fibonacci_gen(10)), [1, 1, 2, 3, 5, 8, 13, 21, 34, 55])  # add assertion here


class MoreTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print(f'Run before the first test in this class (MoreTests) is run')

    @classmethod
    def tearDownClass(cls) -> None:
        print(f'Run after the last test in this class (MoreTests) is run')

    def setUp(self) -> None:
        print(f'Run before each test in MoreTests')

    def tearDown(self) -> None:
        print(f'Run after each test in MoreTests')

    def test_case1(self):
        self.assertEqual(list(fibonacci.fibonacci_gen(6)), [1, 1, 2, 3, 5, 8])  # add assertion here

    def test_case2(self):
        self.assertEqual(list(fibonacci.fibonacci_gen(7)), [1, 1, 2, 3, 5, 8, 13])  # add assertion here

    def test_case3(self):
        self.assertEqual(list(fibonacci.fibonacci_gen(8)), [1, 1, 2, 3, 5, 8, 13, 21])  # add assertion here


class TestFibN(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print(f'Run before the first test in this class (TestFibN) is run')

    @classmethod
    def tearDownClass(cls) -> None:
        print(f'Run after the last test in this class (TestFibN) is run')

    def setUp(self) -> None:
        print(f'Run before each test in TestFibN')

    def tearDown(self) -> None:
        print(f'Run after each test in TestFibN')

    def test_case1(self):
        self.assertEqual(fibonacci.fib_n(0), None)  # add assertion here

    def test_case2(self):
        self.assertEqual(fibonacci.fib_n(1), 1)  # add assertion here

    def test_case3(self):
        self.assertEqual(fibonacci.fib_n(2), 1)  # add assertion here

    def test_case4(self):
        self.assertEqual(fibonacci.fib_n(3), 2)  # add assertion here

    def test_case5(self):
        self.assertEqual(fibonacci.fib_n(25), 75025)  # add assertion here


if __name__ == '__main__':
    unittest.main()
