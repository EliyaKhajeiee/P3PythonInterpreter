# project3_sanitycheck.py
#
# ICS 33 Spring 2023
# Project 3: Why Not Smile?
#
# This is a sanity checker for your Project 3 solution, which checks whether
# your solution meets some basic requirements with respect to reading input
# and formatting its output, as well as verifying that at least one example
# can be run all the way to completion.  It runs your program, passes it
# one legal input, then assesses whether the output is exactly correct.
#
# In order for the sanity check to run successfully, you'll need to meet
# these requirements:
#
# * This module is in the project directory alongside "project3.py" and
#   whatever additional modules comprise your solution.
# * It's possible to run the program by executing that "project3.py" module.
# * Your program generates precisely correct output for one scenario.
#
# If your program is unable to pass this sanity checker, it will certainly be
# unable to pass all of our automated tests (and it may well fail all of them).
# On the other hand, there are other tests you'll want to run besides the one
# scenario here, because we'll be testing more than just one when we grade
# your work.
#
# YOU DO NOT NEED TO READ OR UNDERSTAND THIS CODE, though you can certainly
# feel free to take a look at it.

from collections.abc import Sequence
import contextlib
import locale
from pathlib import Path
import queue
import subprocess
import sys
import tempfile
import threading
import time
import traceback



class TextProcessReadTimeout(Exception):
    pass


class TextProcess:
    _READ_INTERVAL_IN_SECONDS = 0.025

    def __init__(self, args: [str], working_directory: str):
        self._process = subprocess.Popen(
            args, cwd = working_directory, bufsize = 0,
            stdin = subprocess.PIPE, stdout = subprocess.PIPE,
            stderr = subprocess.STDOUT)

        self._stdout_read_trigger = queue.Queue()
        self._stdout_buffer = queue.Queue()

        self._stdout_thread = threading.Thread(
            target = self._stdout_read_loop, daemon = True)

        self._stdout_thread.start()

    def __enter__(self):
        return self

    def __exit__(self, tr, exc, val):
        self.close()

    def close(self):
        self._stdout_read_trigger.put('stop')
        self._process.terminate()
        self._process.wait()
        self._process.stdout.close()
        self._process.stdin.close()

    def write_line(self, line: str) -> None:
        try:
            self._process.stdin.write((line + '\n').encode(locale.getpreferredencoding(False)))
            self._process.stdin.flush()
        except OSError:
            pass

    def read_line(self, timeout: float = None) -> tuple[str, bool] or None:
        self._stdout_read_trigger.put('read')

        sleep_time = 0

        while timeout is None or sleep_time < timeout:
            try:
                next_result = self._stdout_buffer.get_nowait()

                if next_result is None:
                    return None
                elif isinstance(next_result, Exception):
                    raise next_result
                else:
                    line = next_result.decode(locale.getpreferredencoding(False))
                    had_newline = False

                    if line.endswith('\r\n'):
                        line = line[:-2]
                        had_newline = True
                    elif line.endswith('\n'):
                        line = line[:-1]
                        had_newline = True

                    return line, had_newline
            except queue.Empty:
                time.sleep(TextProcess._READ_INTERVAL_IN_SECONDS)
                sleep_time += TextProcess._READ_INTERVAL_IN_SECONDS

        raise TextProcessReadTimeout()

    def _stdout_read_loop(self):
        try:
            while self._process.returncode is None:
                if self._stdout_read_trigger.get() == 'read':
                    line = self._process.stdout.readline()

                    if line == b'':
                        self._stdout_buffer.put(None)
                    else:
                        self._stdout_buffer.put(line)
                else:
                    break
        except Exception as e:
            self._stdout_buffer.put(e)


class TestFailure(Exception):
    pass


class TestInputLine:
    def __init__(self, text: str):
        self._text = text

    def execute(self, process: TextProcess) -> None:
        try:
            process.write_line(self._text)
        except Exception:
            print_labeled_output(
                'EXCEPTION',
                *[tb_line.rstrip() for tb_line in traceback.format_exc().split('\n')])

            raise TestFailure()

        print_labeled_output('INPUT', self._text)


class TestOutputLine:
    def __init__(self, text: str, timeout_in_seconds: float):
        self._text = text
        self._timeout_in_seconds = timeout_in_seconds

    def execute(self, process: TextProcess) -> None:
        try:
            output_line = process.read_line(self._timeout_in_seconds)
        except TextProcessReadTimeout:
            output_line = None
        except Exception:
            print_labeled_output(
                'EXCEPTION',
                [tb_line.rstrip() for tb_line in traceback.format_exc().split('\n')])

            raise TestFailure()

        if output_line is not None:
            output_text, had_newline = output_line

            print_labeled_output('OUTPUT', output_text)

            if output_text != self._text:
                print_labeled_output('EXPECTED', self._text)

                index = min(len(output_text), len(self._text))

                for i in range(min(len(output_text), len(self._text))):
                    if output_text[i] != self._text[i]:
                        index = i
                        break

                print_labeled_output('', (' ' * index) + '^')

                print_labeled_output(
                    'ERROR',
                    'This line of output did not match what was expected.  The first',
                    'incorrect character is marked with a ^ above.',
                    '(If you don\'t see a difference, perhaps your program printed',
                    'extra whitespace on the end of this line.)')

                raise TestFailure()
            elif not had_newline:
                print_labeled_output(
                    'ERROR',
                    'This line of output was required to have a newline',
                    'on the end of it, but it did not.')
        else:
            print_labeled_output('EXPECTED', self._text)

            print_labeled_output(
                'ERROR',
                'This line of output was expected, but the program did not generate',
                'any additional output after waiting for {} second(s).'.format(
                    self._timeout_in_seconds))

            raise TestFailure()


class TestEndOfOutput:
    def __init__(self, timeout_in_seconds: float):
        self._timeout_in_seconds = timeout_in_seconds

    def execute(self, process: TextProcess) -> None:
        output_line = process.read_line(self._timeout_in_seconds)

        if output_line is not None:
            print_labeled_output('OUTPUT', output_line)

            print_labeled_output(
                'ERROR',
                'Extra output was printed after the program should not have generated',
                'any additional output')

            raise TestFailure()


def run_test() -> None:
    with contextlib.closing(start_process()) as process:
        try:
            test_lines = make_test_lines()
            run_test_lines(process, test_lines)

            print_labeled_output(
                'PASSED',
                'Your Project 3 implementation passed the sanity checker.  Note that',
                'there are many other tests you\'ll want to run on your own, because',
                'a number of other scenarios exist that are legal and interesting.')
        except TestFailure:
            print_labeled_output(
                'FAILED',
                'The sanity checker has failed, for the reasons described above.')


def start_process() -> TextProcess:
    module_path = Path.cwd() / 'project3.py'

    if not module_path.exists() or not module_path.is_file():
        print_labeled_output(
            'ERROR',
            'Cannot find an executable "project3.py" file in this directory.',
            'Make sure that the sanity checker is in the same directory as the',
            'files that comprise your Project 3 solution.')

        raise TestFailure()
    else:
        return TextProcess(
            [sys.executable, str(module_path)],
            str(Path.cwd()))


def print_labeled_output(label: str, *msg_lines: Sequence[str]) -> None:
    showed_first = False

    for msg_line in msg_lines:
        if not showed_first:
            print('{:10}|{}'.format(label, msg_line))
            showed_first = True
        else:
            print('{:10}|{}'.format(' ', msg_line))

    if not showed_first:
        print(label)


# -------------------------------------------------------------------

def make_test_lines() -> list[TestInputLine | TestOutputLine]:
    return [
        # 1: INPUT
        TestInputLine('LET MESSAGE "Hello Boo!"'),
        TestInputLine('PRINT MESSAGE'),

        # 2: INPUT
        TestInputLine('LET NAME "Boo"'),  # test setting string variable
        TestInputLine('LET AGE 13.015625'),  # test setting float variable
        TestInputLine('PRINT NAME'),  # test print string variable
        TestInputLine('PRINT AGE'),  # test print float variable

        # 3: INPUT
        TestInputLine('PRINT "Number: "'),
        TestInputLine('INNUM X'),  # test innum
        TestInputLine('INNUM Y'),  # test innum
        TestInputLine('ADD X 7'),  # test addition with innum
        TestInputLine('SUB Y 7'),  # test subtraction with innum
        TestInputLine('PRINT X'),
        TestInputLine('PRINT Y'),

        # 4: INPUT
        TestInputLine('LET INT 3'),
        TestInputLine('LET STR "3"'),
        TestInputLine('LET NUM "Number Three"'),
        TestInputLine('PRINT INT'),  # print int variable
        TestInputLine('PRINT STR'),  # print string variable
        TestInputLine('PRINT NUM'),  # print string variable
        TestInputLine('PRINT "Direct String"'),  # print literal string
        TestInputLine('PRINT 3'),  # print int
        TestInputLine('PRINT 3.0'),  # print float

        # 5: INPUT
        TestInputLine('LET A 5'),
        TestInputLine('LET B 10'),
        TestInputLine('LET A B'),  # test assigning variable to variable
        TestInputLine('LET B 7'),
        TestInputLine('PRINT A'),
        TestInputLine('PRINT B'),

        # 6: INPUT
        TestInputLine('LET D 1'),
        TestInputLine('GOTO 2'),  # test goto
        TestInputLine('LET D 2'),  # this line is skipped
        TestInputLine('PRINT D'),

        # 7: INPUT - GOSUB


        # 8: INPUT - addition
        TestInputLine('LET ADDITION 5'),  # set integer variable
        TestInputLine('PRINT ADDITION'),  # 5
        TestInputLine('ADD ADDITION 5'),  # int + int = int
        TestInputLine('PRINT ADDITION'),  # 5 + 5 = 10
        TestInputLine('ADD ADDITION 5.0'),  # int + float = float
        TestInputLine('PRINT ADDITION'),  # 10 + 5.0 = 15.0
        TestInputLine('ADD ADDITION 5'),  # float + int = float
        TestInputLine('PRINT ADDITION'),  # 15.0 + 5 = 20.0
        TestInputLine('ADD ADDITION 10'),  # float + float = float
        TestInputLine('PRINT ADDITION'),  # 20.0 + 10.0 = 30.0
        TestInputLine('LET ADDSTR "This is "'),  # set integer variable
        TestInputLine('ADD ADDSTR "a string."'),  # str + str
        TestInputLine('PRINT ADDSTR'),  # 'this is ' + 'a string' = 'this is a string'

        # 9: INPUT - subtraction
        TestInputLine('LET SUBTRACTION 50'),  # set integer variable
        TestInputLine('PRINT SUBTRACTION'),  # 50
        TestInputLine('SUB SUBTRACTION 5'),  # int - int = int
        TestInputLine('PRINT SUBTRACTION'),  # 50 - 5 = 45
        TestInputLine('SUB SUBTRACTION 5.0'),  # int - float = float
        TestInputLine('PRINT SUBTRACTION'),  # 45 - 5.0 = 40.0
        TestInputLine('SUB SUBTRACTION 10'),  # float - int = float
        TestInputLine('PRINT SUBTRACTION'),  # 40.0 - 10 = 30.0
        TestInputLine('SUB SUBTRACTION 15.0'),  # float - float = float
        TestInputLine('PRINT SUBTRACTION'),  # 30.0 - 15.0 = 15.0

        # 10: INPUT - multiplication
        TestInputLine('LET MULTIPLY 2'),  # set integer variable
        TestInputLine('PRINT MULTIPLY'),  # 5
        TestInputLine('MULT MULTIPLY 3'),  # int * int = int
        TestInputLine('PRINT MULTIPLY'),  # 2 * 3 = 6
        TestInputLine('MULT MULTIPLY 3.0'),  # int * float = float
        TestInputLine('PRINT MULTIPLY'),  # 6 * 3.0 = 18.0
        TestInputLine('MULT MULTIPLY 2'),  # float * int = float
        TestInputLine('PRINT MULTIPLY'),  # 18.0 * 2 = 36.0
        TestInputLine('MULT MULTIPLY 2.0'),  # float * float = float
        TestInputLine('PRINT MULTIPLY'),  # 36.0 * 2.0 = 72.0
        TestInputLine('LET BOO "Boo"'),  # set string variable
        TestInputLine('MULT BOO 3'),  # str * int = str
        TestInputLine('PRINT BOO'),  # BooBooBoo
        TestInputLine('LET NUMBOO 5'),  # set int variable
        TestInputLine('MULT NUMBOO "Boo"'),  # str * int = str
        TestInputLine('PRINT NUMBOO'),  # BooBooBooBooBoo

        # 11: INPUT - division
        TestInputLine('LET DIVISION 100'),  # set integer variable
        TestInputLine('PRINT DIVISION'),  # 100
        TestInputLine('DIV DIVISION 2'),  # int / int = int
        TestInputLine('PRINT DIVISION'),  # 100 / 2 = 50
        TestInputLine('DIV DIVISION 3'),  # int / int = int (floor division)
        TestInputLine('PRINT DIVISION'),  # 50 / 3 = 16
        TestInputLine('DIV DIVISION 2.0'),  # int / float = float
        TestInputLine('PRINT DIVISION'),  # 16 / 2.0 = 8.0
        TestInputLine('DIV DIVISION 2'),  # float / int = float
        TestInputLine('PRINT DIVISION'),  # 8.0 / 2 = 4.0
        TestInputLine('LET DIVISION 7.0'),
        TestInputLine('DIV DIVISION 2'),  # float / int = float
        TestInputLine('PRINT DIVISION'),  # 7.0 / 2 = 3.5
        TestInputLine('LET DIVISION 7.0'),
        TestInputLine('DIV DIVISION 2.0'),  # float / float = float
        TestInputLine('PRINT DIVISION'),  # 7.0 / 2 = 3.5

        # 12: INPUT - GOTO
        TestInputLine('LET Z 6'),  # 1 - start here
        TestInputLine('GOTO 5'),  # 2 (jump)
        TestInputLine('LET C 4'),  # 6 (jumped from 5)
        TestInputLine('PRINT C'),  # 7
        TestInputLine('PRINT Z'),  # 8
        TestInputLine('END'),  # 9 - end program
        TestInputLine('PRINT C'),  # 3 (jumped from 2)
        TestInputLine('PRINT Z'),  # 4
        TestInputLine('GOTO -6'),  # 5 (jump)

        # END OF INPUT
        TestInputLine('.'),  # end of input

        # 1: OUTPUT
        TestOutputLine('Hello Boo!', 100.0),

        # 2: INPUT
        TestOutputLine('Boo', 100.0),
        TestOutputLine('13.015625', 100.0),

        # 3: OUTPUT
        TestOutputLine('Number: ', 100.0),
        TestInputLine('10'),
        TestInputLine('10'),
        TestOutputLine('17', 100.0),
        TestOutputLine('3', 100.0),

        # 4: OUTPUT
        TestOutputLine('3', 100.0),
        TestOutputLine('3', 100.0),
        TestOutputLine('Number Three', 100.0),
        TestOutputLine('Direct String', 100.0),
        TestOutputLine('3', 100.0),
        TestOutputLine('3.0', 100.0),

        # 5: OUTPUT
        TestOutputLine('10', 100.0),
        TestOutputLine('7', 100.0),

        # 6: OUTPUT
        TestOutputLine('1', 100.0),

        # 7: OUTPUT - GOSUB


        # 8: OUTPUT - addition
        TestOutputLine('5', 100.0),
        TestOutputLine('10', 100.0),
        TestOutputLine('15.0', 100.0),
        TestOutputLine('20.0', 100.0),
        TestOutputLine('30.0', 100.0),
        TestOutputLine('This is a string.', 100.0),

        # 9: OUTPUT - subtraction
        TestOutputLine('50', 100.0),
        TestOutputLine('45', 100.0),
        TestOutputLine('40.0', 100.0),
        TestOutputLine('30.0', 100.0),
        TestOutputLine('15.0', 100.0),

        # 10: OUTPUT - multiplication
        TestOutputLine('2', 100.0),
        TestOutputLine('6', 100.0),
        TestOutputLine('18.0', 100.0),
        TestOutputLine('36.0', 100.0),
        TestOutputLine('72.0', 100.0),
        TestOutputLine('BooBooBoo', 100.0),
        TestOutputLine('BooBooBooBooBoo', 100.0),

        # 11: OUTPUT - division
        TestOutputLine('100', 100.0),
        TestOutputLine('50', 100.0),
        TestOutputLine('16', 100.0),
        TestOutputLine('8.0', 100.0),
        TestOutputLine('4.0', 100.0),
        TestOutputLine('3.5', 100.0),
        TestOutputLine('3.5', 100.0),

        # 12: OUTPUT
        TestOutputLine('0', 100.0),
        TestOutputLine('6', 100.0),
        TestOutputLine('4', 100.0),
        TestOutputLine('6', 100.0),

        # END OF OUTPUT
        TestEndOfOutput(2.0)
    ]



def run_test_lines(process: TextProcess, test_lines: list[TestInputLine | TestOutputLine]) -> None:
    for line in test_lines:
        line.execute(process)


if __name__ == '__main__':
    run_test()
