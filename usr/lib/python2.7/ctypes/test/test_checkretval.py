# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/python2.7/ctypes/test/test_checkretval.py
# Compiled at: 2025-09-02 17:07:24
import unittest
from ctypes import *
from ctypes.test import need_symbol

class CHECKED(c_int):

    def _check_retval_(value):
        return str(value.value)

    _check_retval_ = staticmethod(_check_retval_)


class Test(unittest.TestCase):

    def test_checkretval(self):
        import _ctypes_test
        dll = CDLL(_ctypes_test.__file__)
        self.assertEqual(42, dll._testfunc_p_p(42))
        dll._testfunc_p_p.restype = CHECKED
        self.assertEqual('42', dll._testfunc_p_p(42))
        dll._testfunc_p_p.restype = None
        self.assertEqual(None, dll._testfunc_p_p(42))
        del dll._testfunc_p_p.restype
        self.assertEqual(42, dll._testfunc_p_p(42))
        return

    @need_symbol('oledll')
    def test_oledll(self):
        self.assertRaises(WindowsError, oledll.oleaut32.CreateTypeLib2, 0, None, None)
        return


if __name__ == '__main__':
    unittest.main()
return
