# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/TSServiceInfo.py
# Compiled at: 2012-09-09 17:47:53
from Components.Converter.Converter import Converter
from enigma import iServiceInformation, iPlayableService
from Components.Element import cached

class TSServiceInfo(Converter, object):
    xAPID = 0
    xVPID = 1
    xSID = 2

    def __init__(self, type):
        Converter.__init__(self, type)
        self.type, self.interesting_events = {'xAPID': (
                   self.xAPID, (iPlayableService.evUpdatedInfo,)), 
           'xVPID': (
                   self.xVPID, (iPlayableService.evUpdatedInfo,)), 
           'xSID': (
                  self.xSID, (iPlayableService.evUpdatedInfo,))}[type]
        return

    def getServiceInfoString(self, info, what, convert=lambda x: '%d' % x):
        v = info.getInfo(what)
        if v == -1:
            return 'N/A'
        if v == -2:
            return info.getInfoString(what)
        return convert(v)

    @cached
    def getText(self):
        service = self.source.service
        info = service and service.info()
        if not info:
            return ''
        if self.type == self.xAPID:
            try:
                return '%0.4X' % int(self.getServiceInfoString(info, iServiceInformation.sAudioPID))
            except:
                return 'N/A'

        elif self.type == self.xVPID:
            try:
                return '%0.4X' % int(self.getServiceInfoString(info, iServiceInformation.sVideoPID))
            except:
                return 'N/A'

        elif self.type == self.xSID:
            try:
                return '%0.4X' % int(self.getServiceInfoString(info, iServiceInformation.sSID))
            except:
                return 'N/A'

        return ''

    text = property(getText)

    def changed(self, what):
        if what[0] != self.CHANGED_SPECIFIC or what[1] in self.interesting_events:
            Converter.changed(self, what)
        return


return
