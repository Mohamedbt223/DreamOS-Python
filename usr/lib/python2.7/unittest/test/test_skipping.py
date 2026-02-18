# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/python2.7/unittest/test/test_skipping.py
# Compiled at: 2025-09-02 17:07:27
import unittest
from unittest.test.support import LoggingResult

class Test_TestSkipping(unittest.TestCase):

    def test_skipping(self):

        class Foo(unittest.TestCase):

            def test_skip_me(self):
                self.skipTest('skip')
                return

        events = []
        result = LoggingResult(events)
        test = Foo('test_skip_me')
        test.run(result)
        self.assertEqual(events, ['startTest', 'addSkip', 'stopTest'])
        self.assertEqual(result.skipped, [(test, 'skip')])

        class Foo(unittest.TestCase):

            def setUp(self):
                self.skipTest('testing')
                return

            def test_nothing(self):
                return

        events = []
        result = LoggingResult(events)
        test = Foo('test_nothing')
        test.run(result)
        self.assertEqual(events, ['startTest', 'addSkip', 'stopTest'])
        self.assertEqual(result.skipped, [(test, 'testing')])
        self.assertEqual(result.testsRun, 1)
        return

    def test_skipping_decorators(self):
        op_table = ((unittest.skipUnless, False, True),
         (
          unittest.skipIf, True, False))
        for deco, do_skip, dont_skip in op_table:

            class Foo(unittest.TestCase):

                @deco(do_skip, 'testing')
                def test_skip(self):
                    return

                @deco(dont_skip, 'testing')
                def test_dont_skip(self):
                    return

            test_do_skip = Foo('test_skip')
            test_dont_skip = Foo('test_dont_skip')
            suite = unittest.TestSuite([test_do_skip, test_dont_skip])
            events = []
            result = LoggingResult(events)
            suite.run(result)
            self.assertEqual(len(result.skipped), 1)
            expected = [6, 7, 8, 
             6, 9, 8]
            self.assertEqual(events, expected)
            self.assertEqual(result.testsRun, 2)
            self.assertEqual(result.skipped, [(test_do_skip, 'testing')])
            self.assertTrue(result.wasSuccessful())

        return

    def test_skip_class(self):

        @unittest.skip('testing')
        class record(unittest.TestCase):

            def test_1(self):
                record.append(1)
                return

        record = []
        result = unittest.TestResult()
        test = Foo('test_1')
        suite = unittest.TestSuite([test])
        suite.run(result)
        self.assertEqual(result.skipped, [(test, 'testing')])
        self.assertEqual(record, [])
        return

    def test_skip_non_unittest_class_old_style(self):

        @unittest.skip('testing')
        class record:

            def test_1(self):
                record.append(1)
                return

        class Foo(Mixin, unittest.TestCase):
            pass

        record = []
        result = unittest.TestResult()
        test = Foo('test_1')
        suite = unittest.TestSuite([test])
        suite.run(result)
        self.assertEqual(result.skipped, [(test, 'testing')])
        self.assertEqual(record, [])
        return

    def test_skip_non_unittest_class_new_style(self):

        @unittest.skip('testing')
        class record(object):

            def test_1(self):
                record.append(1)
                return

        class Foo(Mixin, unittest.TestCase):
            pass

        record = []
        result = unittest.TestResult()
        test = Foo('test_1')
        suite = unittest.TestSuite([test])
        suite.run(result)
        self.assertEqual(result.skipped, [(test, 'testing')])
        self.assertEqual(record, [])
        return

    def test_expected_failure(self):

        class Foo(unittest.TestCase):

            @unittest.expectedFailure
            def test_die(self):
                self.fail('help me!')
                return

        events = []
        result = LoggingResult(events)
        test = Foo('test_die')
        test.run(result)
        self.assertEqual(events, [
         'startTest', 'addExpectedFailure', 'stopTest'])
        self.assertEqual(result.expectedFailures[0][0], test)
        self.assertTrue(result.wasSuccessful())
        return

    def test_unexpected_success(self):

        class Foo(unittest.TestCase):

            @unittest.expectedFailure
            def test_die(self):
                return

        events = []
        result = LoggingResult(events)
        test = Foo('test_die')
        test.run(result)
        self.assertEqual(events, [
         'startTest', 'addUnexpectedSuccess', 'stopTest'])
        self.assertFalse(result.failures)
        self.assertEqual(result.unexpectedSuccesses, [test])
        self.assertTrue(result.wasSuccessful())
        return

    def test_skip_doesnt_run_setup(self):

        class Foo(unittest.TestCase):
            wasSetUp = False
            wasTornDown = False

            def setUp(self):
                Foo.wasSetUp = True
                return

            def tornDown(self):
                Foo.wasTornDown = True
                return

            @unittest.skip('testing')
            def test_1(self):
                return

        result = unittest.TestResult()
        test = Foo('test_1')
        suite = unittest.TestSuite([test])
        suite.run(result)
        self.assertEqual(result.skipped, [(test, 'testing')])
        self.assertFalse(Foo.wasSetUp)
        self.assertFalse(Foo.wasTornDown)
        return

    def test_decorated_skip(self):

        def decorator(func):

            def inner(*a):
                return func(*a)

            return inner

        class Foo(unittest.TestCase):

            @decorator
            @unittest.skip('testing')
            def test_1(self):
                return

        result = unittest.TestResult()
        test = Foo('test_1')
        suite = unittest.TestSuite([test])
        suite.run(result)
        self.assertEqual(result.skipped, [(test, 'testing')])
        return


if __name__ == '__main__':
    unittest.main()
return
