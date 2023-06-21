import unittest
import math_opt
from unittest import mock
from io import StringIO
from contextlib import redirect_stdout

class Math_Operations(unittest.TestCase):
    def test_init(self):
        boo = math_opt.Math_Operations(5, 5)

    def test_add(self):
        boo = math_opt.Math_Operations(5, 5)
        ans = boo.add()
        self.assertEqual(ans, 10)

    def test_add_runtime(self):
        boo = math_opt.Math_Operations("BOO", 5)
        self.assertRaises(SystemExit, boo.add)

    def test_div_runtime(self):
        boo = math_opt.Math_Operations("BOO", 5)
        with self.assertRaises(SystemExit):
            boo.divide()

    def test_div_int_runtime(self):
        boo = math_opt.Math_Operations("BOO", 5)
        with self.assertRaises(SystemExit):
            boo.divide_ints()
    def test_sub_runtime(self):
        boo = math_opt.Math_Operations("BOO", 5)
        with self.assertRaises(SystemExit):
            boo.subtract()

    def test_sub(self):
        boo = math_opt.Math_Operations(10, 5)
        ans = boo.subtract()
        self.assertEqual(ans, 5)


    def test_mul(self):
        boo = math_opt.Math_Operations(5, 5)
        ans = boo.multiply()
        self.assertEqual(ans, 25)

    def test_div(self):
        boo = math_opt.Math_Operations(10, 2)
        ans = boo.divide_ints()
        self.assertEqual(ans, 5)

    def test_div_floats(self):
        boo = math_opt.Math_Operations(10.0, 2)
        ans = boo.divide()
        self.assertEqual(ans, 5.0)


    def test_div_zero_ints(self):
        boo = math_opt.Math_Operations(10, 0)
        with self.assertRaises(ValueError):
            boo.divide_ints()

    def test_div_zero_floats(self):
        boo = math_opt.Math_Operations(10.0, 0)
        with self.assertRaises(ValueError):
            boo.divide()


    def test_less_than_or_equal(self):
        result = math_opt.Math_Operations(3, 5).evaluate_comparison("<=")
        self.assertTrue(result)

    def test_less_than(self):
        result = math_opt.Math_Operations(3, 5).evaluate_comparison("<")
        self.assertTrue(result)

    def test_equal(self):
        result = math_opt.Math_Operations(3, 5).evaluate_comparison("=")
        self.assertFalse(result)

    def test_greater_than(self):
        result = math_opt.Math_Operations(3, 5).evaluate_comparison(">")
        self.assertFalse(result)

    def test_greater_than_or_equal(self):
        result = math_opt.Math_Operations(3, 5).evaluate_comparison(">=")
        self.assertFalse(result)

    def test_not_equal(self):
        result = math_opt.Math_Operations(3, 5).evaluate_comparison("<>")
        self.assertTrue(result)

    def test_add_string(self):
        result = math_opt.Math_Operations("boo", "man").add_string()
        self.assertEqual(result, "booman")

    def test_mult_string_val1_str(self):
        result = math_opt.Math_Operations("boo", 2).multiply_string()
        self.assertEqual(result, "booboo")

    def test_mult_string_val2_str(self):
        result = math_opt.Math_Operations(2, "boo").multiply_string()
        self.assertEqual(result, "booboo")

    def test_invalid_operator(self):
        with self.assertRaises(ValueError):
            math_opt.Math_Operations(3, 5).evaluate_comparison("%")

    def test_less_than_or_equal_wrong(self):
        with self.assertRaises(SystemExit):
            math_opt.Math_Operations("3", 5).evaluate_comparison("<=")

    def test_less_than_wrong(self):
        with self.assertRaises(SystemExit):
            math_opt.Math_Operations("3", 5).evaluate_comparison("<")


    def test_greater_than_wrong(self):
        with self.assertRaises(SystemExit):
            math_opt.Math_Operations("3", 5).evaluate_comparison(">")

    def test_greater_than_or_equal_wrong(self):
        with self.assertRaises(SystemExit):
            math_opt.Math_Operations("3", 5).evaluate_comparison(">=")


if __name__ == '__main__':
    unittest.main()

