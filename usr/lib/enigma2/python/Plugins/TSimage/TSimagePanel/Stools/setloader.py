# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/Stools/setloader.py
# Compiled at: 2018-04-09 19:45:47
from enigma import *
from Screens.MessageBox import MessageBox
from Components.Label import Label
from Components.Button import Button
from Components.Sources.List import List
from Tools.Directories import resolveFilename, SCOPE_CURRENT_SKIN, SCOPE_CURRENT_PLUGIN, SCOPE_SKIN_IMAGE, copyfile, pathExists, createDir, removeDir, fileExists, copytree
from Tools.LoadPixmap import LoadPixmap
from Components.Pixmap import Pixmap
from Tools.HardwareInfo import HardwareInfo
from Components.config import ConfigSelection, config, ConfigSubsection, ConfigText, ConfigYesNo, getConfigListEntry, configfile
from time import *
from Screens.Screen import Screen
from Components.ActionMap import ActionMap, NumberActionMap
from Components.Sources.ServiceEvent import ServiceEvent
from Components.ServiceEventTracker import ServiceEventTracker
import os, sys
from Components.ConfigList import ConfigListScreen
from urlparse import urlparse
import xml.etree.cElementTree, httplib
from tsimage import TSimagePanelImage
import datetime
from ServiceReference import ServiceReference
from enigma import eTimer, eDVBDB, eServiceCenter, eServiceReference, iPlayableService, iFrontendInformation, getDesktop
desktopSize = getDesktop(0).size()
SIOUD_HOST = 'tunisia-dreambox.info'
SIOUD_PATH = '/TSimage-addons-2/settings/TunisiaSat/'
CYRUS_HOST = 'adams.mine.nu'
CYRUS_PATH = '/cyrus/'
VHANNIBAL_HOST = 'tunisia-dreambox.info'
VHANNIBAL_PATH = '/TSimage-addons-2/settings/Vhannibal/'
MORPHEUS_HOST = 'openee.sifteam.eu'
MORPHEUS_PATH = '/settings/morph883/'
TMP_SETTINGS_PWD = '/tmp/sl_settings_tmp'
TMP_IMPORT_PWD = '/tmp/sl_import_tmp'
ENIGMA2_SETTINGS_PWD = '/etc/enigma2'
ENIGMA2_TUXBOX_PWD = '/etc/tuxbox'
config.plugins.settingsloader = ConfigSubsection()
config.plugins.settingsloader.keepterrestrial = ConfigYesNo(False)
config.plugins.settingsloader.keepsatellitesxml = ConfigYesNo(False)
config.plugins.settingsloader.keepcablesxml = ConfigYesNo(False)
config.plugins.settingsloader.keepterrestrialxml = ConfigYesNo(False)
config.plugins.settingsloader.keepbouquets = ConfigText('', False)
config.plugins.settingsloader.updatebouquets = ConfigSelection(default='no', choices=[('no', _('no')), ('select', _('select bouquets to keep')), ('yes', _('yes'))])

class TSSLScreenSummary(Screen):
    if '820' in HardwareInfo().get_device_name():
        skin = '\n\t\t\t<screen position="0,0" size="96,64" id="2">\n\t\t\t\t<eLabel text="Settings loader" position="1,0" size="94,30" font="Regular;13" halign="center" valign="center"/>\n                                <eLabel position="2,30" size="92,1" backgroundColor="#21b0cf"/> \n\t\t\t\t<widget name="text1" position="1,34" size="94,30" font="Regular;12" halign="center" valign="center"/>\n\t\t\t</screen>'
    elif '7080' in HardwareInfo().get_device_name():
        skin = '\n\t\t\t<screen position="0,0" size="132,64">\n\t\t\t\t<eLabel text="Settings loader" position="6,0" size="120,30" font="Regular;13" halign="center" valign="center"/>\n\t\t\t\t<eLabel position="2,30" size="128,1" backgroundColor="white" /> \n\t\t\t\t<widget name="text1" position="6,34" size="120,30" font="Regular;12" halign="center" valign="center"/>\n\t\t\t</screen>'
    elif '900' in HardwareInfo().get_device_name() or '920' in HardwareInfo().get_device_name():
        skin = '\n\t\t\t<screen position="0,0" size="400,240" id="3">\n\t\t\t\t<ePixmap pixmap="/usr/share/enigma2/skin_default/display_bg.png" position="0,0" size="400,240" zPosition="-1"/>\n\t\t\t\t<eLabel text="Settings loader" position="10,0" size="380,75" font="Display;48" halign="center" valign="center" transparent="1"/>\n\t\t\t\t<eLabel position="10,85" size="380,2" backgroundColor="white" /> \n\t\t\t\t<widget name="text1" position="0,85" size="400,155" font="Display;58" halign="center" valign="center" transparent="1"/>\n\t\t\t</screen>'

    def __init__(self, session, parent):
        Screen.__init__(self, session)
        self['text1'] = Label()
        self.onLayoutFinish.append(self.layoutEnd)
        return

    def layoutEnd(self):
        self['text1'].setText(_('Please wait...'))
        return

    def setText(self, text, line):
        self['text1'].setText(text)
        return


class TSiServersScreen(Screen):
    skin_1280 = '\n                    <screen name="TSiServersScreen"  position="center,77"  title="Settings loader"  size="920,600"  >\n\t\t    <widget source="list" render="Listbox" position="20,15" size="880,416" scrollbarMode="showOnDemand" transparent="1" zPosition="1" >\n\t\t                <convert type="TemplatedMultiContent">\n\t\t\t\t\t{"template": [\n\t\t\t\t\t                MultiContentEntryPixmapAlphaTest(pos = (0, 4), size = (24, 24), png = 1), # type Icon,\n\t\t\t\t\t\t\tMultiContentEntryText(pos = (40, 0), size = (650, 32), font=0, flags = RT_HALIGN_LEFT| RT_VALIGN_CENTER, text = 0),\n\t\t\t\t\t\t],\n\t\t\t\t\t"fonts": [gFont("Regular", 22)],\n\t\t\t\t\t"itemHeight": 32\n\t\t\t\t\t}\n\t\t\t\t</convert>\n                    </widget>                \t                   \n                    <eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\n    \t            <ePixmap name="red"    position="70,545"   zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" transparent="1" alphatest="blend" />\n                    <ePixmap name="green"  position="280,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_green.png" transparent="1" alphatest="blend" />\n                    <ePixmap name="yellow" position="490,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_yellow.png" transparent="1" alphatest="blend" /> \n            \t    <widget name="key_red" position="70,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" /> \n                    <widget name="key_yellow" position="490,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;20" transparent="1" />        \n                    </screen>'
    skin_1920 = '    <screen name="TSiServersScreen" position="center,200" size="1300,720" title="Addons Manager">\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png" position="50,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green-big.png" position="360,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/yellow-big.png" position="670,640" size="200,40" alphatest="blend" />\n        <widget name="key_red" position="50,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#940d0d" transparent="1" />\n        <widget name="key_yellow" position="670,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#bba502" transparent="1" />\n        <widget source="list" render="Listbox" position="20,20" size="1260,600" zPosition="2" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background"  transparent="1" >\n        <convert type="TemplatedMultiContent">\n        {"template": [\n        MultiContentEntryText(pos = (45, 0), size = (1000, 40), flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 0) ,\n        MultiContentEntryPixmapAlphaBlend(pos = (2, 7), size = (28, 28), png = 1),\n        ],\n        "fonts": [gFont("Regular", 30)],\n        "itemHeight": 40\n        }\n        </convert>\n        </widget>\n        </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session):
        Screen.__init__(self, session)
        self.serverIcon = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, 'TSimage/TSimagePanel/buttons/addons.png'))
        self.serversnames = []
        self.serversnames.append(('Morpheus883 settings', self.serverIcon))
        self.serversnames.append(('Vhannibal settings', self.serverIcon))
        self.serversnames.append(('TunisiaSat settings', self.serverIcon))
        self['key_red'] = Button(_('Close'))
        self['key_yellow'] = Button(_('Settings'))
        self['list'] = List(self.serversnames)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': (self.openSelected), 'yellow': (self.showsettings), 
           'cancel': (self.close)}, -2)
        self.onShown.append(self.setWindowTitle)
        self['list'].onSelectionChanged.append(self.selectionChanged)
        return

    def setWindowTitle(self):
        self.setTitle(_('Settings loader'))
        self.selectionChanged()
        return

    def showsettings(self):
        self.session.open(TSSLSetup)
        return

    def openSelected(self):
        index = self['list'].getIndex()
        self.host = ''
        self.path = ''
        self.title = ''
        self.xml = 'lista.xml'
        if index == 0:
            self.host = MORPHEUS_HOST
            self.path = MORPHEUS_PATH
            self.title = 'Morpheus Settings'
            self.xml = 'morph883.xml'
        elif index == 1:
            self.host = VHANNIBAL_HOST
            self.path = VHANNIBAL_PATH
            self.title = 'Vhannibal Settings'
        elif index == 2:
            self.host = SIOUD_HOST
            self.path = SIOUD_PATH
            self.title = 'TunisiaSat Settings'
        self.setTitle('Settings loader')
        self.session.open(TSSLSelection, self.host, self.path, self.title, self.xml)
        return

    def selectionChanged(self):
        index = self['list'].getIndex()
        self.updateOLED(self.serversnames[index][0])
        return

    def createSummary(self):
        return TSSLScreenSummary

    def updateOLED(self, text):
        self.summaries.setText(text, 1)
        return


class TSSLSelection(Screen):
    skin_1280 = '\n                    <screen name="TSSLSelection"  position="center,77"  title="Settings loader"  size="920,600"  >\n                    <widget source="list" render="Listbox" position="20,20" size="880,480" scrollbarMode="showOnDemand" transparent="1" zPosition="2" >\n\t\t\t\t<convert type="TemplatedMultiContent">\n\t\t\t\t\t{"template": [\n\t\t\t\t\t\tMultiContentEntryText(pos = (70, 0), size = (560, 40), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 1),\n\t\t\t\t\t\tMultiContentEntryText(pos = (730, 0), size = (150, 40), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 2),\n\t\t\t\t\t\tMultiContentEntryPixmapAlphaBlend(pos = (10, 7), size = (25, 25), png = 0), # Icon\n\n\t\t\t\t\t\t],\n\t\t\t\t\t\t"fonts": [gFont("Regular", 22)],\n\t\t\t\t\t\t"itemHeight": 40\n\t\t\t\t\t}\n\t\t\t\t</convert>\n\t\t\t</widget>\t          \n                    <eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\n                    <ePixmap name="red"    position="70,545"   zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" transparent="1" alphatest="blend" />               \n      \t    \t    <ePixmap name="green"  position="280,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_green.png" transparent="1" alphatest="blend" />\n                    <widget name="key_red" position="70,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" /> \n        \t    <widget name="key_green" position="280,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" />\n                    <widget name="waiting" position="20,20" size="880,480" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" /> \n        \t     \t\t\t\n\t\t</screen>'
    skin_1920 = '    <screen name="TSSLSelection" position="center,200" size="1300,720" title="Addons Manager">\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png" position="375,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green-big.png" position="725,640" size="200,40" alphatest="blend" />\n        <widget name="key_red" position="375,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#940d0d" transparent="1" />\n        <widget name="key_green" position="725,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#2d872d" transparent="1" />\n        <widget name="waiting" position="20,20" size="1260,600" foregroundColor="foreground" backgroundColor="background" font="Regular;32" valign="center" halign="center" transparent="1" zPosition="1" />\n        <widget source="list" render="Listbox" position="20,20" size="1260,600" zPosition="2" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background"  transparent="1" >\n        <convert type="TemplatedMultiContent">\n        {"template": [\n        MultiContentEntryText(pos = (45, 0), size = (1000, 40), flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 1) ,\n        MultiContentEntryText(pos = (0, 0), size = (1220, 40), flags = RT_HALIGN_RIGHT | RT_VALIGN_CENTER, text = 2) ,\n        MultiContentEntryPixmapAlphaBlend(pos = (2, 7), size = (28, 28), png = 0),\n        ],\n        "fonts": [gFont("Regular", 28)],\n        "itemHeight": 40\n        }\n        </convert>\n        </widget>\n        </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session, settings_host=None, settings_path=None, title=None, xmlname=None):
        Screen.__init__(self, session)
        self.session = session
        self.path = settings_path
        self.host = settings_host
        self.title = title
        self.xml = xmlname
        self.bouquetsel_switch = False
        self.transfering = False
        self.drawList = []
        self.listAll = []
        self.selTVList = []
        self.selRadioList = []
        self.bouquet_selection = False
        self.index = 0
        self.pixmap_on = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/images/lock_on.png'))
        self.pixmap_off = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/images/lock_off.png'))
        self.pixmap_tv = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/images/settings.png'))
        self['list'] = List(self.drawList)
        self['key_red'] = Button(_('Back'))
        self['key_green'] = Button(_('Install'))
        self['waiting'] = Label('')
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'ok': (self.ok), 'red': (self.quit), 
           'green': (self.transfer), 
           'cancel': (self.quit)}, -2)
        self['waiting'].setText(_('Downloading settings list, please wait...'))
        self.timer = eTimer()
        self.timer_conn = self.timer.timeout.connect(self.download)
        self.timer.start(200, 1)
        self.onShown.append(self.setWindowTitle)
        self['list'].onSelectionChanged.append(self.selectionChanged)
        return

    def setWindowTitle(self):
        self.setTitle(_('Settings selection'))
        return

    def buildListEntry(self, enabled, name, type):
        if enabled == None:
            pixmap = self.pixmap_tv
        elif enabled:
            pixmap = self.pixmap_on
        else:
            pixmap = self.pixmap_off
        return (
         pixmap, name, type)

    def download(self):
        self.settingsList = []
        self.urlList = []
        try:
            conn = httplib.HTTPConnection(self.host)
            conn.request('GET', self.path + self.xml)
            httpres = conn.getresponse()
            if httpres.status == 200:
                mdom = xml.etree.cElementTree.parse(httpres)
                root = mdom.getroot()
                for node in root:
                    if node.tag == 'MAIN':
                        sat = ''
                        date = ''
                        url = ''
                        for x in node:
                            if x.tag == 'SAT':
                                sat = str(x.text)
                            elif x.tag == 'DATE':
                                date = x.text
                            elif x.tag == 'URL':
                                url = x.text

                        self.settingsList.append(self.buildListEntry(None, sat, date))
                        self.urlList.append(url)
                    elif node.tag == 'package':
                        sat = node.text
                        date = node.get('date')
                        print date[:4]
                        print date[4:6]
                        print date[-2:]
                        date = datetime.date(int(date[:4]), int(date[4:6]), int(date[-2:]))
                        date = date.strftime('%d %b')
                        url = 'http://' + self.host + self.path + node.get('filename')
                        self.settingsList.append(self.buildListEntry(None, sat, date))
                        self.urlList.append(url)

                if self.settingsList == []:
                    self.session.open(MessageBox, _('Cannot download settings list'), MessageBox.TYPE_ERROR)
                    self.quit()
            else:
                self.session.open(MessageBox, _('Cannot download settings list'), MessageBox.TYPE_ERROR)
                self.quit()
        except Exception as e:
            print e
            self.session.open(MessageBox, _('Cannot download settings list'), MessageBox.TYPE_ERROR)
            self.quit()

        self['waiting'].setText('')
        self['list'].setList(self.settingsList)
        return

    def ShowBouquetsList(self):
        settings = SL_Settings()
        self.listTv = settings.readBouquetsTvList(TMP_SETTINGS_PWD)
        self.listRadio = settings.readBouquetsRadioList(TMP_SETTINGS_PWD)
        self.drawList = []
        self.selTVList = []
        self.selRadioList = []
        self.listAll = []
        if self.listTv is not None and self.listRadio is not None:
            for x in self.listTv:
                self.drawList.append(self.buildListEntry(True, str(x[1]), 'TV'))
                self.selTVList.append(self.buildListEntry(True, str(x[1]), 'TV'))
                self.listAll.append(x)

            for x in self.listRadio:
                self.drawList.append(self.buildListEntry(True, str(x[1]), 'Radio'))
                self.selRadioList.append(self.buildListEntry(True, str(x[1]), 'Radio'))
                self.listAll.append(x)

        self['list'].setList(self.drawList)
        return

    def clean_tmp(self):
        if os.path.exists(TMP_IMPORT_PWD):
            os.system('rm -R %s' % TMP_IMPORT_PWD)
        if os.path.exists(TMP_SETTINGS_PWD):
            os.system('rm -R %s' % TMP_SETTINGS_PWD)
        return

    def download2(self):
        self.bouquetsel_switch = False
        self.bouquet_selection = True
        self.clean_tmp()
        os.mkdir(TMP_SETTINGS_PWD)
        os.mkdir(TMP_IMPORT_PWD)
        self.installed = False
        url = urlparse(self.url)
        try:
            conn = httplib.HTTPConnection(url.netloc)
            conn.request('GET', url.path)
            httpres = conn.getresponse()
            if httpres.status == 200:
                tmp = url.path.split('/')
                filename = TMP_IMPORT_PWD + '/' + tmp[len(tmp) - 1]
                print '[Settings Browser] filename: %s' % filename
                out = open(filename, 'w')
                out.write(httpres.read())
                out.close()
                self.installed = SL_Deflate().deflate(filename)
            else:
                self.session.open(MessageBox, _('Cannot download settings (%s)') % self.url, MessageBox.TYPE_ERROR)
                self.installed = False
                self.quit()
        except Exception as e:
            print e
            self.installed = False
            self.clean_tmp()

        if self.installed == True:
            if not self.transfering:
                self.ShowBouquetsList()
                self['waiting'].setText('')
            else:
                self['list'].setList([])
                self['waiting'].setText(_('Transfering settings, please wait...'))
                self.timer2 = eTimer()
                self.timer2_conn = self.timer2.timeout.connect(self.dotransfer)
                self.timer2.start(200, 1)
        else:
            self.session.open(MessageBox, _('Settings installation failed, format may be not supported'), type=MessageBox.TYPE_ERROR, timeout=5)
            self.transfering = False
            self.quit()
        return

    def updateChanges(self, filename, sellist):
        f = open(filename, 'r')
        line = f.readline()
        self.line_list = []
        self.removed_filename_list = []
        self.line_list.append(line)
        for idx in range(1, len(sellist)):
            line = f.readline()
            if sellist[idx - 1][0] == self.pixmap_on:
                self.line_list.append(line)
            else:
                line = line.replace('#SERVICE', '')
                line = line.replace('1:7:1:0:0:0:0:0:0:0:', '')
                line = line.replace(':', '')
                line = line.replace('FROM BOUQUET', '')
                line = line.replace('ORDER BY bouquet', '')
                line = line.replace('"', '')
                bouquet_filename = TMP_SETTINGS_PWD + '/' + line.strip()
                if os.path.exists(bouquet_filename):
                    os.remove(bouquet_filename)

        f.close()
        f = open(filename, 'w')
        for idx in range(0, len(self.line_list) - 1):
            f.write('%s' % self.line_list[idx])

        f.close()
        return

    def transfer(self):
        self.transfering = True
        if not self.bouquet_selection:
            self['waiting'].setText(_('Downloading settings, please wait...'))
            self.updateOLED(_('Downloading settings, please wait...'))
            self.index = self['list'].getIndex()
            self.url = str(self.urlList[self.index])
            self['list'].setList([])
            self.timer = eTimer()
            self.timer_conn = self.timer.timeout.connect(self.download2)
            self.timer.start(200, 1)
        else:
            self['list'].setList([])
            self['waiting'].setText(_('Transfering settings, please wait...'))
            self.timer2 = eTimer()
            self.timer2_conn = self.timer2.timeout.connect(self.dotransfer)
            self.timer2.start(200, 1)
        return

    def dotransfer(self):
        if os.path.exists(TMP_SETTINGS_PWD):
            if not len(self.selTVList) == 0:
                self.updateChanges(TMP_SETTINGS_PWD + '/' + 'bouquets.tv', self.selTVList)
            if not len(self.selRadioList) == 0:
                self.updateChanges(TMP_SETTINGS_PWD + '/' + 'bouquets.radio', self.selRadioList)
            settings = SL_Settings()
            settings.apply()
            os.system('rm -R %s' % TMP_SETTINGS_PWD)
            self['waiting'].setText('')
            self.session.open(MessageBox, _('Settings successfully transfered !'), MessageBox.TYPE_INFO)
            self.clean_tmp()
            self.close()
        self.transfering = False
        return

    def ok(self):
        self.bouquetsel_switch = True
        if self.bouquet_selection:
            self.updateOLED(_('Please wait...'))
            self.switchSelection()
        else:
            self['waiting'].setText(_('Loading settings bouquets, please wait...'))
            self.index = self['list'].getIndex()
            self.url = str(self.urlList[self.index])
            self['list'].setList([])
            self.timer = eTimer()
            self.timer_conn = self.timer.timeout.connect(self.download2)
            self.timer.start(200, 1)
        return

    def switchSelection(self):
        if len(self.listAll) == 0:
            return
        index = self['list'].getIndex()
        name = str(self.drawList[index][1])
        typetv = str(self.drawList[index][2])
        if self.drawList[index][0] == self.pixmap_on:
            self.drawList[index] = self.buildListEntry(False, name, typetv)
            if typetv == 'TV':
                self.selTVList[index] = self.buildListEntry(False, name, typetv)
            elif typetv == 'Radio':
                self.selRadioList[index - len(self.selTVList)] = self.buildListEntry(False, name, typetv)
        else:
            self.drawList[index] = self.buildListEntry(True, name, typetv)
            if typetv == 'TV':
                self.selTVList[index] = self.buildListEntry(True, name, typetv)
            elif typetv == 'Radio':
                self.selRadioList[index - len(self.selTVList)] = self.buildListEntry(True, name, typetv)
        self.bouquetsel_switch = False
        self['list'].setList(self.drawList)
        self['list'].setIndex(index)
        return

    def quit(self):
        if self.bouquet_selection:
            self.bouquet_selection = False
            self['waiting'].setText('')
            self['list'].setList(self.settingsList)
            self['list'].setIndex(self.index)
        else:
            self.clean_tmp()
            self.close()
        return

    def saveconfig(self):
        config.save()
        self.close()
        return

    def selectionChanged(self):
        oledText = ' '
        index = self['list'].getIndex()
        if self.bouquet_selection:
            if index < len(self.drawList):
                self.setTitle(_('Bouquets selection'))
                oledText = self.drawList[index][1]
        elif self.bouquetsel_switch:
            self.setTitle(_('Bouquets selection'))
            oledText = _('Please wait...')
        elif index < len(self.settingsList):
            self.setTitle(_('Settings selection'))
            oledText = self.settingsList[index][1]
        if self.transfering:
            oledText = _('Transfering, please wait...')
        self.updateOLED(oledText)
        return

    def createSummary(self):
        return TSSLScreenSummary

    def updateOLED(self, text):
        self.summaries.setText(text, 1)
        return


class TSSLSetup(Screen, ConfigListScreen):
    skin_1280 = '\n                        <screen name="TSSLSetup"  position="center,77"  title="Settings loader setup"  size="920,600"  >\n                        <widget name="config" position="20,20" size="880,300" scrollbarMode="showOnDemand" zPosition="2" transparent="1"  />\n                        <eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\n\t\t\t<widget name="key_red" position="70,550" size="140,40" valign="center" halign="center" zPosition="5" transparent="1" font="Regular;18"/>\n\t\t\t<widget name="key_green" position="280,550" size="140,40" valign="center" halign="center" zPosition="5" transparent="1" font="Regular;18"/>\t\t\t\n\t\t\t<ePixmap name="red" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" position="70,545" size="140,40" zPosition="4" transparent="1" alphatest="on"/>\n\t\t\t<ePixmap name="green" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_green.png" position="280,545" size="140,40" zPosition="4" transparent="1" alphatest="on"/>\n\t\t\t<ePixmap name="yellow" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_yellow.png" position="490,545" size="140,40" zPosition="4" transparent="1" alphatest="on"/>\t\t\t\t\t\t\n\t\t\t<ePixmap name="blue" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_blue.png" position="700,545" size="140,40" zPosition="4" transparent="1" alphatest="on"/>\t\t\t\t\t\t\n\t\t\t<widget name="key_blue" position="700,550" size="140,40" valign="center" halign="center" zPosition="5" transparent="1" font="Regular;18"/>\n\t\t</screen>'
    skin_1920 = '    <screen name="TSSLSetup" position="center,200" size="1300,720" title="Settings loader setup">\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png" position="50,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green-big.png" position="360,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/yellow-big.png" position="670,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/blue-big.png" position="980,640" size="200,40" alphatest="blend" />\n        <widget name="key_red" position="50,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#940d0d" transparent="1" />\n        <widget name="key_green" position="360,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#2d872d" transparent="1" />\n        <widget name="key_blue" position="980,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#18188b" transparent="1" />\n        <widget name="config" position="20,30" size="1260,600" zPosition="2" itemHeight="40" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background"  transparent="1" />\n        </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        ConfigListScreen.__init__(self, self.list, session=session)
        self['key_red'] = Button(_('Cancel'))
        self['key_green'] = Button(_('Save'))
        self['key_blue'] = Button(_('Bouquets'))
        self['key_blue'].hide()
        if config.plugins.settingsloader.updatebouquets.value == 'select':
            self['key_blue'].show()
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'red': (self.keyCancel), 'green': (self.ok), 
           'blue': (self.selectbq), 
           'cancel': (self.keyCancel)}, -2)
        self.createSetup()
        self.onShown.append(self.setWindowTitle)
        return

    def setWindowTitle(self):
        self.setTitle('Settings loader setup')
        return

    def createSetup(self):
        self.list = []
        self.list.append(getConfigListEntry(_('Keep currently installed bouquets:'), config.plugins.settingsloader.updatebouquets))
        self.list.append(getConfigListEntry(_('Keep terrestrial settings:'), config.plugins.settingsloader.keepterrestrial))
        self.list.append(getConfigListEntry(_('Keep satellites.xml:'), config.plugins.settingsloader.keepsatellitesxml))
        self.list.append(getConfigListEntry(_('Keep terrestrial.xml:'), config.plugins.settingsloader.keepterrestrialxml))
        self.list.append(getConfigListEntry(_('Keep cables.xml:'), config.plugins.settingsloader.keepcablesxml))
        self['config'].setList(self.list)
        return

    def selectbq(self):
        if config.plugins.settingsloader.updatebouquets.value == 'select':
            self.session.open(TSSLKeepBouquets)
        return

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        if config.plugins.settingsloader.updatebouquets.value == 'select':
            self['key_blue'].show()
        else:
            self['key_blue'].hide()
        return

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        if config.plugins.settingsloader.updatebouquets.value == 'select':
            self['key_blue'].show()
        else:
            self['key_blue'].hide()
        return

    def ok(self):
        self.keySave()
        return

    def keySave(self):
        for x in self['config'].list:
            x[1].save()

        configfile.save()
        self.close()
        return


class TSSLKeepBouquets(Screen):
    skin_1280 = '\n                    <screen name="TSSLKeepBouquets"  position="center,77"  title="Settings loader keep bouquets"  size="920,600"  >\n                    <widget source="list" render="Listbox" position="20,20" size="880,480" scrollbarMode="showOnDemand" transparent="1" zPosition="2" >\n\t\t\t\t<convert type="TemplatedMultiContent">\n\t\t\t\t\t{"template": [\n\t\t\t\t\t\tMultiContentEntryText(pos = (70, 0), size = (360, 40), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 1),\n\t\t\t\t\t\tMultiContentEntryText(pos = (730, 0), size = (150, 40), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 2),\n\t\t\t\t\t\tMultiContentEntryPixmapAlphaBlend(pos = (10, 7), size = (25, 25), png = 0), # Icon\n\n\t\t\t\t\t\t],\n\t\t\t\t\t\t"fonts": [gFont("Regular", 22)],\n\t\t\t\t\t\t"itemHeight": 40\n\t\t\t\t\t}\n\t\t\t\t</convert>\n\t\t\t</widget>\t          \n                    <eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\n                    <ePixmap name="red"    position="70,545"   zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" transparent="1" alphatest="blend" />               \n      \t    \t    <ePixmap name="green"  position="280,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_green.png" transparent="1" alphatest="blend" />\n                    <widget name="key_red" position="70,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" /> \n        \t    <widget name="key_green" position="280,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" /> \t\t\t\n\t\t</screen>'
    skin_1920 = '    <screen name="TSSLKeepBouquets" position="center,200" size="1300,720" title="Settings loader keep bouquets">\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png" position="375,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green-big.png" position="725,640" size="200,40" alphatest="blend" />\n        <widget name="key_red" position="375,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#940d0d" transparent="1" />\n        <widget name="key_green" position="725,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#2d872d" transparent="1" />\n        <widget source="list" render="Listbox" position="20,20" size="1260,600" zPosition="2" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background"  transparent="1" >\n        <convert type="TemplatedMultiContent">\n        {"template": [\n        MultiContentEntryText(pos = (45, 0), size = (1000, 40), flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 1) ,\n        MultiContentEntryText(pos = (0, 0), size = (1220, 40), flags = RT_HALIGN_RIGHT | RT_VALIGN_CENTER, text = 2) ,\n        MultiContentEntryPixmapAlphaBlend(pos = (2, 7), size = (28, 28), png = 0),\n        ],\n        "fonts": [gFont("Regular", 28)],\n        "itemHeight": 40\n        }\n        </convert>\n        </widget>\n        </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        self.drawList = []
        self['list'] = List(self.drawList)
        self['key_red'] = Button(_('Cancel'))
        self['key_green'] = Button(_('Save'))
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'ok': (self.ok), 'red': (self.close), 
           'green': (self.saveconfig), 
           'cancel': (self.quit)}, -2)
        self.refresh()
        self.onShown.append(self.setWindowTitle)
        return

    def setWindowTitle(self):
        self.setTitle('Keep Bouquets')
        return

    def buildListEntry(self, enabled, name, type):
        if enabled:
            pixmap = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/images/lock_on.png'))
        else:
            pixmap = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/images/lock_off.png'))
        return (
         pixmap, name, type)

    def refresh(self):
        settings = SL_Settings()
        self.listTv = settings.readBouquetsTvList(ENIGMA2_SETTINGS_PWD)
        self.listRadio = settings.readBouquetsRadioList(ENIGMA2_SETTINGS_PWD)
        self.drawList = []
        self.listAll = []
        self.bouquets = config.plugins.settingsloader.keepbouquets.value.split('|')
        if self.listTv is not None and self.listRadio is not None:
            for x in self.listTv:
                if x[0] in self.bouquets:
                    self.drawList.append(self.buildListEntry(True, str(x[1]), 'TV'))
                else:
                    self.drawList.append(self.buildListEntry(False, str(x[1]), 'TV'))
                self.listAll.append(x)

            for x in self.listRadio:
                if x[0] in self.bouquets:
                    self.drawList.append(self.buildListEntry(True, str(x[1]), 'Radio'))
                else:
                    self.drawList.append(self.buildListEntry(False, str(x[1]), 'Radio'))
                self.listAll.append(x)

        self['list'].setList(self.drawList)
        return

    def ok(self):
        if len(self.listAll) == 0:
            return
        index = self['list'].getIndex()
        name = str(self.drawList[index][1])
        typetv = str(self.drawList[index][2])
        if self.listAll[index][0] in self.bouquets:
            self.bouquets.remove(self.listAll[index][0])
            pixmap = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/images/lock_off.png'))
            self.drawList[index] = self.buildListEntry(False, name, typetv)
        else:
            self.bouquets.append(self.listAll[index][0])
            pixmap = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/images/lock_on.png'))
            self.drawList[index] = self.buildListEntry(True, name, typetv)
        config.plugins.settingsloader.keepbouquets.value = ('|').join(self.bouquets)
        self['list'].setList(self.drawList)
        self['list'].setIndex(index)
        return

    def quit(self):
        self.close()
        return

    def saveconfig(self):
        config.save()
        self.close()
        return


class SL_Deflate():

    def __init__(self):
        return

    def deflatebz(self, filename):
        if os.path.exists(TMP_SETTINGS_PWD):
            os.system('rm -R %s' % TMP_SETTINGS_PWD)
            os.mkdir(TMP_SETTINGS_PWD)
        os.system('tar -xjvf ' + filename + ' -C ' + TMP_SETTINGS_PWD)
        os.system('cd ' + TMP_SETTINGS_PWD + ' && find -type f -exec mv {} . \\;')
        return

    def deflateTar(self, filename):
        if os.path.exists(TMP_SETTINGS_PWD):
            os.system('rm -R %s' % TMP_SETTINGS_PWD)
            os.mkdir(TMP_SETTINGS_PWD)
        os.system('tar zxf ' + filename + ' -C ' + TMP_SETTINGS_PWD)
        os.system('cd ' + TMP_SETTINGS_PWD + ' && find -type f -exec mv {} . \\;')
        return

    def deflateIpk(self, filename):
        try:
            dirsremove(TMP_SETTINGS_PWD)
        except:
            pass

        try:
            os.mkdir(TMP_SETTINGS_PWD)
        except:
            pass

        os.system('cp ' + filename + ' ' + TMP_SETTINGS_PWD + '/tmp.ipk')
        os.system('cd ' + TMP_SETTINGS_PWD + ' && ar -x tmp.ipk')
        os.system('tar zxf ' + TMP_SETTINGS_PWD + '/data.tar.gz -C ' + TMP_SETTINGS_PWD)
        os.system('cd ' + TMP_SETTINGS_PWD + ' && find -type f -exec mv {} . \\;')
        return

    def deflate(self, filename):
        if filename.endswith('.tar.bz2') or filename.endswith('.tbz2') or filename.endswith('.tbz'):
            self.deflatebz(filename)
        elif filename[-7:] == '.tar.gz' or filename[-8:] == '.tgz':
            self.deflateTar(filename)
        elif filename[-4:] == '.ipk':
            self.deflateIpk(filename)
        else:
            return False
        return True


class SL_Settings():

    def __init__(self):
        self.providers = []
        self.providersT = []
        self.services = []
        self.servicesT = []
        return

    def read(self, pwd):
        self.providers = []
        self.services = []
        try:
            f = open(pwd + '/lamedb')
        except Exception as e:
            print e
            return

        while True:
            line = f.readline()
            if line == '':
                return
            line = line.strip()
            if line == 'transponders':
                break

        while True:
            line = f.readline()
            if line == '':
                return
            line = line.strip()
            if line == 'end':
                break
            line2 = f.readline().strip()
            line3 = f.readline().strip()
            self.providers.append([line.split(':'), line2.split(':'), line3.split(':')])

        while True:
            line = f.readline()
            if line == '':
                return
            line = line.strip()
            if line == 'services':
                break

        while True:
            line = f.readline()
            if line == '':
                return
            line = line.strip()
            if line == 'end':
                break
            line2 = f.readline().strip('\n')
            line3 = f.readline().strip('\n')
            self.services.append([line.split(':'), line2.split(':'), line3.split(':')])

        f.close()
        return

    def write(self, pwd):
        try:
            f = open(pwd + '/lamedb', 'w')
        except Exception as e:
            print e
            return

        f.write('eDVB services /4/\n')
        f.write('transponders\n')
        for provider in self.providers:
            f.write((':').join(provider[0]) + '\n')
            f.write('\t' + (':').join(provider[1]) + '\n')
            f.write((':').join(provider[2]) + '\n')

        f.write('end\n')
        f.write('services\n')
        for service in self.services:
            f.write((':').join(service[0]) + '\n')
            f.write((':').join(service[1]) + '\n')
            f.write((':').join(service[2]) + '\n')

        f.write('end\n')
        f.write('Have a lot of bugs!\n')
        f.close()
        return

    def saveTerrestrial(self):
        providersT = []
        servicesT = []
        for provider in self.providers:
            if provider[1][0][:1] == 't':
                providersT.append(provider)

        for service in self.services:
            for provider in providersT:
                if service[0][1] == provider[0][0] and service[0][2] == provider[0][1] and service[0][3] == provider[0][2]:
                    servicesT.append(service)

        self.providersT = providersT
        self.servicesT = servicesT
        return

    def restoreTerrestrial(self):
        tmp = self.providersT
        for provider in self.providers:
            if provider[1][0][:1] != 't':
                tmp.append(provider)

        self.providers = tmp
        tmp = self.servicesT
        for service in self.services:
            if service[0][1][:4] != 'eeee':
                tmp.append(service)

        self.services = tmp
        return

    def readBouquetsTvList(self, pwd):
        return self.readBouquetsList(pwd, 'bouquets.tv')

    def readBouquetsRadioList(self, pwd):
        return self.readBouquetsList(pwd, 'bouquets.radio')

    def readBouquetsList(self, pwd, bouquetname):
        try:
            f = open(pwd + '/' + bouquetname)
        except Exception as e:
            print e
            return

        ret = []
        while True:
            line = f.readline()
            if line == '':
                break
            if line[:8] != '#SERVICE':
                continue
            tmp = line.strip().split(':')
            line = tmp[len(tmp) - 1]
            filename = None
            if line[:12] == 'FROM BOUQUET':
                tmp = line[13:].split(' ')
                filename = tmp[0].strip('"')
            else:
                filename = line
            if filename:
                try:
                    fb = open(pwd + '/' + filename)
                except Exception as e:
                    print e
                    continue

                tmp = fb.readline().strip()
                if tmp[:6] == '#NAME ':
                    ret.append([filename, tmp[6:]])
                else:
                    ret.append([filename, filename])
                fb.close()

        return ret

    def copyBouquetsTv(self, srcpwd, dstpwd, keeplist):
        return self.copyBouquets(srcpwd, dstpwd, 'bouquets.tv', keeplist)

    def copyBouquetsRadio(self, srcpwd, dstpwd, keeplist):
        return self.copyBouquets(srcpwd, dstpwd, 'bouquets.radio', keeplist)

    def copyBouquets(self, srcpwd, dstpwd, bouquetname, keeplist):
        srclist = self.readBouquetsList(srcpwd, bouquetname)
        dstlist = self.readBouquetsList(dstpwd, bouquetname)
        if srclist is None:
            srclist = []
        if dstlist is None:
            dstlist = []
        count = 0
        for item in dstlist:
            if item[0] in keeplist:
                found = False
                for x in srclist:
                    if x[0] == item[0]:
                        found = True
                        break

                if not found:
                    srclist.insert(count, item)
            else:
                os.remove(dstpwd + '/' + item[0])
            count += 1

        for x in srclist:
            if x[0] not in keeplist:
                try:
                    copyfile(srcpwd + '/' + x[0], dstpwd + '/' + x[0])
                except:
                    pass

        try:
            f = open(dstpwd + '/' + bouquetname, 'w')
        except Exception as e:
            print e
            return

        if bouquetname[-3:] == '.tv':
            f.write('#NAME Bouquets (TV)\n')
        else:
            f.write('#NAME Bouquets (Radio)\n')
        for x in srclist:
            if bouquetname[-3:] == '.tv':
                f.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "' + x[0] + '" ORDER BY bouquet\n')
            else:
                f.write('#SERVICE 1:7:2:0:0:0:0:0:0:0:FROM BOUQUET "' + x[0] + '" ORDER BY bouquet\n')

        return

    def apply(self):
        if config.plugins.settingsloader.updatebouquets.value == 'yes':
            print 'ok delete old bq m3'
            copyfile(TMP_SETTINGS_PWD + '/lamedb', ENIGMA2_SETTINGS_PWD + '/lamedb')
            if config.plugins.settingsloader.keepsatellitesxml.value == False:
                print 'ok delete old bq m3'
                copyfile(TMP_SETTINGS_PWD + '/satellites.xml', ENIGMA2_TUXBOX_PWD + '/satellites.xml')
            eDVBDB.getInstance().reloadServicelist()
            eDVBDB.getInstance().reloadBouquets()
            return
        if config.plugins.settingsloader.keepterrestrial.value:
            self.read(ENIGMA2_SETTINGS_PWD)
            self.saveTerrestrial()
            self.read(TMP_SETTINGS_PWD)
            self.restoreTerrestrial()
            self.write(ENIGMA2_SETTINGS_PWD)
            keeplist = config.plugins.settingsloader.keepbouquets.value.split('|')
        else:
            self.read(TMP_SETTINGS_PWD)
            self.write(ENIGMA2_SETTINGS_PWD)
            keeplist = []
        if config.plugins.settingsloader.updatebouquets.value == 'select':
            keeplist = config.plugins.settingsloader.keepbouquets.value.split('|')
        else:
            keeplist = []
        self.copyBouquets(TMP_SETTINGS_PWD, ENIGMA2_SETTINGS_PWD, 'bouquets.tv', keeplist)
        self.copyBouquets(TMP_SETTINGS_PWD, ENIGMA2_SETTINGS_PWD, 'bouquets.radio', keeplist)
        if not config.plugins.settingsloader.keepsatellitesxml.value:
            try:
                copyfile(TMP_SETTINGS_PWD + '/satellites.xml', ENIGMA2_TUXBOX_PWD + '/satellites.xml')
            except Exception as e:
                print e

        if not config.plugins.settingsloader.keepcablesxml.value:
            try:
                copyfile(TMP_SETTINGS_PWD + '/cables.xml', ENIGMA2_TUXBOX_PWD + '/cables.xml')
            except Exception as e:
                print e

        if not config.plugins.settingsloader.keepterrestrialxml.value:
            try:
                copyfile(TMP_SETTINGS_PWD + '/terrestrial.xml', ENIGMA2_TUXBOX_PWD + '/terrestrial.xml')
            except Exception as e:
                print e

        try:
            copyfile(TMP_SETTINGS_PWD + '/whitelist', ENIGMA2_SETTINGS_PWD + '/whitelist')
        except Exception as e:
            print e

        try:
            copyfile(TMP_SETTINGS_PWD + '/blacklist', ENIGMA2_SETTINGS_PWD + '/blacklist')
        except Exception as e:
            print e

        eDVBDB.getInstance().reloadServicelist()
        eDVBDB.getInstance().reloadBouquets()
        return


return
