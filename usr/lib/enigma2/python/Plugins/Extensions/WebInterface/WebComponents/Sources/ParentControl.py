# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebComponents/Sources/ParentControl.py
# Compiled at: 2025-09-18 23:33:40
from Components.Sources.Source import Source
from Components.ParentalControl import parentalControl
from Components.config import config
from ServiceReference import ServiceReference

class ParentControl(Source):

    def __init__(self, session):
        Source.__init__(self)
        self.session = session
        return

    def command(self):
        print 'ParentControl was called'
        if config.ParentalControl.configured.value:
            parentalControl.open()
            if config.ParentalControl.type.value == 'whitelist':
                servicelist = parentalControl.whitelist
            else:
                servicelist = parentalControl.blacklist
            list = [(str(service_ref), ServiceReference(service_ref).getServiceName()) for service_ref in servicelist]
        else:
            list = []
        print 'list', list
        return list

    list = property(command)
    lut = {'ServiceReference': 0, 'ServiceName': 1}


return
