# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebComponents/Sources/PowerState.py
# Compiled at: 2025-09-18 23:33:40
from Components.Sources.Source import Source

class PowerState(Source):

    def __init__(self, session):
        self.cmd = None
        self.session = session
        Source.__init__(self)
        return

    def handleCommand(self, cmd):
        self.cmd = cmd
        return

    def getStandby(self):
        from Screens.Standby import inStandby
        if inStandby is None:
            return 'false'
        else:
            return 'true'
            return

    def getText(self):
        if self.cmd == '' or self.cmd is None:
            return self.getStandby()
        else:
            try:
                from Screens.Standby import inStandby
                from Screens.Standby import Standby
                type = int(self.cmd)
                if type == -1:
                    return self.getStandby()
                if type == 0:
                    print '[PowerState.py] Standby 0'
                    if inStandby is None:
                        self.session.open(Standby)
                        return 'true'
                    inStandby.Power()
                    return 'false'
                elif type == 4:
                    print '[PowerState.py] Standby 4'
                    if inStandby is not None:
                        inStandby.Power()
                        return 'false'
                    return 'true'
                elif type == 5:
                    print '[PowerState.py] Standby 5'
                    if inStandby is None:
                        self.session.open(Standby)
                        return 'true'
                    return 'false'
                else:
                    if type == 6:
                        print '[PowerState.py] Standby 6'
                        from twisted.internet import reactor
                        from subprocess import call
                        reactor.callLater(1, call, ['killall', '-9', 'enigma2'])
                        return 'true'
                    else:
                        if 0 < type < 4:
                            print '[PowerState.py] TryQuitMainloop'
                            from Screens.Standby import TryQuitMainloop
                            from twisted.internet import reactor
                            reactor.callLater(1, self.session.open, TryQuitMainloop, type)
                            return 'true'
                        print '[PowerState.py] cmd unknown' % type
                        return 'error'

            except ValueError:
                return 'error'

            return

    text = property(getText)


return
