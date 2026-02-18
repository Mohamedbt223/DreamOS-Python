# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/python2.7/unittest/test/__init__.py
# Compiled at: 2025-09-02 17:07:27
import os, sys, unittest
here = os.path.dirname(__file__)
loader = unittest.defaultTestLoader

def suite():
    suite = unittest.TestSuite()
    for fn in os.listdir(here):
        if fn.startswith('test') and fn.endswith('.py'):
            modname = 'unittest.test.' + fn[:-3]
            __import__(modname)
            module = sys.modules[modname]
            suite.addTest(loader.loadTestsFromModule(module))

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
return
