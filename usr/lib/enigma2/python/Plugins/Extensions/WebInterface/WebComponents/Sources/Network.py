# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebComponents/Sources/Network.py
# Compiled at: 2025-09-18 23:33:40
from Components.Sources.Source import Source
from Components.Network import iNetworkInfo
from Tools.Log import Log

class Interface:

    def __init__(self, name):
        self.name = name
        self.mac = None
        self.dhcp = None
        self.ip = None
        self.netmask = None
        self.gateway = None
        return


class Network(Source):
    LAN = 0
    WLAN = 1

    def __init__(self, device=LAN):
        Source.__init__(self)
        if device is self.LAN:
            self.iface = 'eth0'
        elif device is self.WLAN:
            self.iface = 'ath0'
        return

    ConvertIP = lambda self, l: '%s.%s.%s.%s' % tuple(l) if l and len(l) == 4 else '0.0.0.0'

    def __getInterfaceAttribs(self, iface):
        Log.i(iface)
        attribs = [iface.ethernet.interface, iface.ethernet.mac]
        ip4 = iface.ipv4
        ip6 = iface.ipv6
        if ip4:
            attribs.extend((
             ip4.method,
             ip4.address,
             ip4.netmask,
             ip4.gateway))
        else:
            attribs.extend(['N/A', 'N/A', 'N/A', 'N/A'])
        if ip6:
            attribs.extend((
             ip6.method,
             ip6.address,
             ip6.netmask,
             ip6.gateway))
        else:
            attribs.extend(['N/A', 'N/A', 'N/A', 'N/A'])
        return attribs

    def getInterface(self):
        ifaces = iNetworkInfo.getConfiguredInterfaces()
        Log.i(ifaces)
        for key in ifaces.iterkeys():
            iface = ifaces[key]
            if iface.ethernet.interface == self.iface:
                return self.__getInterfaceAttribs(iface)

        return [
         1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    interface = property(getInterface)

    def getList(self):
        lst = []
        ifaces = iNetworkInfo.getConfiguredInterfaces()
        Log.i(ifaces)
        for key in ifaces.iterkeys():
            iface = ifaces[key]
            lst.append(self.__getInterfaceAttribs(iface))

        return lst

    list = property(getList)
    lut = {'Name': 0, 
       'Mac': 1, 
       'Dhcp': 2, 
       'Ip': 3, 
       'Netmask': 4, 
       'Gateway': 5, 
       'Method6': 6, 
       'Ip6': 7, 
       'Netmask6': 8, 
       'Gateway6': 9}


return
