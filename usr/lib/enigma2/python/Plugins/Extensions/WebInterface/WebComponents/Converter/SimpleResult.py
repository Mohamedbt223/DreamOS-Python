# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebComponents/Converter/SimpleResult.py
# Compiled at: 2025-09-18 23:33:39
from Components.Converter.Converter import Converter
from Components.Element import cached

class SimpleResult(Converter):
    RESULT = 0
    RESULTTEXT = 1

    def __init__(self, type):
        Converter.__init__(self, type)
        self.type = {'Result': (self.RESULT), 'ResultText': (self.RESULTTEXT)}[type]
        return

    @cached
    def getText(self):
        result = self.source.result
        if self.type is self.RESULT:
            return str(result[0])
        else:
            if self.type is self.RESULTTEXT:
                return str(result[1])
            return 'N/A'

        return

    text = property(getText)


return
