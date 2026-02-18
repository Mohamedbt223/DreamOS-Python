# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/python2.7/ctypes/test/test_varsize_struct.py
# Compiled at: 2025-09-02 17:07:25
from ctypes import *
import unittest

class VarSizeTest(unittest.TestCase):

    def test_resize(self):

        class X(Structure):
            _fields_ = [
             (
              'item', c_int),
             (
              'array', c_int * 1)]

        self.assertEqual(sizeof(X), sizeof(c_int) * 2)
        x = X()
        x.item = 42
        x.array[0] = 100
        self.assertEqual(sizeof(x), sizeof(c_int) * 2)
        new_size = sizeof(X) + sizeof(c_int) * 1
        resize(x, new_size)
        self.assertEqual(sizeof(x), new_size)
        self.assertEqual((x.item, x.array[0]), (42, 100))
        new_size = sizeof(X) + sizeof(c_int) * 9
        resize(x, new_size)
        self.assertEqual(sizeof(x), new_size)
        self.assertEqual((x.item, x.array[0]), (42, 100))
        new_size = sizeof(X) + sizeof(c_int) * 1
        resize(x, new_size)
        self.assertEqual(sizeof(x), new_size)
        self.assertEqual((x.item, x.array[0]), (42, 100))
        return

    def test_array_invalid_length(self):
        self.assertRaises(ValueError, (lambda : c_int * -1))
        self.assertRaises(ValueError, (lambda : c_int * -3))
        return

    def test_zerosized_array(self):
        array = (c_int * 0)()
        self.assertRaises(IndexError, array.__setitem__, 0, None)
        self.assertRaises(IndexError, array.__getitem__, 0)
        self.assertRaises(IndexError, array.__setitem__, 1, None)
        self.assertRaises(IndexError, array.__getitem__, 1)
        self.assertRaises(IndexError, array.__setitem__, -1, None)
        self.assertRaises(IndexError, array.__getitem__, -1)
        return


if __name__ == '__main__':
    unittest.main()
return
