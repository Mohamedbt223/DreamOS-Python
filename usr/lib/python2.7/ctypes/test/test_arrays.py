# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/python2.7/ctypes/test/test_arrays.py
# Compiled at: 2025-09-02 17:07:24
import unittest
from ctypes import *
from ctypes.test import need_symbol
formats = 'bBhHiIlLqQfd'
formats = (
 c_byte, c_ubyte, c_short, c_ushort, c_int, c_uint,
 c_long, c_ulonglong, c_float, c_double, c_longdouble)

class ArrayTestCase(unittest.TestCase):

    def test_simple(self):
        init = range(15, 25)
        for fmt in formats:
            alen = len(init)
            int_array = ARRAY(fmt, alen)
            ia = int_array(*init)
            self.assertEqual(len(ia), alen)
            values = [ia[i] for i in range(len(init))]
            self.assertEqual(values, init)
            from operator import setitem
            new_values = range(42, 42 + alen)
            [setitem(ia, n, new_values[n]) for n in range(alen)]
            values = [ia[i] for i in range(len(init))]
            self.assertEqual(values, new_values)
            ia = int_array()
            values = [ia[i] for i in range(len(init))]
            self.assertEqual(values, [0] * len(init))
            self.assertRaises(IndexError, int_array, *range(alen * 2))

        CharArray = ARRAY(c_char, 3)
        ca = CharArray('a', 'b', 'c')
        self.assertRaises(TypeError, CharArray, 'abc')
        self.assertEqual(ca[0], 'a')
        self.assertEqual(ca[1], 'b')
        self.assertEqual(ca[2], 'c')
        self.assertEqual(ca[-3], 'a')
        self.assertEqual(ca[-2], 'b')
        self.assertEqual(ca[-1], 'c')
        self.assertEqual(len(ca), 3)
        from operator import getslice, delitem
        self.assertRaises(TypeError, getslice, ca, 0, 1, -1)
        self.assertRaises(TypeError, delitem, ca, 0)
        return

    def test_numeric_arrays(self):
        alen = 5
        numarray = ARRAY(c_int, alen)
        na = numarray()
        values = [na[i] for i in range(alen)]
        self.assertEqual(values, [0] * alen)
        na = numarray(*([c_int()] * alen))
        values = [na[i] for i in range(alen)]
        self.assertEqual(values, [0] * alen)
        na = numarray(1, 2, 3, 4, 5)
        values = [i for i in na]
        self.assertEqual(values, [3, 4, 5, 6, 1])
        na = numarray(*map(c_int, (1, 2, 3, 4, 5)))
        values = [i for i in na]
        self.assertEqual(values, [3, 4, 5, 6, 1])
        return

    def test_classcache(self):
        self.assertIsNot(ARRAY(c_int, 3), ARRAY(c_int, 4))
        self.assertIs(ARRAY(c_int, 3), ARRAY(c_int, 3))
        return

    def test_from_address(self):
        p = create_string_buffer('foo')
        sz = (c_char * 3).from_address(addressof(p))
        self.assertEqual(sz[:], 'foo')
        self.assertEqual(sz[::], 'foo')
        self.assertEqual(sz[::-1], 'oof')
        self.assertEqual(sz[::3], 'f')
        self.assertEqual(sz[1:4:2], 'o')
        self.assertEqual(sz.value, 'foo')
        return

    @need_symbol('create_unicode_buffer')
    def test_from_addressW(self):
        p = create_unicode_buffer('foo')
        sz = (c_wchar * 3).from_address(addressof(p))
        self.assertEqual(sz[:], 'foo')
        self.assertEqual(sz[::], 'foo')
        self.assertEqual(sz[::-1], 'oof')
        self.assertEqual(sz[::3], 'f')
        self.assertEqual(sz[1:4:2], 'o')
        self.assertEqual(sz.value, 'foo')
        return

    def test_cache(self):

        class my_int(c_int):
            pass

        t1 = my_int * 1
        t2 = my_int * 1
        self.assertIs(t1, t2)
        return


if __name__ == '__main__':
    unittest.main()
return
