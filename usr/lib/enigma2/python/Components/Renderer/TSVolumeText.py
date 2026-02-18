# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Components/Renderer/TSVolumeText.py
# Compiled at: 2015-01-31 17:55:50
from Components.VariableText import VariableText
from enigma import eLabel, eDVBVolumecontrol, eTimer
from Renderer import Renderer

class TSVolumeText(Renderer, VariableText):

    def __init__(self):
        Renderer.__init__(self)
        VariableText.__init__(self)
        self.vol_timer = eTimer()
        self.vol_timer_conn = self.vol_timer.timeout.connect(self.pollme)
        return

    GUI_WIDGET = eLabel

    def changed(self, what):
        if not self.suspended:
            self.text = str(eDVBVolumecontrol.getInstance().getVolume())
        return

    def pollme(self):
        self.changed(None)
        return

    def onShow(self):
        self.suspended = False
        self.vol_timer.start(200)
        return

    def onHide(self):
        self.suspended = True
        self.vol_timer.stop()
        return


return
