# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/TSProcessList.py
# Compiled at: 2015-12-25 09:24:26
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.Label import Label
from Components.MenuList import MenuList
from Tools.TSTools import getCmdOutput
from enigma import getDesktop
desktopSize = getDesktop(0).size()

class TSProcessList(Screen):
    skin_1280 = '\n                       <screen name="TSProcessList" position="center,77" size="920,600"  title="General Info" >\n                       <widget name="header" position="40,35" zPosition="5" size="850,30" font="Regular;20" transparent="1" />\n                       <widget name="menu" position="40,65" size="850,500" scrollbarMode="showOnDemand" zPosition="-2" transparent="1"/>\n                       </screen>'
    skin_1920 = '  <screen name="TSProcessList" position="center,200" size="1300,720" title="Process List">\n        <widget name="header" position="20,20" zPosition="4" size="1260,50" font="Regular;30" transparent="1" halign="left" valign="center" />\n        <widget name="menu" position="20,70" size="1260,600" zPosition="2" foregroundColor="foreground" backgroundColor="background" scrollbarMode="showOnDemand" itemHeight="40" enableWrapAround="1" transparent="1" />\n        </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session):
        Screen.__init__(self, session)
        self.processlist = []
        self['header'] = Label('')
        self['menu'] = MenuList(self.processlist)
        self['key_red'] = Button(_('Close'))
        self['setupActions'] = ActionMap(['SetupActions'], {'ok': (self.cancel), 'cancel': (self.cancel), 
           'red': (self.cancel)})
        self.onShown.append(self.setWindowTitle)
        self.onLayoutFinish.append(self.getProcessList)
        return

    def setWindowTitle(self):
        self.setTitle(_('Process List'))
        return

    def getProcessList(self):
        self.processlist = []
        tmp = getCmdOutput("ps -A | awk '{print $1}'")
        pid = tmp.split('\n')
        tmp = getCmdOutput("ps -A | awk '{print $2}'")
        tty = tmp.split('\n')
        tmp = getCmdOutput("ps -A | awk '{print $3}'")
        time = tmp.split('\n')
        tmp = getCmdOutput("ps -A | awk '{print $4}'")
        cmd = tmp.split('\n')
        for i in range(len(pid)):
            if i == 0:
                self['header'].setText('%s\t%s\t%s\t%s' % (pid[i],
                 tty[i],
                 time[i],
                 cmd[i]))
            else:
                self.processlist.append('%s\t%s\t%s\t%s' % (pid[i],
                 tty[i],
                 time[i],
                 cmd[i]))

        self['menu'].setList(self.processlist)
        return

    def cancel(self):
        self.close()
        return


return
