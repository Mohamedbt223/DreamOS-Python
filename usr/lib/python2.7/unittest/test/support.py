# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/python2.7/unittest/test/support.py
# Compiled at: 2025-09-02 17:07:27
import unittest

class TestHashing(object):
    """Used as a mixin for TestCase"""

    def test_hash(self):
        for obj_1, obj_2 in self.eq_pairs:
            try:
                if not hash(obj_1) == hash(obj_2):
                    self.fail('%r and %r do not hash equal' % (obj_1, obj_2))
            except KeyboardInterrupt:
                raise
            except Exception as e:
                self.fail('Problem hashing %r and %r: %s' % (obj_1, obj_2, e))

        for obj_1, obj_2 in self.ne_pairs:
            try:
                if hash(obj_1) == hash(obj_2):
                    self.fail("%s and %s hash equal, but shouldn't" % (
                     obj_1, obj_2))
            except KeyboardInterrupt:
                raise
            except Exception as e:
                self.fail('Problem hashing %s and %s: %s' % (obj_1, obj_2, e))

        return


class TestEquality(object):
    """Used as a mixin for TestCase"""

    def test_eq(self):
        for obj_1, obj_2 in self.eq_pairs:
            self.assertEqual(obj_1, obj_2)
            self.assertEqual(obj_2, obj_1)

        return

    def test_ne(self):
        for obj_1, obj_2 in self.ne_pairs:
            self.assertNotEqual(obj_1, obj_2)
            self.assertNotEqual(obj_2, obj_1)

        return


class LoggingResult(unittest.TestResult):

    def __init__(self, log):
        self._events = log
        super(LoggingResult, self).__init__()
        return

    def startTest(self, test):
        self._events.append('startTest')
        super(LoggingResult, self).startTest(test)
        return

    def startTestRun(self):
        self._events.append('startTestRun')
        super(LoggingResult, self).startTestRun()
        return

    def stopTest(self, test):
        self._events.append('stopTest')
        super(LoggingResult, self).stopTest(test)
        return

    def stopTestRun(self):
        self._events.append('stopTestRun')
        super(LoggingResult, self).stopTestRun()
        return

    def addFailure(self, *args):
        self._events.append('addFailure')
        super(LoggingResult, self).addFailure(*args)
        return

    def addSuccess(self, *args):
        self._events.append('addSuccess')
        super(LoggingResult, self).addSuccess(*args)
        return

    def addError(self, *args):
        self._events.append('addError')
        super(LoggingResult, self).addError(*args)
        return

    def addSkip(self, *args):
        self._events.append('addSkip')
        super(LoggingResult, self).addSkip(*args)
        return

    def addExpectedFailure(self, *args):
        self._events.append('addExpectedFailure')
        super(LoggingResult, self).addExpectedFailure(*args)
        return

    def addUnexpectedSuccess(self, *args):
        self._events.append('addUnexpectedSuccess')
        super(LoggingResult, self).addUnexpectedSuccess(*args)
        return


class ResultWithNoStartTestRunStopTestRun(object):
    """An object honouring TestResult before startTestRun/stopTestRun."""

    def __init__(self):
        self.failures = []
        self.errors = []
        self.testsRun = 0
        self.skipped = []
        self.expectedFailures = []
        self.unexpectedSuccesses = []
        self.shouldStop = False
        return

    def startTest(self, test):
        return

    def stopTest(self, test):
        return

    def addError(self, test):
        return

    def addFailure(self, test):
        return

    def addSuccess(self, test):
        return

    def wasSuccessful(self):
        return True


return
