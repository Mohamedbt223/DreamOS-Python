# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/python2.7/ctypes/test/test_sizes.py
# Compiled at: 2025-09-02 17:07:25
from ctypes import *
import sys, unittest

class SizesTestCase(unittest.TestCase):

    def test_8(self):
        self.assertEqual(1, sizeof(c_int8))
        self.assertEqual(1, sizeof(c_uint8))
        return

    def test_16(self):
        self.assertEqual(2, sizeof(c_int16))
        self.assertEqual(2, sizeof(c_uint16))
        return

    def test_32(self):
        self.assertEqual(4, sizeof(c_int32))
        self.assertEqual(4, sizeof(c_uint32))
        return

    def test_64(self):
        self.assertEqual(8, sizeof(c_int64))
        self.assertEqual(8, sizeof(c_uint64))
        return

    def test_size_t(self):
        self.assertEqual(sizeof(c_void_p), sizeof(c_size_t))
        return

    def test_ssize_t(self):
        self.assertEqual(sizeof(c_void_p), sizeof(c_ssize_t))
        return


if __name__ == '__main__':
    unittest.main()
return
