import unittest

from sd1 import get_4d


class Tests(unittest.TestCase):

    def test_open_m(self):
        with self.assertRaises(SyntaxError):
            get_4d("cell a+~v+2/1)^(2+asd)")

    def test_close_m(self):
        with self.assertRaises(SyntaxError):
            get_4d("cell a+~(v+2/1^(2+asd)")

    def test_cell_const(self):
        with self.assertRaises(SyntaxError):
            get_4d("cell 1+~(v+2/1^(2+asd)")

    def test_const_with_letters(self):
        with self.assertRaises(SyntaxError):
            get_4d("1asd+2")

    def test_cell_op(self):
        with self.assertRaises(SyntaxError):
            get_4d("cell+2")

    def test_ok(self):
        x = get_4d("cell a+~(v+2/1)^(2+asd)")
        self.assertEqual(x, [(0, 'cell', 'a', '', '$0'),
                             (1, '/', '1', '2', '$1'),
                             (2, '+', '$1', 'v', '$2'),
                             (3, '~', '$2', '', '$3'),
                             (4, '+', 'asd', '2', '$4'),
                             (5, '^', '$4', '$3', '$5'),
                             (6, '+', '$5', '$0', '$6')])


if __name__ == '__main__':
    unittest.main()