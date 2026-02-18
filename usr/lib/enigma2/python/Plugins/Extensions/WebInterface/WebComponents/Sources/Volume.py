# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebComponents/Sources/Volume.py
# Compiled at: 2025-09-18 23:33:40
from enigma import eDVBVolumecontrol
from Components.Sources.Source import Source
from GlobalActions import globalActionMap
from Components.VolumeControl import VolumeControl

class Volume(Source):

    def __init__(self, session):
        global globalActionMap
        Source.__init__(self)
        self.actionmap = globalActionMap
        self.volctrl = eDVBVolumecontrol.getInstance()
        self.vol = (True, 'State', self.volctrl.getVolume(), self.volctrl.isMuted())
        return

    def handleCommand(self, cmd):
        l = []
        if cmd == 'state':
            l.extend((True, _('State')))
        elif cmd == 'up':
            self.actionmap.actions['volumeUp']()
            l.extend((True, _('Volume changed')))
        elif cmd == 'down':
            self.actionmap.actions['volumeDown']()
            l.extend((True, _('Volume changed')))
        elif cmd == 'mute':
            self.actionmap.actions['volumeMute']()
            l.extend((True, _('Mute toggled')))
        elif cmd.startswith('set'):
            try:
                targetvol = int(cmd[3:])
                if targetvol > 100:
                    targetvol = 100
                if targetvol < 0:
                    targetvol = 0
                self.volctrl.setVolume(targetvol, targetvol)
                l.extend((True, _('Volume set to %i') % targetvol))
            except ValueError:
                l.extend((False, _("Wrong parameter format 'set=%s'. Use set=set15") % cmd))

        else:
            l.extend((False, _('Unknown Volume command %s') % cmd))
        l.extend((self.volctrl.getVolume(), self.volctrl.isMuted()))
        self.vol = l
        return

    volume = property((lambda self: self.vol))


return
