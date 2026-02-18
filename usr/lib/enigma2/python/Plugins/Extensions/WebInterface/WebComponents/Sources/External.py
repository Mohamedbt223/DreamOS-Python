# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebComponents/Sources/External.py
# Compiled at: 2025-09-18 23:33:40
from Components.Sources.Source import Source
from Plugins.Extensions.WebInterface.WebChilds import Toplevel

class External(Source):

    def getList(self):
        l = []
        append = l.append
        for child in Toplevel.externalChildren:
            Len = len(child)
            if Len > 5:
                child = (
                 child[0], child[2], child[3], child[4], child[5])
            elif Len == 5:
                child = (
                 child[0], child[2], child[3], child[4], '_blank')
            elif Len == 4:
                child = (
                 child[0], child[2], child[3], False, '_blank')
            elif Len == 3:
                child = (
                 child[0], child[2], 'unknown', False, '_blank')
            elif Len == 2:
                child = (
                 child[0], child[0], 'unknown', False, '_blank')
            else:
                continue
            append(child)

        return l

    list = property(getList)
    lut = {'Path': 0, 
       'Name': 1, 
       'Version': 2, 
       'HasGUI': 3, 
       'GUITarget': 4}


return
