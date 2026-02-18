# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/TSKernelModules.py
# Compiled at: 2015-12-25 09:22:12
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.Label import Label
from Components.MenuList import MenuList
from Tools.TSTools import getCmdOutput
from enigma import getDesktop
desktopSize = getDesktop(0).size()

class TSKernelModules(Screen):
    skin_1280 = '\n                       <screen name="TSKernelModules" position="center,77" size="920,600"  title="General Info" >\n                       <widget name="header" position="40,35" zPosition="5" size="850,30" font="Regular;20" transparent="1"  />\n                       <widget name="menu" position="40,65" size="850,500" scrollbarMode="showOnDemand" zPosition="-2" transparent="1"/>\n                       </screen>'
    skin_1920 = '  <screen name="TSKernelModules" position="center,200" size="1300,720" title="Kernel Modules">\n        <widget name="header" position="20,20" zPosition="4" size="1260,50" font="Regular;30" transparent="1" halign="left" valign="center" />\n        <widget name="menu" position="20,70" size="1260,600" zPosition="2" foregroundColor="foreground" backgroundColor="background" scrollbarMode="showOnDemand" itemHeight="40" enableWrapAround="1" transparent="1" />\n        </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session):
        Screen.__init__(self, session)
        self.moduleslist = []
        self['header'] = Label('')
        self['menu'] = MenuList(self.moduleslist)
        self['key_red'] = Button(_('Close'))
        self['setupActions'] = ActionMap(['SetupActions'], {'ok': (self.cancel), 'cancel': (self.cancel), 
           'red': (self.cancel)})
        self.onShown.append(self.setWindowTitle)
        self.onLayoutFinish.append(self.getKernelModules)
        return

    def setWindowTitle(self):
        self.setTitle(_('Kernels Modules'))
        return

    def getKernelModules(self):
        self.moduleslist = []
        tmp = getCmdOutput("lsmod | awk '{print $1}'")
        mod = tmp.split('\n')
        tmp = getCmdOutput("lsmod | awk '{print $2}'")
        size = tmp.split('\n')
        tmp = getCmdOutput("lsmod | awk '{print $3}'")
        used = tmp.split('\n')
        tmp = getCmdOutput("lsmod | awk '{print $4}'")
        by = tmp.split('\n')
        for i in range(len(mod)):
            if i == 0:
                self['header'].setText('%s\t\t%s\t%s  %s' % (mod[i],
                 size[i],
                 used[i],
                 by[i]))
            elif len(mod[i]) < 15:
                self.moduleslist.append('%s\t\t%s\t%s  %s' % (mod[i],
                 size[i],
                 used[i],
                 by[i]))
            else:
                self.moduleslist.append('%s\t%s\t%s  %s' % (mod[i],
                 size[i],
                 used[i],
                 by[i]))

        self['menu'].setList(self.moduleslist)
        return

    def cancel(self):
        self.close()
        return


return
