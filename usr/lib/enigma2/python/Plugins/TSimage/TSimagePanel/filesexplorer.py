# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/filesexplorer.py
# Compiled at: 2025-09-10 14:58:52
from tsimage import TSimagePanelImage
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.InfoBar import MoviePlayer as MP_parent
from Screens.InfoBar import InfoBar
from Screens.Console import Console
from Screens.ChoiceBox import ChoiceBox
from Screens.MessageBox import MessageBox
from Screens.EventView import EventViewSimple
from Screens.InputBox import InputBox
from Screens.NumericalTextInputHelpDialog import NumericalTextInputHelpDialog
from Components.ActionMap import ActionMap, NumberActionMap
from Components.FileList import FileList
from Components.MenuList import MenuList
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Components.Pixmap import Pixmap
from Components.AVSwitch import AVSwitch
from Components.config import config, ConfigSubsection, ConfigText
from Components.Input import Input
from Components.Harddisk import harddiskmanager
from Components.Language import language
from Tools.Directories import fileExists, pathExists
from Tools.HardwareInfo import HardwareInfo
from Tools.BoundFunction import boundFunction
from Tools.LoadPixmap import LoadPixmap
from ServiceReference import ServiceReference
from enigma import eConsoleAppContainer, eServiceReference, ePicLoad, getDesktop, eServiceCenter, RT_HALIGN_LEFT, RT_VALIGN_CENTER, eListboxPythonMultiContent, eServiceCenter, gFont, iServiceInformation, eRCInput, getPrevAsciiCode, getDesktop, eTimer
from os import system as os_system
from os import stat as os_stat
from os import walk as os_walk
from os import popen as os_popen
from os import rename as os_rename
from os import mkdir as os_mkdir
from os import path as os_path, listdir, stat as os_stat
from os import listdir as os_listdir
from time import strftime as time_strftime
from time import localtime as time_localtime
from re import compile as re_compile
from myNumericalTextInput import myNumericalTextInput
if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/PicturePlayer/plugin.pyo'):
    from Plugins.Extensions.PicturePlayer.plugin import Pic_Thumb, picshow
    PicPlayerAviable = True
else:
    PicPlayerAviable = False
if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/DVDPlayer/plugin.pyo'):
    from Plugins.Extensions.DVDPlayer.plugin import DVDPlayer
    DVDPlayerAviable = True
else:
    DVDPlayerAviable = False
if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/MerlinMusicPlayer/plugin.pyo'):
    from Plugins.Extensions.MerlinMusicPlayer.plugin import MerlinMusicPlayerScreen, Item
    MMPavaiable = True
else:
    MMPavaiable = False
config.plugins.FileExplorer = ConfigSubsection()
config.plugins.FileExplorer.startDir = ConfigText(default='/')
config.plugins.FileExplorer.MediaFilter = ConfigText(default='off')
config.plugins.FileExplorer.CopyDest = ConfigText(default='/')
explSession = None
HDSkn = False
desktopSize = getDesktop(0).size()
sz_w = desktopSize.width()
if sz_w > 800:
    HDSkn = True
else:
    HDSkn = False
EXTENSIONS = {'mp2': 'music', 'mp3': 'music', 'wav': 'music', 'ogg': 'music', 'flac': 'music', 
   'm4a': 'music', 
   'jpg': 'picture', 
   'jpeg': 'picture', 
   'jpe': 'picture', 
   'png': 'picture', 
   'bmp': 'picture', 
   'mvi': 'picture', 
   'ts': 'movie', 
   'm2ts': 'movie', 
   'avi': 'movie', 
   'divx': 'movie', 
   'mpg': 'movie', 
   'mpeg': 'movie', 
   'mkv': 'movie', 
   'mp4': 'movie', 
   'mov': 'movie', 
   'vob': 'movie', 
   'ifo': 'movie', 
   'iso': 'movie', 
   'flv': 'movie', 
   '3gp': 'movie', 
   'mod': 'movie', 
   'wmv': 'movie', 
   'ipk': 'package', 
   'gz': 'package', 
   'bz2': 'package', 
   'sh': 'script'}

class vInputBox(Screen, myNumericalTextInput):
    vibnewx = str(getDesktop(0).size().width() - 80)
    sknew = '<screen name="vInputBox" position="center,center" size="' + vibnewx + ',70" title="Input...">\n'
    sknew = sknew + '<widget name="text" position="5,5" size="1270,25" font="Console;16"/>\n<widget name="input" position="0,40" size="'
    sknew = sknew + vibnewx + ',30" font="Console;22"/>\n</screen>'
    skin = sknew

    def __init__(self, session, title='', windowTitle=_('Input'), useableChars=None, **kwargs):
        Screen.__init__(self, session)
        myNumericalTextInput.__init__(self, nextFunc=None, handleTimeout=False)
        self.session = session
        self['text'] = Label(title)
        self['input'] = Input(**kwargs)
        self.onShown.append(boundFunction(self.setTitle, windowTitle))
        if useableChars is not None:
            self['input'].setUseableChars(useableChars)
        self['actions'] = NumberActionMap(['WizardActions',
         'InputBoxActions',
         'InputAsciiActions',
         'KeyboardInputActions'], {'gotAsciiCode': (self.gotAsciiCode), 'ok': (self.go), 'back': (self.cancel), 
           'left': (self.keyLeft), 
           'right': (self.keyRight), 
           'home': (self.keyHome), 
           'end': (self.keyEnd), 
           'deleteForward': (self.keyDelete), 
           'deleteBackward': (self.keyBackspace), 
           'tab': (self.keyTab), 
           'toggleOverwrite': (self.keyInsert), 
           '1': (self.keyNumberGlobal), 
           '2': (self.keyNumberGlobal), 
           '3': (self.keyNumberGlobal), 
           '4': (self.keyNumberGlobal), 
           '5': (self.keyNumberGlobal), 
           '6': (self.keyNumberGlobal), 
           '7': (self.keyNumberGlobal), 
           '8': (self.keyNumberGlobal), 
           '9': (self.keyNumberGlobal), 
           '0': (self.keyNumberGlobal)}, -1)
        if self['input'].type == Input.TEXT:
            rcinput = eRCInput.getInstance()
            rcinput.setKeyboardMode(rcinput.kmAscii)
        self.onLayoutFinish.append(self.NumDlgInit)
        return

    def NumDlgInit(self):
        self.help_window = self.session.instantiateDialog(NumericalTextInputHelpDialog, self)
        self.help_window.show()
        return

    def gotAsciiCode(self):
        self['input'].handleAscii(getPrevAsciiCode())
        return

    def keyLeft(self):
        self['input'].left()
        return

    def keyRight(self):
        self['input'].right()
        return

    def keyNumberGlobal(self, number):
        self['input'].number(number)
        return

    def keyDelete(self):
        self['input'].delete()
        return

    def go(self):
        rcinput = eRCInput.getInstance()
        rcinput.setKeyboardMode(rcinput.kmNone)
        self.session.deleteDialog(self.help_window)
        self.help_window = None
        self.close(self['input'].getText())
        return

    def cancel(self):
        rcinput = eRCInput.getInstance()
        rcinput.setKeyboardMode(rcinput.kmNone)
        self.session.deleteDialog(self.help_window)
        self.help_window = None
        self.close(None)
        return

    def keyHome(self):
        self['input'].home()
        return

    def keyEnd(self):
        self['input'].end()
        return

    def keyBackspace(self):
        self['input'].deleteBackward()
        return

    def keyTab(self):
        self['input'].tab()
        return

    def keyInsert(self):
        self['input'].toggleOverwrite()
        return


def FileEntryComponent(name, absolute=None, isDir=False):
    res = [(absolute, isDir)]
    if desktopSize.width() == 1920:
        res.append((eListboxPythonMultiContent.TYPE_TEXT,
         55,
         0,
         1000,
         40,
         0,
         RT_HALIGN_LEFT | RT_VALIGN_CENTER,
         name))
    else:
        res.append((eListboxPythonMultiContent.TYPE_TEXT,
         43,
         0,
         1000,
         30,
         0,
         RT_HALIGN_LEFT | RT_VALIGN_CENTER,
         name))
    if isDir:
        png = LoadPixmap('/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/dir.png')
    else:
        extension = name.split('.')
        extension = extension[-1].lower()
        if EXTENSIONS.has_key(extension):
            png = LoadPixmap('/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/' + EXTENSIONS[extension] + '.png')
        else:
            png = None
    if png is not None:
        if desktopSize.width() == 1920:
            res.append((eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST,
             10,
             2,
             36,
             36,
             png))
        else:
            res.append((eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST,
             10,
             2,
             26,
             26,
             png))
    return res


class myFileList(MenuList):

    def __init__(self, directory, showDirectories=True, showFiles=True, showMountpoints=True, matchingPattern=None, useServiceRef=False, inhibitDirs=False, inhibitMounts=False, isTop=False, enableWrapAround=True, additionalExtensions=None):
        MenuList.__init__(self, list, enableWrapAround, eListboxPythonMultiContent)
        self.additional_extensions = additionalExtensions
        self.mountpoints = []
        self.current_directory = None
        self.current_mountpoint = None
        self.useServiceRef = useServiceRef
        self.showDirectories = showDirectories
        self.showMountpoints = showMountpoints
        self.showFiles = showFiles
        self.isTop = isTop
        self.matchingPattern = matchingPattern
        self.inhibitDirs = inhibitDirs or []
        self.inhibitMounts = inhibitMounts or []
        self.refreshMountpoints()
        self.changeDir(directory)
        if desktopSize.width() == 1920:
            self.l.setFont(0, gFont('Regular', 28))
            self.l.setItemHeight(40)
        else:
            self.l.setFont(0, gFont('Regular', 19))
            self.l.setItemHeight(30)
        self.serviceHandler = eServiceCenter.getInstance()
        return

    def refreshMountpoints(self):
        self.mountpoints = [os_path.join(p.mountpoint, '') for p in harddiskmanager.getMountedPartitions()]
        self.mountpoints.sort(reverse=True)
        return

    def getMountpoint(self, file):
        file = os_path.join(os_path.realpath(file), '')
        for m in self.mountpoints:
            if file.startswith(m):
                return m

        return False

    def getMountpointLink(self, file):
        if os_path.realpath(file) == file:
            return self.getMountpoint(file)
        else:
            if file[-1] == '/':
                file = file[:-1]
            mp = self.getMountpoint(file)
            last = file
            file = os_path.dirname(file)
            while last != '/' and mp == self.getMountpoint(file):
                last = file
                file = os_path.dirname(file)

            return os_path.join(last, '')

        return

    def getSelection(self):
        if self.l.getCurrentSelection() is None:
            return
        else:
            return self.l.getCurrentSelection()[0]
            return

    def getCurrentEvent(self):
        l = self.l.getCurrentSelection()
        if not l or l[0][1] == True:
            return
        return self.serviceHandler.info(l[0][0]).getEvent(l[0][0])

    def getFileList(self):
        return self.list

    def inParentDirs(self, dir, parents):
        dir = os_path.realpath(dir)
        for p in parents:
            if dir.startswith(p):
                return True

        return False

    def changeDir(self, directory, select=None):
        self.list = []
        if self.current_directory is None:
            if directory and self.showMountpoints:
                self.current_mountpoint = self.getMountpointLink(directory)
            else:
                self.current_mountpoint = None
        self.current_directory = directory
        directories = []
        files = []
        if directory is None and self.showMountpoints:
            for p in harddiskmanager.getMountedPartitions():
                path = os_path.join(p.mountpoint, '')
                if path not in self.inhibitMounts and not self.inParentDirs(path, self.inhibitDirs):
                    self.list.append(FileEntryComponent(name=p.description, absolute=path, isDir=True))

            files = []
            directories = []
        elif directory is None:
            files = []
            directories = []
        elif self.useServiceRef:
            root = eServiceReference('2:0:1:0:0:0:0:0:0:0:' + directory)
            if self.additional_extensions:
                root.setName(self.additional_extensions)
            serviceHandler = eServiceCenter.getInstance()
            list = serviceHandler.list(root)
            while 1:
                s = list.getNext()
                if not s.valid():
                    del list
                    break
                if s.flags & s.mustDescent:
                    directories.append(s.getPath())
                else:
                    files.append(s)

            directories.sort()
            files.sort()
        elif os_path.exists(directory):
            try:
                files = listdir(directory)
            except:
                files = []

            files.sort()
            tmpfiles = files[:]
            for x in tmpfiles:
                if os_path.isdir(directory + x):
                    directories.append(directory + x + '/')
                    files.remove(x)

        if directory is not None and self.showDirectories and not self.isTop:
            if directory == self.current_mountpoint and self.showMountpoints:
                self.list.append(FileEntryComponent(name='<' + _('List of Storage Devices') + '>', absolute=None, isDir=True))
            elif directory != '/' and not (self.inhibitMounts and self.getMountpoint(directory) in self.inhibitMounts):
                self.list.append(FileEntryComponent(name='<' + _('Parent Directory') + '>', absolute=('/').join(directory.split('/')[:-2]) + '/', isDir=True))
        if self.showDirectories:
            for x in directories:
                if not (self.inhibitMounts and self.getMountpoint(x) in self.inhibitMounts) and not self.inParentDirs(x, self.inhibitDirs):
                    name = x.split('/')[-2]
                    self.list.append(FileEntryComponent(name=name, absolute=x, isDir=True))

        if self.showFiles:
            for x in files:
                if self.useServiceRef:
                    path = x.getPath()
                    name = path.split('/')[-1]
                else:
                    path = directory + x
                    name = x
                    nx = None
                    if config.plugins.FileExplorer.MediaFilter.value == 'on':
                        nx = self.getTSInfo(path)
                        if nx is not None:
                            name = nx
                EXext = os_path.splitext(path)[1]
                EXext = EXext.replace('.', '')
                EXext = EXext.lower()
                if EXext == '':
                    EXext = 'nothing'
                if self.matchingPattern is None or EXext in self.matchingPattern:
                    if nx is None:
                        self.list.append(FileEntryComponent(name=name, absolute=x, isDir=False))
                    else:
                        res = [(x, False)]
                        res.append((eListboxPythonMultiContent.TYPE_TEXT,
                         40,
                         2,
                         1000,
                         22,
                         0,
                         RT_HALIGN_LEFT,
                         name + ' [' + self.getTSLength(path) + ']'))
                        png = LoadPixmap('/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/movie.png')
                        res.append((eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST,
                         12,
                         3,
                         20,
                         20,
                         png))
                        self.list.append(res)

        self.l.setList(self.list)
        if select is not None:
            i = 0
            self.moveToIndex(0)
            for x in self.list:
                p = x[0][0]
                if isinstance(p, eServiceReference):
                    p = p.getPath()
                if p == select:
                    self.moveToIndex(i)
                i += 1

        return

    def getCurrentDirectory(self):
        return self.current_directory

    def canDescent(self):
        if self.getSelection() is None:
            return False
        else:
            return self.getSelection()[1]
            return

    def descent(self):
        if self.getSelection() is None:
            return
        else:
            self.changeDir(self.getSelection()[0], select=self.current_directory)
            return
            return

    def getFilename(self):
        if self.getSelection() is None:
            return
        else:
            x = self.getSelection()[0]
            if isinstance(x, eServiceReference):
                x = x.getPath()
            return x
            return

    def getServiceRef(self):
        if self.getSelection() is None:
            return
        else:
            x = self.getSelection()[0]
            if isinstance(x, eServiceReference):
                return x
            return
            return

    def execBegin(self):
        harddiskmanager.on_partition_list_change.append(self.partitionListChanged)
        return

    def execEnd(self):
        harddiskmanager.on_partition_list_change.remove(self.partitionListChanged)
        return

    def refresh(self):
        self.changeDir(self.current_directory, self.getFilename())
        return

    def partitionListChanged(self, action, device):
        self.refreshMountpoints()
        if self.current_directory is None:
            self.refresh()
        return

    def getTSInfo(self, path):
        if path.endswith('.ts'):
            serviceref = eServiceReference('1:0:0:0:0:0:0:0:0:0:' + path)
            if not serviceref.valid():
                return
            serviceHandler = eServiceCenter.getInstance()
            info = serviceHandler.info(serviceref)
            if info is not None:
                txt = info.getName(serviceref)
                description = info.getInfoString(serviceref, iServiceInformation.sDescription)
                if not txt.endswith('.ts'):
                    if description is not '':
                        return txt + ' - ' + description
                    else:
                        return txt

                else:
                    evt = info.getEvent(serviceref)
                    if evt:
                        return evt.getEventName() + ' - ' + evt.getShortDescription()
                    return
        return

    def getTSLength(self, path):
        tslen = ''
        if path.endswith('.ts'):
            serviceref = eServiceReference('1:0:0:0:0:0:0:0:0:0:' + path)
            serviceHandler = eServiceCenter.getInstance()
            info = serviceHandler.info(serviceref)
            tslen = info.getLength(serviceref)
            if tslen > 0:
                tslen = '%d:%02d' % (tslen / 60, tslen % 60)
            else:
                tslen = ''
        return tslen

    def byNameFunc(self, a, b):
        return cmp(b[0][1], a[0][1]) or cmp(a[1][7], b[1][7])

    def sortName(self):
        self.list.sort(self.byNameFunc)
        self.l.setList(self.list)
        self.moveToIndex(0)
        return

    def byDateFunc(self, a, b):
        try:
            stat1 = os_stat(self.current_directory + a[0][0])
            stat2 = os_stat(self.current_directory + b[0][0])
        except:
            return 0

        return cmp(b[0][1], a[0][1]) or cmp(stat2.st_ctime, stat1.st_ctime)

    def sortDate(self):
        self.list.sort(self.byDateFunc)
        self.l.setList(self.list)
        self.moveToIndex(0)
        return


class FileExplorerII(Screen):
    if HDSkn:
        if desktopSize.width() > 1030:
            skin_1280 = '\n                               <screen  position="center,77" size="920,600" title="Files Explorer"  >\n                                <widget name="info" position="15,0" zPosition="4" size="890,40" font="Regular;22" transparent="1" halign="left" valign="center" /> \n                                <eLabel position="20,50" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\n                                <widget name="filelist" position="15,60" scrollbarMode="showOnDemand" size="880,450" zPosition="4" transparent="1" />\n                                <eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\n                                <ePixmap name="red"    position="44,545"   zPosition="2" size="150,30" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" transparent="1" alphatest="blend" />\n\t                        <ePixmap name="green"  position="200,545" zPosition="2" size="150,30" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_green.png" transparent="1" alphatest="blend" />\n\t                        <ePixmap name="yellow" position="356,545" zPosition="2" size="150,30" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_yellow.png" transparent="1" alphatest="blend" /> \n        \t                <ePixmap name="blue"   position="512,545" zPosition="2" size="150,30" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_blue.png" transparent="1" alphatest="blend" /> \n        \t                <eLabel name="key_red" text="Delete" position="44,550" size="150,30" valign="center" halign="center" zPosition="4" font="Regular;20" transparent="1" /> \n        \t                <eLabel name="key_green" text="Rename" position="200,550" size="150,30" valign="center" halign="center" zPosition="4" font="Regular;20" transparent="1" /> \n                                <eLabel name="key_yellow" text="Move/Copy" position="356,550" size="150,30" valign="center" halign="center" zPosition="4" font="Regular;20" transparent="1" />\n        \t                <eLabel name="key_blue" text="Bookmarks" position="512,550" size="150,30" valign="center" halign="center" zPosition="4" font="Regular;20" transparent="1" />\n\t\t\t\t<ePixmap alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_menu.png" position="680,545" size="35,25" zPosition="5"/>\n\t\t\t\t<ePixmap alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_info.png" position="815,545" size="35,25" zPosition="5"/>\n\t\t\t\t<eLabel font="Regular;18" halign="left" position="725,547" size="120,25" text="Options" transparent="1" valign="center" zPosition="6"/>\n\t\t\t\t<eLabel font="Regular;18" halign="left" position="860,547" size="90,25" text="Info" transparent="1" valign="center" zPosition="6"/>\n\t\t\t\t</screen>'
            skin_1920 = '    <screen name="FileExplorerII" position="center,200" size="1300,720" title=" \n                FileExplorer">\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png" position="50,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green-big.png" position="360,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/yellow-big.png" position="670,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/blue-big.png" position="980,640" size="200,40" alphatest="blend" />\n        <eLabel name="key_red" text="Delete" position="50,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#940d0d" transparent="1" />\n        <eLabel name="key_green" text="Rename" position="360,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#2d872d" transparent="1" />\n        <eLabel name="key_yellow" text="Move/Copy" position="670,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#bba502" transparent="1" />\n        <eLabel name="key_blue" text="Bookmarks" position="980,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#18188b" transparent="1" />\n        <ePixmap name="key_info" position="1248,636" size="48,48" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_info-big.png" transparent="1" alphatest="blend" />\n        <ePixmap name="key_menu" position="1190,636" size="48,48" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_menu-big.png" transparent="1" alphatest="blend" />\n        <widget name="info" position="20,530" size="1260,40" foregroundColor="foreground" backgroundColor="background" font="Regular;28" valign="center" halign="left" transparent="1" zPosition="1" />\n        <eLabel position="10,520" zPosition="4" size="1280,1" backgroundColor="foreground" />\n        <widget name="filelist" position="20,20" size="1260,480" zPosition="2" itemHeight="40" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background"  transparent="1" />\n        </screen>'
            if desktopSize.width() == 1920:
                skin = skin_1920
            else:
                skin = skin_1280
        else:
            skin = '\n\t\t\t\t<screen position="center,77" size="900,450" title="Files Explorer">\n\t\t\t\t<widget name="filelist" position="5,2" scrollbarMode="showOnDemand" size="890,416" zPosition="4"/>\n\t\t\t\t<eLabel backgroundColor="#555555" position="5,420" size="890,2" zPosition="5"/>\n\t\t\t\t<ePixmap alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" position="0,425" size="35,25" zPosition="5"/>\n\t\t\t\t<ePixmap alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_green.png" position="155,425" size="35,25" zPosition="5"/>\n\t\t\t\t<ePixmap alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_yellow.png" position="310,425" size="35,25" zPosition="5"/>\n\t\t\t\t<ePixmap alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_blue.png" position="465,425" size="35,25" zPosition="5"/>\n\t\t\t\t<ePixmap alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_menu.png" position="620,425" size="35,25" zPosition="5"/>\n\t\t\t\t<ePixmap alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_info.png" position="775,425" size="35,25" zPosition="5"/>\n\t\t\t\t<eLabel font="Regular;18" halign="left" position="35,425" size="120,25" text="Delete" transparent="1" valign="center" zPosition="6"/>\n\t\t\t\t<eLabel font="Regular;18" halign="left" position="190,425" size="120,25" text="Rename" transparent="1" valign="center" zPosition="6"/>\n\t\t\t\t<eLabel font="Regular;18" halign="left" position="345,425" size="120,25" text="Move/Copy" transparent="1" valign="center" zPosition="6"/>\n\t\t\t\t<eLabel font="Regular;18" halign="left" position="500,425" size="120,25" text="Bookmarks" transparent="1" valign="center" zPosition="6"/>\n\t\t\t\t<eLabel font="Regular;18" halign="left" position="655,425" size="120,25" text="Options" transparent="1" valign="center" zPosition="6"/>\n\t\t\t\t<eLabel font="Regular;18" halign="left" position="810,425" size="90,25" text="Info" transparent="1" valign="center" zPosition="6"/>\n\t\t\t\t</screen>'
    else:
        skin = '\n\t\t\t<screen position="center,77" size="620,450" title="Files Explorer">\n\t\t\t<widget name="filelist" position="5,2" scrollbarMode="showOnDemand" size="610,416" zPosition="4"/>\n\t\t\t<eLabel backgroundColor="#555555" position="5,420" size="610,2" zPosition="5"/>\n\t\t\t<ePixmap alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" position="0,425" size="35,25" zPosition="5"/>\n\t\t\t<ePixmap alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_green.png" position="145,425" size="35,25" zPosition="5"/>\n\t\t\t<ePixmap alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_yellow.png" position="290,425" size="35,25" zPosition="5"/>\n\t\t\t<ePixmap alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_blue.png" position="430,425" size="35,25" zPosition="5"/>\n\t\t\t<ePixmap alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_info.png" position="555,425" size="35,25" zPosition="5"/>\n\t\t\t<ePixmap alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_menu.png" position="585,425" size="35,25" zPosition="5"/>\n\t\t\t<eLabel font="Regular;16" halign="left" position="35,425" size="100,25" text="Delete" transparent="1" valign="center" zPosition="6"/>\n\t\t\t<eLabel font="Regular;16" halign="left" position="180,425" size="100,25" text="Rename" transparent="1" valign="center" zPosition="6"/>\n\t\t\t<eLabel font="Regular;16" halign="left" position="325,425" size="100,25" text="Move/Copy" transparent="1" valign="center" zPosition="6"/>\n\t\t\t<eLabel font="Regular;16" halign="left" position="465,425" size="100,25" text="Bookmarks" transparent="1" valign="center" zPosition="6"/>\n\t\t\t</screen>'

    def __init__(self, session, args=None):
        self.skin = FileExplorerII.skin
        Screen.__init__(self, session)
        self.sesion = session
        self.altservice = self.session.nav.getCurrentlyPlayingServiceReference()
        self.MyBox = HardwareInfo().get_device_name()
        self.commando = ['ls']
        self.selectedDir = '/tmp/'
        self.booklines = []
        self.MediaPattern = '^.*\\.(ts|m2ts|mp3|wav|ogg|jpg|jpeg|jpe|png|bmp|mpg|mpeg|mkv|mp4|mov|divx|avi|mp2|m4a|flac|ifo|vob|iso|sh|flv|3gp|mod|wmv)'
        if pathExists(config.plugins.FileExplorer.startDir.value):
            StartMeOn = config.plugins.FileExplorer.startDir.value
        else:
            StartMeOn = None
        if config.plugins.FileExplorer.MediaFilter.value == 'off':
            self.MediaFilter = False
            self['filelist'] = myFileList(StartMeOn, showDirectories=True, showFiles=True, matchingPattern=None, useServiceRef=False)
        else:
            self.MediaFilter = True
            self['filelist'] = myFileList(StartMeOn, showDirectories=True, showFiles=True, matchingPattern=self.MediaPattern, useServiceRef=False)
        self['TEMPfl'] = FileList('/', matchingPattern='(?i)^.*\\.(jpeg|jpg|jpe|png|bmp)')
        self['info'] = Label('')
        self['actions'] = ActionMap([15, 
         16, 
         17, 
         18, 
         19, 
         20], {'ok': (self.ok), 'back': (self.explExit), 'green': (self.ExecRename), 
           'red': (self.ExecDelete), 
           'blue': (self.goToBookmark), 
           'yellow': (self.go2CPmaniger), 
           'menu': (self.explContextMenu), 
           'info': (self.Info), 
           'left': (self.left), 
           'right': (self.right), 
           'up': (self.up), 
           'down': (self.down), 
           'nextBouquet': (self.sortName), 
           'prevBouquet': (self.sortDate), 
           'showMovies': (self.CloseAndPlay)}, -1)
        self.onShown.append(self.setWindowTitle)
        self.onLayoutFinish.append(self.byLayoutEnd)
        return

    def setWindowTitle(self):
        self.setTitle('Files Explorer')
        return

    def ok(self):
        global DVDPlayerAviable
        if self['filelist'].canDescent():
            self['filelist'].descent()
            self.updateLocationInfo()
        else:
            filename = self['filelist'].getCurrentDirectory() + self['filelist'].getFilename()
            testFileName = self['filelist'].getFilename()
            testFileName = testFileName.lower()
            if filename != None:
                if testFileName.endswith('.ts'):
                    fileRef = eServiceReference('1:0:0:0:0:0:0:0:0:0:' + filename)
                    self.session.open(MoviePlayer, fileRef)
                elif testFileName.endswith('.mpg') or testFileName.endswith('.mpeg') or testFileName.endswith('.mkv') or testFileName.endswith('.m2ts') or testFileName.endswith('.vob') or testFileName.endswith('.mod'):
                    fileRef = eServiceReference('4097:0:0:0:0:0:0:0:0:0:' + filename)
                    self.session.open(MoviePlayer, fileRef)
                elif testFileName.endswith('.avi') or testFileName.endswith('.mp4') or testFileName.endswith('.divx') or testFileName.endswith('.mov') or testFileName.endswith('.flv') or testFileName.endswith('.3gp') or testFileName.endswith('.wmv') and self.MyBox == 'dm7020hd':
                    if not self.MyBox == 'dm7025':
                        fileRef = eServiceReference('4097:0:0:0:0:0:0:0:0:0:' + filename)
                        self.session.open(MoviePlayer, fileRef)
                elif testFileName.endswith('.mp3') or testFileName.endswith('.wav') or testFileName.endswith('.ogg') or testFileName.endswith('.m4a') or testFileName.endswith('.mp2') or testFileName.endswith('.flac'):
                    if self.MyBox == 'dm7025' and (testFileName.endswith('.m4a') or testFileName.endswith('.mp2') or testFileName.endswith('.flac')):
                        return
                    if MMPavaiable:
                        SongList, SongIndex = self.searchMusic()
                        try:
                            self.session.open(MerlinMusicPlayerScreen, SongList, SongIndex, False, self.altservice, None)
                        except:
                            self.session.open(MessageBox, _('Incompatible MerlinMusicPlayer version!'), MessageBox.TYPE_INFO)

                    else:
                        fileRef = eServiceReference('4097:0:0:0:0:0:0:0:0:0:' + filename)
                        m_dir = self['filelist'].getCurrentDirectory()
                        self.session.open(MusicExplorer, fileRef, m_dir, testFileName)
                elif testFileName.endswith('.jpg') or testFileName.endswith('.jpeg') or testFileName.endswith('.jpe') or testFileName.endswith('.png') or testFileName.endswith('.bmp'):
                    if self['filelist'].getSelectionIndex() != 0:
                        Pdir = self['filelist'].getCurrentDirectory()
                        self.session.open(PictureExplorerII, filename, Pdir)
                elif testFileName.endswith('.mvi'):
                    self.session.nav.stopService()
                    self.session.open(MviExplorer, filename)
                elif testFileName == 'video_ts.ifo':
                    if DVDPlayerAviable:
                        if self['filelist'].getCurrentDirectory().lower().endswith('video_ts/'):
                            self.session.open(DVDPlayer, dvd_filelist=[self['filelist'].getCurrentDirectory()])
                elif testFileName.endswith('.iso'):
                    if DVDPlayerAviable:
                        self.session.open(DVDPlayer, dvd_filelist=[filename])
                elif testFileName.endswith('.bootlogo.tar.gz'):
                    self.commando = ['mount -rw /boot -o remount',
                     'sleep 3',
                     'tar -xzvf ' + filename + ' -C /',
                     'mount -ro /boot -o remount']
                    askList = [(_('Cancel'), 'NO'), (_('Install new bootlogo...'), 'YES2ALL')]
                    dei = self.session.openWithCallback(self.SysExecution, ChoiceBox, title=_('Bootlogo-package:\\n' + filename), list=askList)
                    dei.setTitle(_('Files-Explorer : Install...'))
                elif testFileName.endswith('.tar.gz'):
                    self.commando = ['tar -xzvf ' + filename + ' -C /']
                    askList = [(_('Cancel'), 'NO'), (_('Install this package'), 'YES')]
                    dei = self.session.openWithCallback(self.SysExecution, ChoiceBox, title=_('GZ-package:\\n' + filename), list=askList)
                    dei.setTitle(_('Files-Explorer : Install...'))
                elif testFileName.endswith('.tar.bz2'):
                    self.commando = ['tar -xjvf ' + filename + ' -C /']
                    askList = [(_('Cancel'), 'NO'), (_('Install this package'), 'YES')]
                    dei = self.session.openWithCallback(self.SysExecution, ChoiceBox, title=_('BZ2-package:\\n' + filename), list=askList)
                    dei.setTitle(_('Files-Explorer : Install...'))
                elif testFileName.endswith('.deb'):
                    if fileExists('/usr/bin/dpkg'):
                        self.commando = ['dpkg -i ' + filename]
                    askList = [
                     (
                      _('Cancel'), 'NO'), (_('Install this package'), 'YES')]
                    dei = self.session.openWithCallback(self.SysExecution, ChoiceBox, title=_('DPKG-package:\\n' + filename), list=askList)
                    dei.setTitle(_('Files-Explorer : Install...'))
                elif testFileName.endswith('.ipk'):
                    if fileExists('/usr/bin/opkg'):
                        self.commando = ['opkg install ' + filename]
                    else:
                        self.commando = [
                         'ipkg install ' + filename]
                    askList = [
                     (
                      _('Cancel'), 'NO'), (_('Install this package'), 'YES')]
                    dei = self.session.openWithCallback(self.SysExecution, ChoiceBox, title=_('IPKG-package:\\n' + filename), list=askList)
                    dei.setTitle(_('Files-Explorer : Install...'))
                elif testFileName.endswith('.pyc') or testFileName.endswith('.pyo'):
                    self.commando = ['/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/pyc2xml ' + filename]
                    askList = [(_('Cancel'), 'NO'), (_('Disassemble to bytecode...'), 'YES')]
                    dei = self.session.openWithCallback(self.SysExecution, ChoiceBox, title=_('Pyc-Script:\\n' + filename), list=askList)
                    dei.setTitle(_('Files-Explorer : Disassemble...'))
                elif testFileName.endswith('.sh'):
                    self.commando = [filename]
                    askList = [(_('Cancel'), 'NO'), (_('View this shell-script'), 'VIEW'), (_('Start execution'), 'YES')]
                    self.session.openWithCallback(self.SysExecution, ChoiceBox, title=_('Do you want to execute?\\n' + filename), list=askList)
                else:
                    xfile = os_stat(filename)
                    if xfile.st_size < 61440:
                        self.session.open(vEditor, filename)
        return

    def byLayoutEnd(self):
        self.updateLocationInfo()
        if fileExists('/etc/myBookmarks'):
            try:
                booklist = open('/etc/myBookmarks', 'r')
            except:
                dei = self.session.open(MessageBox, _('Error by reading bookmarks !!!'), MessageBox.TYPE_ERROR)
                dei.setTitle(_('Files Explorer'))

            if booklist is not None:
                for oneline in booklist:
                    self.booklines.append(oneline)

                booklist.close()
        return

    def updateLocationInfo(self):
        try:
            if self.MediaFilter:
                self['info'].setText(_('[Media files] ' + self['filelist'].getCurrentDirectory()))
            else:
                self['info'].setText(_('[All files] ' + self['filelist'].getCurrentDirectory()))
        except:
            self['info'].setText(_(''))

        return

    def explContextMenu(self):
        if self.MediaFilter:
            mftext = 'Disable'
        else:
            mftext = 'Enable'
        if self['filelist'].canDescent():
            if self['filelist'].getSelectionIndex() != 0:
                self.selectedDir = self['filelist'].getSelection()[0]
                if self.selectedDir + '\n' in self.booklines:
                    BMtext = 'Remove directory from Bookmarks'
                    BMstring = 'DELLINK'
                else:
                    BMtext = 'Add directory to Bookmarks'
                    BMstring = 'ADDLINK'
                contextDirList = [
                 (
                  _('Cancel'), 'NO'),
                 (
                  _(mftext + ' Media-filter'), 'FILTER'),
                 (
                  _('Sort by name (bouquet+)'), 'SORTNAME'),
                 (
                  _('Sort by date (bouquet-)'), 'SORTDATE'),
                 (
                  _(BMtext), BMstring),
                 (
                  _('Create new file'), 'NEWFILE'),
                 (
                  _('Create new directory'), 'NEWDIR'),
                 (
                  _('Set start directory'), 'SETSTARTDIR')]
                dei = self.session.openWithCallback(self.SysExecution, ChoiceBox, title=_('Options:\n'), list=contextDirList)
                dei.setTitle(_('Files Explorer'))
            else:
                contextFileList = [(_('Cancel'), 'NO'),
                 (
                  _(mftext + ' Media-filter'), 'FILTER'),
                 (
                  _('Sort by name (bouquet+)'), 'SORTNAME'),
                 (
                  _('Sort by date (bouquet-)'), 'SORTDATE'),
                 (
                  _('Pack my bootlogo'), 'PACKLOGOS')]
                dei = self.session.openWithCallback(self.SysExecution, ChoiceBox, title=_('Options:\n'), list=contextFileList)
                dei.setTitle(_('Files Explorer'))
        else:
            contextFileList = [
             (
              _('Cancel'), 'NO'),
             (
              _(mftext + ' Media-filter'), 'FILTER'),
             (
              _('Sort by name (bouquet+)'), 'SORTNAME'),
             (
              _('Sort by date (bouquet-)'), 'SORTDATE'),
             (
              _('Preview all pictures'), 'PLAYDIRPICTURE'),
             (
              _('Create new file'), 'NEWFILE'),
             (
              _('Create new directory'), 'NEWDIR'),
             (
              _('Create softlink...'), 'SOFTLINK'),
             (
              _('Set archive mode (644)'), 'CHMOD644'),
             (
              _('Set executable mode (755)'), 'CHMOD755')]
            dei = self.session.openWithCallback(self.SysExecution, ChoiceBox, title=_('Options:\n'), list=contextFileList)
            dei.setTitle(_('Files Explorer'))
        return

    def SysExecution(self, answer):
        global PicPlayerAviable
        answer = answer and answer[1]
        if answer == 'YES':
            self.session.open(Console, cmdlist=[self.commando[0]])
        elif answer == 'YES2ALL':
            self.session.open(Console, cmdlist=self.commando)
        elif answer == 'PACKLOGOS':
            self.session.open(Console, cmdlist=['cd /tmp/', 'tar -czf /tmp/dreambox.bootlogo.tar.gz /usr/share/bootlogo.mvi /usr/share/bootlogo_wait.mvi /usr/share/backdrop.mvi /boot/bootlogo-' + self.MyBox + '.jpg'])
        elif answer == 'VIEW':
            yfile = os_stat(self.commando[0])
            if yfile.st_size < 61440:
                self.session.open(vEditor, self.commando[0])
        elif answer == 'PLAYDIRPICTURE':
            if PicPlayerAviable:
                self['TEMPfl'].changeDir(self['filelist'].getCurrentDirectory())
                self.session.open(Pic_Thumb, self['TEMPfl'].getFileList(), 0, self['filelist'].getCurrentDirectory())
            else:
                dei = self.session.open(MessageBox, _('Picture-Player not aviable.'), MessageBox.TYPE_ERROR)
                dei.setTitle(_('Files Explorer'))
        elif answer == 'ADDLINK':
            try:
                newbooklist = open('/etc/myBookmarks', 'w')
            except:
                dei = self.session.open(MessageBox, _('Error by writing bookmarks !!!'), MessageBox.TYPE_ERROR)
                dei.setTitle(_('Files Explorer'))

            if newbooklist is not None:
                self.booklines.append(self.selectedDir + '\n')
                for one_line in self.booklines:
                    newbooklist.write(one_line)

                newbooklist.close()
        elif answer == 'DELLINK':
            temp_book = []
            for bidx in range(len(self.booklines) - 1):
                if self.selectedDir not in self.booklines[bidx]:
                    temp_book.append(self.booklines[bidx])

            self.booklines = []
            self.booklines = temp_book
            try:
                newbooklist = open('/etc/myBookmarks', 'w')
            except:
                dei = self.session.open(MessageBox, _('Error by writing bookmarks !!!'), MessageBox.TYPE_ERROR)
                dei.setTitle(_('Files Explorer'))

            if newbooklist is not None:
                for one_line in self.booklines:
                    newbooklist.write(one_line)

                newbooklist.close()
        elif answer == 'FILTER':
            if self.MediaFilter:
                self.MediaFilter = False
                config.plugins.FileExplorer.MediaFilter.value = 'off'
                config.plugins.FileExplorer.MediaFilter.save()
                self['filelist'].matchingPattern = None
                self['filelist'].refresh()
                self.updateLocationInfo()
            else:
                self.MediaFilter = True
                config.plugins.FileExplorer.MediaFilter.value = 'on'
                config.plugins.FileExplorer.MediaFilter.save()
                self['filelist'].matchingPattern = self.MediaPattern
                self['filelist'].refresh()
                self.updateLocationInfo()
        elif answer == 'NEWFILE':
            self.session.openWithCallback(self.callbackNewFile, vInputBox, title=_(self['filelist'].getCurrentDirectory()), windowTitle=_('Create new file in...'), text='name')
        elif answer == 'NEWDIR':
            self.session.openWithCallback(self.callbackNewDir, vInputBox, title=_(self['filelist'].getCurrentDirectory()), windowTitle=_('Create new directory in...'), text='name')
        elif answer == 'SETSTARTDIR':
            newStartDir = self['filelist'].getSelection()[0]
            dei = self.session.openWithCallback(self.callbackSetStartDir, MessageBox, _('Do you want to set\n' + newStartDir + '\nas start directory?'), MessageBox.TYPE_YESNO)
            dei.setTitle(_('Files-Explorer...'))
        elif answer == 'SORTNAME':
            list = self.sortName()
        elif answer == 'SORTDATE':
            list = self.sortDate()
        elif answer == 'SOFTLINK':
            if not self.MediaFilter:
                self.session.openWithCallback(self.callbackCPmaniger, SoftLinkScreen, self['filelist'].getCurrentDirectory())
        elif answer == 'CHMOD644':
            os_system('chmod 644 ' + self['filelist'].getCurrentDirectory() + self['filelist'].getFilename())
        elif answer == 'CHMOD755':
            os_system('chmod 755 ' + self['filelist'].getCurrentDirectory() + self['filelist'].getFilename())
        return

    def up(self):
        self['filelist'].up()
        self.updateLocationInfo()
        return

    def down(self):
        self['filelist'].down()
        self.updateLocationInfo()
        return

    def left(self):
        self['filelist'].pageUp()
        self.updateLocationInfo()
        return

    def right(self):
        self['filelist'].pageDown()
        self.updateLocationInfo()
        return

    def Humanizer(self, size):
        if size < 1024:
            humansize = str(size) + ' B'
        elif size < 1048576:
            humansize = str(size / 1024) + ' KB'
        else:
            humansize = str(size / 1048576) + ' MB'
        return humansize

    def Info(self):
        if self['filelist'].canDescent():
            if self['filelist'].getSelectionIndex() != 0:
                curSelDir = self['filelist'].getSelection()[0]
                dir_stats = os_stat(curSelDir)
                dir_infos = 'size ' + str(self.Humanizer(dir_stats.st_size)) + '    '
                dir_infos = dir_infos + 'last-mod ' + time_strftime('%d.%m.%Y %H:%M:%S', time_localtime(dir_stats.st_mtime)) + '    '
                dir_infos = dir_infos + 'mode ' + str(dir_stats.st_mode)
                self['info'].setText(_(dir_infos))
            else:
                dei = self.session.open(MessageBox, _('Dreambox: ' + self.MyBox + '\n\n' + ScanSysem_str()), MessageBox.TYPE_INFO)
                dei.setTitle(_('Files Explorer'))
        else:
            curSelFile = self['filelist'].getCurrentDirectory() + self['filelist'].getFilename()
            file_stats = os_stat(curSelFile)
            file_infos = 'size ' + str(self.Humanizer(file_stats.st_size)) + '    '
            file_infos = file_infos + 'last-mod ' + time_strftime('%d.%m.%Y %H:%M:%S', time_localtime(file_stats.st_mtime)) + '    '
            file_infos = file_infos + 'mode ' + str(file_stats.st_mode)
            self['info'].setText(_(file_infos))
            if curSelFile.endswith('.ts'):
                serviceref = eServiceReference('1:0:0:0:0:0:0:0:0:0:' + curSelFile)
                serviceHandler = eServiceCenter.getInstance()
                info = serviceHandler.info(serviceref)
                evt = info.getEvent(serviceref)
                if evt:
                    self.session.open(EventViewSimple, evt, ServiceReference(serviceref))
        return

    def setBookmark(self, answer):
        answer = answer and answer[1]
        try:
            if answer[0] == '/':
                self['filelist'].changeDir(answer[:-1])
                self.updateLocationInfo()
        except:
            pass

        return

    def goToBookmark(self):
        bml = [
         (
          _('Cancel'), 'BACK')]
        for onemark in self.booklines:
            bml.append((_(onemark), onemark))

        dei = self.session.openWithCallback(self.setBookmark, ChoiceBox, title=_('My Bookmarks'), list=bml)
        dei.setTitle(_('Files Explorer'))
        return

    def ExecDelete(self):
        if self.MediaFilter:
            dei = self.session.open(MessageBox, _('Turn off the media-filter first.'), MessageBox.TYPE_INFO)
            dei.setTitle(_('Files-Explorer...'))
            return
        if not self['filelist'].canDescent():
            DELfilename = self['filelist'].getCurrentDirectory() + self['filelist'].getFilename()
            dei = self.session.openWithCallback(self.callbackExecDelete, MessageBox, _('Do you realy want to DELETE:\n' + DELfilename), MessageBox.TYPE_YESNO)
            dei.setTitle(_('Files-Explorer - DELETE file...'))
        elif self['filelist'].getSelectionIndex() != 0 and self['filelist'].canDescent():
            DELDIR = self['filelist'].getSelection()[0]
            dei = self.session.openWithCallback(self.callbackDelDir, MessageBox, _('Do you realy want to DELETE:\n' + DELDIR + '\n\nYou do it at your own risk!'), MessageBox.TYPE_YESNO)
            dei.setTitle(_('Files-Explorer - DELETE DIRECTORY...'))
        return

    def callbackExecDelete(self, answer):
        if answer is True:
            DELfilename = self['filelist'].getCurrentDirectory() + self['filelist'].getFilename()
            order = 'rm -f "' + DELfilename + '"'
            try:
                os_system(order)
                self['filelist'].refresh()
            except:
                dei = self.session.open(MessageBox, _('%s \nFAILED!' % order), MessageBox.TYPE_ERROR)
                dei.setTitle(_('Files Explorer'))
                self['filelist'].refresh()

        return

    def callbackDelDir(self, answer):
        if answer is True:
            DELDIR = self['filelist'].getSelection()[0]
            order = 'rm -r "' + DELDIR + '"'
            try:
                os_system(order)
                self['filelist'].refresh()
            except:
                dei = self.session.open(MessageBox, _('%s \nFAILED!' % order), MessageBox.TYPE_ERROR)
                dei.setTitle(_('Files Explorer'))
                self['filelist'].refresh()

        return

    def ExecRename(self):
        if self.MediaFilter:
            dei = self.session.open(MessageBox, _('Turn off the media-filter first.'), MessageBox.TYPE_INFO)
            dei.setTitle(_('Files-Explorer...'))
            return
        if not self['filelist'].canDescent():
            RENfilename = self['filelist'].getFilename()
            self.session.openWithCallback(self.callbackExecRename, vInputBox, title=_('old:  ' + RENfilename), windowTitle=_('Rename file...'), text=RENfilename)
        elif self['filelist'].getSelectionIndex() != 0 and self['filelist'].canDescent():
            RENDIR = self['filelist'].getSelection()[0]
            self.session.openWithCallback(self.callbackRenDir, vInputBox, title=_('old:  ' + RENDIR), windowTitle=_('Rename directory...'), text=RENDIR)
        return

    def callbackExecRename(self, answer):
        if answer is not None:
            source = self['filelist'].getCurrentDirectory() + self['filelist'].getFilename()
            dest = self['filelist'].getCurrentDirectory() + answer
            try:
                os_rename(source, dest)
                self['filelist'].refresh()
            except:
                dei = self.session.open(MessageBox, _('Rename: %s \nFAILED!' % answer), MessageBox.TYPE_ERROR)
                dei.setTitle(_('Files Explorer'))
                self['filelist'].refresh()

        return

    def callbackRenDir(self, answer):
        if answer is not None:
            source = self['filelist'].getSelection()[0]
            dest = answer
            try:
                os_rename(source, dest)
                self['filelist'].refresh()
            except:
                dei = self.session.open(MessageBox, _('Rename: %s \nFAILED!' % answer), MessageBox.TYPE_ERROR)
                dei.setTitle(_('Files Explorer'))
                self['filelist'].refresh()

        return

    def callbackNewFile(self, answer):
        if answer is None:
            return
        else:
            dest = self['filelist'].getCurrentDirectory()
            if ' ' in answer or ' ' in dest or answer == '':
                dei = self.session.open(MessageBox, _('File name error !'), MessageBox.TYPE_ERROR)
                dei.setTitle(_('Files Explorer'))
                return
            order = 'touch ' + dest + answer
            try:
                if not fileExists(dest + answer):
                    os_system(order)
                self['filelist'].refresh()
            except:
                dei = self.session.open(MessageBox, _('%s \nFAILED!' % order), MessageBox.TYPE_ERROR)
                dei.setTitle(_('Files Explorer'))
                self['filelist'].refresh()

            return
            return

    def callbackNewDir(self, answer):
        if answer is None:
            return
        else:
            dest = self['filelist'].getCurrentDirectory()
            if ' ' in answer or ' ' in dest or answer == '':
                dei = self.session.open(MessageBox, _('Directory name error !'), MessageBox.TYPE_ERROR)
                dei.setTitle(_('Files Explorer'))
                return
            order = dest + answer
            try:
                if not pathExists(dest + answer):
                    os_mkdir(order)
                self['filelist'].refresh()
            except:
                dei = self.session.open(MessageBox, _('%s \nFAILED!' % order), MessageBox.TYPE_ERROR)
                dei.setTitle(_('Files Explorer'))
                self['filelist'].refresh()

            return
            return

    def go2CPmaniger(self):
        if self.MediaFilter:
            dei = self.session.open(MessageBox, _('Turn off the media-filter first.'), MessageBox.TYPE_INFO)
            dei.setTitle(_('Files-Explorer...'))
            return
        if not self['filelist'].canDescent():
            source = self['filelist'].getCurrentDirectory() + self['filelist'].getFilename()
            self.session.openWithCallback(self.callbackCPmaniger, CPmaniger, source)
        elif self['filelist'].getSelectionIndex() != 0 and self['filelist'].canDescent():
            source = self['filelist'].getSelection()[0]
            self.session.openWithCallback(self.callbackCPmaniger, CPmaniger, source)
        return

    def callbackCPmaniger(self, answer):
        self['filelist'].refresh()
        return

    def callbackSetStartDir(self, answerSD):
        if answerSD is True:
            config.plugins.FileExplorer.startDir.value = self['filelist'].getSelection()[0]
            config.plugins.FileExplorer.startDir.save()
        return

    def sortName(self):
        list = self['filelist'].sortName()
        try:
            if self.MediaFilter:
                self['info'].setText(_('[sort by Name] ' + self['filelist'].getCurrentDirectory()))
            else:
                self['info'].setText(_('[sort by Name] ' + self['filelist'].getCurrentDirectory()))
        except:
            self['info'].setText(_(''))

        return

    def sortDate(self):
        list = self['filelist'].sortDate()
        try:
            if self.MediaFilter:
                self['info'].setText(_('[sort by Date] ' + self['filelist'].getCurrentDirectory()))
            else:
                self['info'].setText(_('[sort by Date] ' + self['filelist'].getCurrentDirectory()))
        except:
            self['info'].setText(_(''))

        return

    def searchMusic(self):
        slist = []
        foundIndex = 0
        index = 0
        files = os_listdir(self['filelist'].getCurrentDirectory())
        files.sort()
        for name in files:
            testname = name.lower()
            if testname.endswith('.mp3') or name.endswith('.m4a') or name.endswith('.ogg') or name.endswith('.flac'):
                slist.append((Item(text=name, filename=os_path.join(self['filelist'].getCurrentDirectory(), name)),))
                if self['filelist'].getFilename() == name:
                    foundIndex = index
                index = index + 1

        return (slist, foundIndex)

    def explExit(self):
        self.session.nav.playService(self.altservice)
        try:
            if self.MediaFilter:
                config.plugins.FileExplorer.MediaFilter.value = 'on'
            else:
                config.plugins.FileExplorer.MediaFilter.value = 'off'
            config.plugins.FileExplorer.MediaFilter.save()
        except:
            pass

        self.close()
        return

    def CloseAndPlay(self):
        try:
            if self.MediaFilter:
                config.plugins.FileExplorer.MediaFilter.value = 'on'
            else:
                config.plugins.FileExplorer.MediaFilter.value = 'off'
            config.plugins.FileExplorer.MediaFilter.save()
        except:
            pass

        self.close()
        return


class vEditor(Screen):
    if HDSkn:
        if getDesktop(0).size().width() > 1030:
            skin_1280 = '\n\t\t\t<screen position="50,80" size="1180,590" title="File-Explorer">\n\t\t\t\t<widget name="filedata" position="5,7" size="1170,575" itemHeight="25"/>\n\t\t\t</screen>'
            skin_1920 = '    <screen name="vEditor" position="center,150" size="1770,860" title="File-Explorer">\n                <widget name="filedata" position="8,20" size="1755,838" itemHeight="38"/>\n                </screen>'
            if desktopSize.width() == 1920:
                skin = skin_1920
            else:
                skin = skin_1280
        else:
            skin = '\n\t\t\t<screen position="center,77" size="900,450" title="File-Explorer">\n\t\t\t\t<widget name="filedata" position="2,0" size="896,450" itemHeight="25"/>\n\t\t\t</screen>'
    else:
        skin = '\n\t\t<screen position="center,77" size="620,450" title="File-Explorer">\n\t\t\t<widget name="filedata" position="0,0" size="620,450" itemHeight="25"/>\n\t\t</screen>'

    def __init__(self, session, file):
        self.skin = vEditor.skin
        Screen.__init__(self, session)
        self.session = session
        self.file_name = file
        self.list = []
        self['filedata'] = MenuList(self.list)
        self['actions'] = ActionMap(['WizardActions'], {'ok': (self.editLine), 'back': (self.exitEditor)}, -1)
        self.selLine = None
        self.oldLine = None
        self.isChanged = False
        self.GetFileData(file)
        return

    def exitEditor(self):
        if self.isChanged:
            warningtext = '\nhave been CHANGED! Do you want to save it?\n\nWARNING!'
            warningtext = warningtext + '\n\nThe Editor-Funktions are beta (not full tested) !!!'
            warningtext = warningtext + '\nThe author is NOT RESPONSIBLE\nfor DATA LOST OR DISORDERS !!!'
            dei = self.session.openWithCallback(self.SaveFile, MessageBox, _(self.file_name + warningtext), MessageBox.TYPE_YESNO)
            dei.setTitle(_('Files-Explorer...'))
        else:
            self.close()
        return

    def GetFileData(self, fx):
        try:
            flines = open(fx, 'r')
            for line in flines:
                self.list.append(line)

            flines.close()
            self['info'].setText(fx)
        except:
            pass

        return

    def editLine(self):
        try:
            self.selLine = self['filedata'].getSelectionIndex()
            self.oldLine = self.list[self.selLine]
            editableText = self.list[self.selLine][:-1]
            self.session.openWithCallback(self.callbackEditLine, vInputBox, title=_('old:  ' + self.list[self.selLine]), windowTitle=_('Edit line ' + str(self.selLine + 1)), text=editableText)
        except:
            dei = self.session.open(MessageBox, _('This line is not editable!'), MessageBox.TYPE_ERROR)
            dei.setTitle(_('Error...'))

        return

    def callbackEditLine(self, newline):
        if newline is not None:
            for x in self.list:
                if x == self.oldLine:
                    self.isChanged = True
                    self.list.remove(x)
                    self.list.insert(self.selLine, newline + '\n')

        self.selLine = None
        self.oldLine = None
        return

    def SaveFile(self, answer):
        if answer is True:
            try:
                eFile = open(self.file_name, 'w')
                for x in self.list:
                    eFile.writelines(x)

                eFile.close()
            except:
                pass

            self.close()
        else:
            self.close()
        return


class MviExplorer(Screen):
    skin = '\n\t\t<screen position="-300,-300" size="10,10" title="mvi-Explorer">\n\t\t</screen>'

    def __init__(self, session, file):
        self.skin = MviExplorer.skin
        Screen.__init__(self, session)
        self.file_name = file
        self['actions'] = ActionMap(['WizardActions'], {'ok': (self.close), 'back': (self.close)}, -1)
        self.onLayoutFinish.append(self.showMvi)
        return

    def showMvi(self):
        os_system('/usr/bin/showiframe ' + self.file_name)
        return


class PictureExplorerII(Screen):
    if HDSkn:
        if getDesktop(0).size().width() > 1030:
            skin_1280 = '\n\t\t\t\t<screen flags="wfNoBorder" position="0,0" size="1280,720" title="Picture-Explorer" backgroundColor="#00121214">\n\t\t\t\t\t<widget name="Picture" position="0,0" size="1280,720" zPosition="1" alphatest="on" />\n\t\t\t\t\t<widget name="State" font="Regular;20" halign="center" position="0,650" size="1280,70" backgroundColor="#01080911" foregroundColor="#fcc000" transparent="0" zPosition="9"/>\n\t\t\t\t</screen>'
            skin_1920 = '\n\t\t\t\t<screen flags="wfNoBorder" position="0,0" size="1920,1080" title="Picture-Explorer" backgroundColor="#00121214">\n\t\t\t\t\t<widget name="Picture" position="0,0" size="1920,1080" zPosition="1" alphatest="on" />\n\t\t\t\t\t<widget name="State" font="Regular;30" halign="center" position="0,975" size="1920,105" backgroundColor="#01080911" foregroundColor="#fcc000" transparent="0" zPosition="9"/>\n\t\t\t\t</screen>'
            if desktopSize.width() == 1920:
                skin = skin_1920
            else:
                skin = skin_1280
        else:
            skin = '\n\t\t\t\t<screen backgroundColor="#101214" flags="wfNoBorder" position="0,0" size="1024,576" title="Picture-Explorer">\n\t\t\t\t\t<widget alphatest="on" backgroundColor="#00141415" name="Picture" position="0,0" size="1024,576" zPosition="1"/>\n\t\t\t\t\t<widget name="State" font="Regular;20" halign="center" position="0,506" size="1024,70" backgroundColor="#01080911" foregroundColor="#fcc000" transparent="0" zPosition="9"/>\n\t\t\t\t</screen>'
    else:
        skin = '\n\t\t\t<screen flags="wfNoBorder" position="0,0" size="720,576" title="Picture-Explorer" backgroundColor="#00121214">\n\t\t\t\t<widget name="Picture" position="0,0" size="720,576" zPosition="1" alphatest="on" />\n\t\t\t\t<widget name="State" font="Regular;20" halign="center" position="0,506" size="720,70" backgroundColor="#01080911" foregroundColor="#fcc000" transparent="0" zPosition="9"/>\n\t\t\t</screen>'

    def __init__(self, session, whatPic=None, whatDir=None):
        self.skin = PictureExplorerII.skin
        Screen.__init__(self, session)
        self.session = session
        self.whatPic = whatPic
        self.whatDir = whatDir
        self.picList = []
        self.Pindex = 0
        self['Picture'] = Pixmap()
        self['State'] = Label(_('loading... ' + self.whatPic))
        self['actions'] = ActionMap(['WizardActions', 'DirectionActions'], {'ok': (self.info), 'back': (self.close), 'up': (self.info), 
           'down': (self.close), 
           'left': (self.Pleft), 
           'right': (self.Pright)}, -1)
        self.EXscale = AVSwitch().getFramebufferScale()
        self.EXpicload = ePicLoad()
        self.EXpicload_conn = self.EXpicload.PictureData.connect(self.DecodeAction)
        self.onLayoutFinish.append(self.Show_Picture)
        return

    def Show_Picture(self):
        if self.whatPic is not None:
            params = (self['Picture'].instance.size().width(),
             self['Picture'].instance.size().height(),
             self.EXscale[0],
             self.EXscale[1],
             True,
             1,
             '#002C2C39')
            self.EXpicload.setPara(params)
            self.EXpicload.startDecode(self.whatPic)
        if self.whatDir is not None:
            pidx = 0
            for root, dirs, files in os_walk(self.whatDir):
                for name in files:
                    if name.endswith('.jpg') or name.endswith('.jpeg') or name.endswith('.Jpg') or name.endswith('.Jpeg') or name.endswith('.JPG') or name.endswith('.JPEG'):
                        self.picList.append(name)
                        if name in self.whatPic:
                            self.Pindex = pidx
                        pidx = pidx + 1

            files.sort()
        return

    def DecodeAction(self, pictureInfo=''):
        if self.whatPic is not None:
            self['State'].setText(_('ready...'))
            self['State'].visible = False
            ptr = self.EXpicload.getData()
            self['Picture'].instance.setPixmap(ptr)
        return

    def Pright(self):
        if len(self.picList) > 2:
            if self.Pindex < len(self.picList) - 1:
                self.Pindex = self.Pindex + 1
                self.whatPic = self.whatDir + str(self.picList[self.Pindex])
                self['State'].visible = True
                self['State'].setText(_('loading... ' + self.whatPic))
                self.EXpicload.startDecode(self.whatPic)
            else:
                self['State'].setText(_('wait...'))
                self['State'].visible = False
                self.session.open(MessageBox, _('No more picture-files.'), MessageBox.TYPE_INFO)
        return

    def Pleft(self):
        if len(self.picList) > 2:
            if self.Pindex > 0:
                self.Pindex = self.Pindex - 1
                self.whatPic = self.whatDir + str(self.picList[self.Pindex])
                self['State'].visible = True
                self['State'].setText(_('loading... ' + self.whatPic))
                self.EXpicload.startDecode(self.whatPic)
            else:
                self['State'].setText(_('wait...'))
                self['State'].visible = False
                self.session.open(MessageBox, _('No more picture-files.'), MessageBox.TYPE_INFO)
        return

    def info(self):
        if self['State'].visible:
            self['State'].setText(_('wait...'))
            self['State'].visible = False
        else:
            self['State'].visible = True
            self['State'].setText(_(self.whatPic))
        return


class MoviePlayer(MP_parent):

    def __init__(self, session, service):
        self.session = session
        self.WithoutStopClose = False
        MP_parent.__init__(self, self.session, service)
        return

    def leavePlayer(self):
        try:
            self.updateMovieData()
        except:
            pass

        self.is_closing = True
        self.close()
        return

    def leavePlayerConfirmed(self, answer):
        return

    def doEofInternal(self, playing):
        try:
            self.updateMovieData()
        except:
            pass

        if not self.execing:
            return
        if not playing:
            return
        self.leavePlayer()
        return

    def showMovies(self):
        try:
            self.updateMovieData()
        except:
            pass

        self.WithoutStopClose = True
        self.close()
        return

    def movieSelected(self, service):
        self.leavePlayer(self.de_instance)
        return

    def __onClose(self):
        if not self.WithoutStopClose:
            self.session.nav.playService(self.lastservice)
        return


class MusicExplorer(MoviePlayer):
    skin = '\n\t<screen backgroundColor="#50070810" flags="wfNoBorder" name="MusicExplorer" position="center,center" size="720,30">\n\t\t<widget font="Regular;24" halign="right" position="50,0" render="Label" size="100,30" source="session.CurrentService" transparent="1" valign="center" zPosition="1">\n\t\t\t<convert type="ServicePosition">Remaining</convert>\n\t\t</widget>\n\t\t<widget font="Regular;24" position="170,0" render="Label" size="650,30" source="session.CurrentService" transparent="1" valign="center" zPosition="1">\n\t\t\t<convert type="ServiceName">Name</convert>\n\t\t</widget>\n\t</screen>'

    def __init__(self, session, service, MusicDir, theFile):
        self.session = session
        MoviePlayer.__init__(self, session, service)
        self.MusicDir = MusicDir
        self.musicList = []
        self.Mindex = 0
        self.curFile = theFile
        self.searchMusic()
        self.onLayoutFinish.append(self.showMMI)
        MoviePlayer.WithoutStopClose = False
        return

    def showMMI(self):
        os_system('/usr/bin/showiframe /usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/music.mvi')
        return

    def searchMusic(self):
        midx = 0
        for root, dirs, files in os_walk(self.MusicDir):
            for name in files:
                name = name.lower()
                if name.endswith('.mp3') or name.endswith('.mp2') or name.endswith('.ogg') or name.endswith('.wav') or name.endswith('.flac') or name.endswith('.m4a'):
                    self.musicList.append(name)
                    if self.curFile in name:
                        self.Mindex = midx
                    midx = midx + 1

        return

    def seekFwd(self):
        if len(self.musicList) > 2:
            if self.Mindex < len(self.musicList) - 1:
                self.Mindex = self.Mindex + 1
                nextfile = self.MusicDir + str(self.musicList[self.Mindex])
                nextRef = eServiceReference('4097:0:0:0:0:0:0:0:0:0:' + nextfile)
                self.session.nav.playService(nextRef)
            else:
                self.session.open(MessageBox, _('No more playable files.'), MessageBox.TYPE_INFO)
        return

    def seekBack(self):
        if len(self.musicList) > 2:
            if self.Mindex > 0:
                self.Mindex = self.Mindex - 1
                nextfile = self.MusicDir + str(self.musicList[self.Mindex])
                nextRef = eServiceReference('4097:0:0:0:0:0:0:0:0:0:' + nextfile)
                self.session.nav.playService(nextRef)
            else:
                self.session.open(MessageBox, _('No more playable files.'), MessageBox.TYPE_INFO)
        return

    def doEofInternal(self, playing):
        if not self.execing:
            return
        if not playing:
            return
        self.seekFwd()
        return


def ScanSysem_str():
    try:
        ret = ''
        out_line = os_popen('uptime').readline()
        ret = ret + 'at' + out_line + '\n'
        out_lines = []
        out_lines = os_popen('cat /proc/meminfo').readlines()
        for lidx in range(len(out_lines) - 1):
            tstLine = out_lines[lidx].split()
            if 'MemTotal:' in tstLine:
                ret = ret + out_lines[lidx]
            elif 'MemFree:' in tstLine:
                ret = ret + out_lines[lidx] + '\n'

        out_lines = []
        out_lines = os_popen('cat /proc/stat').readlines()
        for lidx in range(len(out_lines) - 1):
            tstLine = out_lines[lidx].split()
            if 'procs_running' in tstLine:
                ret = ret + 'Running processes: ' + tstLine[1]

        return ret
    except:
        return 'N/A'

    return


class vInputBox(InputBox):
    if desktopSize.width() == 1920:
        offset = 110
        vibheight = 105
        smallfont = 23
        smalltextsize = 30
        defaultfont = 28
        defaulttextsize = 40
    else:
        offset = 80
        vibheight = 70
        smallfont = 15
        smalltextsize = 25
        defaultfont = 20
        defaulttextsize = 30
    vibnewx = str(getDesktop(0).size().width() - offset)
    sknew = '<screen name="vInputBox" position="center,center" size="' + vibnewx + ',%d" title="Input...">\n' % vibheight
    sknew = sknew + '<widget name="text" position="5,5" size="%s,%d" font="Regular;%d"/>\n<widget name="input" position="5,40" size="' % (vibnewx, smalltextsize, smallfont)
    sknew = sknew + vibnewx + ',%d" font="Regular;%d"/>\n</screen>' % (defaulttextsize, defaultfont)
    skin = sknew

    def __init__(self, session, title='', windowTitle=_('Input'), useableChars=None, **kwargs):
        InputBox.__init__(self, session, title, windowTitle, useableChars, **kwargs)
        return


class CPmaniger(Screen):
    if HDSkn:
        if getDesktop(0).size().width() > 1030:
            skin_1280 = '\n\t\t\t\t<screen position="center,center" size="920,450" title="Select Copy/Move location...">\n\t\t\t\t<widget name="File" font="Regular;20" halign="center" position="5,0" size="890,100" foregroundColor="yellow" transparent="1" valign="center" zPosition="4"/>\n                                <eLabel position="20,90" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\n\t\t\t\t<widget name="CPto" position="5,100" scrollbarMode="showOnDemand" size="890,240" zPosition="4"/>\n                                <eLabel position="20,385" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\n                                <ePixmap name="red"    position="70,405"   zPosition="2" size="150,30" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" transparent="1" alphatest="blend" />\n\t                        <ePixmap name="green"  position="280,405" zPosition="2" size="150,30" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_green.png" transparent="1" alphatest="blend" />\n\t                        <ePixmap name="yellow" position="490,405" zPosition="2" size="150,30" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_yellow.png" transparent="1" alphatest="blend" /> \n        \t                <ePixmap name="blue"   position="700,405" zPosition="2" size="150,30" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_blue.png" transparent="1" alphatest="blend" /> \n        \t                <eLabel name="key_red" text="Move" position="70,410" size="150,30" valign="center" halign="center" zPosition="4" font="Regular;20" transparent="1" /> \n                                <eLabel name="key_yellow" text="Copy" position="490,410" size="150,30" valign="center" halign="center" zPosition="4" font="Regular;20" transparent="1" />\n\t\t\t\t</screen>'
            skin_1920 = '    <screen name="CPmaniger" position="center,200" size="1300,720" title="Select Copy/Move location...">\n                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png" position="50,640" size="200,40" alphatest="blend" />\n                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green-big.png" position="360,640" size="200,40" alphatest="blend" />\n                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/yellow-big.png" position="670,640" size="200,40" alphatest="blend" />\n                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/blue-big.png" position="980,640" size="200,40" alphatest="blend" />\n                    <eLabel name="key_red" text="Move" position="50,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#940d0d" transparent="1" />\n                    <eLabel name="key_yellow" text="Copy" position="670,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#bba502" transparent="1" />\n                    <widget name="File" position="20,20" size="1260,150" foregroundColor="foreground" backgroundColor="background" font="Regular;28" valign="center" halign="center" transparent="1" zPosition="1" />\n                    <eLabel position="10,170" zPosition="4" size="1280,1" backgroundColor="foreground" />\n                    <widget name="CPto" position="20,180" size="1260,440" zPosition="2" itemHeight="40" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background"  transparent="1" />\n                    </screen>'
            if desktopSize.width() == 1920:
                skin = skin_1920
            else:
                skin = skin_1280
        else:
            skin = '\n\t\t\t\t<screen position="center,77" size="900,450" title="Select Copy/Move location...">\n\t\t\t\t<widget name="File" font="Regular;20" halign="center" position="5,0" size="890,100" transparent="1" valign="center" zPosition="4"/>\n\t\t\t\t<widget name="CPto" position="5,100" scrollbarMode="showOnDemand" size="890,312" zPosition="4"/>\n\t\t\t\t<eLabel backgroundColor="#555555" position="5,420" size="890,2" zPosition="5"/>\n\t\t\t\t<ePixmap alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" position="0,425" size="35,25" zPosition="5"/>\n\t\t\t\t<ePixmap alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_yellow.png" position="310,425" size="35,25" zPosition="5"/>\n\t\t\t\t<eLabel font="Regular;18" halign="left" position="35,425" size="120,25" text="MOVE" transparent="1" valign="center" zPosition="6"/>\n\t\t\t\t<eLabel font="Regular;18" halign="left" position="345,425" size="120,25" text="COPY" transparent="1" valign="center" zPosition="6"/>\n\t\t\t\t</screen>'
    else:
        skin = '\n\t\t\t<screen position="center,77" size="620,450" title="Select Copy/Move location...">\n\t\t\t\t<widget name="File" font="Regular;20" halign="center" position="5,0" size="610,100" transparent="1" valign="center" zPosition="4"/>\n\t\t\t\t<widget name="CPto" position="5,100" scrollbarMode="showOnDemand" size="610,312" zPosition="4"/>\n\t\t\t\t<eLabel backgroundColor="#555555" position="5,420" size="610,2" zPosition="5"/>\n\t\t\t\t<ePixmap alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" position="0,425" size="35,25" zPosition="5"/>\n\t\t\t\t<ePixmap alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_yellow.png" position="310,425" size="35,25" zPosition="5"/>\n\t\t\t\t<eLabel font="Regular;18" halign="left" position="35,425" size="120,25" text="MOVE" transparent="1" valign="center" zPosition="6"/>\n\t\t\t\t<eLabel font="Regular;18" halign="left" position="345,425" size="120,25" text="COPY" transparent="1" valign="center" zPosition="6"/>\n\t\t\t</screen>'

    def __init__(self, session, source='/tmp/none'):
        self.skin = CPmaniger.skin
        Screen.__init__(self, session)
        self.sesion = session
        self.src = source
        self['File'] = Label(_('WARNING! they doing now COPY or MOVE\n' + source + '\nto:'))
        self['CPto'] = myFileList(config.plugins.FileExplorer.CopyDest.value, showDirectories=True, showFiles=False, matchingPattern='^.*\\.*', useServiceRef=False)
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': (self.ok), 'back': (self.NothingToDo), 'red': (self.MoveFile), 
           'yellow': (self.CopyFile)}, -1)
        self.onLayoutFinish.append(self.OneDescent)
        return

    def OneDescent(self):
        if self['CPto'].canDescent():
            self['CPto'].descent()
        return

    def ok(self):
        if self['CPto'].canDescent():
            self['CPto'].descent()
        return

    def NothingToDo(self):
        self.close(' ')
        return

    def CopyFile(self):
        if self['CPto'].getSelectionIndex() != 0:
            dest = self['CPto'].getSelection()[0]
            if self.src[len(self.src) - 1] == '/':
                order = 'cp -af "' + self.src + '" "' + dest + '"'
            else:
                order = 'cp "' + self.src + '" "' + dest + '"'
            try:
                config.plugins.FileExplorer.CopyDest.value = dest
                config.plugins.FileExplorer.CopyDest.save()
                os_system(order)
            except:
                dei = self.session.open(MessageBox, _('%s \nFAILED!' % order), MessageBox.TYPE_ERROR)
                dei.setTitle(_('Files Explorer'))

            self.close(' ')
        return

    def MoveFile(self):
        if self['CPto'].getSelectionIndex() != 0:
            dest = self['CPto'].getSelection()[0]
            if self.src[len(self.src) - 1] == '/':
                order = 'cp -af "' + self.src + '" "' + dest + '"'
                DELorder = 'rm -r "' + self.src + '"'
            else:
                order = 'cp "' + self.src + '" "' + dest + '"'
                DELorder = 'rm -f "' + self.src + '"'
            try:
                config.plugins.FileExplorer.CopyDest.value = dest
                config.plugins.FileExplorer.CopyDest.save()
                os_system(order)
            except:
                dei = self.session.open(MessageBox, _('%s \nFAILED!' % order), MessageBox.TYPE_ERROR)
                dei.setTitle(_('Files Explorer'))

            try:
                os_system(DELorder)
            except:
                dei = self.session.open(MessageBox, _('%s \nFAILED!' % DELorder), MessageBox.TYPE_ERROR)
                dei.setTitle(_('Files Explorer'))

            self.close(' ')
        return


class SoftLinkScreen(Screen):
    if HDSkn:
        if getDesktop(0).size().width() > 1030:
            skin_1280 = '\n\t\t\t\t<screen position="center,center" size="900,450" title="Make a softlink...">\n\t\t\t\t<widget name="File" font="Regular;20" halign="center" position="5,0" size="890,100" foregroundColor="foreground" backgroundColor="background" transparent="1" valign="center" zPosition="4"/>\n\t\t\t\t<widget name="SLto" position="5,100" scrollbarMode="showOnDemand" size="890,312" zPosition="4"/>\n\t\t\t\t<eLabel foregroundColor="foreground" backgroundColor="background" position="5,420" size="890,2" zPosition="5"/>\n\t\t\t\t<ePixmap alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" position="0,425" size="35,25" zPosition="5"/>\n\t\t\t\t<ePixmap alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_yellow.png" position="310,425" size="35,25" zPosition="5"/>\n\t\t\t\t<eLabel font="Regular;18" halign="left" position="35,425" size="120,25" text="Set name" foregroundColor="foreground" backgroundColor="background" transparent="1" valign="center" zPosition="6"/>\n\t\t\t\t<eLabel font="Regular;18" halign="left" position="345,425" size="220,25" text="Make a softlink" foregroundColor="foreground" backgroundColor="background" transparent="1" valign="center" zPosition="6"/>\n\t\t\t\t</screen>'
            skin_1920 = '\n\t\t\t\t<screen position="center,center" size="1350,675" title="Make a softlink...">\n\t\t\t\t<widget name="File" font="Regular;30" halign="center" position="8,0" size="1335,150" foregroundColor="foreground" backgroundColor="background" transparent="1" valign="center" zPosition="4"/>\n\t\t\t\t<widget name="SLto" position="8,150" scrollbarMode="showOnDemand" size="1335,440" zPosition="4"/>\n\t\t\t\t<eLabel foregroundColor="foreground" backgroundColor="background" position="8,630" size="1335,2" zPosition="5"/>\n\t\t\t\t<ePixmap alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" position="0,638" size="60,30" zPosition="5"/>\n\t\t\t\t<ePixmap alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_yellow.png" position="465,638" size="60,30" zPosition="5"/>\n\t\t\t\t<eLabel font="Regular;27" halign="left" position="70,633" size="180,40" text="Set name" foregroundColor="foreground" backgroundColor="background" transparent="1" valign="center" zPosition="6"/>\n\t\t\t\t<eLabel font="Regular;27" halign="left" position="545,633" size="330,40" text="Make a softlink" foregroundColor="foreground" backgroundColor="background" transparent="1" valign="center" zPosition="6"/>\n\t\t\t\t</screen>'
            if desktopSize.width() == 1920:
                skin = skin_1920
            else:
                skin = skin_1280
        else:
            skin = '\n\t\t\t\t<screen position="center,77" size="900,450" title="Make a softlink...">\n\t\t\t\t<widget name="File" font="Regular;20" halign="center" position="5,0" size="890,100" transparent="1" valign="center" zPosition="4"/>\n\t\t\t\t<widget name="SLto" position="5,100" scrollbarMode="showOnDemand" size="890,312" zPosition="4"/>\n\t\t\t\t<eLabel backgroundColor="#555555" position="5,420" size="890,2" zPosition="5"/>\n\t\t\t\t<ePixmap alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" position="0,425" size="35,25" zPosition="5"/>\n\t\t\t\t<ePixmap alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_yellow.png" position="310,425" size="35,25" zPosition="5"/>\n\t\t\t\t<eLabel font="Regular;18" halign="left" position="35,425" size="120,25" text="Set name" transparent="1" valign="center" zPosition="6"/>\n\t\t\t\t<eLabel font="Regular;18" halign="left" position="345,425" size="220,25" text="Make a softlink" transparent="1" valign="center" zPosition="6"/>\n\t\t\t\t</screen>'
    else:
        skin = '\n\t\t\t<screen position="center,77" size="620,450" title="Make a softlink...">\n\t\t\t\t<widget name="File" font="Regular;20" halign="center" position="5,0" size="610,100" transparent="1" valign="center" zPosition="4"/>\n\t\t\t\t<widget name="SLto" position="5,100" scrollbarMode="showOnDemand" size="610,312" zPosition="4"/>\n\t\t\t\t<eLabel backgroundColor="#555555" position="5,420" size="610,2" zPosition="5"/>\n\t\t\t\t<ePixmap alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" position="0,425" size="35,25" zPosition="5"/>\n\t\t\t\t<ePixmap alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_yellow.png" position="310,425" size="35,25" zPosition="5"/>\n\t\t\t\t<eLabel font="Regular;18" halign="left" position="35,425" size="120,25" text="Set name" transparent="1" valign="center" zPosition="6"/>\n\t\t\t\t<eLabel font="Regular;18" halign="left" position="345,425" size="220,25" text="Make a softlink" transparent="1" valign="center" zPosition="6"/>\n\t\t\t</screen>'

    def __init__(self, session, source='/tmp/'):
        self.skin = SoftLinkScreen.skin
        Screen.__init__(self, session)
        self.sesion = session
        self.src = source
        self.newSLname = ' '
        self['File'] = Label('Set first the Softlink name ...')
        self['SLto'] = myFileList('/', showDirectories=True, showFiles=True, matchingPattern=None, useServiceRef=False)
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': (self.ok), 'back': (self.NothingToDo), 'red': (self.GetSLname), 
           'yellow': (self.MakeSLnow)}, -1)
        return

    def GetSLname(self):
        self.session.openWithCallback(self.callbackSetLinkName, vInputBox, title=_('Write the new softlink name here:'), windowTitle=_('Dream Explorer...'), text='newname')
        return

    def callbackSetLinkName(self, answer):
        if answer is None:
            return
        else:
            if ' ' in answer or answer == '':
                dei = self.session.open(MessageBox, _('Softlink name error !'), MessageBox.TYPE_ERROR)
                dei.setTitle(_('Files Explorer'))
                return
            else:
                self.newSLname = self.src + answer
                self['File'].setText(_('WARNING! they make now a softlink from\n' + self.newSLname + '\nto:'))
                return

            return

    def ok(self):
        if self['SLto'].canDescent():
            self['SLto'].descent()
        return

    def NothingToDo(self):
        self.close(' ')
        return

    def MakeSLnow(self):
        if self.newSLname != ' ':
            if self['SLto'].getSelectionIndex() != 0:
                if self['SLto'].canDescent():
                    order = 'ln -s "' + self['SLto'].getSelection()[0] + '" "' + self.newSLname + '"'
                else:
                    order = 'ln -s "' + (self['SLto'].getCurrentDirectory() + self['SLto'].getFilename()) + '" "' + self.newSLname + '"'
                os_system(order)
                self.close(' ')
        else:
            dei = self.session.open(MessageBox, _('Softlink name error !'), MessageBox.TYPE_ERROR)
            dei.setTitle(_('Files Explorer'))
        return


return
