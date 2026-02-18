# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/python2.7/ctypes/test/test_values.py
# Compiled at: 2025-09-02 17:07:25
"""
A testcase which accesses *values* in a dll.
"""
import unittest, sys
from ctypes import *
import _ctypes_test

class ValuesTestCase(unittest.TestCase):

    def test_an_integer(self):
        ctdll = CDLL(_ctypes_test.__file__)
        an_integer = c_int.in_dll(ctdll, 'an_integer')
        x = an_integer.value
        self.assertEqual(x, ctdll.get_an_integer())
        an_integer.value *= 2
        self.assertEqual(x * 2, ctdll.get_an_integer())
        return

    def test_undefined(self):
        ctdll = CDLL(_ctypes_test.__file__)
        self.assertRaises(ValueError, c_int.in_dll, ctdll, 'Undefined_Symbol')
        return


@unittest.skipUnless(sys.platform == 'win32', 'Windows-specific test')
class Win_ValuesTestCase(unittest.TestCase):
    """This test only works when python itself is a dll/shared library"""

    def test_optimizeflag(self):
        opt = c_int.in_dll(pythonapi, 'Py_OptimizeFlag').value
        self.assertEqual(opt, 0)
        return

    def test_frozentable(self):

        class struct_frozen(Structure):
            _fields_ = [
             (
              'name', c_char_p),
             (
              'code', POINTER(c_ubyte)),
             (
              'size', c_int)]

        FrozenTable = POINTER(struct_frozen)
        ft = FrozenTable.in_dll(pythonapi, 'PyImport_FrozenModules')
        items = []
        for entry in ft:
            if entry.name is None:
                break
            items.append((entry.name, entry.size))

        expected = [('__hello__', 104),
         ('__phello__', -104),
         ('__phello__.spam', 104)]
        self.assertEqual(items, expected)
        from ctypes import _pointer_type_cache
        del _pointer_type_cache[struct_frozen]
        return

    def test_undefined(self):
        self.assertRaises(ValueError, c_int.in_dll, pythonapi, 'Undefined_Symbol')
        return


if __name__ == '__main__':
    unittest.main()
return
