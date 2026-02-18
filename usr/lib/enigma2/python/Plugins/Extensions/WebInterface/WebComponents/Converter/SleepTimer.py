# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebComponents/Converter/SleepTimer.py
# Compiled at: 2025-09-18 23:33:39
from Components.Converter.Converter import Converter
from Components.Element import cached

class SleepTimer(Converter):
    ENABLED = 0
    TIME = 1
    ACTION = 2
    CONFIRMED = 3
    TEXT = 4

    def __init__(self, type):
        Converter.__init__(self, type)
        self.type = {'Enabled': (self.ENABLED), 'Time': (self.TIME), 
           'Action': (self.ACTION), 
           'Text': (self.TEXT), 
           'Confirmed': (self.CONFIRMED)}[type]
        return

    @cached
    def getText(self):
        timer = self.source.timer
        if self.type is self.ENABLED:
            return str(timer[0])
        else:
            if self.type is self.TIME:
                return str(timer[1])
            if self.type is self.ACTION:
                return str(timer[2])
            if self.type is self.CONFIRMED:
                return str(timer[3])
            if self.type is self.TEXT:
                if timer[4] is not None:
                    return str(timer[4])
                else:
                    return ''

            else:
                return 'N/A'
            return

    text = property(getText)


return
