# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Components/Renderer/TSMaxTemp.py
# Compiled at: 2015-02-01 19:08:08
from Components.VariableText import VariableText
from Components.Sensors import sensors
from Tools.HardwareInfo import HardwareInfo
from enigma import eLabel
from Renderer import Renderer
from os import popen

class TSMaxTemp(Renderer, VariableText):

    def __init__(self):
        Renderer.__init__(self)
        VariableText.__init__(self)
        if '8000' in HardwareInfo().get_device_name() or '800se' in HardwareInfo().get_device_name() or '500' in HardwareInfo().get_device_name():
            self.ZeigeTemp = True
        else:
            self.ZeigeTemp = False
        self.DescriptionText = 'default'
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
            if self.ZeigeTemp:
                maxtemp = 0
                try:
                    templist = sensors.getSensorsList(sensors.TYPE_TEMPERATURE)
                    tempcount = len(templist)
                    for count in range(tempcount):
                        id = templist[count]
                        tt = sensors.getSensorValue(id)
                        if tt > maxtemp:
                            maxtemp = tt

                except:
                    pass

                if self.DescriptionText == 'default':
                    self.text = 'Temp: ' + str(maxtemp) + b'\xb0C'
                else:
                    self.text = self.DescriptionText + str(maxtemp) + b'\xb0C'
            else:
                loada = 'N/A'
                try:
                    out_line = popen('cat /proc/loadavg').readline().split('.')
                    loada = ' %s %%' % int(out_line[1][:2])
                except:
                    pass

                if self.DescriptionText == 'default':
                    self.text = 'CPU: ' + loada
                else:
                    self.text = self.DescriptionText + loada
        return

    def onShow(self):
        self.suspended = False
        self.changed(None)
        return

    def onHide(self):
        self.suspended = True
        return


return
