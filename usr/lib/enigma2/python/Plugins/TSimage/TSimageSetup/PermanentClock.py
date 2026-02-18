# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/TSimageSetup/PermanentClock.py
# Compiled at: 2016-11-22 07:46:06
from Components.ActionMap import ActionMap
from Components.config import config, ConfigInteger, ConfigSubsection, ConfigYesNo
from Components.Language import language
from Components.MenuList import MenuList
from enigma import ePoint, eTimer, getDesktop
from os import environ
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Tools.Directories import resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
import gettext
config.plugins.PermanentClock = ConfigSubsection()
desktopSize = getDesktop(0).size()
SKIN_1280 = '\n\t<screen position="0,0" size="120,30" zPosition="5" backgroundColor="#ff111111" title="%s" flags="wfNoBorder">\n\t\t<widget source="global.CurrentTime" render="Label" position="1,1" size="120,30" foregroundColor="#00ffffff" backgroundColor="#ff000000" font="Regular;26" valign="center" halign="center" transparent="1">\n\t\t\t<convert type="ClockToText">Default</convert>\n\t\t</widget>\n\t</screen>' % _('Permanent Clock')
SKIN_1920 = '\n\t<screen position="0,0" size="200,50" zPosition="5" backgroundColor="#ff111111" title="%s" flags="wfNoBorder">\n\t\t<widget source="global.CurrentTime" render="Label" position="1,1" size="200,50" foregroundColor="#00ffffff" backgroundColor="#ff000000" font="Regular;34" valign="center" halign="center" transparent="1">\n\t\t\t<convert type="ClockToText">Default</convert>\n\t\t</widget>\n\t</screen>' % _('Permanent Clock')
if desktopSize.width() == 1920:
    SKIN = SKIN_1920
else:
    SKIN = SKIN_1280

class PermanentClockScreen(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self.skin = SKIN
        self.onShow.append(self.movePosition)
        return

    def movePosition(self):
        if self.instance:
            self.instance.move(ePoint(config.plugins.PermanentClock.position_x.value, config.plugins.PermanentClock.position_y.value))
        return


class PermanentClock:

    def __init__(self):
        self.dialog = None
        return

    def gotSession(self, session):
        self.dialog = session.instantiateDialog(PermanentClockScreen)
        self.showHide()
        return

    def changeVisibility(self):
        if config.plugins.PermanentClock.enabled.value:
            config.plugins.PermanentClock.enabled.value = False
        else:
            config.plugins.PermanentClock.enabled.value = True
        config.plugins.PermanentClock.enabled.save()
        self.showHide()
        return

    def showHide(self):
        if config.plugins.PermanentClock.enabled.value:
            self.dialog.show()
        else:
            self.dialog.hide()
        return


pClock = PermanentClock()

class PermanentClockPositioner(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self.skin = SKIN
        self['actions'] = ActionMap(['WizardActions'], {'left': (self.left), 'up': (self.up), 
           'right': (self.right), 
           'down': (self.down), 
           'ok': (self.ok), 
           'back': (self.exit)}, -1)
        desktop = getDesktop(0)
        self.desktopWidth = desktop.size().width()
        self.desktopHeight = desktop.size().height()
        self.moveTimer = eTimer()
        self.moveTimer_conn = self.moveTimer.timeout.connect(self.movePosition)
        self.moveTimer.start(50, 1)
        return

    def movePosition(self):
        self.instance.move(ePoint(config.plugins.PermanentClock.position_x.value, config.plugins.PermanentClock.position_y.value))
        self.moveTimer.start(50, 1)
        return

    def left(self):
        value = config.plugins.PermanentClock.position_x.value
        value -= 1
        if value < 0:
            value = 0
        config.plugins.PermanentClock.position_x.value = value
        return

    def up(self):
        value = config.plugins.PermanentClock.position_y.value
        value -= 1
        if value < 0:
            value = 0
        config.plugins.PermanentClock.position_y.value = value
        return

    def right(self):
        value = config.plugins.PermanentClock.position_x.value
        value += 1
        if value > self.desktopWidth:
            value = self.desktopWidth
        config.plugins.PermanentClock.position_x.value = value
        return

    def down(self):
        value = config.plugins.PermanentClock.position_y.value
        value += 1
        if value > self.desktopHeight:
            value = self.desktopHeight
        config.plugins.PermanentClock.position_y.value = value
        return

    def ok(self):
        config.plugins.PermanentClock.position_x.save()
        config.plugins.PermanentClock.position_y.save()
        self.close()
        return

    def exit(self):
        config.plugins.PermanentClock.position_x.cancel()
        config.plugins.PermanentClock.position_y.cancel()
        self.close()
        return


return
