# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Components/Renderer/TSShowReference.py
# Compiled at: 2014-03-11 21:59:49
from Renderer import Renderer
from enigma import eLabel
from Components.VariableText import VariableText
from enigma import eServiceReference

class TSShowReference(VariableText, Renderer):

    def __init__(self):
        Renderer.__init__(self)
        VariableText.__init__(self)
        return

    GUI_WIDGET = eLabel

    def connect(self, source):
        Renderer.connect(self, source)
        self.changed((self.CHANGED_DEFAULT,))
        return

    def changed(self, what):
        if self.instance:
            self.text = 'Reference: X:X:X:XXXX:XXX:X:XXXXXX:X:X:X'
            if what[0] != self.CHANGED_CLEAR:
                service = self.source.service
                marker = service.flags & eServiceReference.isMarker == eServiceReference.isMarker
                bouquet = service.flags & eServiceReference.flagDirectory == eServiceReference.flagDirectory
                sname = service.toString()
                if not marker and not bouquet and sname is not None and sname != '':
                    if sname[-1] != ':' and ('http' in sname or '//' in sname):
                        self.text = sname.replace(':', '_').replace(' ', '_').replace('%', '_').replace('/', '')
                    else:
                        pos = sname.rfind(':')
                        if pos != -1:
                            sname = sname[:pos].rstrip(':')
                            if '::' not in sname:
                                self.text = 'Reference: ' + sname
        return


return
