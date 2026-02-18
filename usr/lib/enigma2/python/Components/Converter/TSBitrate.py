# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/TSBitrate.py
# Compiled at: 2015-04-12 11:51:35
from Components.Converter.Converter import Converter
from enigma import iServiceInformation, iPlayableService, eTimer, eServiceReference
from Components.Element import cached
from Screens.InfoBar import InfoBar
import os
if os.path.isfile('/usr/lib/enigma2/python/Plugins/Extensions/BitrateViewer/bitratecalc.so'):
    from Plugins.Extensions.BitrateViewer.bitratecalc import eBitrateCalculator
    binaryfound = True
else:
    binaryfound = False

class TSBitrate(Converter, object):
    VBIT = 0
    ABIT = 1
    FORMAT = 2

    def __init__(self, type):
        Converter.__init__(self, type)
        if type == 'VideoBitrate':
            self.type = self.VBIT
        elif type == 'AudioBitrate':
            self.type = self.ABIT
        self.clearData()
        self.initTimer = eTimer()
        self.initTimer_conn = self.initTimer.timeout.connect(self.initBitrateCalc)
        return

    def clearData(self):
        self.videoBitrate = None
        self.audioBitrate = None
        self.video = self.audio = '0 kbit/s'
        self.CHANSEL = None
        return

    def initBitrateCalc(self):
        service = self.source.service
        vpid = apid = dvbnamespace = tsid = onid = -1
        if self.CHANSEL == None:
            self.CHANSEL = InfoBar.instance.servicelist
        ref = self.CHANSEL.servicelist.getCurrent()
        if binaryfound:
            if service:
                serviceInfo = service.info()
                vpid = serviceInfo.getInfo(iServiceInformation.sVideoPID)
                apid = serviceInfo.getInfo(iServiceInformation.sAudioPID)
                tsid = serviceInfo.getInfo(iServiceInformation.sTSID)
                onid = serviceInfo.getInfo(iServiceInformation.sONID)
                dvbnamespace = serviceInfo.getInfo(iServiceInformation.sNamespace)
            if vpid:
                self.videoBitrate = eBitrateCalculator(vpid, ref.toString(), 1000, 1048576)
                self.videoBitrate.callback = self.getVideoBitrateData
            if apid:
                self.audioBitrate = eBitrateCalculator(apid, ref.toString(), 1000, 65536)
                self.audioBitrate.callback = self.getAudioBitrateData
        return

    @cached
    def getText(self):
        if not binaryfound:
            return 'Opps'
        if self.type is self.VBIT:
            return 'Video: %s' % self.video
        if self.type is self.ABIT:
            return 'Audio: %s' % self.audio
        return

    text = property(getText)

    def getVideoBitrateData(self, value, status):
        if status:
            self.video = '%d kbit/s' % value
        else:
            self.videoBitrate = None
        Converter.changed(self, (self.CHANGED_POLL,))
        return

    def getAudioBitrateData(self, value, status):
        if status:
            self.audio = '%d kbit/s' % value
        else:
            self.audioBitrate = None
        Converter.changed(self, (self.CHANGED_POLL,))
        return

    def changed(self, what):
        if what[0] is self.CHANGED_SPECIFIC:
            if what[1] is iPlayableService.evStart or what[1] is iPlayableService.evUpdatedInfo:
                self.initTimer.start(100, True)
            elif what[1] is iPlayableService.evEnd:
                self.clearData()
                Converter.changed(self, what)
        return


return
