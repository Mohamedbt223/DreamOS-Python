# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebComponents/Sources/StopService.py
# Compiled at: 2025-09-18 23:33:40
from Components.Sources.Source import Source

class StopService(Source):

    def __init__(self, session):
        Source.__init__(self)
        self.session = session
        return

    def pipAvailable(self):
        try:
            self.session.pipshown
            pipavailable = True
        except:
            pipavailable = False

        return pipavailable

    def command(self):
        currentServiceRef = self.session.nav.getCurrentlyPlayingServiceReference()
        if currentServiceRef is not None:
            text = currentServiceRef.toString()
        else:
            text = 'N/A'
        self.session.nav.stopService()
        if self.pipAvailable():
            if self.session.pipshown:
                self.session.pipshown = False
                self.session.deleteDialog(self.session.pip)
                del self.session.pip
        return text

    text = property(command)


return
