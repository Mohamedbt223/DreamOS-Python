# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebComponents/Converter/HddInfo.py
# Compiled at: 2025-09-18 23:33:39
from Components.Converter.Converter import Converter

class HddInfo(Converter):
    MODEL = 0
    CAPACITY = 1
    FREE = 2

    def __init__(self, type):
        Converter.__init__(self, type)
        self.type = {'Model': (self.MODEL), 
           'Capacity': (self.CAPACITY), 
           'Free': (self.FREE)}[type]
        return

    def getText(self):
        hdd = self.source.hdd
        if hdd is not None:
            if self.type == self.MODEL:
                return '%s' % hdd.model()
            if self.type == self.CAPACITY:
                return '%s' % hdd.capacity()
            if self.type == self.FREE:
                if hdd.free() > 1024:
                    free = float(hdd.free()) / float(1024)
                    return '%.3f GB' % free
                else:
                    return '%i MB' % hdd.free()

        return _('N/A')

    text = property(getText)


return
