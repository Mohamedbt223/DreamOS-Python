# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/TSCustomCmd.py
# Compiled at: 2015-12-24 15:27:10
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Sources.List import List
from Components.Pixmap import Pixmap
from Screens.VirtualKeyBoard import VirtualKeyBoard
from os import listdir, chmod, system
from Components.Label import Label
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import fileExists, SCOPE_CURRENT_PLUGIN, resolveFilename
from Plugins.TSimage.TSimagePanel.multInstaller import TSConsole
from enigma import getDesktop
desktopSize = getDesktop(0).size()

class TSCustomCmd(Screen):
    skin_1280 = '\n                <screen  name="TSCustomCmd" position="center,77" size="920,600" title=""  >\n\t\t<widget source="menu" render="Listbox" position="20,15" size="880,416" scrollbarMode="showOnDemand" transparent="1" zPosition="1" >\n\t\t                <convert type="TemplatedMultiContent">\n\t\t\t\t\t{"template": [\n\t\t\t\t\t                MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (22, 22), png = 1), # Status Icon,\n\t\t\t\t\t\t\tMultiContentEntryText(pos = (40, 0), size = (650, 32), font=0, flags = RT_HALIGN_LEFT| RT_VALIGN_CENTER, text = 0),\n\t\t\t\t\t\t],\n\t\t\t\t\t"fonts": [gFont("Regular", 22)],\n\t\t\t\t\t"itemHeight": 32\n\t\t\t\t\t}\n\t\t\t\t</convert>\n                </widget>                \t                   \n\t        <eLabel position="20,470" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\n\t\t<widget name="info" position="20,460" zPosition="4" size="880,80" font="Regular;24" foregroundColor="yellow" transparent="1" halign="center" valign="center" />\n\t\t<eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\n                <widget name="red"    position="70,545"   zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" transparent="1" alphatest="blend" />\n\t        <widget name="green"  position="280,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_green.png" transparent="1" alphatest="blend" />\n\t        <widget name="yellow" position="490,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_yellow.png" transparent="1" alphatest="blend" /> \n        \t<widget name="key_red" position="70,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" /> \n        \t<widget name="key_green" position="280,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" /> \n                <widget name="key_yellow" position="490,555" size="140,45" valign="center" halign="center" zPosition="2" font="Regular;20" transparent="1" />\n        \t</screen>\n\t\t'
    skin_1920 = '    <screen name="TSCustomCmd" position="center,200" size="1300,720" title="">\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png" position="50,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green-big.png" position="360,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/yellow-big.png" position="670,640" size="200,40" alphatest="blend" />\n        <widget name="key_red" position="50,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#940d0d" transparent="1" />\n        <widget name="key_green" position="360,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#2d872d" transparent="1" />\n        <eLabel name="key_yellow" text="Command" position="670,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#bba502" transparent="1" />\n        <widget name="info" position="20,530" size="1260,40" foregroundColor="foreground" backgroundColor="background" font="Regular;28" valign="center" halign="center" transparent="1" zPosition="1" />\n        <widget source="menu" render="Listbox" position="20,20" size="1260,480" zPosition="2" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background"  transparent="1" >\n        <convert type="TemplatedMultiContent">\n        {"template": [\n        MultiContentEntryText(pos = (45, 0), size = (1000, 40), flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 0) ,\n        MultiContentEntryPixmapAlphaBlend(pos = (2, 7), size = (28, 28), png = 1),\n        ],\n        "fonts": [gFont("Regular", 32)],\n        "itemHeight": 40\n        }\n        </convert>\n        </widget>\n        </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session):
        Screen.__init__(self, session)
        self.path = '/usr/script/'
        self.scriptIcon = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, 'TSimage/TSimagePanel/buttons/script.png'))
        self.script_list = []
        self['menu'] = List(self.script_list)
        self['red'] = Pixmap()
        self['green'] = Pixmap()
        self['yellow'] = Pixmap()
        self['key_red'] = Label(_('Close'))
        self['key_green'] = Label(_('Execute'))
        self['key_yellow'] = Label(_('Custom Command'))
        self['info'] = Label('FTP your script to /usr/script/')
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'red': (self.close), 'green': (self.doCommand), 
           'yellow': (self.virtualKeyb), 
           'ok': (self.doCommand), 
           'cancel': (self.close)}, -2)
        self.listScripts()
        self.onShown.append(self.setWindowTitle)
        return

    def setWindowTitle(self):
        self.setTitle(_('Select Script to execute...'))
        return

    def listScripts(self):
        self.script_list = []
        if fileExists(self.path):
            for x in listdir(self.path):
                x = x.replace('.sh', '')
                if x == 'cam' or x == 'script':
                    pass
                else:
                    self.script_list.append((x, self.scriptIcon))

            if not len(self.script_list) == 0:
                self.script_list.sort()
                self['menu'].setList(self.script_list)
        return

    def doCommand(self):
        if not len(self.script_list) == 0:
            selectedfolder = self['menu'].getCurrent()[0]
            script = self.path + selectedfolder + '.sh'
            chmod(script, 755)
            title = _('Executing script %s...') % selectedfolder
            cmd = 'sh ' + script + ' ; echo ; echo Done.'
            self.session.open(TSConsole, cmd, title)
        return

    def virtualKeyb(self):
        self.session.openWithCallback(self.doCustomCommand, VirtualKeyBoard, title=_('Enter Command'))
        return

    def doCustomCommand(self, sel=None):
        if sel:
            system('echo %s > /tmp/.custcmd.sh' % sel)
            script = '/tmp/.custcmd.sh'
            chmod(script, 755)
            title = _('Executing custom command %s...') % sel
            cmd = 'sh ' + script + ' ; echo ; echo Done.'
            self.session.open(TSConsole, cmd, title)
        return


return
