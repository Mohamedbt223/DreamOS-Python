# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/python2.7/ctypes/test/test_struct_fields.py
# Compiled at: 2025-09-02 17:07:25
import unittest
from ctypes import *

class StructFieldsTestCase(unittest.TestCase):

    def test_1_A(self):

        class X(Structure):
            pass

        self.assertEqual(sizeof(X), 0)
        X._fields_ = []
        self.assertRaises(AttributeError, setattr, X, '_fields_', [])
        return

    def test_1_B(self):

        class X(Structure):
            _fields_ = []

        self.assertRaises(AttributeError, setattr, X, '_fields_', [])
        return

    def test_2(self):

        class X(Structure):
            pass

        X()
        self.assertRaises(AttributeError, setattr, X, '_fields_', [])
        return

    def test_3(self):

        class X(Structure):
            pass

        class Y(Structure):
            _fields_ = [
             (
              'x', X)]

        self.assertRaises(AttributeError, setattr, X, '_fields_', [])
        return

    def test_4(self):

        class X(Structure):
            pass

        class Y(X):
            pass

        self.assertRaises(AttributeError, setattr, X, '_fields_', [])
        Y._fields_ = []
        self.assertRaises(AttributeError, setattr, X, '_fields_', [])
        return


if __name__ == '__main__':
    unittest.main()
return
