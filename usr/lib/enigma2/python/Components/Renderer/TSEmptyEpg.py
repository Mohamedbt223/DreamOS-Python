# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Components/Renderer/TSEmptyEpg.py
# Compiled at: 2015-01-31 17:56:41
from Renderer import Renderer
from enigma import eLabel, eTimer
from Components.VariableText import VariableText
from Components.config import config

class TSEmptyEpg(VariableText, Renderer):

    def __init__(self):
        Renderer.__init__(self)
        VariableText.__init__(self)
        self.EmptyText = 'No EPG Data Available !'
        self.fillTimer = eTimer()
        self.fillTimer_conn = self.fillTimer.timeout.connect(self.__fillText)
        self.backText = 'No EPG Data Available !'
        self.typewriter = 'off'
        self.speed = '300'
        return

    def applySkin(self, desktop, parent):
        attribs = []
        for attrib, value in self.skinAttributes:
            if attrib == 'size':
                self.sizeX = int(value.strip().split(',')[0])
                attribs.append((attrib, value))
            elif attrib == 'emptyText':
                self.EmptyText = value
            elif attrib == 'typewriter':
                self.typewriter = value
            elif attrib == 'speed':
                self.speed = int(value)
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
            try:
                typewriter = config.plugins.TSSkinSetup.typewriter.value
            except:
                pass

            self.text = self.source.text
            if self.instance and self.backText != self.text:
                if self.text == '':
                    self.text = self.EmptyText
                text_width = self.instance.calculateSize().width()
                if text_width > self.sizeX:
                    while text_width > self.sizeX:
                        self.text = self.text[:-1]
                        text_width = self.instance.calculateSize().width()

                    self.text = self.text[:-3] + '...'
                if self.backText != self.text:
                    self.backText = self.text
                    if typewriter and self.typewriter != 'off':
                        try:
                            self.speed = config.plugins.TSSkinSetup.typingSpeed.value
                        except:
                            pass

                        self.text = '_'
                        self.endPoint = len(self.backText)
                        self.posIdx = 0
                        if self.fillTimer.isActive():
                            self.fillTimer.stop()
                        self.fillTimer.start(self.speed, True)
        return

    def __fillText(self):
        self.fillTimer.stop()
        self.posIdx += 1
        if self.posIdx <= self.endPoint:
            self.text = self.backText[:self.posIdx] + '_'
            self.fillTimer.start(50, True)
        else:
            self.text = self.backText
        return


return
