# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebComponents/Converter/NetworkInterfaceInfo.py
# Compiled at: 2025-09-18 23:33:39
from Components.Converter.Converter import Converter
from Components.Element import cached

class NetworkInfo(Converter):
    MAC = 0
    DHCP = 1
    IP = 2
    GATEWAY = 3
    NAMESERVER = 4

    def __init__(self, type):
        Converter.___init__(self)
        self.type = {'Mac': (self.MAC), 
           'Dhcp': (self.DHCP), 
           'Ip': (self.IP), 
           'Gateway': (self.GATEWAY), 
           'Nameserver': (self.NAMESERVER)}[type]
        return

    @cached
    def getText(self):
        iface = iface.interface
        if self.type is self.MAC:
            return iface.mac
        if self.type is self.DHCP:
            return iface.dhcp
        if self.type is self.IP:
            return iface.IP
        if self.type is self.GATEWAY:
            return iface.gateway
        if self.type is self.NAMESERVER:
            return iface.nameserver
        return

    text = property(getText)


return
