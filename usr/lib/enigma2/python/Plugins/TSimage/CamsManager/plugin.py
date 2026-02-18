# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/CamsManager/plugin.py
# Compiled at: 2025-09-10 14:58:38
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Sources.List import List
from Screens.MessageBox import MessageBox
from Plugins.Plugin import PluginDescriptor
from Components.Pixmap import Pixmap
from Components.Button import Button
from Components.Label import Label
from Components.config import config, configfile
from Tools.LoadPixmap import LoadPixmap
from twisted.web.client import getPage
from Tools.Directories import fileExists, resolveFilename, SCOPE_CURRENT_PLUGIN, SCOPE_PLUGINS, SCOPE_LANGUAGE
from Tools.HardwareInfo import HardwareInfo
from Plugins.TSimage.TSimagePanel.multInstaller import TSGetMultiipk
from CCcamOscamInfo.plugin import main as CCcamOscamInfoMain
from CCcamInfo.plugin import CCcamInfoMain
from MGcamdInfo.plugin import MGcamdInfoMain
from enigma import eTimer, eConsoleAppContainer, getDesktop
from os import environ, statvfs as os_statvfs, remove as os_remove, path as os_path, system as os_system, walk as os_walk
from Tools.TSTools import getDistroFeed, getHostname, getArch
from Components.Language import language
import gettext, urllib2
from xml.dom import Node, minidom
dpkg_busy_filename = '/tmp/.dpkg_busy'
dpkg_ready_filename = '/tmp/.dpkg_ready'
dpkg_updater_filename = '/tmp/.dpkg_updater'
dpkg_ugradable_filename = '/tmp/.dpkg_ugradable'
dpkg_list_filename = '/tmp/.dpkglist'
dpkg_tmplist_filename = '/tmp/.tmplist'

def _(txt):
    t = gettext.dgettext('CamsManager', txt)
    if t == txt:
        t = gettext.gettext(txt)
    return t


plugin_path = '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/'
cccaminfo = False
hostname = getHostname()
distro_feed, debarchname = getDistroFeed(hostname)
boxarch = getArch()
desktopSize = getDesktop(0).size()

def getipkinfos(ipkfile):
    try:
        version = 'Version: N/A'
        status = 'install'
        ipkfile = str(os_path.basename(ipkfile))
        opkgpath = '/var/lib/dpkg/info/'
        ipkparts = []
        ipkparts = ipkfile.split('_')
        ipkname = str(ipkparts[0]).strip()
        ipkversion = str(ipkparts[1]).strip()
        ipkfilename = opkgpath + ipkname + '.list'
        if fileExists(ipkfilename):
            status = 'remove'
    except:
        version = 'Version: N/A'
        status = 'install'

    return (version.strip(), status)


class TSSoftcamsManager(Screen):
    skin_1280 = '<screen name="TSSoftcamsManager" position="center,77" size="920,600" title="Softcams Manager">\n        <widget source="menu" render="Listbox" position="20,20" size="800,30" scrollbarMode="showOnDemand" enableWrapAround="1" transparent="1" zPosition="2">\n            <convert type="TemplatedMultiContent">\n                {"template": [\n                    MultiContentEntryPixmapAlphaBlend(pos=(8,2), size=(25,25), png=0),\n                    MultiContentEntryText(pos=(35,0), size=(615,30), font=0, flags=RT_HALIGN_LEFT|RT_VALIGN_CENTER, text=1)\n                 ],\n                 "fonts": [gFont("Regular",23)],\n                 "itemHeight": 30\n                }\n            </convert>\n        </widget>\n\n        <widget name="cams_count" position="830,15" zPosition="1" size="80,40" font="Regular;16" transparent="1" halign="center" valign="center" backgroundColor="background"/>\n\n        <eLabel position="20,235" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"/>\n\n        <widget source="session.CurrentService" render="Label" position="30,245" zPosition="1" size="880,270" font="Regular;22" transparent="1" halign="left" valign="top" backgroundColor="background">\n            <convert type="TSEcmInfo">Default</convert>\n        </widget>\n\n        <eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"/>\n\n        <ePixmap name="red"    position="70,545"  zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png"    transparent="1" alphatest="blend"/>\n        <ePixmap name="green"  position="280,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_green.png"  transparent="1" alphatest="blend"/>\n        <ePixmap name="yellow" position="490,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_yellow.png" transparent="1" alphatest="blend"/>\n        <ePixmap name="blue"   position="700,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_blue.png"   transparent="1" alphatest="blend"/>\n\n        <widget name="key_red"    position="70,550"  size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1"/>\n        <widget name="key_green"  position="280,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1"/>\n        <widget name="key_yellow" position="490,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1"/>\n        <widget name="key_blue"   position="690,550" size="150,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1"/>\n    </screen>\n    '
    skin_1920 = '<screen name="TSSoftcamsManager" position="center,200" size="1300,720" title="Softcams Manager">\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png"    position="50,640"  size="200,40" alphatest="blend"/>\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green-big.png"  position="360,640" size="200,40" alphatest="blend"/>\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/yellow-big.png" position="670,640" size="200,40" alphatest="blend"/>\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/blue-big.png"   position="980,640" size="200,40" alphatest="blend"/>\n\n        <widget name="key_red"    position="50,640"  size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#940d0d" transparent="1"/>\n        <widget name="key_green"  position="360,640" size="400,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#2d872d" transparent="1"/>\n        <widget name="key_yellow" position="670,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#bba502" transparent="1"/>\n        <widget name="key_blue"   position="970,640" size="220,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#18188b" transparent="1"/>\n\n        <eLabel position="10,200" zPosition="4" size="1280,1" backgroundColor="foreground"/>\n\n        <widget source="menu" render="Listbox" position="20,20" size="1150,40" zPosition="2" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background" transparent="1">\n            <convert type="TemplatedMultiContent">\n                {"template": [\n                    MultiContentEntryText(pos=(45,0), size=(1000,40), flags=RT_HALIGN_LEFT|RT_VALIGN_CENTER, text=1),\n                    MultiContentEntryPixmapAlphaBlend(pos=(2,7), size=(25,25), png=0)\n                 ],\n                 "fonts": [gFont("Regular",32)],\n                 "itemHeight": 40\n                }\n            </convert>\n        </widget>\n\n        <widget name="cams_count" position="1170,15" zPosition="1" size="110,50" font="Regular;20" transparent="1" halign="center" valign="center" backgroundColor="background"/>\n\n        <widget source="session.CurrentService" render="Label" position="20,210" size="1260,350" zPosition="1" font="Regular;28" transparent="1" halign="left" valign="top" backgroundColor="background">\n            <convert type="TSEcmInfo">Default</convert>\n        </widget>\n    </screen>\n    '
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session, args=0):
        self.session = session
        Screen.__init__(self, session)
        self.greenStatus = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green_25.png'))
        self.greyStatus = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/grey_25.png'))
        self.index = 0
        self.actIndex = 0
        self.last = 0
        self.sclist = []
        self.namelist = []
        self.lastCam = ''
        self.oldService = self.session.nav.getCurrentlyPlayingServiceReference()
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'ok': (self.ok), 'cancel': (self.close), 'green': (self.action), 'red': (self.stop), 
           'blue': (self.download), 
           'yellow': (self.showcccaminfo)}, -1)
        self['key_green'] = Label(_('Start'))
        self['key_blue'] = Button(_('Install/Remove'))
        self['key_red'] = Button(_('Stop'))
        self['key_yellow'] = Button(_('CCcamInfo'))
        self['pixmap'] = Pixmap()
        self.lastCam = self.readCurrent()
        self.softcamlist = []
        self['cams_count'] = Label(_('%s Cam(s) installed') % str(len(self.softcamlist)))
        self['menu'] = List(self.softcamlist)
        self.readScripts()
        self['menu'].onSelectionChanged.append(self.updateSummary)
        self.onShown.append(self.updateSummary)
        self.onShown.append(self.setWindowTitle)
        self.onShown.append(self.updateCCcamInfoButton)
        return

    def setWindowTitle(self):
        self.setTitle('Softcams Manager')
        self['menu'].setIndex(self.last)
        return

    def showcccaminfo(self):
        if not len(self.softcamlist) == 0:
            try:
                if 'oscam' in self.lastCam.lower():
                    CCcamOscamInfoMain(self.session)
                elif 'cccam' in self.lastCam.lower():
                    self.session.open(CCcamInfoMain)
                elif 'mgcam' in self.lastCam.lower():
                    self.session.open(MGcamdInfoMain)
                else:
                    return
            except:
                return

        return

    def updateCCcamInfoButton(self):
        try:
            if 'oscam' in self.lastCam.lower():
                self['key_yellow'].setText(_('CCcamOScamInfo'))
                self['key_yellow'].show()
            elif 'cccam' in self.lastCam.lower():
                self['key_yellow'].setText(_('CCcamInfo'))
                self['key_yellow'].show()
            elif 'mgcam' in self.lastCam.lower():
                self['key_yellow'].setText(_('MGcamdInfo'))
                self['key_yellow'].show()
            else:
                self['key_yellow'].hide()
        except:
            self['key_yellow'].hide()

        return

    def download(self):
        self.session.openWithCallback(self.readScripts, Getipklist)
        return

    def getLastIndex(self):
        a = 0
        if len(self.namelist) > 0:
            for x in self.namelist:
                if x == self.lastCam:
                    return a
                a += 1

        else:
            return -1
        return -1

    def ok(self):
        if len(self.softcamlist) > 0:
            idx = self['menu'].getIndex()
            statusIcon = self.softcamlist[idx][0]
            if statusIcon == self.greenStatus:
                self.stop()
            else:
                self.action()
        return

    def executeCmdDownUp(self):
        self.container = eConsoleAppContainer()
        self.container.appClosed.connect(self.executeCmdUp)
        self.container.execute(self.cmd_down)
        return

    def executeCmdUp(self, retval):
        self.container = eConsoleAppContainer()
        self.container.appClosed.connect(self.cmdOnClosed)
        self.container.execute(self.cmd_up)
        return

    def executeCmd(self, cmd):
        self.container = eConsoleAppContainer()
        self.container.appClosed.connect(self.cmdOnClosed)
        self.container.execute(cmd)
        return

    def cmdOnClosed(self, retval):
        self.container.kill()
        return

    def action(self):
        if len(self.softcamlist) > 0:
            if os_path.exists('/tmp/ecm.info'):
                os_remove('/tmp/ecm.info')
            self.session.nav.playService(None)
            self.last = self.getLastIndex()
            idx = self['menu'].getIndex()
            if self.last > -1:
                if self.last == idx:
                    self.executeCmd('/usr/script/cam/' + self.sclist[idx] + ' cam_res')
                else:
                    self.cmd_down = '/usr/script/cam/' + self.sclist[self.last] + ' cam_down'
                    self.cmd_up = '/usr/script/cam/' + self.sclist[idx] + ' cam_up'
                    self.executeCmdDownUp()
            else:
                self.executeCmd('/usr/script/cam/' + self.sclist[idx] + ' cam_up')
            if self.last != idx:
                self.lastCam = self.softcamlist[idx][1]
                self.writeFile()
            self.readScripts()
            self.session.nav.playService(self.oldService)
        else:
            return
        return

    def writeFile(self):
        if self.lastCam is not None:
            clist = open('/etc/clist.list', 'w')
            clist.write(self.lastCam)
            clist.close()
        return

    def stop(self):
        if len(self.softcamlist) > 0:
            idx = self['menu'].getIndex()
            statusIcon = self.softcamlist[idx][0]
            if statusIcon == self.greenStatus:
                if os_path.exists('/tmp/ecm.info'):
                    os_remove('/tmp/ecm.info')
                self.session.nav.playService(None)
                self.lastCam = self.softcamlist[idx][1]
                self.last = self.getLastIndex()
                if self.last > -1:
                    self.executeCmd('/usr/script/cam/' + self.sclist[self.last] + ' cam_down')
                self.lastCam = ' '
                self.writeFile()
                self.readScripts()
                self.session.nav.playService(self.oldService)
        else:
            return
        return

    def readScripts(self):
        self.index = 0
        scriptliste = []
        pliste = []
        path = '/usr/script/cam/'
        for root, dirs, files in os_walk(path):
            for name in files:
                name = name.strip()
                scriptliste.append(name)

        self.sclist = scriptliste
        i = len(self.softcamlist)
        del self.softcamlist[0:i]
        for lines in scriptliste:
            dat = path + lines
            datei = open(dat, 'r')
            for line in datei:
                if line[0:3] == 'OSD':
                    line = line.strip()
                    nam = line[5:-1]
                    if self.lastCam is not None:
                        if nam == self.lastCam:
                            self.softcamlist.append((self.greenStatus, nam, self.index))
                            self.actIndex = self.index
                            self.last = self.index
                        else:
                            self.softcamlist.append((self.greyStatus, nam, self.index))
                        self.index += 1
                    else:
                        self.softcamlist.append((self.greyStatus, nam, self.index))
                        self.index += 1
                    pliste.append(nam)

            datei.close()
            self.namelist = pliste

        self['cams_count'].setText(_('%s Cam(s) installed') % str(len(self.softcamlist)))
        self['menu'].setList(self.softcamlist)
        self['menu'].setIndex(self.last)
        self.updateCCcamInfoButton()
        return

    def readCurrent(self):
        try:
            clist = open('/etc/clist.list', 'r')
        except:
            return

        lastcam = 'nothing'
        if clist is not None:
            for line in clist:
                lastcam = line

            clist.close()
        return lastcam

    def autocam(self):
        current = None
        try:
            clist = open('/etc/clist.list', 'r')
            print 'found list'
        except:
            return

        if clist is not None:
            for line in clist:
                current = line

            clist.close()
        print 'current =', current
        if os_path.isfile('/etc/autocam.txt') is False:
            alist = open('/etc/autocam.txt', 'w')
            alist.close()
        self.cleanauto()
        alist = open('/etc/autocam.txt', 'a')
        alist.write(self.oldService.toString() + '\n')
        last = self.getLastIndex()
        alist.write(current + '\n')
        alist.close()
        self.session.openWithCallback(self.callback, MessageBox, _('Autocam assigned to the current channel'), type=1, timeout=10)
        return

    def cleanauto(self):
        if os_path.isfile('/etc/autocam.txt') is False:
            return
        return

    def createSummary(self):
        return TSipanelCamsManagerSummary

    def updateSummary(self):
        text = ''
        status = ''
        if len(self.softcamlist) > 0:
            idx = self['menu'].getIndex()
            text = self.softcamlist[idx][1]
            statusIcon = self.softcamlist[idx][0]
            if statusIcon == self.greenStatus:
                status = 'running'
                self['key_red'].show()
                self['key_green'].setText(_('Restart'))
            else:
                status = 'stopped'
                self['key_red'].hide()
                self['key_green'].setText(_('Start'))
        else:
            self['key_red'].hide()
            self['key_green'].setText(' ')
        self.summaries.setText(text, 1)
        self.summaries.setText(status, 2)
        return


class TSipanelCamsManagerSummary(Screen):
    if '820' in HardwareInfo().get_device_name():
        skin = '<screen name="TSipanelCamsManagerSummary" position="0,0" size="96,64" id="2">\n            <widget name="plugin" position="1,0" size="94,30" font="Regular;14" halign="center" valign="center"/>\n            <eLabel position="2,30" size="92,1" backgroundColor="#e16f00"/>\n            <widget name="listentry" position="0,36" size="96,14" font="Regular;11"/>\n            <widget name="status" position="0,49" size="96,14" font="Regular;11"/>\n        </screen>\n        '
    elif 'two' in HardwareInfo().get_device_name():
        skin = '<screen name="TSipanelCamsManagerSummary" position="0,0" size="264,128">\n            <widget name="plugin" position="6,0" size="252,30" font="Regular;17" halign="center" valign="center"/>\n            <eLabel position="2,30" size="260,1" backgroundColor="white"/>\n            <widget name="listentry" position="6,38" size="252,34" font="Regular;14" halign="center" valign="center"/>\n            <widget name="status" position="6,78" size="252,34" font="Regular;14" halign="center" valign="center"/>\n        </screen>\n        '
    elif '7080' in HardwareInfo().get_device_name():
        skin = '<screen name="TSipanelCamsManagerSummary" position="0,0" size="132,64">\n            <widget name="plugin" position="4,0" size="124,35" font="Regular;15"/>\n            <eLabel position="2,30" size="128,1" backgroundColor="white"/>\n            <widget name="listentry" position="4,36" size="124,14" font="Regular;11"/>\n            <widget name="status" position="4,49" size="124,14" font="Regular;11"/>\n        </screen>\n        '
    elif '900' in HardwareInfo().get_device_name() or '920' in HardwareInfo().get_device_name():
        skin = '<screen name="TSipanelCamsManagerSummary" position="0,0" size="400,240" id="3">\n            <ePixmap pixmap="/usr/share/enigma2/skin_default/display_bg.png" position="0,0" size="400,240" zPosition="-1"/>\n            <widget name="plugin" position="10,0" size="380,75" font="Display;48" halign="center" valign="center" transparent="1"/>\n            <eLabel position="10,85" size="380,2" backgroundColor="white"/>\n            <widget name="listentry" position="0,105" size="400,55" font="Display;38" halign="center" valign="center" transparent="1"/>\n            <widget name="status" position="0,165" size="400,55" font="Display;38" halign="center" valign="center" transparent="1"/>\n        </screen>\n        '

    def __init__(self, session, parent):
        Screen.__init__(self, session)
        self['plugin'] = Label()
        self['listentry'] = Label()
        self['status'] = Label()
        self.onLayoutFinish.append(self.layoutEnd)
        return

    def layoutEnd(self):
        self['plugin'].setText('Softcams')
        self['listentry'].setText('TestCam')
        self['status'].setText('stopped')
        return

    def setText(self, text, line):
        if line == 1:
            self['listentry'].setText(text)
        if line == 2:
            self['status'].setText(text)
        return


class Getipklist(Screen):
    skin_1280 = '<screen name="Getipklist" position="center,77" size="920,600" title="">\n        <widget source="list" render="Listbox" position="50,20" size="850,418" scrollbarMode="showOnDemand" transparent="1" zPosition="2">\n            <convert type="TemplatedMultiContent">\n                {"template": [\n                    MultiContentEntryPixmapAlphaBlend(pos=(8,8), size=(16,16), png=1),\n                    MultiContentEntryText(pos=(35,0), size=(650,32), font=0, flags=RT_HALIGN_LEFT|RT_VALIGN_CENTER, text=0),\n                    MultiContentEntryPixmapAlphaBlend(pos=(3,3), size=(26,26), png=2)\n                 ],\n                 "fonts": [gFont("Regular",23)],\n                 "itemHeight": 32\n                }\n            </convert>\n        </widget>\n\n        <eLabel position="20,470" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"/>\n        <widget name="fspace" position="20,460" zPosition="4" size="880,80" font="Regular;24" foregroundColor="yellow" transparent="1" halign="center" valign="center"/>\n        <eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"/>\n\n        <widget name="waiting" position="250,230" zPosition="4" size="430,50" font="Regular;25" transparent="1" halign="center" valign="center"/>\n        <widget name="info" position="250,435" zPosition="4" size="430,30" font="Regular;23" transparent="1" halign="center" valign="center"/>\n\n        <ePixmap name="red"   position="250,540" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png"   transparent="1" alphatest="on"/>\n        <ePixmap name="green" position="460,540" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_green.png" transparent="1" alphatest="on"/>\n\n        <widget name="key_red"   position="250,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;20" transparent="1"/>\n        <widget name="key_green" position="460,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;20" transparent="1"/>\n    </screen>\n    '
    skin_1920 = '<screen name="Getipklist" position="center,200" size="1300,720" title="Softcams Manager">\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png"   position="375,640" size="200,40" alphatest="blend"/>\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green-big.png" position="725,640" size="200,40" alphatest="blend"/>\n\n        <widget name="key_red"   position="375,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#940d0d" transparent="1"/>\n        <widget name="key_green" position="725,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#2d872d" transparent="1"/>\n\n        <widget name="fspace"  position="40,490" size="300,140" foregroundColor="foreground" backgroundColor="background" font="Regular;26" valign="top" halign="left" transparent="1" zPosition="1"/>\n        <widget name="info"    position="20,440" size="1260,40" foregroundColor="yellow"   backgroundColor="background" font="Regular;26" valign="center" halign="center" transparent="1" zPosition="1"/>\n        <widget name="waiting" position="20,20"  size="1260,600" foregroundColor="foreground" backgroundColor="background" font="Regular;32" valign="center" halign="center" transparent="1" zPosition="1"/>\n\n        <eLabel position="10,480" zPosition="4" size="1280,1" backgroundColor="foreground"/>\n\n        <widget source="list" render="Listbox" position="20,20" size="1260,400" zPosition="2" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background" transparent="1">\n            <convert type="TemplatedMultiContent">\n                {"template": [\n                    MultiContentEntryText(pos=(45,0), size=(1000,40), flags=RT_HALIGN_LEFT|RT_VALIGN_CENTER, text=0),\n                    MultiContentEntryPixmapAlphaBlend(pos=(7,7), size=(26,26), png=1),\n                    MultiContentEntryPixmapAlphaBlend(pos=(0,0), size=(40,40), png=2)\n                 ],\n                 "fonts": [gFont("Regular",30)],\n                 "itemHeight": 40\n                }\n            </convert>\n        </widget>\n    </screen>\n    '
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session):
        Screen.__init__(self, session)
        self.greenStatus = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green.png'))
        self.blueStatus = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/blue.png'))
        self.greyStatus = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/grey.png'))
        self.installIcon = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/install.png'))
        self.removeIcon = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/remove.png'))
        self.updateIcon = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/update.png'))
        self['key_green'] = Button(_('Execute'))
        self['key_red'] = Button(_('Back'))
        self['key_green'].hide()
        self['list'] = List([])
        self['info'] = Label()
        self['waiting'] = Label(_('Downloading list, please wait...'))
        self['fspace'] = Label()
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'red': (self.close), 'green': (self.selgreen), 'ok': (self.selclicked), 'cancel': (self.close)}, -1)
        self.downloading = False
        self['fspace'].setText(self.freespace())
        self.onLayoutFinish.append(self.createIpklist)
        self.onShown.append(self.setWindowTitle)
        self['list'].onSelectionChanged.append(self.selectionChanged)
        return

    def setWindowTitle(self):
        self.setTitle(_('Install/Remove'))
        return

    def freespace(self):
        try:
            diskSpace = os_statvfs('/')
            capacity = float(diskSpace.f_bsize * diskSpace.f_blocks)
            available = float(diskSpace.f_bsize * diskSpace.f_bavail)
            fspace = round(float(available / 1048576.0), 2)
            tspace = round(float(capacity / 1048576.0), 1)
            spacestr = 'Free space(' + str(fspace) + 'MB) Total space(' + str(tspace) + 'MB)'
            return spacestr
        except:
            return ''

        return

    def createIpklist(self):
        self.installList = []
        self.removeList = []
        self.names = []
        if fileExists(dpkg_list_filename):
            cmd = 'grep -E \'^(gp4-cams-|nobody-cams-|enigma2-plugin-softcams(-|$))\' "%s" | awk \'{printf "%%s_%%s\\n", $1, $3}\'' % dpkg_list_filename
            self.count = 0
            self.cache = None
            self.container_conn = None
            self.container_data = None
            self['waiting'].setText(_('Getting cams list, please wait...'))
            self.container = eConsoleAppContainer()
            self.container_conn = self.container.appClosed.connect(self.ongetIpkgListClose)
            self.container_data = self.container.dataAvail.connect(self.cmdData)
            self.container.execute(cmd)
        else:
            self['waiting'].setText(_('apt update, please wait...'))
            self.dpkgupdate()
        return

    def ongetIpkgListClose(self, retval=None):
        self.container_data = None
        self.container_conn = None
        self['waiting'].setText('')
        self['list'].setList(self.names)
        self.selectionChanged()
        return

    def cmdData(self, data):
        if self.cache is None:
            self.cache = data
        else:
            self.cache += data
        if '\n' in data:
            splitcache = self.cache.split('\n')
            if self.cache[-1] == '\n':
                iteration = splitcache
                self.cache = None
            else:
                iteration = splitcache[:-1]
                self.cache = splitcache[-1]
            for line in iteration:
                line = line.strip()
                if not line:
                    continue
                if line.startswith('enigma2-cams-default'):
                    continue
                self.addIpkg(line, boxarch)

        return

    def addIpkg(self, data, arch):
        sp = data.split('_', 2)
        url = distro_feed + arch.replace(boxarch, debarchname) + '/'
        fullname = url + data + '_' + arch + '.deb'
        if len(sp) > 1 and ':' in sp[1]:
            idx = sp[1].find(':')
            sp[1] = sp[1][idx + 1:]
            data = sp[0] + '_' + sp[1]
            fullname = url + data + '_' + arch + '.deb'
        ver, processmode = getipkinfos(fullname)
        name = sp[0]
        if name.startswith('gp4-cams-'):
            item = name[len('gp4-cams-'):]
        elif name.startswith('nobody-cams-'):
            item = name[len('nobody-cams-'):]
        elif name.startswith('enigma2-plugin-softcams-'):
            item = name[len('enigma2-plugin-softcams-'):]
        else:
            item = name
        if processmode == 'install':
            self.names.append((item, self.greyStatus, None, processmode, fullname))
        elif processmode == 'update':
            self.names.append((item, self.blueStatus, None, processmode, fullname))
        elif processmode == 'remove':
            self.count += 1
            self.names.append((item, self.greenStatus, None, processmode, fullname))
        return

    def reloadIpklist(self):
        self.createIpklist()
        self['waiting'].setText('')
        return

    def updateInstall(self, status):
        self['list'].setList([])
        self['fspace'].setText(self.freespace())
        self['waiting'].setText(_('Reloading list, please wait...'))
        self['info'].setText('')
        self.timer = eTimer()
        self.timer_conn = self.timer.timeout.connect(self.reloadIpklist)
        self.timer.start(200, 1)
        self['key_green'].hide()
        if os_path.exists('/tmp/.restart_e2'):
            os_remove('/tmp/.restart_e2')
        return

    def selectionChanged(self):
        if not len(self.names) == 0:
            cindex = self['list'].getIndex()
            if not self.names[cindex][2] == None:
                self['info'].setText(_('Press OK to select for reset'))
            elif self.names[cindex][1] == self.greyStatus:
                self['info'].setText(_('Press OK to select for install'))
            elif self.names[cindex][1] == self.greenStatus:
                self['info'].setText(_('Press OK to select for remove'))
            elif self.names[cindex][1] == self.blueStatus:
                self['info'].setText(_('Press OK to select for update'))
        return

    def selgreen(self):
        if len(self.removeList) > 0 or len(self.installList) > 0:
            self.session.openWithCallback(self.updateInstall, TSGetMultiipk, self.installNameList, self.removeNameList, self.installList, self.removeList)
        return

    def selclicked(self):
        if not len(self.names) == 0:
            idx = self['list'].getIndex()
            processmode = self.names[idx][3]
            if processmode == 'install':
                self.names[idx] = (
                 self.names[idx][0],
                 self.names[idx][1],
                 self.installIcon,
                 'remove+',
                 self.names[idx][4])
                self['info'].setText(_('Press OK to select for reset'))
            elif processmode == 'remove':
                self.names[idx] = (
                 self.names[idx][0],
                 self.names[idx][1],
                 self.removeIcon,
                 'install+',
                 self.names[idx][4])
                self['info'].setText(_('Press OK to select for reset'))
            elif processmode == 'update':
                self.names[idx] = (
                 self.names[idx][0],
                 self.names[idx][1],
                 self.updateIcon,
                 'update+',
                 self.names[idx][4])
                self['info'].setText(_('Press OK to select for remove'))
            elif processmode == 'update+':
                self.names[idx] = (
                 self.names[idx][0],
                 self.names[idx][1],
                 self.removeIcon,
                 'update++',
                 self.names[idx][4])
                self['info'].setText(_('Press OK to select for reset'))
            elif processmode == 'install+':
                self.names[idx] = (
                 self.names[idx][0],
                 self.names[idx][1],
                 None,
                 'remove',
                 self.names[idx][4])
                self['info'].setText(_('Press OK to select for remove'))
            elif processmode == 'remove+':
                self.names[idx] = (
                 self.names[idx][0],
                 self.names[idx][1],
                 None,
                 'install',
                 self.names[idx][4])
                self['info'].setText(_('Press OK to select for install'))
            elif processmode == 'update++':
                self.names[idx] = (
                 self.names[idx][0],
                 self.names[idx][1],
                 None,
                 'update',
                 self.names[idx][4])
                self['info'].setText(_('Press OK to select for update'))
            self.updateLists()
            self['list'].updateList(self.names)
        return

    def updateLists(self):
        self.installNameList = []
        self.removeNameList = []
        self.installList = []
        self.removeList = []
        url = distro_feed + debarchname + '/'
        for idx in range(len(self.names)):
            if self.names[idx][2] == self.installIcon or self.names[idx][2] == self.updateIcon:
                self.installNameList.append(self.names[idx][4])
                self.installList.append(url + self.names[idx][4] + '_' + debarchname + '.deb')
            elif self.names[idx][2] == self.removeIcon:
                self.removeNameList.append(self.names[idx][4])
                self.removeList.append(url + self.names[idx][4] + '_' + debarchname + '.deb')

        if len(self.removeList) > 0 or len(self.installList) > 0:
            self['key_green'].show()
        else:
            self['key_green'].hide()
        return

    def dpkgupdate(self):
        if os_path.exists(dpkg_ready_filename) or not os_path.exists(dpkg_updater_filename):
            self.upgradable_nr = 0
            self.is_dpkg_busy = True
            if os_path.exists(dpkg_busy_filename):
                os_remove(dpkg_busy_filename)
            if os_path.exists(dpkg_ready_filename):
                os_remove(dpkg_ready_filename)
            if os_path.exists(dpkg_list_filename):
                os_remove(dpkg_list_filename)
            print '[dpkg update] start'
            cmd = 'touch %s ; COLUMNS=2000 apt-get update' % dpkg_busy_filename
            self['waiting'].setText('Starting deb update...')
            self.cache = None
            self.error = None
            self.container = eConsoleAppContainer()
            self.container_conn = self.container.appClosed.connect(self.ondpkgUpdateClose)
            self.container_data = self.container.dataAvail.connect(self.cmdData2)
            self.container.execute(cmd)
        return

    def cmdData2(self, data):
        if self.cache is None:
            self.cache = data
        else:
            self.cache += data
        if '\n' in data:
            splitcache = self.cache.split('\n')
            if self.cache[-1] == '\n':
                iteration = splitcache
                self.cache = None
            else:
                iteration = splitcache[:-1]
                self.cache = splitcache[-1]
            for mydata in iteration:
                if mydata != '':
                    if mydata.startswith('Ign'):
                        self['waiting'].setText('Downloading repositories...')
                    elif mydata.startswith('Get'):
                        self['waiting'].setText('Inflating repositories...')
                    elif mydata.startswith('E:'):
                        self.error = mydata.split(': ', 3)[2].strip()
                        self['waiting'].setText('error: %s' % self.error)
                    elif mydata.startswith('E:'):
                        self.error = mydata.split(': ', 2)[1].strip()
                        self['waiting'].setText('%s' % self.error)

        return

    def ondpkgUpdateClose(self, status):
        self.container_conn = None
        self['waiting'].setText('Saving list of available packages...')
        self.dpkgList()
        return

    def dpkgList(self, retval=None):
        if os_path.exists(dpkg_updater_filename):
            print '[MultiIpk RessourcesCheck] resources busy...'
            cmd = 'echo\n'
            self.container = eConsoleAppContainer()
            self.container.appClosed.connect(self.dpkgList)
            self.container.execute(cmd)
        else:
            cmd = 'COLUMNS=2000 apt-opkg list | grep -E \'^(gp4-cams-|nobody-cams-|enigma2-plugin-(extensions|systemplugins|softcams)(-|$)|enigma2-skin-ts-|enigma2-cams-|kernel-)|exfat|ntfs-\' > "%s"' % dpkg_list_filename
            self.container = eConsoleAppContainer()
            self.container_conn = self.container.appClosed.connect(self.ondpkgListClose)
            self.container.execute(cmd)
        return

    def ondpkgListClose(self, status):
        self.container_conn = None
        os_system('touch %s' % dpkg_ready_filename)
        if os_path.exists(dpkg_busy_filename):
            os_remove(dpkg_busy_filename)
        self['waiting'].setText('Checking for available updates...')
        self.dpkgUpgradeAvailable()
        return

    def dpkgUpgradeAvailable(self, retval=None):
        if os_path.exists(dpkg_updater_filename):
            print '[MultiIpk RessourcesCheck] resources busy...'
            cmd = 'echo\n'
            self.container = eConsoleAppContainer()
            self.container_conn = self.container.appClosed.connect(self.dpkgUpgradeAvailable)
            self.container.execute(cmd)
        else:
            self['key_green'].hide()
            cmd = 'COLUMNS=2000 apt-opkg list_upgradable > %s' % dpkg_ugradable_filename
            self.container = eConsoleAppContainer()
            self.container_conn = self.container.appClosed.connect(self.ondpkgUpgradableClose)
            self.container.execute(cmd)
        return

    def ondpkgUpgradableClose(self, retval=None):
        self.upgradable_nr = self.getdpkgUpgradale()
        config.plugins.TSUpdater.UpdateAvailable.value = str(self.upgradable_nr)
        config.plugins.TSUpdater.save()
        configfile.save()
        self.createIpklist()
        return

    def getdpkgUpgradale(self):
        f = open(dpkg_ugradable_filename, 'r')
        line = 'dummy'
        count = 0
        while line:
            line = f.readline()
            if not line == '':
                count = count + 1

        f.close()
        print '[upgradable_list] updatable packages: %d' % count
        return count


return
