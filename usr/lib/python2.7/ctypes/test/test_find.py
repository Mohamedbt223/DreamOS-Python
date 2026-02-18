# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/python2.7/ctypes/test/test_find.py
# Compiled at: 2025-09-02 17:07:24
import unittest, os, sys
from ctypes import *
from ctypes.util import find_library
from ctypes.test import is_resource_enabled
if sys.platform == 'win32':
    lib_gl = find_library('OpenGL32')
    lib_glu = find_library('Glu32')
    lib_gle = None
elif sys.platform == 'darwin':
    lib_gl = lib_glu = find_library('OpenGL')
    lib_gle = None
else:
    lib_gl = find_library('GL')
    lib_glu = find_library('GLU')
    lib_gle = find_library('gle')
if is_resource_enabled('printing'):
    if lib_gl or lib_glu or lib_gle:
        print 'OpenGL libraries:'
        for item in (('GL', lib_gl),
         (
          'GLU', lib_glu),
         (
          'gle', lib_gle)):
            print '\t', item

class Test_OpenGL_libs(unittest.TestCase):

    def setUp(self):
        self.gl = self.glu = self.gle = None
        if lib_gl:
            try:
                self.gl = CDLL(lib_gl, mode=RTLD_GLOBAL)
            except OSError:
                pass

        if lib_glu:
            try:
                self.glu = CDLL(lib_glu, RTLD_GLOBAL)
            except OSError:
                pass

        if lib_gle:
            try:
                self.gle = CDLL(lib_gle)
            except OSError:
                pass

        return

    def tearDown(self):
        self.gl = self.glu = self.gle = None
        return

    @unittest.skipUnless(lib_gl, 'lib_gl not available')
    def test_gl(self):
        if self.gl:
            self.gl.glClearIndex
        return

    @unittest.skipUnless(lib_glu, 'lib_glu not available')
    def test_glu(self):
        if self.glu:
            self.glu.gluBeginCurve
        return

    @unittest.skipUnless(lib_gle, 'lib_gle not available')
    def test_gle(self):
        if self.gle:
            self.gle.gleGetJoinStyle
        return


@unittest.skip('test disabled')
@unittest.skipUnless(os.name == 'posix' and sys.platform != 'darwin', 'test not suitable for this platform')
class LoadLibs(unittest.TestCase):

    def test_libm(self):
        import math
        libm = cdll.libm
        sqrt = libm.sqrt
        sqrt.argtypes = (c_double,)
        sqrt.restype = c_double
        self.assertEqual(sqrt(2), math.sqrt(2))
        return


if __name__ == '__main__':
    unittest.main()
return
