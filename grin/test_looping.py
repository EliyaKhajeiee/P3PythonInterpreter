import contextlib
import unittest
import looping
import grin
import io
import sys
from unittest import mock

class LoopingStuffTestCase(unittest.TestCase):

    def test_init(self):
        loop = looping.Loop_de_loop()
        self.assertEqual(loop.tokens, [])

    def test_dot_statement(self):
        with mock.patch('builtins.input', return_value="."):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new=output):
                    loop.while_loop()
                    loop.print_values()
                self.assertEqual(output.getvalue(), "")

    def test_let_statement(self):
        inputs = ["LET A 5", "LET B A", "PRINT A", "PRINT B", "."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "5\n5\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_let_without_defining(self):
        inputs = ["LET B C", "PRINT B", "."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "0\n"
                self.assertEqual(output.getvalue(), expected_output)
    def test_add_statement(self):
        inputs = ["LET A 5", "LET B A", "ADD A B", "PRINT A", "."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "10\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_sub_statement(self):
        inputs = ["LET A 5", "LET B A", "SUB A B", "PRINT A", "."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "0\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_mult_statement(self):
        inputs = ["LET A 5", "LET B A", "MULT A B", "PRINT A", "."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "25\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_div_statement_normal_ints(self):
        inputs = ["LET A 5", "LET B A", "DIV A B", "PRINT A", "."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "1\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_div_statements_normal_ints_odd_numbers(self):
        inputs = ["LET A 5", "LET B 2", "DIV A B", "PRINT A", "."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "2\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_div_statement_zero(self):
        inputs = ["LET A 5", "LET B A", "DIV A C", "PRINT A", "."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    with self.assertRaises(ValueError) as cm:
                        loop.while_loop()
                    self.assertEqual(str(cm.exception), "Division by zero is not allowed")

    def test_div_statement_floats(self):
        inputs = ["LET A 5.5", "LET B 2", "DIV A B", "PRINT A", "."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "2.75\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_INNUM_normal_ints(self):
        inputs = ["LET A 5", "INNUM A", "PRINT A",".","3"]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "3\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_INNUM_normal_floats(self):
        inputs = ["INNUM A", "PRINT A",".","3.14"]
        with mock.patch('builtins.input', side_effect=inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new=output):
                    loop.while_loop()
                expected_output = "3.14\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_INSTR_normal_str(self):
        inputs = ['INSTR HI',"PRINT HI",".","HI"]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "HI\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_print_int_and_float(self):
        inputs = ["PRINT 15", "PRINT 15.0","."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "15\n15.0\n"
                self.assertEqual(output.getvalue(), expected_output)
    def test_print_values(self):
        inputs = ["LET A 5","INNUM A", "PRINT B","PRINT A",".","6"]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "0\n6\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_go_to_zero_val(self):
        inputs = ["GOTO 0", "INNUM A", "PRINT B", "."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    with self.assertRaises(SystemExit):
                        loop.while_loop()
                    expected_output = "You can't GOTO 0\n"
                    self.assertEqual(output.getvalue(), expected_output)

    def test_go_to_normal(self):
        inputs = ["GOTO 2", "PRINT 5", "PRINT 6","."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "6\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_is_float(self):
        loop = looping.Loop_de_loop()
        result = loop.is_float("3.14")
        self.assertTrue(result)

    def test_is_not_float(self):
        loop = looping.Loop_de_loop()
        result = loop.is_float("ABC")
        self.assertFalse(result)

    def test_one_goto(self):
        inputs = ["GOTO 2 IF 1 = 1", "PRINT 5", "PRINT 6","."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "6\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_one_goto_with_literals(self):
        inputs = ["GOTO 2 IF A = B", "PRINT 5", "PRINT 6","."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "6\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_one_goto_with_literals_given(self):
        inputs = ["LET A 3","LET B 3","GOTO 2 IF A = B", "PRINT 5", "PRINT 6","."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "6\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_one_goto_with_strings(self):
        inputs = ['GOTO 2 IF "Boo" = "Boo"', "PRINT 5", "PRINT 6", "."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "6\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_one_goto_with_strings_FAIL(self):
        inputs = ['GOTO 2 IF "BooNO" = "Boo"', "PRINT 5", "PRINT 6", "."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "5\n6\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_goto_too_many_lines(self):
        inputs = ['GOTO 15 IF "Boo" = "Boo"', "PRINT 5", "PRINT 6", "."]
        with mock.patch('builtins.input', side_effect=inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new=output):
                    with self.assertRaises(SystemExit) as cm:
                        loop.while_loop()
                self.assertEqual(cm.exception.code, None)
    def test_simple_gosub(self):
        inputs = ['GOSUB 4 IF A <> 2', "PRINT 5", "PRINT 6", "END","PRINT 7","RETURN","."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "7\n5\n6\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_goto_label(self):
        inputs = ['GOTO "C"', "PRINT 5", "PRINT 6", "END","C: PRINT 7","."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "7\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_goto_label_iden(self):
        inputs = ['LET A "C"','GOTO A', "PRINT 5", "PRINT 6", "END","C: PRINT 7","."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "7\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_goto_label_iden_not_found(self):
        inputs = ['LET A "C"','GOTO A', "PRINT 5", "PRINT 6", "END","D: PRINT 7","."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with self.assertRaises(SystemExit):
                loop.while_loop()
    def test_goto_label_iden_int(self):
        inputs = ['LET A 4','GOTO A', "PRINT 5", "PRINT 6", "END","PRINT 7","."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "7\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_goto_zero(self):
        inputs = ['GOTO 0 IF "Boo" = "Boo"', "PRINT 5", "PRINT 6", "."]
        with mock.patch('builtins.input', side_effect=inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new=output):
                    with self.assertRaises(SystemExit) as cm:
                        loop.while_loop()
                self.assertEqual(cm.exception.code, None)

    def test_goto_zero_literal(self):
        inputs = ['LET A 0','GOTO A', "PRINT 5", "PRINT 6", "."]
        with mock.patch('builtins.input', side_effect=inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new=output):
                    with self.assertRaises(SystemExit) as cm:
                        loop.while_loop()
                self.assertEqual(cm.exception.code, None)

    def test_goto_too_many_lines_int(self):
        inputs = ['LET A 12','GOTO A', "PRINT 5", "PRINT 6", "."]
        with mock.patch('builtins.input', side_effect=inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new=output):
                    with self.assertRaises(SystemExit) as cm:
                        loop.while_loop()
                self.assertEqual(cm.exception.code, None)

    def test_goto_label_but_none(self):
        inputs = ['GOTO "A"', "PRINT 7", "."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with self.assertRaises(SystemExit):
                loop.while_loop()

    def test_add_one_int_no_var_found(self):
        inputs = ['ADD A 7', "PRINT A","."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "7\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_add_one_int_one_var_found(self):
        inputs = ['LET A 3','ADD A 7', "PRINT A","."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "10\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_add_one_int_two_var_found(self):
        inputs = ['LET B 4','LET A 3', 'ADD A B', "PRINT A", "."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "7\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_add_no_int_no_var_found(self):
        inputs = ['ADD A B', "PRINT A", "."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "0\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_add_strings_1_var_first(self):
        inputs = ['LET A "BOO"','ADD A "Boo"', "PRINT A", "."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "BOOBoo\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_add_strings_1_var_second(self):
        inputs = ['ADD A "Boo"', "PRINT A", "."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with self.assertRaises(SystemExit):
                loop.while_loop()

    def test_mult_one_int_no_var_found(self):
        inputs = ['MULT A 7', "PRINT A","."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "0\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_mult_one_int_one_var_found(self):
        inputs = ['LET A 3','MULT A 7', "PRINT A","."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "21\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_mult_one_int_two_var_found(self):
        inputs = ['LET B 4','LET A 3', 'MULT A B', "PRINT A", "."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "12\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_mult_no_int_no_var_found(self):
        inputs = ['MULT A B', "PRINT A", "."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "0\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_mult_strings_1_var_first(self):
        inputs = ['LET A 2','MULT A "Boo"', "PRINT A", "."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "BooBoo\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_mult_strings_1_var_second(self):
        inputs = ['MULT A "Boo"', "PRINT A", "."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_mult_strings_1_var_second_int(self):
        inputs = ['LET A "Boo"','MULT A 2', "PRINT A", "."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "BooBoo\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_sub_one_int_no_var_found(self):
        inputs = ['SUB A 7', "PRINT A","."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "-7\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_sub_one_int_one_var_found(self):
        inputs = ['LET A 3','SUB A 7', "PRINT A","."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "-4\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_sub_one_int_two_var_found(self):
        inputs = ['LET B 4','LET A 3', 'SUB A B', "PRINT A", "."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "-1\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_sub_no_int_no_var_found(self):
        inputs = ['SUB A B', "PRINT A", "."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "0\n"
                self.assertEqual(output.getvalue(), expected_output)


    def test_div_one_int_no_var_found(self):
        inputs = ['DIV A 7', "PRINT A","."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "0\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_div_one_int_one_var_found_int_div(self):
        inputs = ['LET A 3','DIV A 7', "PRINT A","."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "0\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_div_two_var_found_int_div(self):
        inputs = ['LET B 4','LET A 3', 'DIV A B', "PRINT A", "."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "0\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_div_no_int_no_var_found(self):
        inputs = ['DIV A B', "PRINT A", "."]
        with mock.patch('builtins.input', side_effect=inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new=output):
                    with self.assertRaises(ValueError) as cm:
                        loop.while_loop()
                self.assertEqual(str(cm.exception), "Division by zero is not allowed")


    def test_INNUM_normal_ints_not_valid(self):
        inputs = ["LET A 5", "INNUM A", "PRINT A", ".", '"HELLO"']
        with mock.patch('builtins.input', side_effect=inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new=output):
                    with self.assertRaises(SystemExit) as cm:
                        loop.while_loop()
                self.assertEqual(cm.exception.code, None)

    def test_INSTR_normal_string_valid(self):
        inputs = ["INSTR A", "PRINT A",".",'A']
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "A\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_print_string(self):
        inputs = ['PRINT "HELLO"',"."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "HELLO\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_rint_string_random_colon(self):
        inputs = ["G: PRINT 5",'PRINT "HELLO"',"."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "5\nHELLO\n"
                self.assertEqual(output.getvalue(), expected_output)


    def test_goto_one(self):
        inputs = ["GOTO 1","."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with self.assertRaises(SystemExit):
                loop.while_loop()

    def test_goto_wrong(self):
        inputs = ["GOTO 4","."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with self.assertRaises(SystemExit):
                loop.while_loop()

    def test_goto_at_the_End(self):
        inputs = ["LET Z 5","GOTO 5","LET C 4","PRINT C","PRINT Z","END","PRINT C","PRINT Z","GOTO -6","."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "0\n5\n4\n5\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_return_with_no_GOSUB(self):
        inputs = ["PRINT 1","RETURN","."]
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with self.assertRaises(SystemExit):
                loop.while_loop()

    def test_INNUM_normal_string_valid_neg(self):
        inputs = ["INNUM A", "PRINT A",".",'-10']
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "-10\n"
                self.assertEqual(output.getvalue(), expected_output)

    def test_INNUM_normal_string_valid_neg_float(self):
        inputs = ["INNUM A", "PRINT A",".",'-10.0']
        with mock.patch('builtins.input', side_effect = inputs):
            loop = looping.Loop_de_loop()
            with io.StringIO() as output:
                with mock.patch('sys.stdout', new = output):
                    loop.while_loop()
                expected_output = "-10.0\n"
                self.assertEqual(output.getvalue(), expected_output)





if __name__ == '__main__':
    unittest.main()
