# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebComponents/Sources/SwitchService.py
# Compiled at: 2025-09-18 23:33:40
from enigma import eServiceReference, iPlayableServicePtr
from Components.Sources.Source import Source
from Components.Converter import ServiceName
from Components.config import config
from Screens.InfoBar import InfoBar, MoviePlayer
from Tools.Log import Log

class SwitchService(Source):

    def __init__(self, session):
        Source.__init__(self)
        self.session = session
        self.info = None
        self.res = (False, _('Obligatory parameter sRef is missing'))
        return

    def handleCommand(self, cmd):
        self.res = self.switchService(cmd)
        return

    def playService(self, ref, root=None):
        from Screens.InfoBar import InfoBar
        if root and InfoBar.instance:
            try:
                InfoBar.instance.servicelist.zap(ref, root)
                return
            except:
                try:
                    from types import MethodType

                    def zap(self, nref=None, root=None):
                        self.revertMode = None
                        ref = self.session.nav.getCurrentlyPlayingServiceReference()
                        if not nref:
                            nref = self.getCurrentSelection()
                        if root:
                            if not self.preEnterPath(root):
                                self.clearPath()
                                self.enterPath(eServiceReference(root))
                        if ref is None or ref != nref:
                            self.new_service_played = True
                            self.session.nav.playService(nref)
                            self.saveRoot()
                            self.saveChannel(nref)
                            config.servicelist.lastmode.save()
                            self.addToHistory(nref)
                        return

                    InfoBar.instance.servicelist.zap = MethodType(zap, InfoBar.instance.servicelist)
                    InfoBar.instance.servicelist.zap(ref, root)
                    return
                except:
                    Log.w('Patch failed! Will fallback primitive zap')

        self.session.nav.playService(ref)
        return

    def switchService(self, cmd):
        print '[SwitchService] ref=%s, root=%s' % (cmd['sRef'], cmd['root'])
        root = cmd['root']
        if config.plugins.Webinterface.allowzapping.value:
            from Screens.Standby import inStandby
            if inStandby == None:
                if cmd['sRef']:
                    pc = config.ParentalControl.configured.value
                    if pc:
                        config.ParentalControl.configured.value = False
                    eref = eServiceReference(cmd['sRef'])
                    if cmd['title']:
                        eref.setName(cmd['title'])
                    isRec = eref.getPath()
                    isRec = isRec and isRec.startswith('/')
                    if not isRec:
                        if isinstance(self.session.current_dialog, MoviePlayer):
                            self.session.current_dialog.lastservice = eref
                            self.session.current_dialog.close()
                        self.playService(eref, root)
                    elif isRec:
                        if isinstance(self.session.current_dialog, InfoBar):
                            self.session.open(MoviePlayer, eref)
                        else:
                            self.playService(eref, root)
                    if pc:
                        config.ParentalControl.configured.value = pc
                    name = cmd['sRef']
                    if cmd['title'] is None:
                        service = self.session.nav.getCurrentService()
                        info = None
                        if isinstance(service, iPlayableServicePtr):
                            info = service and service.info()
                            ref = None
                        if info != None:
                            name = ref and info.getName(ref)
                            if name is None:
                                name = info.getName()
                            name.replace('\x86', '').replace('\x87', '')
                    elif eref.getName() != '':
                        name = eref.getName()
                    return (
                     True, _("Active service is now '%s'") % name)
                else:
                    return (
                     False, _("Obligatory parameter 'sRef' is missing"))

            else:
                return (
                 False, _('Cannot zap while device is in Standby'))
        else:
            return (
             False, _('Zapping is disabled in WebInterface Configuration'))
        return

    result = property((lambda self: self.res))


return
