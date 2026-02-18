# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/python2.7/ctypes/test/runtests.py
# Compiled at: 2025-09-02 17:07:24
"""Usage: runtests.py [-q] [-r] [-v] [-u resources] [mask]

Run all tests found in this directory, and print a summary of the results.
Command line flags:
  -q     quiet mode: don't print anything while the tests are running
  -r     run tests repeatedly, look for refcount leaks
  -u<resources>
         Add resources to the lits of allowed resources. '*' allows all
         resources.
  -v     verbose mode: print the test currently executed
  -x<test1[,test2...]>
         Exclude specified tests.
  mask   mask to select filenames containing testcases, wildcards allowed
"""
import sys, ctypes.test
if __name__ == '__main__':
    sys.exit(ctypes.test.main(ctypes.test))
return
