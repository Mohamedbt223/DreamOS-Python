# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Components/Renderer/TSHDDTemp.py
# Compiled at: 2016-01-08 15:33:42
from Components.VariableText import VariableText
from Tools.Directories import fileExists
from enigma import eLabel
from Renderer import Renderer
from Tools.TSTools import getCmdOutput

class TSHDDTemp(Renderer, VariableText):

    def __init__(self):
        Renderer.__init__(self)
        VariableText.__init__(self)
        self.DescriptionText = 'HDD: '
        return

    GUI_WIDGET = eLabel

    def applySkin(self, desktop, parent):
        attribs = []
        for attrib, value in self.skinAttributes:
            if attrib == 'DescriptionText':
                self.DescriptionText = value
            else:
                attribs.append((attrib, value))

        self.skinAttributes = attribs
        return Renderer.applySkin(self, desktop, parent)

    def changed(self, what):
        if not self.suspended:
            maxtemp = ''
            self.text = ''
            if fileExists('/etc/init.d/hddtemp') and fileExists('/dev/sda'):
                try:
                    maxtemp_str = getCmdOutput('hddtemp /dev/sda').split(': ', 3)
                    maxtemp = maxtemp_str[len(maxtemp_str) - 1]
                except:
                    maxtemp = '?'

                if maxtemp.startswith('drive is sleeping'):
                    maxtemp = 'Stby'
                elif maxtemp.endswith('C'):
                    maxtemp = maxtemp.replace('C', '') + b'\xb0C'
                else:
                    maxtemp = _('N/A')
                self.text = self.DescriptionText + maxtemp
        return

    def onShow(self):
        self.suspended = False
        self.changed(None)
        return

    def onHide(self):
        self.suspended = True
        return


return
