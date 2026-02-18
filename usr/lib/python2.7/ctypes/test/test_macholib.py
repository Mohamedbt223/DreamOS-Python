# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/python2.7/ctypes/test/test_macholib.py
# Compiled at: 2025-09-02 17:07:24
import os, sys, unittest
from ctypes.macholib.dyld import dyld_find

def find_lib(name):
    possible = [
     'lib' + name + '.dylib', name + '.dylib', name + '.framework/' + name]
    for dylib in possible:
        try:
            return os.path.realpath(dyld_find(dylib))
        except ValueError:
            pass

    raise ValueError('%s not found' % (name,))
    return


class MachOTest(unittest.TestCase):

    @unittest.skipUnless(sys.platform == 'darwin', 'OSX-specific test')
    def test_find(self):
        self.assertEqual(find_lib('pthread'), '/usr/lib/libSystem.B.dylib')
        result = find_lib('z')
        self.assertRegexpMatches(result, '.*/lib/libz\\..*.*\\.dylib')
        self.assertEqual(find_lib('IOKit'), '/System/Library/Frameworks/IOKit.framework/Versions/A/IOKit')
        return


if __name__ == '__main__':
    unittest.main()
return
