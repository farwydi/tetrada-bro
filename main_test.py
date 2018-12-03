import unittest

from poliz import poliz
from sd1 import get_4d
from trans import to_trans


class Tests(unittest.TestCase):

    def test_ez_func(self):
        x, _, _ = to_trans(poliz(get_4d("f{1,h}")))
        self.assertEqual(x[:-1], [(0, 'push', '1', '', ''),
                                  (1, 'push', 'h', '', ''),
                                  (2, 'argx', 2, '', ''),
                                  (3, 'call', 'f', '', '$0')])


if __name__ == '__main__':
    unittest.main()
