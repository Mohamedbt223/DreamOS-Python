# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/python2.7/ctypes/test/test_random_things.py
# Compiled at: 2025-09-02 17:07:25
from ctypes import *
import unittest, sys

def callback_func(arg):
    42 // arg
    raise ValueError(arg)
    return


@unittest.skipUnless(sys.platform == 'win32', 'Windows-specific test')
class call_function_TestCase(unittest.TestCase):

    def test(self):
        from _ctypes import call_function
        windll.kernel32.LoadLibraryA.restype = c_void_p
        windll.kernel32.GetProcAddress.argtypes = (c_void_p, c_char_p)
        windll.kernel32.GetProcAddress.restype = c_void_p
        hdll = windll.kernel32.LoadLibraryA('kernel32')
        funcaddr = windll.kernel32.GetProcAddress(hdll, 'GetModuleHandleA')
        self.assertEqual(call_function(funcaddr, (None, )), windll.kernel32.GetModuleHandleA(None))
        return


class CallbackTracbackTestCase(unittest.TestCase):

    def capture_stderr(self, func, *args, **kw):
        import StringIO
        old_stderr = sys.stderr
        logger = sys.stderr = StringIO.StringIO()
        try:
            func(*args, **kw)
        finally:
            sys.stderr = old_stderr

        return logger.getvalue()

    def test_ValueError(self):
        cb = CFUNCTYPE(c_int, c_int)(callback_func)
        out = self.capture_stderr(cb, 42)
        self.assertEqual(out.splitlines()[-1], 'ValueError: 42')
        return

    def test_IntegerDivisionError(self):
        cb = CFUNCTYPE(c_int, c_int)(callback_func)
        out = self.capture_stderr(cb, 0)
        self.assertEqual(out.splitlines()[-1][:19], 'ZeroDivisionError: ')
        return

    def test_FloatDivisionError(self):
        cb = CFUNCTYPE(c_int, c_double)(callback_func)
        out = self.capture_stderr(cb, 0.0)
        self.assertEqual(out.splitlines()[-1][:19], 'ZeroDivisionError: ')
        return

    def test_TypeErrorDivisionError(self):
        cb = CFUNCTYPE(c_int, c_char_p)(callback_func)
        out = self.capture_stderr(cb, 'spam')
        self.assertEqual(out.splitlines()[-1], "TypeError: unsupported operand type(s) for //: 'int' and 'str'")
        return


if __name__ == '__main__':
    unittest.main()
return
