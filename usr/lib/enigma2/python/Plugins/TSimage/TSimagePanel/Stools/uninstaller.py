# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/Stools/uninstaller.py
# Compiled at: 2016-06-29 14:14:28
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from enigma import eListboxPythonMultiContent, gFont, loadPNG, getDesktop, RT_HALIGN_LEFT, RT_VALIGN_CENTER
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import SCOPE_CURRENT_PLUGIN, resolveFilename
from Tools.Directories import fileExists
from Plugins.TSimage.TSimagePanel.multInstaller import TSConsole
from Components.Sources.List import List
from Components.Label import Label
from Components.Pixmap import Pixmap
from os import statvfs, listdir, path as os_path
from Screens.MessageBox import MessageBox
Cmenu_list = [
 _('Uninstall package'),
 _('Remove plugin folder'),
 _('Remove skin'),
 _('Remove crashlogs')]
PACK_ICON = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, 'TSimage/TSimagePanel/buttons/package.png'))
FOLDER_ICON = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, 'TSimage/TSimagePanel/buttons/dir.png'))
SKIN_ICON = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, 'TSimage/TSimagePanel/buttons/skin.png'))
PLUGINS_PATH = '/usr/lib/enigma2/python/Plugins/Extensions/'
SKINS_PATH = '/usr/share/enigma2/'
desktopSize = getDesktop(0).size()

def freespace():
    try:
        diskSpace = statvfs('/')
        capacity = float(diskSpace.f_bsize * diskSpace.f_blocks)
        available = float(diskSpace.f_bsize * diskSpace.f_bavail)
        fspace = round(float(available / 1048576.0), 2)
        tspace = round(float(capacity / 1048576.0), 1)
        spacestr = 'Free space(' + str(fspace) + 'MB) Total space(' + str(tspace) + 'MB)'
        return spacestr
    except:
        return ''

    return


def CmenuListEntry(name, idx):
    res = [name]
    if idx == 0:
        png = '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/images/ipkgremove.png'
    if idx == 1:
        png = '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/images/folderdelete.png'
    elif idx == 2:
        png = '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/images/removeskin.png'
    elif idx == 3:
        png = '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/images/deletecrash.png'
    elif idx == 4:
        png = '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/images/soccernews.png'
    if fileExists(png):
        res.append(MultiContentEntryPixmapAlphaTest(pos=(20, 0), size=(100, 100), png=loadPNG(png)))
        res.append(MultiContentEntryText(pos=(140, 0), size=(460, 100), font=0, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER, text=name))
    return res


class CmenuList(MenuList):

    def __init__(self, list):
        MenuList.__init__(self, list, False, eListboxPythonMultiContent)
        if desktopSize.width() == 1920:
            self.l.setItemHeight(100)
            self.l.setFont(0, gFont('Regular', 40))
        else:
            self.l.setItemHeight(100)
            self.l.setFont(0, gFont('Regular', 25))
        return


class TSiMenuscrn(Screen):
    skin_1280 = '\n                <screen name="TSiMenuscrn"  position="center,77"  title="Uninstaller menu"  size="920,600"  >\n                <widget name="menu" position="20,20" size="880,500" scrollbarMode="showOnDemand" transparent="1" zPosition="2" />\n\t        \n        </screen>'
    skin_1920 = '    <screen name="TSiMenuscrn" position="center,200" size="1300,720" title="">\n        <widget name="menu" position="20,20" size="820,680" zPosition="2" itemHeight="100" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/images/tsimagelogo2.png" position="945,160" size="250,243" zPosition="-1" alphatest="blend" />\n        <widget source="global.CurrentTime" render="Label" position="840,50" size="460,70" font="Regular;65" halign="center" foregroundColor="foreground" backgroundColor="background" transparent="1">\n        <convert type="ClockToText">Default</convert>\n        </widget>\n        <widget source="session.CurrentService" render="Label" position="850,480" size="440,100" font="Regular;38" halign="center" foregroundColor="foreground" backgroundColor="background" transparent="1">\n        <convert type="ServiceName">Name</convert>\n        </widget>\n        </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        self['menu'] = CmenuList([])
        self.working = False
        self.selection = 'all'
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': (self.okClicked), 'cancel': (self.close)}, -2)
        self.onShown.append(self.setWindowTitle)
        self.onLayoutFinish.append(self.updateMenuList)
        return

    def setWindowTitle(self):
        self.setTitle('Uninstaller menu')
        return

    def updateMenuList(self):
        self.menu_list = []
        list = []
        idx = 0
        for x in Cmenu_list:
            list.append(CmenuListEntry(x, idx))
            self.menu_list.append(x)
            idx += 1

        self['menu'].setList(list)
        return

    def showabout(self):
        self.session.open(AboutScreen)
        return

    def okClicked(self):
        self.keyNumberGlobal(self['menu'].getSelectedIndex())
        return

    def keyNumberGlobal(self, idx):
        sel = self.menu_list[idx]
        if sel == _('Uninstall package'):
            self.session.open(TSRemoveList, None, PACK_ICON)
        elif sel == _('Remove plugin folder'):
            self.session.open(TSRemoveList, PLUGINS_PATH, FOLDER_ICON)
        elif sel == _('Remove skin'):
            self.session.open(TSRemoveList, SKINS_PATH, SKIN_ICON)
        elif sel == _('Remove crashlogs'):
            self.clearcrashlog()
        return

    def clearcrashlog(self):
        title = _('Removing crashlogs..')
        itempath = '/media/hdd/enigma2_crash*'
        cmd = "echo 'Removing enigma2 crashlogs...' ; rm -rf " + itempath + ' ; echo Done.'
        self.session.open(TSConsole, cmd, title)
        return


class TSRemoveList(Screen):
    skin_1280 = '\n                <screen  name="TSRemoveList" position="center,77" size="920,600" title=""  >\n\t\t<widget source="menu" render="Listbox" position="20,15" size="880,416" scrollbarMode="showOnDemand" transparent="1" zPosition="1" >\n\t\t                <convert type="TemplatedMultiContent">\n\t\t\t\t\t{"template": [\n\t\t\t\t\t                MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (22, 22), png = 1), # Status Icon,\n\t\t\t\t\t\t\tMultiContentEntryText(pos = (40, 0), size = (650, 32), font=0, flags = RT_HALIGN_LEFT| RT_VALIGN_CENTER, text = 0),\n\t\t\t\t\t\t],\n\t\t\t\t\t"fonts": [gFont("Regular", 22)],\n\t\t\t\t\t"itemHeight": 32\n\t\t\t\t\t}\n\t\t\t\t</convert>\n                </widget>                \t                   \n\t        <eLabel position="20,470" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\n\t\t<widget name="info" position="20,460" zPosition="4" size="880,80" font="Regular;24" foregroundColor="yellow" transparent="1" halign="center" valign="center" />\n\t\t<eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\n        \t<widget name="ButtonBlue" position="700,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_blue.png" transparent="1" alphatest="blend" /> \n      \t        <widget name="ButtonBluetext" position="700,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" />\n        \t</screen>\n\t\t'
    skin_1920 = '    <screen name="TSRemoveList" position="center,200" size="1300,720" title="">\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png" position="50,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green-big.png" position="360,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/yellow-big.png" position="670,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/blue-big.png" position="980,640" size="200,40" alphatest="blend" />\n        <widget name="ButtonRedtext" position="50,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#940d0d" transparent="1" />\n        <widget name="ButtonBluetext" position="980,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#18188b" transparent="1" />\n        <widget name="info" position="20,530" size="1260,40" foregroundColor="foreground" backgroundColor="background" font="Regular;28" valign="center" halign="center" transparent="1" zPosition="1" />\n        <widget source="menu" render="Listbox" position="20,20" size="1260,480" zPosition="2" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background"  transparent="1" >\n        <convert type="TemplatedMultiContent">\n        {"template": [\n        MultiContentEntryText(pos = (45, 0), size = (1000, 40), flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 0) ,\n        MultiContentEntryPixmapAlphaBlend(pos = (2, 7), size = (28, 28), png = 1),\n        ],\n        "fonts": [gFont("Regular", 32)],\n        "itemHeight": 40\n        }\n        </convert>\n        </widget>\n        </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session, path, icon):
        Screen.__init__(self, session)
        self.path = path
        self.icon = icon
        self['menu'] = List([])
        self['ButtonRed'] = Pixmap()
        self['ButtonRedtext'] = Label(_('Back'))
        self['ButtonBlue'] = Pixmap()
        self['ButtonBluetext'] = Label(_('Uninstall'))
        self['info'] = Label()
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'red': (self.close), 'blue': (self.keyUninstall), 
           'ok': (self.keyUninstall), 
           'cancel': (self.close)}, -2)
        self.onLayoutFinish.append(self.createList)
        return

    def createList(self, retval=True):
        title = _('Remove package')
        self.createList_packs()
        if self.path == PLUGINS_PATH:
            title = _('Remove plugin')
            self.packList = self.itemList
            self.createList_folders()
        elif self.path == SKINS_PATH:
            title = _('Remove skin')
            self.packList = self.itemList
            self.createList_skins()
        self.updateButton()
        self.setTitle(title)
        self['menu'].setList(self.itemList)
        self['info'].setText(freespace())
        return

    def updateButton(self):
        if len(self.itemList) > 0:
            self['ButtonBluetext'].show()
        else:
            self['ButtonBluetext'].hide()
        return

    def createList_packs(self):
        fname = '/var/lib/dpkg/status'
        packs = []
        status = []
        self.itemList = []
        for line in open(fname, 'r').readlines():
            if line.startswith('Package:'):
                packs.append(line)
            if line.startswith('Status:'):
                status.append(line)

        i = 0
        for x in status:
            if 'install ok installed' in x:
                f = packs[i]
                f = f.replace('Package:', '')
                f = f.strip()
                self.itemList.append((f, self.icon))
            i = i + 1

        self.itemList.sort()
        return

    def createList_folders(self):
        self.itemList = []
        for x in listdir(self.path):
            if not os_path.isfile(self.path + x):
                self.itemList.append((x, self.icon))

        self.itemList.sort()
        return

    def createList_skins(self):
        self.itemList = []
        for x in listdir(self.path):
            filepath = self.path + x + '/skin.xml'
            if os_path.exists(filepath):
                self.itemList.append((x, self.icon))

        self.itemList.sort()
        return

    def keyUninstall(self):
        if len(self.itemList) > 0:
            self.item = self['menu'].getCurrent()[0]
            if self.path is None:
                self.session.openWithCallback(self.prompt_packs, MessageBox, _('Really delete %s?') % self.item)
            else:
                self.session.openWithCallback(self.prompt_remove, MessageBox, _('Really delete %s?') % self.item)
        return

    def prompt_packs(self, answer):
        if answer:
            self.removeIpk(self.item)
        return

    def prompt_remove(self, answer):
        if answer:
            title = _('Removing folder...')
            itempath = self.path + self.item
            pack = self.checkPack(itempath)
            if pack == '':
                cmd = 'echo \'Removing folder "' + self.item + '"...\' ; rm -rf ' + itempath + ' ; echo Done.'
                self.session.openWithCallback(self.createList, TSConsole, cmd, title)
            else:
                self.removeIpk(pack)
        return

    def removeIpk(self, pack):
        title = _('Removing package...')
        cmd = 'echo \'Removing "' + pack + '" package...\' ; apt-get -y remove ' + pack + ' ; echo Done.'
        self.session.openWithCallback(self.createList, TSConsole, cmd, title)
        return

    def checkPack(self, folderpath):
        for pkg in self.packList:
            fname = '/var/lib/dpkg/info/' + pkg[0] + '.list'
            if os_path.exists(fname):
                for line in open(fname, 'r').readlines():
                    if folderpath in line:
                        return pkg[0]

        return ''


return
