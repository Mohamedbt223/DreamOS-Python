# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/python2.7/ctypes/test/test_repr.py
# Compiled at: 2025-09-02 17:07:25
from ctypes import *
import unittest
subclasses = []
for base in [c_byte, c_short, c_int, c_long, c_longlong, 
 c_ubyte, c_ushort, c_uint, 
 c_ulong, c_ulonglong, 
 c_float, c_double, c_longdouble, c_bool]:

    class X(base):
        pass


    subclasses.append(X)

class X(c_char):
    pass


class ReprTest(unittest.TestCase):

    def test_numbers(self):
        for typ in subclasses:
            base = typ.__bases__[0]
            self.assertTrue(repr(base(42)).startswith(base.__name__))
            self.assertEqual('<X object at', repr(typ(42))[:12])

        return

    def test_char(self):
        self.assertEqual("c_char('x')", repr(c_char('x')))
        self.assertEqual('<X object at', repr(X('x'))[:12])
        return


if __name__ == '__main__':
    unittest.main()
return
