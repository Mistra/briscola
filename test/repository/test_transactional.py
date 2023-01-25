
import unittest

from src.repository.transaction import transactional


class TestTransactional(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_decorator(self):
        tmp = self.callable1()

    @transactional
    def callable1(self) -> int:
        return 1

    @transactional
    def callable2(self) -> int:
        return 2
