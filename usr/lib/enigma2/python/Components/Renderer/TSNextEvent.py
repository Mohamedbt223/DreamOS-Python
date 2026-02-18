# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Components/Renderer/TSNextEvent.py
# Compiled at: 2012-09-08 22:34:58
from Components.VariableText import VariableText
from enigma import eLabel, eEPGCache
from Components.config import config
from Renderer import Renderer
from time import localtime

class TSNextEvent(VariableText, Renderer):

    def __init__(self):
        Renderer.__init__(self)
        VariableText.__init__(self)
        self.epgcache = eEPGCache.getInstance()
        self.sizeX = 728
        self.descText = ' >>> '
        return

    def applySkin(self, desktop, parent):
        attribs = []
        for attrib, value in self.skinAttributes:
            if attrib == 'size':
                self.sizeX = int(value.strip().split(',')[0])
                attribs.append((attrib, value))
            elif attrib == 'descText':
                self.descText = value
            else:
                attribs.append((attrib, value))

        self.skinAttributes = attribs
        return Renderer.applySkin(self, desktop, parent)

    GUI_WIDGET = eLabel

    def connect(self, source):
        Renderer.connect(self, source)
        self.changed((self.CHANGED_DEFAULT,))
        return

    def changed(self, what):
        if what[0] == self.CHANGED_CLEAR:
            self.text = ''
        else:
            ref = self.source.service
            info = ref and self.source.info
            if info is None:
                self.text = ''
                return
            ENext = ''
            eventNext = self.epgcache.lookupEvent(['IBDCTSERNX', (ref.toString(), 1, -1)])
            if eventNext:
                if eventNext[0][4]:
                    t = localtime(eventNext[0][1])
                    duration = '(%d min)' % (eventNext[0][2] / 60)
                    ENext = self.descText + '%02d:%02d  %s  %s' % (t[3], t[4], duration, eventNext[0][4])
            self.text = ENext
            if self.instance:
                text_width = self.instance.calculateSize().width()
                if text_width > self.sizeX:
                    while text_width > self.sizeX:
                        self.text = self.text[:-1]
                        text_width = self.instance.calculateSize().width()

                    self.text = self.text[:-3] + '...'
        return


return
