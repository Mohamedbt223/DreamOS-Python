# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebBouquetEditor/WebComponents/Sources/ProtectionSettings.py
# Compiled at: 2025-09-18 23:33:38
from Components.Sources.Source import Source
from enigma import eServiceCenter, eServiceReference
from Components.ParentalControl import LIST_BLACKLIST
from Components.config import config

class ProtectionSettings(Source):

    def __init__(self):
        Source.__init__(self)
        return

    def getProtectionSettings(self):
        configured = config.ParentalControl.configured.value
        if configured:
            if config.ParentalControl.type.value == LIST_BLACKLIST:
                type = '0'
            else:
                type = '1'
            setuppin = config.ParentalControl.setuppin.value
            setuppinactive = config.ParentalControl.setuppinactive.value
        else:
            type = ''
            setuppin = ''
            setuppinactive = ''
        return [
         (
          configured, type, setuppinactive, setuppin)]

    def handleCommand(self, cmd):
        self.getProtectionSettings()
        return

    list = property(getProtectionSettings)
    lut = {'Configured': 0, 'Type': 1, 'SetupPinActive': 2, 'SetupPin': 3}


return
