# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/python2.7/ctypes/test/test_buffers.py
# Compiled at: 2025-09-02 17:07:24
from ctypes import *
from ctypes.test import need_symbol
import unittest

class StringBufferTestCase(unittest.TestCase):

    def test_buffer(self):
        b = create_string_buffer(32)
        self.assertEqual(len(b), 32)
        self.assertEqual(sizeof(b), 32 * sizeof(c_char))
        self.assertIs(type(b[0]), str)
        b = create_string_buffer('abc')
        self.assertEqual(len(b), 4)
        self.assertEqual(sizeof(b), 4 * sizeof(c_char))
        self.assertIs(type(b[0]), str)
        self.assertEqual(b[0], 'a')
        self.assertEqual(b[:], 'abc\x00')
        self.assertEqual(b[::], 'abc\x00')
        self.assertEqual(b[::-1], '\x00cba')
        self.assertEqual(b[::2], 'ac')
        self.assertEqual(b[::5], 'a')
        return

    def test_buffer_interface(self):
        self.assertEqual(len(bytearray(create_string_buffer(0))), 0)
        self.assertEqual(len(bytearray(create_string_buffer(1))), 1)
        return

    def test_string_conversion(self):
        b = create_string_buffer(u'abc')
        self.assertEqual(len(b), 4)
        self.assertEqual(sizeof(b), 4 * sizeof(c_char))
        self.assertTrue(type(b[0]) is str)
        self.assertEqual(b[0], 'a')
        self.assertEqual(b[:], 'abc\x00')
        self.assertEqual(b[::], 'abc\x00')
        self.assertEqual(b[::-1], '\x00cba')
        self.assertEqual(b[::2], 'ac')
        self.assertEqual(b[::5], 'a')
        return

    @need_symbol('c_wchar')
    def test_unicode_buffer(self):
        b = create_unicode_buffer(32)
        self.assertEqual(len(b), 32)
        self.assertEqual(sizeof(b), 32 * sizeof(c_wchar))
        self.assertIs(type(b[0]), unicode)
        b = create_unicode_buffer(u'abc')
        self.assertEqual(len(b), 4)
        self.assertEqual(sizeof(b), 4 * sizeof(c_wchar))
        self.assertIs(type(b[0]), unicode)
        self.assertEqual(b[0], u'a')
        self.assertEqual(b[:], 'abc\x00')
        self.assertEqual(b[::], 'abc\x00')
        self.assertEqual(b[::-1], '\x00cba')
        self.assertEqual(b[::2], 'ac')
        self.assertEqual(b[::5], 'a')
        return

    @need_symbol('c_wchar')
    def test_unicode_conversion(self):
        b = create_unicode_buffer('abc')
        self.assertEqual(len(b), 4)
        self.assertEqual(sizeof(b), 4 * sizeof(c_wchar))
        self.assertIs(type(b[0]), unicode)
        self.assertEqual(b[0], u'a')
        self.assertEqual(b[:], 'abc\x00')
        self.assertEqual(b[::], 'abc\x00')
        self.assertEqual(b[::-1], '\x00cba')
        self.assertEqual(b[::2], 'ac')
        self.assertEqual(b[::5], 'a')
        return


if __name__ == '__main__':
    unittest.main()
return
