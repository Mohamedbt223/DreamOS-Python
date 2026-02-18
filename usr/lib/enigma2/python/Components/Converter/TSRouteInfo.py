# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/TSRouteInfo.py
# Compiled at: 2015-04-06 14:11:55
from Components.Converter.Converter import Converter
from Components.Element import cached

class TSRouteInfo(Converter, object):
    Info = 0
    Lan = 1
    Wifi = 2
    Modem = 3

    def __init__(self, type):
        Converter.__init__(self, type)
        if type == 'Info':
            self.type = self.Info
        elif type == 'Lan':
            self.type = self.Lan
        elif type == 'Wifi':
            self.type = self.Wifi
        elif type == '3G':
            self.type = self.Modem
        return

    @cached
    def getBoolean(self):
        info = False
        for line in open('/proc/net/route'):
            if self.type == self.Lan and line.split()[0] == 'eth0' and line.split()[3] == '0003':
                info = True
            elif self.type == self.Wifi and (line.split()[0] == 'wlan0' or line.split()[0] == 'ra0') and line.split()[3] == '0003':
                info = True
            elif self.type == self.Modem and line.split()[0] == 'ppp0' and line.split()[3] == '0003':
                info = True

        return info

    boolean = property(getBoolean)

    @cached
    def getText(self):
        info = ''
        for line in open('/proc/net/route'):
            if self.type == self.Info and line.split()[0] == 'eth0' and line.split()[3] == '0003':
                info = 'lan'
            elif self.type == self.Info and (line.split()[0] == 'wlan0' or line.split()[0] == 'ra0') and line.split()[3] == '0003':
                info = 'wifi'
            elif self.type == self.Info and line.split()[0] == 'ppp0' and line.split()[3] == '0003':
                info = '3g'

        return info

    text = property(getText)

    def changed(self, what):
        Converter.changed(self, what)
        return


return
