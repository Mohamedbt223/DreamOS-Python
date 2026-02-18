# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/Stools/ScreenGrabber/ScreenGrabber.py
# Compiled at: 2015-12-25 11:37:00
from Components.Label import Label
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.ActionMap import ActionMap
from Components.Pixmap import Pixmap
from Components.AVSwitch import AVSwitch
from Components.config import config
from Tools.Directories import fileExists, pathExists, copyfile
from ServiceReference import ServiceReference
from enigma import getDesktop, ePicLoad
from os import popen, system, path, listdir, remove
from Components.Sources.StaticText import StaticText
from Components.Sources.List import List
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import SCOPE_CURRENT_PLUGIN, resolveFilename
from Components.FileList import FileList
from Plugins.Extensions.PicturePlayer.plugin import Pic_Thumb, Pic_Full_View
from Components.ConfigList import ConfigList, ConfigListScreen
from Components.config import config, ConfigDirectory, ConfigSubsection, ConfigSelection, getConfigListEntry, configfile
config.plugins.ScreenGrabber = ConfigSubsection()
config.plugins.ScreenGrabber.items = ConfigSelection(default='Disabled', choices=[('All', _('Grab All')),
 (
  '-v', _('Video only')),
 (
  '-o', _('OSD only')),
 (
  'Disabled', _('Off'))])
config.plugins.ScreenGrabber.storedir = ConfigDirectory(default='/tmp/')
config.plugins.ScreenGrabber.scut = ConfigSelection(default='help', choices=[('text', _('Text')),
 (
  'help', _('Help')),
 (
  'info', _('Info')),
 (
  'video', _('Video')),
 (
  'mute', _('Mute')),
 (
  'radio', _('Radio'))])
config.plugins.ScreenGrabber.newsize = ConfigSelection(default='Disabled', choices=[('-r1920', _('1920x1080')),
 (
  '-r1280', _('1280x720')),
 (
  '-r800', _('800x450')),
 (
  '-r600', _('600x337')),
 (
  'Disabled', _('osd resolution'))])
config.plugins.ScreenGrabber.format = ConfigSelection(default='-j100', choices=[('-j100', _('jpg100')),
 (
  '-j80', _('jpg80')),
 (
  '-j60', _('jpg60')),
 (
  '-j40', _('jpg40')),
 (
  '-j20', _('jpg20')),
 (
  '-p', _('PNG'))])
config.plugins.ScreenGrabber.fixedaspectratio = ConfigSelection(default='Disabled', choices=[('-n', _('Enabled')), ('Disabled', _('Off'))])
config.plugins.ScreenGrabber.always43 = ConfigSelection(default='Disabled', choices=[('-l', _('Enabled')), ('Disabled', _('Off'))])
config.plugins.ScreenGrabber.bicubic = ConfigSelection(default='Disabled', choices=[('-b', _('Enabled')), ('Disabled', _('Off'))])
desktopSize = getDesktop(0).size()

class TSiScreenGrabberFiles(Screen):
    skin_1280 = '\n                        <screen name="TSiScreenGrabberFiles"  position="center,77"  title="Screen grabber files"  size="920,600"  >\n                        <widget source="menu" render="Listbox" position="20,15" size="880,416" scrollbarMode="showOnDemand" transparent="1" zPosition="1" >\n\t\t                <convert type="TemplatedMultiContent">\n\t\t\t\t\t{"template": [\n\t\t\t\t\t                MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (22, 22), png = 0), # Status Icon,\n\t\t\t\t\t\t\tMultiContentEntryText(pos = (40, 0), size = (650, 32), font=0, flags = RT_HALIGN_LEFT| RT_VALIGN_CENTER, text = 1),\n\t\t\t\t\t\t],\n\t\t\t\t\t"fonts": [gFont("Regular", 22)],\n\t\t\t\t\t"itemHeight": 32\n\t\t\t\t\t}\n\t\t\t\t</convert>\n                </widget>\n      \t\t        <eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\n                       \t<eLabel name="ButtonRedtext" text="Back" position="70,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" /> \n                        <widget name="ButtonGreentext" position="280,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" />\n       \t                <widget name="ButtonYellowtext" position="490,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" />\n       \t                <widget name="ButtonBluetext" position="700,550" size="160,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" />\n\t\t\t<ePixmap name="red" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" position="70,545" size="140,40" zPosition="4" transparent="1" alphatest="on"/>\n\t\t\t<ePixmap name="green" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_green.png" position="280,545" size="140,40" zPosition="4" transparent="1" alphatest="on"/>\n\t\t\t<widget name="ButtonYellow" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_yellow.png" position="490,545" size="140,40" zPosition="4" transparent="1" alphatest="on"/>\t\t\t\t\t\t\n       \t                <widget name="ButtonBlue"   position="700,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_blue.png" transparent="1" alphatest="blend" /> \t                  \n        \t</screen>\n\t\t'
    skin_1920 = '    <screen name="TSiScreenGrabberFiles" position="center,200" size="1300,720" title="Screen grabber files">\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png" position="50,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green-big.png" position="360,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/yellow-big.png" position="670,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/blue-big.png" position="980,640" size="200,40" alphatest="blend" />\n        <widget name="ButtonRedtext" position="50,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#940d0d" transparent="1" />\n        <widget name="ButtonGreentext" position="360,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#2d872d" transparent="1" />\n        <widget name="ButtonYellowtext" position="670,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#bba502" transparent="1" />\n        <widget name="ButtonBluetext" position="970,640" size="220,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#18188b" transparent="1" />\n        <widget source="menu" render="Listbox" position="20,20" size="1260,480" zPosition="2" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background"  transparent="1" >\n            <convert type="TemplatedMultiContent">\n                {"template": [\n                    MultiContentEntryText(pos = (45, 0), size = (1000, 40), flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 1) ,\n                    MultiContentEntryPixmapAlphaBlend(pos = (2, 7), size = (28, 28), png = 0),\n                    ],\n                    "fonts": [gFont("Regular", 30)],\n                    "itemHeight": 40\n                    }\n            </convert>\n        </widget>\n    </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session):
        Screen.__init__(self, session)
        self.icon = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, 'TSimage/TSimagePanel/buttons/skin.png'))
        self['ButtonBlue'] = Pixmap()
        self['ButtonBluetext'] = Label(_('Thumbnails'))
        self['ButtonYellow'] = Pixmap()
        self['ButtonYellowtext'] = Label(_('Delete'))
        self['ButtonGreen'] = Pixmap()
        self['ButtonGreentext'] = Label(_('Show'))
        self['ButtonRed'] = Pixmap()
        self['ButtonRedtext'] = Label(_('Back'))
        self.currDir = config.plugins.ScreenGrabber.storedir.value
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'red': (self.close), 'green': (self.showFullView), 
           'yellow': (self.keyRemove), 
           'blue': (self.showThumbnail), 
           'ok': (self.showFullView), 
           'cancel': (self.close)}, -2)
        self.filelist = FileList(self.currDir, showDirectories=False, matchingPattern='(?i)^.*\\.(jpeg|jpg|jpe|png|bmp|gif)')
        self['menu'] = List([])
        self.createFileList()
        return

    def createFileList(self):
        l = []
        if not self.filelist.canDescent():
            if self.filelist.getCurrentDirectory() and self.filelist.getFilename():
                for idx in range(len(self.filelist.getFileList())):
                    l.append((self.icon, self.filelist.getFileList()[idx][0][0]))

            else:
                self['ButtonGreentext'].setText(' ')
                self['ButtonYellowtext'].setText(' ')
                self['ButtonBluetext'].setText(' ')
        self['menu'].setList(l)
        return

    def showFullView(self):
        if not self.filelist.canDescent():
            if self.filelist.getCurrentDirectory() and self.filelist.getFilename():
                self.session.openWithCallback(self.callbackView, Pic_Full_View, self.filelist.getFileList(), self['menu'].getIndex(), self.filelist.getCurrentDirectory())
        return

    def showThumbnail(self):
        if not self.filelist.canDescent():
            if self.filelist.getCurrentDirectory() and self.filelist.getFilename():
                self.session.openWithCallback(self.callbackView, Pic_Thumb, self.filelist.getFileList(), self['menu'].getIndex(), self.filelist.getCurrentDirectory())
        return

    def callbackView(self, val=0):
        if val > 0:
            self.filelist.moveToIndex(val)
            self['menu'].setIndex(val)
        return

    def removeFile(self, result):
        if result:
            filename = self.currDir + self['menu'].getCurrent()[1]
            if fileExists(filename):
                remove(filename)
                self.filelist.refresh()
                self.createFileList()
        return

    def keyRemove(self):
        if not self.filelist.canDescent():
            if self.filelist.getCurrentDirectory() and self.filelist.getFilename():
                self.session.openWithCallback(self.removeFile, MessageBox, _('Really delete %s?') % self['menu'].getCurrent()[1])
        return


class TSiScreenGrabberSetup(Screen, ConfigListScreen):
    skin_1280 = '\n                        <screen name="TSiScreenGrabberSetup"  position="center,77"  title="Screen Grabber Setup"  size="920,600"  >\n                        <widget name="config" position="20,20" size="880,300" scrollbarMode="showOnDemand" zPosition="2" transparent="1"  />\n                        <eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\n\t\t\t<widget source="key_red" render="Label" position="70,550" size="140,40" valign="center" halign="center" zPosition="5" transparent="1" font="Regular;21"/>\n\t\t\t<widget source="key_green" render="Label" position="280,550" size="140,40" valign="center" halign="center" zPosition="5" transparent="1" font="Regular;21"/>\t\t\t\n                        <widget source="key_yellow" render="Label" position="490,550" size="140,40" valign="center" halign="center" zPosition="5" font="Regular;21" transparent="1" />\n\t\t\t<ePixmap name="red" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" position="70,545" size="140,40" zPosition="4" transparent="1" alphatest="on"/>\n\t\t\t<ePixmap name="green" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_green.png" position="280,545" size="140,40" zPosition="4" transparent="1" alphatest="on"/>\n\t\t\t<ePixmap name="yellow" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_yellow.png" position="490,545" size="140,40" zPosition="4" transparent="1" alphatest="on"/>\n\t\t\t<widget name="key_ok" position="870,550" size="30,30" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_ok.png" transparent="1" alphatest="blend" />\t\t\t\t\t\t\n                </screen>'
    skin_1920 = '    <screen name="TSiScreenGrabberSetup" position="center,200" size="1300,720" title="Screen Grabber Setup">\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png" position="50,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green-big.png" position="360,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/yellow-big.png" position="670,640" size="200,40" alphatest="blend" />\n        <widget source="key_red" render="Label" position="50,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#940d0d" transparent="1" />\n        <widget source="key_green" render="Label" position="360,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#2d872d" transparent="1" />\n        <widget source="key_yellow" render="Label" position="670,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#bba502" transparent="1" />\n        <widget name="config" position="20,30" size="1260,600" zPosition="2" itemHeight="40" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background"  transparent="1" />\n        <widget name="key_ok" position="1190,636" size="48,48" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_ok-big.png" transparent="1" alphatest="blend" />\n        </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session):
        Screen.__init__(self, session)
        self['key_ok'] = Pixmap()
        self['key_red'] = StaticText(_('Cancel'))
        self['key_green'] = StaticText(_('Save'))
        self['key_yellow'] = StaticText(_('Files'))
        self.list = []
        ConfigListScreen.__init__(self, self.list, session)
        self.createSetup()
        self['setupActions'] = ActionMap(['SetupActions', 'ColorActions'], {'yellow': (self.showfiles), 'green': (self.keySave), 
           'ok': (self.keyOk), 
           'cancel': (self.keyCancel)}, -2)
        self.onitem = config.plugins.ScreenGrabber.items.value
        self.scut = config.plugins.ScreenGrabber.scut.value
        self['config'].onSelectionChanged.append(self.selectionChanged)
        self.picload = ePicLoad()
        self.onLayoutFinish.append(self.setOkPic)
        return

    def selectionChanged(self):
        if self['config'].getCurrent()[1] == config.plugins.ScreenGrabber.storedir:
            self['key_ok'].show()
        else:
            self['key_ok'].hide()
        return

    def setOkPic(self):
        self.setTitle(_('Screen Grabber Setup'))
        sc = AVSwitch().getFramebufferScale()
        params = (
         self['key_ok'].instance.size().width(), self['key_ok'].instance.size().height(), sc[0], sc[1], True, 1, '#00000000')
        self.picload.setPara(params)
        return

    def createSetup(self):
        self.list = []
        self.list.append(getConfigListEntry(_('ScreenShot:'), config.plugins.ScreenGrabber.items))
        self.list.append(getConfigListEntry(_('Storing Folder:'), config.plugins.ScreenGrabber.storedir))
        self.list.append(getConfigListEntry(_('Remote screenshot button:'), config.plugins.ScreenGrabber.scut))
        self.list.append(getConfigListEntry(_('Picture size:'), config.plugins.ScreenGrabber.newsize))
        self.list.append(getConfigListEntry(_('screenshot format/quality:'), config.plugins.ScreenGrabber.format))
        self.list.append(getConfigListEntry(_('Fixed Aspect ratio:'), config.plugins.ScreenGrabber.fixedaspectratio))
        self.list.append(getConfigListEntry(_('Fixed Aspect ratio 4:3:'), config.plugins.ScreenGrabber.always43))
        self.list.append(getConfigListEntry(_('Bicubic picture resize:'), config.plugins.ScreenGrabber.bicubic))
        self['config'].setList(self.list)
        return

    def keyOk(self):
        if self['config'].getCurrent()[1] == config.plugins.ScreenGrabber.storedir:
            self.session.openWithCallback(self.directoryBrowserClosed, DirectoryBrowser, config.plugins.ScreenGrabber.storedir.value, _('Directory browser'))
        return

    def directoryBrowserClosed(self, path):
        if path != False:
            config.plugins.ScreenGrabber.storedir.value = path
            self.createSetup()
        return

    def showfiles(self):
        self.session.open(TSiScreenGrabberFiles)
        return

    def keySave(self):
        for x in self['config'].list:
            x[1].save()

        configfile.save()
        if not self.onitem == config.plugins.ScreenGrabber.items.value or not self.scut == config.plugins.ScreenGrabber.scut.value:
            cmd = 'touch /tmp/.newsettings'
            system(cmd)
        self.close(True)
        return


class DirectoryBrowser(Screen):
    skin = '<screen name="DirectoryBrowser" position="center,center" size="520,440" title="Directory browser" >\n\t\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="0,0" size="140,40" alphatest="on" />\n\t\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="140,0" size="140,40" alphatest="on" />\n\t\t\t<widget source="key_red" render="Label" position="0,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t\t<widget source="key_green" render="Label" position="140,0" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />\n\t\t\t<widget source="curdir" render="Label" position="5,50" size="510,20"  font="Regular;20" halign="left" valign="center" backgroundColor="background" transparent="1" noWrap="1" />\n\t\t\t<widget name="filelist" position="5,80" size="510,345" scrollbarMode="showOnDemand" />\n\t\t</screen>'

    def __init__(self, session, curdir, title):
        Screen.__init__(self, session)
        self.title = title
        self['key_red'] = StaticText(_('Cancel'))
        self['key_green'] = StaticText(_('Save'))
        self['curdir'] = StaticText('current:  %s' % (curdir or ''))
        inhibitDirs = [8, 
         9, 
         10, 
         11, 
         12, 
         13, 
         14, 
         15, 
         16, 
         17, 
         18]
        inhibitMounts = []
        self.filelist = FileList(curdir, showDirectories=True, showFiles=False, inhibitMounts=inhibitMounts, inhibitDirs=inhibitDirs)
        self.filelist.onSelectionChanged.append(self.__selChanged)
        self['filelist'] = self.filelist
        self['FilelistActions'] = ActionMap(['SetupActions', 'ColorActions'], {'green': (self.keyGreen), 'red': (self.keyRed), 
           'ok': (self.keyOk), 
           'cancel': (self.keyRed)})
        self.onLayoutFinish.append(self.__layoutFinished)
        return

    def __layoutFinished(self):
        self.setTitle(self.title)
        return

    def getCurrentSelected(self):
        dirname = self.filelist.getCurrentDirectory()
        filename = self.filelist.getFilename()
        if not filename and not dirname:
            cur = ''
        elif not filename:
            cur = dirname
        elif not dirname:
            cur = filename
        elif not self.filelist.canDescent() or len(filename) <= len(dirname):
            cur = dirname
        else:
            cur = filename
        return cur or ''

    def __selChanged(self):
        self['curdir'].setText('current:  %s' % self.getCurrentSelected())
        return

    def keyOk(self):
        if self.filelist.canDescent():
            self.filelist.descent()
        return

    def keyGreen(self):
        self.close(self.getCurrentSelected())
        return

    def keyRed(self):
        self.close(False)
        return


class TSiScreenGrabberView(Screen):

    def __init__(self, session):
        nowService = session.nav.getCurrentlyPlayingServiceReference()
        self.nowService = nowService
        self.srvName = ServiceReference(session.nav.getCurrentlyPlayingServiceReference()).getServiceName()
        session.nav.stopService()
        cmd = ''
        tcmd = ''
        if config.plugins.ScreenGrabber.items.value == '-v':
            items = '-v'
        elif config.plugins.ScreenGrabber.items.value == '-o':
            items = '-o'
        else:
            items = ''
        newsize = config.plugins.ScreenGrabber.newsize.value.replace('Disabled', '')
        format = config.plugins.ScreenGrabber.format.value
        fixedaspectratio = config.plugins.ScreenGrabber.fixedaspectratio.value.replace('Disabled', '')
        always43 = config.plugins.ScreenGrabber.always43.value.replace('Disabled', '')
        bicubic = config.plugins.ScreenGrabber.bicubic.value.replace('Disabled', '')
        tcmd = items + ' ' + newsize + ' ' + format + ' ' + fixedaspectratio + ' ' + always43 + ' ' + bicubic
        print tcmd
        self.pictureformat = ''
        if format == '-p':
            self.pictureformat = '/tmp/ScreenGrabber.png'
        else:
            self.pictureformat = '/tmp/ScreenGrabber.jpg'
        r = popen('grab ' + tcmd + ' ' + self.pictureformat).readlines()
        w = desktopSize.width()
        h = desktopSize.height()
        PreviewString = '<screen flags="wfNoBorder" position="0,0" size="' + str(w) + ',' + str(h) + '" title="Preview">\n'
        PreviewString = PreviewString + ' <widget name="Picture" position="0,0" size="' + str(w) + ',' + str(h) + '" zPosition="5" alphatest="on" />\n'
        if w == 1920:
            PreviewString = PreviewString + ' <eLabel font="Regular;24" halign="left" valign="center" position="30,80" size="400,40" text="Please wait....." zPosition="1"/>\n'
            PreviewString = PreviewString + ' <eLabel font="Regular;24" halign="left" valign="center" position="50,50" size="720,40" text=" OK=Save        Exit=Play TV        Green=Setup        Yellow=Files" zPosition="9"/>\n'
        else:
            PreviewString = PreviewString + ' <eLabel font="Regular;18" halign="left" valign="center" position="30,80" size="300,25" text="Please wait....." zPosition="1"/>\n'
            PreviewString = PreviewString + ' <eLabel font="Regular;18" halign="left" valign="center" position="50,50" size="620,25" text=" OK=Save        Exit=Play TV        Green=Setup        Yellow=Files" zPosition="9"/>\n'
        PreviewString = PreviewString + '</screen>'
        prvScreen = PreviewString
        self.skin = prvScreen
        Screen.__init__(self, session)
        self.session = session
        self['Picture'] = Pixmap()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': (self.SavePic), 'back': (self.dexit), 
           'green': (self.showsetup), 
           'yellow': (self.showfiles)}, -1)
        self.whatPic = self.pictureformat
        self.EXscale = AVSwitch().getFramebufferScale()
        self.EXpicload = ePicLoad()
        self.EXpicload_conn = self.EXpicload.PictureData.connect(self.DecodeAction)
        self.onLayoutFinish.append(self.Show_Picture)
        return

    def showsetup(self):
        self.session.open(TSiScreenGrabberSetup)
        self.dexit()
        return

    def showfiles(self):
        self.session.open(TSiScreenGrabberFiles)
        self.dexit()
        return

    def dexit(self):
        self.session.nav.playService(self.nowService)
        self.close()
        return

    def Show_Picture(self):
        if fileExists(self.whatPic):
            params = (self['Picture'].instance.size().width(), self['Picture'].instance.size().height(), self.EXscale[0], self.EXscale[1], True, 1, '#00080808')
            self.EXpicload.setPara(params)
            self.EXpicload.startDecode(self.whatPic)
        return

    def DecodeAction(self, pictureInfo=''):
        if fileExists(self.whatPic):
            ptr = self.EXpicload.getData()
            self['Picture'].instance.setPixmap(ptr)
        return

    def SavePic(self):
        import datetime
        now = datetime.datetime.now()
        datestr = '%s%s%s-%s%s' % (now.day,
         now.month,
         now.year,
         now.hour,
         now.second)
        if fileExists(self.whatPic):
            srvName = ServiceReference(self.session.nav.getCurrentlyPlayingServiceReference()).getServiceName()
            srvName = srvName.replace('\x86', '').replace('\x87', '')
            srvName = srvName.replace(' ', '_')
            self.currDir = config.plugins.ScreenGrabber.storedir.value
            try:
                if pathExists(self.currDir):
                    if self.pictureformat.endswith('jpg'):
                        filename = self.currDir + self.srvName + '-' + datestr + '.jpg'
                    else:
                        filename = self.currDir + self.srvName + '-' + datestr + '.png'
                    command = 'cp ' + self.pictureformat + ' ' + filename
                    mtext = 'saving picture to...\n' + filename
                    copyfile(self.pictureformat, filename)
                    self.session.open(MessageBox, text=_(filename), type=MessageBox.TYPE_INFO, timeout=3, close_on_any_key=True)
                else:
                    self.session.open(MessageBox, text=_('Location not available!'), type=MessageBox.TYPE_ERROR, timeout=5, close_on_any_key=True)
            except:
                self.session.open(MessageBox, text=_('Failed saving file!'), type=MessageBox.TYPE_ERROR, timeout=5, close_on_any_key=True)

        self.dexit()
        return


return
