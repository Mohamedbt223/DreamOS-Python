# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/TSRefString.py
from Components.Converter.Converter import Converter
from Components.Element import cached
from Screens.InfoBar import InfoBar

class TSRefString(Converter, object):
    CURRENT = 0
    EVENT = 1

    def __init__(self, type):
        Converter.__init__(self, type)
        self.CHANSEL = None
        self.type = {'CurrentRef': (self.CURRENT), 
           'ServicelistRef': (self.EVENT)}[type]
        return

    @cached
    def getText(self):
        if self.type == self.EVENT:
            return str(self.source.service.toString())
        else:
            if self.type == self.CURRENT:
                if self.CHANSEL == None:
                    self.CHANSEL = InfoBar.instance.servicelist
                vSrv = self.CHANSEL.servicelist.getCurrent()
                return str(vSrv.toString())
            else:
                return 'na'

            return

    text = property(getText)


return
