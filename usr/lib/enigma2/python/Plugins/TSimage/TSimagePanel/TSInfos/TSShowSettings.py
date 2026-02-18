# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/TSShowSettings.py
# Compiled at: 2015-12-25 09:24:27
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.Label import Label
from Components.MenuList import MenuList
from Tools.TSTools import getCmdOutput
from enigma import getDesktop
desktopSize = getDesktop(0).size()

class TSShowSettings(Screen):
    skin_1280 = '\n                       <screen name="TSShowSettings" position="center,77" size="920,600"  title="General Info" >\n                       <widget name="menu" position="40,35" size="850,500" scrollbarMode="showOnDemand" zPosition="-2" transparent="1"/>\n                       </screen>'
    skin_1920 = '  <screen name="TSShowSettings" position="center,200" size="1300,720" title="Show Settings">\n        <widget name="menu" position="20,20" size="1260,680" zPosition="2" foregroundColor="foreground" backgroundColor="background" scrollbarMode="showOnDemand" itemHeight="40" enableWrapAround="1" transparent="1" />\n        </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session, cmd='cat /etc/enigma2/settings', title=_('E2 Settings')):
        Screen.__init__(self, session)
        self.settingslist = []
        self.cmd = cmd
        self.title = title
        self['menu'] = MenuList(self.settingslist)
        self['key_red'] = Button(_('Close'))
        self['setupActions'] = ActionMap(['SetupActions'], {'ok': (self.cancel), 'cancel': (self.cancel), 
           'red': (self.cancel)})
        self.onShown.append(self.setWindowTitle)
        self.onLayoutFinish.append(self.getProcessList)
        return

    def setWindowTitle(self):
        self.setTitle(self.title)
        return

    def getProcessList(self):
        self.processlist = []
        tmp = getCmdOutput(self.cmd)
        settings = tmp.split('\n')
        for i in range(len(settings)):
            self.settingslist.append('%s' % settings[i])

        self['menu'].setList(self.settingslist)
        return

    def cancel(self):
        self.close()
        return


return
