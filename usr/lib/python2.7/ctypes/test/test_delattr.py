# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/python2.7/ctypes/test/test_delattr.py
# Compiled at: 2025-09-02 17:07:24
import unittest
from ctypes import *

class X(Structure):
    _fields_ = [
     (
      'foo', c_int)]


class TestCase(unittest.TestCase):

    def test_simple(self):
        self.assertRaises(TypeError, delattr, c_int(42), 'value')
        return

    def test_chararray(self):
        self.assertRaises(TypeError, delattr, (c_char * 5)(), 'value')
        return

    def test_struct(self):
        self.assertRaises(TypeError, delattr, X(), 'foo')
        return


if __name__ == '__main__':
    unittest.main()
return
