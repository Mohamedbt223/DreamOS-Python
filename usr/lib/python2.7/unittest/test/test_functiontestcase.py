# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/python2.7/unittest/test/test_functiontestcase.py
# Compiled at: 2025-09-02 17:07:27
import unittest
from unittest.test.support import LoggingResult

class Test_FunctionTestCase(unittest.TestCase):

    def test_countTestCases(self):
        test = unittest.FunctionTestCase((lambda : None))
        self.assertEqual(test.countTestCases(), 1)
        return

    def test_run_call_order__error_in_setUp(self):
        events = []
        result = LoggingResult(events)

        def setUp():
            events.append('setUp')
            raise RuntimeError('raised by setUp')
            return

        def test():
            events.append('test')
            return

        def tearDown():
            events.append('tearDown')
            return

        expected = ['startTest', 'setUp', 'addError', 'stopTest']
        unittest.FunctionTestCase(test, setUp, tearDown).run(result)
        self.assertEqual(events, expected)
        return

    def test_run_call_order__error_in_test(self):
        events = []
        result = LoggingResult(events)

        def setUp():
            events.append('setUp')
            return

        def test():
            events.append('test')
            raise RuntimeError('raised by test')
            return

        def tearDown():
            events.append('tearDown')
            return

        expected = [4, 5, 6, 7, 8, 
         9]
        unittest.FunctionTestCase(test, setUp, tearDown).run(result)
        self.assertEqual(events, expected)
        return

    def test_run_call_order__failure_in_test(self):
        events = []
        result = LoggingResult(events)

        def setUp():
            events.append('setUp')
            return

        def test():
            events.append('test')
            self.fail('raised by test')
            return

        def tearDown():
            events.append('tearDown')
            return

        expected = [4, 5, 6, 7, 8, 
         9]
        unittest.FunctionTestCase(test, setUp, tearDown).run(result)
        self.assertEqual(events, expected)
        return

    def test_run_call_order__error_in_tearDown(self):
        events = []
        result = LoggingResult(events)

        def setUp():
            events.append('setUp')
            return

        def test():
            events.append('test')
            return

        def tearDown():
            events.append('tearDown')
            raise RuntimeError('raised by tearDown')
            return

        expected = [4, 5, 6, 7, 8, 
         9]
        unittest.FunctionTestCase(test, setUp, tearDown).run(result)
        self.assertEqual(events, expected)
        return

    def test_id(self):
        test = unittest.FunctionTestCase((lambda : None))
        self.assertIsInstance(test.id(), basestring)
        return

    def test_shortDescription__no_docstring(self):
        test = unittest.FunctionTestCase((lambda : None))
        self.assertEqual(test.shortDescription(), None)
        return

    def test_shortDescription__singleline_docstring(self):
        desc = 'this tests foo'
        test = unittest.FunctionTestCase((lambda : None), description=desc)
        self.assertEqual(test.shortDescription(), 'this tests foo')
        return


if __name__ == '__main__':
    unittest.main()
return
