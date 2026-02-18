# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/Oled_Poll.py
# Compiled at: 2020-08-06 17:48:48
from enigma import eTimer
from Components.Converter.Converter import Converter

class Oled_Poll(object):

    def __init__(self):
        self.__poll_timer = eTimer()
        self.__poll_timer_conn = self.__poll_timer.timeout.connect(self.poll)
        self.__interval = 1000
        self.__enabled = False
        return

    def __setInterval(self, interval):
        self.__interval = interval
        suspended = getattr(self, 'suspended', False)
        if self.__enabled and not suspended:
            self.__poll_timer.start(self.__interval)
        else:
            self.__poll_timer.stop()
        return

    def __setEnable(self, enabled):
        self.__enabled = enabled
        self.poll_interval = self.__interval
        return

    poll_interval = property((lambda self: self.__interval), __setInterval)
    poll_enabled = property((lambda self: self.__enabled), __setEnable)

    def poll(self):
        self.changed((self.CHANGED_POLL,))
        return

    def doSuspend(self, suspended):
        if self.__enabled:
            if suspended:
                self.__poll_timer.stop()
            else:
                self.poll()
                self.poll_enabled = True
        return

    def destroy(self):
        self.__poll_timer_conn = None
        return


class Oled_PollConverter(Oled_Poll, Converter):

    def __init__(self, converterType):
        Converter.__init__(self, converterType)
        Poll.__init__(self)
        return


return
