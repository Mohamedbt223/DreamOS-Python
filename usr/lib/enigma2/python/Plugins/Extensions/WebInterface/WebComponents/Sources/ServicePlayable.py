# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebComponents/Sources/ServicePlayable.py
# Compiled at: 2025-09-18 23:33:40
from enigma import eServiceCenter, eServiceReference
from Components.Sources.Source import Source

class ServicePlayable(Source):
    SINGLE = 0
    BOUQUET = 1

    def __init__(self, session, type=SINGLE):
        Source.__init__(self)
        self.session = session
        self.sci = eServiceCenter.getInstance()
        self.command = None
        self.info = None
        self.type = type
        return

    def handleCommand(self, cmd):
        self.command = cmd
        return

    def convertStrTrueFalse(self, int):
        if int > 0:
            return str(True)
        else:
            return str(False)

        return

    def isServicePlayable(self, refToPlay, refPlaying=None):
        if self.info is None:
            self.info = self.sci.info(refToPlay)
        if refPlaying is None:
            return self.convertStrTrueFalse(self.info.isPlayable(refToPlay))
        else:
            return self.convertStrTrueFalse(self.info.isPlayable(refToPlay, refPlaying))
            return false

    def getPlayableServices(self, refToPlay, refPlaying=None):
        list = []
        if self.type == self.BOUQUET:
            slist = self.sci.list(refToPlay)
            services = slist and slist.getContent('S', True)
            if services:
                list.extend([(service, self.isServicePlayable(eServiceReference(service), refPlaying)) for service in services])
        else:
            playable = self.isServicePlayable(refToPlay, refPlaying)
            list.append((refToPlay.toString(), playable))
        return list

    def getList(self):
        list = []
        if 'sRef' in self.command:
            refToPlay = eServiceReference(self.command['sRef'])
            if 'sRefPlaying' in self.command:
                refPlaying = eServiceReference(self.command['sRef'])
                list = self.getPlayableServices(refToPlay, refPlaying)
            else:
                list = self.getPlayableServices(refToPlay)
        return list

    list = property(getList)
    lut = {'ServiceReference': 0, 'ServicePlayable': 1}


return
