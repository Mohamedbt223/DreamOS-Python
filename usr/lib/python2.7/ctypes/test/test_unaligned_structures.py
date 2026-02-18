# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/python2.7/ctypes/test/test_unaligned_structures.py
# Compiled at: 2025-09-02 17:07:25
import sys, unittest
from ctypes import *
structures = []
byteswapped_structures = []
if sys.byteorder == 'little':
    SwappedStructure = BigEndianStructure
else:
    SwappedStructure = LittleEndianStructure
for typ in [c_short, c_int, c_long, c_longlong, 
 c_float, c_double, 
 c_ushort, c_uint, 
 c_ulong, c_ulonglong]:

    class X(Structure):
        _pack_ = 1
        _fields_ = [('pad', c_byte),
         (
          'value', typ)]


    class Y(SwappedStructure):
        _pack_ = 1
        _fields_ = [('pad', c_byte),
         (
          'value', typ)]


    structures.append(X)
    byteswapped_structures.append(Y)

class TestStructures(unittest.TestCase):

    def test_native(self):
        for typ in structures:
            self.assertEqual(typ.value.offset, 1)
            o = typ()
            o.value = 4
            self.assertEqual(o.value, 4)

        return

    def test_swapped(self):
        for typ in byteswapped_structures:
            self.assertEqual(typ.value.offset, 1)
            o = typ()
            o.value = 4
            self.assertEqual(o.value, 4)

        return


if __name__ == '__main__':
    unittest.main()
return
