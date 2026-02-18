# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebComponents/Sources/About.py
# Compiled at: 2025-09-18 23:33:40
from Components.Sources.Source import Source
from Components.Network import iNetworkInfo

class About(Source):

    def __init__(self, session):
        Source.__init__(self)
        self.session = session
        return

    def handleCommand(self, cmd):
        self.result = (False, 'unknown command')
        return

    def command(self):
        ConvertIP = lambda l: '%s.%s.%s.%s' % tuple(l) if len(l) == 4 else '0.0.0.0'
        ifaces = iNetworkInfo.getConfiguredInterfaces()
        for key in ifaces.iterkeys():
            iface = ifaces[key]
            print '[WebComponents.About] iface: %s' % iface
            l = (
             iface.ethernet.mac,
             iface.ipv4.method,
             iface.ipv4.address,
             iface.ipv4.netmask,
             iface.ipv4.gateway)
            break
        else:
            print '[WebComponents.About] no network iface configured!'
            l = ('N/A', 'N/A', 'N/A', 'N/A', 'N/A')

        return (
         l,)

    list = property(command)
    lut = {'lanMac': 0, 'lanDHCP': 1, 
       'lanIP': 2, 
       'lanMask': 3, 
       'lanGW': 4}


return
