# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/python2.7/ctypes/test/test_memfunctions.py
# Compiled at: 2025-09-02 17:07:24
import sys, unittest
from ctypes import *
from ctypes.test import need_symbol

class MemFunctionsTest(unittest.TestCase):

    @unittest.skip('test disabled')
    def test_overflow(self):
        self.assertRaises((OverflowError, MemoryError, SystemError), (lambda : wstring_at(u'foo', sys.maxint - 1)))
        self.assertRaises((OverflowError, MemoryError, SystemError), (lambda : string_at('foo', sys.maxint - 1)))
        return

    def test_memmove(self):
        a = create_string_buffer(1000000)
        p = 'Hello, World'
        result = memmove(a, p, len(p))
        self.assertEqual(a.value, 'Hello, World')
        self.assertEqual(string_at(result), 'Hello, World')
        self.assertEqual(string_at(result, 5), 'Hello')
        self.assertEqual(string_at(result, 16), 'Hello, World\x00\x00\x00\x00')
        self.assertEqual(string_at(result, 0), '')
        return

    def test_memset(self):
        a = create_string_buffer(1000000)
        result = memset(a, ord('x'), 16)
        self.assertEqual(a.value, 'xxxxxxxxxxxxxxxx')
        self.assertEqual(string_at(result), 'xxxxxxxxxxxxxxxx')
        self.assertEqual(string_at(a), 'xxxxxxxxxxxxxxxx')
        self.assertEqual(string_at(a, 20), 'xxxxxxxxxxxxxxxx\x00\x00\x00\x00')
        return

    def test_cast(self):
        a = (c_ubyte * 32)(*map(ord, 'abcdef'))
        self.assertEqual(cast(a, c_char_p).value, 'abcdef')
        self.assertEqual(cast(a, POINTER(c_byte))[:7], [
         4, 5, 6, 7, 8, 9, 10])
        self.assertEqual(cast(a, POINTER(c_byte))[:7:], [
         4, 5, 6, 7, 8, 9, 10])
        self.assertEqual(cast(a, POINTER(c_byte))[6:-1:-1], [
         10, 9, 8, 7, 6, 5, 4])
        self.assertEqual(cast(a, POINTER(c_byte))[:7:2], [
         97, 99, 101, 0])
        self.assertEqual(cast(a, POINTER(c_byte))[:7:7], [
         97])
        return

    def test_string_at(self):
        s = string_at('foo bar')
        self.assertEqual(2, sys.getrefcount(s))
        self.assertTrue(s, 'foo bar')
        self.assertEqual(string_at('foo bar', 8), 'foo bar\x00')
        self.assertEqual(string_at('foo bar', 3), 'foo')
        return

    @need_symbol('create_unicode_buffer')
    def test_wstring_at(self):
        p = create_unicode_buffer('Hello, World')
        a = create_unicode_buffer(1000000)
        result = memmove(a, p, len(p) * sizeof(c_wchar))
        self.assertEqual(a.value, 'Hello, World')
        self.assertEqual(wstring_at(a), 'Hello, World')
        self.assertEqual(wstring_at(a, 5), 'Hello')
        self.assertEqual(wstring_at(a, 16), 'Hello, World\x00\x00\x00\x00')
        self.assertEqual(wstring_at(a, 0), '')
        return


if __name__ == '__main__':
    unittest.main()
return
