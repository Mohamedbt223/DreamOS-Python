# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/python2.7/ctypes/test/test_incomplete.py
# Compiled at: 2025-09-02 17:07:24
import unittest
from ctypes import *

class MyTestCase(unittest.TestCase):

    def test_incomplete_example(self):
        lpcell = POINTER('cell')

        class cell(Structure):
            _fields_ = [
             (
              'name', c_char_p),
             (
              'next', lpcell)]

        SetPointerType(lpcell, cell)
        c1 = cell()
        c1.name = 'foo'
        c2 = cell()
        c2.name = 'bar'
        c1.next = pointer(c2)
        c2.next = pointer(c1)
        p = c1
        result = []
        for i in range(8):
            result.append(p.name)
            p = p.next[0]

        self.assertEqual(result, ['foo', 'bar'] * 4)
        from ctypes import _pointer_type_cache
        del _pointer_type_cache[cell]
        return


if __name__ == '__main__':
    unittest.main()
return
