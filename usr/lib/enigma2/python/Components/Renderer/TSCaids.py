# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Components/Renderer/TSCaids.py
# Compiled at: 2012-09-08 16:17:39
from Renderer import Renderer
from enigma import eCanvas, eRect, gFont
from skin import parseColor, parseFont
from Components.config import config

class TSCaids(Renderer):
    GUI_WIDGET = eCanvas

    def __init__(self):
        Renderer.__init__(self)
        self.foregroundColor = parseColor('#ffffff')
        self.noColor = self.foregroundColor
        self.backgroundColor = parseColor('#171717')
        self.emmColor = parseColor('#f23d21')
        self.ecmColor = parseColor('#389416')
        self.ftaColor = parseColor('#389416')
        self.font = gFont('Regular', 20)
        self.offset = 2
        self.fta = 'off'
        self.ftaText = ''
        self.ftaFont = gFont('Regular', 20)
        self.size = 150
        self.vOffset = 0
        return

    def pull_updates(self):
        if self.instance is None:
            return
        else:
            self.instance.clear(self.backgroundColor)
            caidlist = self.source.getCaidlist
            if caidlist is None:
                return
            self.draw(caidlist)
            return

    def draw(self, caidlist):
        offset = 0
        iscrypted = 0
        pointSize = self.font.pointSize
        caidlength = self.size.width()
        enabled_bg = config.plugins.TSSkinSetup.CaidsColoredBackgroud.value
        for key in caidlist:
            if caidlist[key][0]:
                iscrypted = 1
                length = len(caidlist[key][0]) * pointSize
                if caidlist[key][1] == 0:
                    bg = self.backgroundColor
                    self.instance.fillRect(eRect(offset + 1, 2, length - 1, pointSize), bg)
                    self.instance.writeText(eRect(offset + 1, 0 + int(self.vOffset), length - 1, pointSize), self.noColor, bg, self.font, caidlist[key][0], 2)
                    offset = offset + self.offset + length
                elif caidlist[key][1] == 1:
                    if enabled_bg:
                        bg = self.emmColor
                        fg = self.foregroundColor
                    else:
                        bg = self.backgroundColor
                        fg = self.emmColor
                    self.instance.fillRect(eRect(offset + 1, 2, length - 1, pointSize), bg)
                    self.instance.writeText(eRect(offset + 1, 0 + int(self.vOffset), length - 1, pointSize), fg, bg, self.font, caidlist[key][0], 2)
                    offset = offset + self.offset + length
                else:
                    if enabled_bg:
                        bg = self.ecmColor
                        fg = self.foregroundColor
                    else:
                        bg = self.backgroundColor
                        fg = self.ecmColor
                    self.instance.fillRect(eRect(offset + 1, 2, length - 1, pointSize), bg)
                    self.instance.writeText(eRect(offset + 1, 0 + int(self.vOffset), length - 1, pointSize), fg, bg, self.font, caidlist[key][0], 2)
                    offset = offset + self.offset + length

        if iscrypted == 0:
            if self.fta == 'on':
                ftaPointSize = self.ftaFont.pointSize
                length = len(self.ftaText) * ftaPointSize
                self.instance.writeText(eRect(-40, 0 + int(self.vOffset), length - 1, pointSize), self.ftaColor, self.backgroundColor, self.ftaFont, self.ftaText, 2)
        return

    def changed(self, what):
        self.pull_updates()
        return

    def applySkin(self, desktop, parent):
        attribs = []
        from enigma import eSize

        def parseSize(str):
            x, y = str.split(',')
            return eSize(int(x), int(y))

        for attrib, value in self.skinAttributes:
            if attrib == 'size':
                self.instance.setSize(parseSize(value))
                self.size = parseSize(value)
                attribs.append((attrib, value))
            elif attrib == 'backgroundColor':
                self.backgroundColor = parseColor(value)
            elif attrib == 'emmColor':
                self.emmColor = parseColor(value)
            elif attrib == 'ecmColor':
                self.ecmColor = parseColor(value)
            elif attrib == 'font':
                self.font = parseFont(value, ((1, 1), (1, 1)))
            elif attrib == 'ftaFont':
                self.ftaFont = parseFont(value, ((1, 1), (1, 1)))
            elif attrib == 'foregroundColor':
                self.foregroundColor = parseColor(value)
            elif attrib == 'noColor':
                self.noColor = parseColor(value)
            elif attrib == 'ftaColor':
                self.ftaColor = parseColor(value)
            elif attrib == 'ftaText':
                self.ftaText = value
            elif attrib == 'fta':
                self.fta = value
            elif attrib == 'vOffsetText':
                self.vOffset = value
            else:
                attribs.append((attrib, value))

        self.skinAttributes = attribs
        return Renderer.applySkin(self, desktop, parent)


return
