# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebComponents/Sources/Hdd.py
# Compiled at: 2025-09-18 23:33:40
from Components.Sources.Source import Source
from Components.Harddisk import harddiskmanager

class Hdd(Source):

    def __init__(self, devicecount=0):
        Source.__init__(self)
        self.devicecount = devicecount
        return

    def getHddData(self):
        if harddiskmanager.hdd:
            return harddiskmanager.hdd[0]
        else:
            return
            return

    hdd = property(getHddData)

    def getList(self):
        disks = []
        for hdd in harddiskmanager.hdd:
            model = str(hdd.model())
            capacity = str(hdd.capacity())
            if hdd.free() <= 1024:
                free = '%i MB' % hdd.free()
            else:
                free = hdd.free() / float(1024)
                free = '%.3f GB' % free
            disks.append((model, capacity, free))

        return disks

    list = property(getList)
    lut = {'Model': 0, 'Capacity': 1, 
       'Free': 2}


return
