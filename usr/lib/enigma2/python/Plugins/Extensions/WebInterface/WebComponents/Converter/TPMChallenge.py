# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebComponents/Converter/TPMChallenge.py
# Compiled at: 2025-09-18 23:33:39
from Components.Converter.Converter import Converter
from Components.Element import cached

class TPMChallenge(Converter):
    L2C = 0
    L3C = 1
    VALUE = 2
    RESULT = 3
    TEXT = 4

    def __init__(self, type):
        Converter.__init__(self, type)
        self.type = {'Level2Cert': (self.L2C), 'Level3Cert': (self.L3C), 
           'Value': (self.VALUE), 
           'Result': (self.RESULT), 
           'Text': (self.TEXT)}[type]
        return

    @cached
    def getText(self):
        res = self.source.tpm_result
        if self.type is self.L2C:
            return str(res[0])
        else:
            if self.type is self.L3C:
                return str(res[1])
            if self.type is self.VALUE:
                return str(res[2])
            if self.type is self.RESULT:
                return str(res[3])
            if self.type is self.TEXT:
                return str(res[4])
            return 'N/A'

        return

    text = property(getText)


return
