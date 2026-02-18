# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/TSServiceName.py
# Compiled at: 2014-03-23 23:23:12
from Components.Converter.Converter import Converter
from enigma import iServiceInformation, iPlayableService, iPlayableServicePtr
from Components.Element import cached
from Screens.InfoBar import InfoBar

class TSServiceName(Converter, object):
    NAME = 0
    PROVIDER = 1
    REFERENCE = 2

    def __init__(self, type):
        Converter.__init__(self, type)
        if type == 'Provider':
            self.type = self.PROVIDER
        elif type == 'Reference':
            self.type = self.REFERENCE
        else:
            self.type = self.NAME
        return

    def getServiceInfoValue(self, info, what, ref=None):
        v = ref and info.getInfo(ref, what) or info.getInfo(what)
        if v != iServiceInformation.resIsString:
            value = 'N/A'
            if what == iServiceInformation.sServiceref:
                CHANSEL = InfoBar.instance.servicelist
                vSrv = CHANSEL.servicelist.getCurrent()
                value = str(vSrv.toString())
            return value
        return ref and info.getInfoString(ref, what) or info.getInfoString(what)

    @cached
    def getText(self):
        service = self.source.service
        if isinstance(service, iPlayableServicePtr):
            info = service and service.info()
            ref = None
        else:
            info = service and self.source.info
            ref = service
        if info is None:
            return ''
        else:
            if self.type == self.NAME:
                name = ref and info.getName(ref)
                if name is None:
                    name = info.getName()
                return name.replace('\x86', '').replace('\x87', '')
            if self.type == self.PROVIDER:
                return self.getServiceInfoValue(info, iServiceInformation.sProvider, ref)
            if self.type == self.REFERENCE:
                return self.getServiceInfoValue(info, iServiceInformation.sServiceref, ref)
            return

    text = property(getText)

    def changed(self, what):
        if what[0] != self.CHANGED_SPECIFIC or what[1] in (iPlayableService.evStart,):
            Converter.changed(self, what)
        return


return
