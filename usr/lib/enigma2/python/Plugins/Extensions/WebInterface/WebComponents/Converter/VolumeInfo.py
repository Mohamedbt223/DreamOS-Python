# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebComponents/Converter/VolumeInfo.py
# Compiled at: 2025-09-18 23:33:39
from Components.Converter.Converter import Converter
from Components.Element import cached

class VolumeInfo(Converter):
    RESULT = 0
    RESULTTEXT = 1
    VOLUME = 2
    ISMUTED = 3

    def __init__(self, type):
        Converter.__init__(self, type)
        self.type = {'Result': (self.RESULT), 'ResultText': (self.RESULTTEXT), 
           'Volume': (self.VOLUME), 
           'IsMuted': (self.ISMUTED)}[type]
        return

    @cached
    def getText(self):
        volume = self.source.volume
        if self.type is self.RESULT:
            return str(volume[0])
        else:
            if self.type is self.RESULTTEXT:
                return str(volume[1])
            if self.type is self.VOLUME:
                return str(volume[2])
            if self.type is self.ISMUTED:
                return str(volume[3])
            return 'N/A'

        return

    text = property(getText)


return
