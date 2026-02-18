# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Components/Renderer/TSLcdRoller.py
# Compiled at: 2015-01-24 21:06:09
from Renderer import Renderer
from enigma import eLabel
from enigma import ePoint, eTimer
from Components.VariableText import VariableText
from Tools.HardwareInfo import HardwareInfo

class TSLcdRoller(VariableText, Renderer):

    def __init__(self):
        Renderer.__init__(self)
        VariableText.__init__(self)
        self.EmptyText = 'No EPG Data Available !'
        self.direct = 'R'
        self.x = 2
        self.stt = 0
        self.rep_stt = 2
        self.oled_size = 132
        if HardwareInfo().get_device_name() == 'dm820':
            self.oled_size = 96
        self.moveLCD1Text = eTimer()
        self.moveLCD1Text_conn = self.moveLCD1Text.timeout.connect(self.__moveLCD1TextRun)
        return

    def applySkin(self, desktop, parent):
        attribs = []
        for attrib, value in self.skinAttributes:
            if attrib == 'position':
                self.posY = int(value.strip().split(',')[1])
                attribs.append((attrib, value))
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
            self.text = self.source.text
        if self.instance:
            if self.text == '':
                self.text = self.EmptyText
            text_width = self.instance.calculateSize().width()
            if self.moveLCD1Text.isActive():
                self.moveLCD1Text.stop()
            if text_width > self.oled_size:
                self.end = self.oled_size - text_width - 15
                self.x = 2
                self.direct = 'R'
                self.instance.move(ePoint(self.x, self.posY))
                self.moveLCD1Text.start(2000)
            else:
                self.instance.move(ePoint(2, self.posY))
        return

    def __moveLCD1TextRun(self):
        self.moveLCD1Text.stop()
        if self.x != self.end and self.direct == 'R':
            self.x = self.x - 1
        elif self.x != 2 and self.direct == 'L':
            self.x = self.x + 1
        elif self.x == 2:
            self.direct = 'R'
            self.stt = self.stt + 1
        elif self.x == self.end:
            self.direct = 'L'
            self.stt = self.stt + 1
        self.instance.move(ePoint(self.x, self.posY))
        if self.stt > self.rep_stt:
            self.stt = 0
            self.text = self.text[:12] + '..'
            self.instance.move(ePoint(2, self.posY))
        else:
            self.moveLCD1Text.start(60)
        return


return
