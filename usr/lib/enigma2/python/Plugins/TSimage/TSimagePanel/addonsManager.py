# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/addonsManager.py
# Compiled at: 2025-09-10 14:58:43
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Components.ActionMap import ActionMap
from Components.AVSwitch import AVSwitch
from Components.Button import Button
from Components.ConfigList import ConfigList, ConfigListScreen
from Components.config import config, ConfigSubsection, ConfigNumber, ConfigSelection, ConfigYesNo, getConfigListEntry, configfile
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.ScrollLabel import ScrollLabel
from Components.Sources.List import List
from Tools.Directories import fileExists, SCOPE_CURRENT_PLUGIN, resolveFilename
from Tools.HardwareInfo import HardwareInfo
from Tools.LoadPixmap import LoadPixmap
from enigma import eTimer, eConsoleAppContainer, ePicLoad, gPixmapPtr, eSize, getDesktop
from twisted.web.client import downloadPage, getPage
from xml.dom import minidom
from os import system as os_system, path as os_path, remove as os_remove
from Plugins.TSimage.TSimagePanel.multInstaller import TSGetMultiipk, TSConsole
from Tools.TSTools import getFreeSpace, getDistroFeed, getHostname, getArch, getDigitVersion, getText, getCmdOutput
from Plugins.SystemPlugins.SoftwareManager.plugin import UpdatePlugin
dpkg_busy_filename = '/tmp/.dpkg_busy'
dpkg_ready_filename = '/tmp/.dpkg_ready'
dpkg_updater_filename = '/tmp/.dpkg_updater'
dpkg_ugradable_filename = '/tmp/.dpkg_ugradable'
dpkg_list_filename = '/tmp/.dpkglist'
dpkg_tmplist_filename = '/tmp/.tmplist'
config.plugins.TSUpdater = ConfigSubsection()
config.plugins.TSUpdater.enable = ConfigYesNo(default=True)
config.plugins.TSUpdater.boot = ConfigYesNo(default=True)
config.plugins.TSUpdater.UpdateAvailable = ConfigNumber(default=0)
config.plugins.TSUpdater.refreshInterval = ConfigSelection(default='24', choices=[33, 34, 31, 35, 36])
NEWS_URL = ''
hostname = getHostname()
distro_feed, debarchname = getDistroFeed(hostname)
boxarch = getArch()
desktopSize = getDesktop(0).size()
import re, os

def _normalize_version(s):
    if not s:
        return ''
    s = s.strip()
    if s.startswith('Version:'):
        s = s[len('Version:'):].strip()
    return s


def _dpkg_compare(v1, op, v2):
    try:
        rc = os.system('dpkg --compare-versions "%s" %s "%s"' % (v1, op, v2))
        return rc == 0
    except Exception:
        return

    return


def _tuple_version(v):
    nums = re.findall('\\d+', v or '')
    return tuple(int(x) for x in nums)


def compare_versions(v_installed, v_feed):
    v1 = _normalize_version(v_installed)
    v2 = _normalize_version(v_feed)
    if not v1 and not v2:
        return 0
    if not v1:
        return -1
    if not v2:
        return 1
    gt = _dpkg_compare(v1, 'gt', v2)
    lt = _dpkg_compare(v1, 'lt', v2)
    eq = _dpkg_compare(v1, 'eq', v2)
    if gt is True:
        return 1
    if lt is True:
        return -1
    if eq is True:
        return 0
    t1, t2 = _tuple_version(v1), _tuple_version(v2)
    if t1 > t2:
        return 1
    if t1 < t2:
        return -1
    return 0


def getipkinfos(ipkfile, ipkversion='', dpkgpack_list=[], dpkgversion_list=[], dpkgdesc_list=[], dpkgdepends_list=[], dpkgstatus_list=[]):
    desciption = 'Description: N/A'
    depends = 'Depends: N/A'
    version = ''
    status = 'install'
    dpkgstatus = 'install'
    metadata = False
    prev = 'N/A'
    s = ipkfile.split('/')
    ipkfile = s[-1] if s else ipkfile
    ipkparts = ipkfile.split('_')
    ipkname = str(ipkparts[0]).strip() if ipkparts else ipkfile
    package = 'Package: %s' % ipkname
    if len(ipkparts) >= 2:
        ipkversion = str(ipkparts[1]).strip()
    else:
        ipkversion = ipkversion or '0'
    for i, pkg in enumerate(dpkgpack_list):
        if ipkname == pkg:
            dpkgstatus = dpkgstatus_list[i] if i < len(dpkgstatus_list) else 'install'
            version = dpkgversion_list[i] if i < len(dpkgversion_list) else ''
            desciption = dpkgdesc_list[i] if i < len(dpkgdesc_list) else 'Description: N/A'
            depends = dpkgdepends_list[i] if i < len(dpkgdepends_list) else 'Depends: N/A'
            break

    if version != '':
        cmpres = compare_versions(version, ipkversion)
        if cmpres == 0 and str(dpkgstatus).startswith('install'):
            status = 'remove'
            version = 'Version: ' + _normalize_version(ipkversion)
        elif cmpres > 0:
            status = 'remove'
            version = 'Version: ' + _normalize_version(version) + ' <-- ' + _normalize_version(ipkversion)
        elif cmpres < 0:
            status = 'update'
            version = 'Version: ' + _normalize_version(version) + ' --> ' + _normalize_version(ipkversion)
        else:
            status = 'install'
            version = 'Version: ' + _normalize_version(ipkversion)
    else:
        version = 'Version: ' + _normalize_version(ipkversion)
    return (package, version, desciption, depends, status, metadata, prev)


class TSAddonsManagerSummary(Screen):
    if '820' in HardwareInfo().get_device_name():
        skin = '<screen position="0,0" size="96,64" id="2">\n    <widget name="text0" position="1,0" size="94,30" font="Regular;13" halign="center" valign="center"/>\n    <eLabel position="2,30" size="92,1" backgroundColor="#e16f00"/>\n    <widget name="text1" position="1,34" size="94,30" font="Regular;12" halign="center" valign="center"/>\n</screen>'
    elif '7080' in HardwareInfo().get_device_name() or 'dmtwo' in HardwareInfo().get_device_name():
        skin = '<screen position="0,0" size="132,64">\n    <widget name="text0" position="6,0" size="120,30" font="Regular;13" halign="center" valign="center"/>\n    <eLabel position="2,30" size="128,1" backgroundColor="white" />\n    <widget name="text1" position="6,34" size="120,30" font="Regular;12" halign="center" valign="center"/>\n</screen>'
    elif '900' in HardwareInfo().get_device_name() or '920' in HardwareInfo().get_device_name():
        skin = '<screen position="0,0" size="400,240" id="3">\n    <ePixmap pixmap="/usr/share/enigma2/skin_default/display_bg.png" position="0,0" size="400,240" zPosition="-1"/>\n    <widget name="text0" position="10,0" size="380,60" font="Display;48" halign="center" valign="center" transparent="1"/>\n    <eLabel position="10,85" size="380,2" backgroundColor="white" />\n    <widget name="text1" position="0,85" size="400,155" font="Display;58" halign="center" valign="center" transparent="1"/>\n</screen>'

    def __init__(self, session, parent):
        Screen.__init__(self, session)
        self['text0'] = Label()
        self['text1'] = Label()
        self.onLayoutFinish.append(self.layoutEnd)
        return

    def layoutEnd(self):
        self['text1'].setText(_('Please wait...'))
        self['text0'].setText(_('Addons Manager'))
        return

    def setText(self, text0, text1, line):
        self['text0'].setText(text0)
        self['text1'].setText(text1)
        return


class TSAddonsSetup(ConfigListScreen, Screen):
    skin_1280 = '<screen name="TSAddonsSetup" position="center,77" size="920,600" title="Addons Manager Setup">\n    <widget name="config" position="20,20" size="880,490" scrollbarMode="showOnDemand" transparent="1" zPosition="1" />\n    <eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff" />\n    <ePixmap name="red" position="70,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" transparent="1" alphatest="blend" />\n    <ePixmap name="green" position="280,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_green.png" transparent="1" alphatest="blend" />\n    <widget name="key_red" position="70,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" />\n    <widget name="key_green" position="280,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" />\n</screen>'
    skin_1920 = '<screen name="TSAddonsSetup" position="center,200" size="1300,720" title="Addons Manager Setup">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png" position="375,640" size="200,40" alphatest="blend" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green-big.png" position="725,640" size="200,40" alphatest="blend" />\n    <widget name="key_red" position="375,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#940d0d" transparent="1" />\n    <widget name="key_green" position="725,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#2d872d" transparent="1" />\n    <widget name="config" position="20,30" size="1260,600" zPosition="2" itemHeight="40" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n</screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session):
        Screen.__init__(self, session)
        self['setupActions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': (self.keySave), 
           'cancel': (self.keyCancel), 
           'red': (self.keyCancel), 
           'green': (self.keySave)}, -2)
        self['key_green'] = Button(_('Save'))
        self['key_red'] = Button(_('Cancel'))
        self.list = []
        ConfigListScreen.__init__(self, self.list, session=self.session)
        self.createSetup()
        self.setTitle(_('Addons Manager Setup'))
        return

    def keyCancel(self):
        self.close(False)
        return

    def checkAptConf(self):
        conf_val = getCmdOutput("cat /etc/apt/apt.conf | grep Install-Recommends | awk '{print$2}'")
        conf_val = conf_val.replace('"', '').replace(';', '')
        if conf_val == '':
            cmd = 'APT::Install-Recommends "true";'
            os_system("echo '" + cmd + "' >> /etc/apt/apt.conf")
            self.installRecommends = ConfigYesNo(default=True)
        elif conf_val == 'false':
            self.installRecommends = ConfigYesNo(default=False)
        elif conf_val == 'true':
            self.installRecommends = ConfigYesNo(default=True)
        return

    def createSetup(self):
        self.list = []
        self.checkAptConf()
        self.list.append(getConfigListEntry(_('Enable software update check at boot time'), config.plugins.TSUpdater.boot))
        self.list.append(getConfigListEntry(_('Enable apt update refresh'), config.plugins.TSUpdater.enable))
        if config.plugins.TSUpdater.enable.value:
            self.list.append(getConfigListEntry(_('apt Updater Refresh Interval [h]'), config.plugins.TSUpdater.refreshInterval))
        self.list.append(getConfigListEntry(_('Enable Install-Recommends Packages'), self.installRecommends))
        self['config'].setList(self.list)
        return

    def keySave(self):
        for x in self['config'].list:
            x[1].save()

        configfile.save()
        if self.installRecommends.value:
            os_system('sed -i \'s/APT::Install-Recommends "false";/APT::Install-Recommends "true";/g\' /etc/apt/apt.conf')
        else:
            os_system('sed -i \'s/APT::Install-Recommends "true";/APT::Install-Recommends "false";/g\' /etc/apt/apt.conf')
        self.close(True)
        return

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.checkListentrys()
        return

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.checkListentrys()
        return

    def checkListentrys(self):
        if self['config'].getCurrent()[1] == config.plugins.TSUpdater.enable:
            self.createSetup()
        return


class ServerGroups(Screen):
    skin_1280 = '<screen name="ServerGroups" position="center,77" size="920,600" title="Addons Manager">\n    <widget source="list" render="Listbox" position="20,15" size="880,352" scrollbarMode="showOnDemand" transparent="1" zPosition="1">\n        <convert type="TemplatedMultiContent">\n            {"template": [\n                MultiContentEntryPixmapAlphaBlend(pos = (2, 2), size = (28, 28), png = 1),\n                MultiContentEntryText(pos = (40, 0), size = (650, 32), font=0, flags = RT_HALIGN_LEFT| RT_VALIGN_CENTER, text = 0)\n            ],\n            "fonts": [gFont("Regular", 22)],\n            "itemHeight": 32}\n        </convert>\n    </widget>\n    <widget name="waiting" position="20,0" zPosition="1" size="880,550" font="Regular;22" transparent="1" halign="center" valign="center" />\n    <widget name="info" position="20,465" zPosition="4" size="880,30" font="Regular;20" transparent="1" halign="left" valign="center" />\n    <widget name="info2" position="20,495" zPosition="4" size="880,30" font="Regular;20" transparent="1" halign="left" valign="center" />\n    <eLabel position="20,460" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff" />\n    <widget name="fspace" position="20,400" zPosition="4" size="880,80" font="Regular;22" foregroundColor="yellow" transparent="1" halign="center" valign="center" />\n    <eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff" />\n    <ePixmap name="red" position="50,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" transparent="1" alphatest="blend" />\n    <ePixmap name="green" position="260,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_green.png" transparent="1" alphatest="blend" />\n    <ePixmap name="yellow" position="470,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_yellow.png" transparent="1" alphatest="blend" />\n    <ePixmap name="blue" position="680,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_blue.png" transparent="1" alphatest="blend" />\n    <widget name="key_red" position="50,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" />\n    <widget name="key_green" position="260,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" />\n    <widget name="key_yellow" position="470,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;20" transparent="1" />\n    <widget name="key_blue" position="680,550" size="150,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" />\n    <widget name="key_info" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_info.png" position="890,540" size="35,25" transparent="1" alphatest="blend" />\n    <ePixmap name="key_menu" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_menu.png" position="840,540" size="35,25" transparent="1" alphatest="blend" />\n</screen>'
    skin_1920 = '<screen name="ServerGroups" position="center,200" size="1300,720" title="Addons Manager">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png" position="50,640" size="200,40" alphatest="blend" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green-big.png" position="360,640" size="200,40" alphatest="blend" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/yellow-big.png" position="670,640" size="200,40" alphatest="blend" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/blue-big.png" position="980,640" size="200,40" alphatest="blend" />\n    <widget name="key_red" position="50,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#940d0d" transparent="1" />\n    <widget name="key_green" position="360,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#2d872d" transparent="1" />\n    <widget name="key_yellow" position="670,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#bba502" transparent="1" />\n    <widget name="key_blue" position="980,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#18188b" transparent="1" />\n    <widget name="key_info" position="1248,636" size="48,48" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_info-big.png" transparent="1" alphatest="blend" />\n    <ePixmap name="key_menu" position="1190,636" size="48,48" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_menu-big.png" transparent="1" alphatest="blend" />\n    <widget name="info" position="40,530" size="1000,40" foregroundColor="foreground" backgroundColor="background" font="Regular;28" valign="center" halign="left" transparent="1" zPosition="1" />\n    <widget name="info2" position="40,570" size="1000,40" foregroundColor="foreground" backgroundColor="background" font="Regular;28" valign="center" halign="left" transparent="1" zPosition="1" />\n    <widget name="waiting" position="20,20" size="1260,600" foregroundColor="foreground" backgroundColor="background" font="Regular;32" valign="center" halign="center" transparent="1" zPosition="1" />\n    <eLabel position="10,520" cornerRadius="40" zPosition="4" size="1280,1" backgroundColor="foreground" />\n    <widget source="list" render="Listbox" position="20,20" size="1260,480" zPosition="2" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background" transparent="1">\n        <convert type="TemplatedMultiContent">\n            {"template": [\n                MultiContentEntryText(pos = (45, 0), size = (1000, 40), flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 0),\n                MultiContentEntryPixmapAlphaBlend(pos = (2, 7), size = (28, 28), png = 1)\n            ],\n            "fonts": [gFont("Regular", 30)],\n            "itemHeight": 40}\n        </convert>\n    </widget>\n</screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session):
        Screen.__init__(self, session)
        self.newsdata = ''
        self.downlIcon = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, 'TSimage/TSimagePanel/buttons/addons.png'))
        self['key_red'] = Button(_('Close'))
        self['key_green'] = Button(_('Upgrade'))
        self['key_yellow'] = Button(_('Server news'))
        self['key_blue'] = Button(_('apt Tools'))
        self['key_info'] = Pixmap()
        self['key_red'].show()
        self['key_green'].hide()
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self['key_info'].hide()
        self['list'] = List([])
        self['info'] = Label(_('Last apt update: N/A'))
        self['info2'] = Label(_('Available update: N/A'))
        self['waiting'] = Label(_('Downloading addons groups, please wait...'))
        self['fspace'] = Label(getFreeSpace())
        self.downloading = False
        self.is_dpkg_busy = False
        self.upgradable_nr = 0
        self.cache = None
        self.error = None
        self['actions'] = ActionMap(['SetupActions', 'EPGSelectActions', 'ColorActions', 'MenuActions'], {'ok': (self.okClicked), 
           'green': (self.dpkgupgrade), 
           'yellow': (self.shownews), 
           'blue': (self.openAptTools), 
           'info': (self.showUpgradableInfo), 
           'menu': (self.updatersetup), 
           'cancel': (self.exitclicked)}, -2)
        self.onShown.append(self.setWindowTitle)
        self['list'].onSelectionChanged.append(self.selectionChanged)
        self.onLayoutFinish.append(self.downloadxmlpage)
        return

    def setWindowTitle(self):
        self.setTitle(_('Addons Manager'))
        return

    def selectionChanged(self):
        if not hasattr(self, 'namesList') or not self.namesList:
            return
        index = self['list'].getIndex()
        if index < 0 or index >= len(self.namesList):
            return
        self.updateOLED(_('Addons Manager'), self.namesList[index][0])
        return

    def createSummary(self):
        return TSAddonsManagerSummary

    def updateOLED(self, text0, text1):
        self.summaries.setText(text0, text1, 1)
        return

    def updatersetup(self):
        self.session.open(TSAddonsSetup)
        return

    def dpkgupgrade(self):
        if not self.upgradable_nr == 0:
            self.session.openWithCallback(self.runUpgrade, MessageBox, _('Do you want to update your Dreambox?') + '\n' + _('\nAfter pressing OK, please wait!'))
        return

    def runUpgrade(self, result):
        if result:
            self.session.open(UpdatePlugin, '/usr/lib/enigma2/python/Plugins')
        return

    def openAptTools(self):
        if self.is_dpkg_busy or os_path.exists(dpkg_busy_filename):
            self.session.open(MessageBox, _('Another apt/dpkg task is running.\nPlease wait for it to finish.'), MessageBox.TYPE_INFO, timeout=4)
            return
        choices = [
         (
          _('apt update'), 'update'),
         (
          _('apt upgrade (-y)'), 'upgrade'),
         (
          _('apt-get -f install (-y)'), 'fix'),
         (
          _('remove cache'), 'clear_lists'),
         (
          _('dpkg --configure -a'), 'dpkg_config')]
        self.session.openWithCallback(self._aptToolPicked, ChoiceBox, title=_('Maintenance / apt tools'), list=choices)
        return

    def _aptToolPicked(self, choice):
        if not choice:
            return
        action = choice[1]

        def _prep_ui(start_text):
            self['key_red'].hide()
            self['key_blue'].hide()
            self['key_green'].hide()
            self['key_info'].hide()
            self.upgradable_nr = 0
            self.is_dpkg_busy = True
            for f in (dpkg_busy_filename,):
                if os_path.exists(f):
                    os_remove(f)

            for f in (dpkg_ready_filename, dpkg_list_filename):
                if os_path.exists(f):
                    os_remove(f)

            self['info'].setText(start_text)
            self['info2'].setText('')
            self.cache = None
            self.error = None
            return

        if action == 'update':
            _prep_ui(_('Starting apt update...'))
            self._runAptCommand('touch %s ; COLUMNS=2000 apt-get update' % dpkg_busy_filename, self._onAptUpdateDone, stream_to_info=True)
            return
        if action == 'upgrade':
            _prep_ui(_('Starting apt upgrade...'))
            self._runAptCommand('touch %s ; COLUMNS=2000 apt-get -y upgrade' % dpkg_busy_filename, self._onGenericAptDone, stream_to_info=True, refresh_lists=True)
            return
        if action == 'fix':
            _prep_ui(_('Running apt-get -f install...'))
            self._runAptCommand('touch %s ; COLUMNS=2000 apt-get -y -f install' % dpkg_busy_filename, self._onGenericAptDone, stream_to_info=True, refresh_lists=True)
            return
        if action == 'clear_lists':
            _prep_ui(_('Clearing /var/lib/apt/lists ...'))
            self._runAptCommand('touch %s ; rm -rf /var/lib/apt/lists/*' % dpkg_busy_filename, self._onClearListsDone, stream_to_info=False)
            return
        if action == 'dpkg_config':
            _prep_ui(_('Running dpkg --configure -a ...'))
            self._runAptCommand('touch %s ; dpkg --configure -a' % dpkg_busy_filename, self._onGenericAptDone, stream_to_info=True, refresh_lists=True)
            return
        return

    def _runAptCommand(self, cmd, done_cb, stream_to_info=True, refresh_lists=False):
        """
        Run an APT/DPKG command in eConsoleAppContainer.
        If stream_to_info=True, reuse cmdData() to live-update info label.
        If refresh_lists=True, we will refresh dpkg list afterward.
        """
        self._refresh_lists_after_cmd = bool(refresh_lists)
        self.container = eConsoleAppContainer()
        self.container_conn = self.container.appClosed.connect(done_cb)
        if stream_to_info:
            self.container_data = self.container.dataAvail.connect(self.cmdData)
        else:
            self.container_data = None
        self.container.execute(cmd)
        return

    def _onAptUpdateDone(self, status):
        self.container_conn = None
        self['info'].setText(_('Saving list of available packages...'))
        self.dpkgList()
        return

    def _onClearListsDone(self, status):
        self.container_conn = None
        if os_path.exists(dpkg_busy_filename):
            os_remove(dpkg_busy_filename)
        self['info'].setText(_('Lists cleared. Starting apt update...'))
        self.dpkgupdate()
        return

    def _onGenericAptDone(self, status):
        self.container_conn = None
        if os_path.exists(dpkg_busy_filename):
            os_remove(dpkg_busy_filename)
        if self._refresh_lists_after_cmd:
            self['info'].setText(_('Refreshing package lists...'))
            self.dpkgList()
        else:
            self['info'].setText(_('Operation completed.'))
            self['key_red'].show()
            self['key_blue'].show()
            self.is_dpkg_busy = False
        return

    def dpkgupdate(self):
        if self.downloading == True and not os_path.exists(dpkg_busy_filename):
            if os_path.exists(dpkg_ready_filename) or not os_path.exists(dpkg_updater_filename):
                self['key_red'].hide()
                self['key_blue'].hide()
                self['key_green'].hide()
                self['key_info'].hide()
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
                self['info'].setText('Starting deb update...')
                self['info2'].setText('')
                self.cache = None
                self.error = None
                self.container = eConsoleAppContainer()
                self.container_conn = self.container.appClosed.connect(self.ondpkgUpdateClose)
                self.container_data = self.container.dataAvail.connect(self.cmdData)
                self.container.execute(cmd)
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
            for mydata in iteration:
                if mydata != '':
                    if mydata.startswith('Ign'):
                        self['info'].setText('Downloading repositories...')
                    elif mydata.startswith('Get'):
                        self['info'].setText('Inflating repositories...')
                    elif mydata.startswith('E:'):
                        self.error = mydata.replace('E:', '').strip()
                        self['info'].setText('error: %s' % self.error)

        return

    def ondpkgUpdateClose(self, status):
        self.container_conn = None
        self['info'].setText('Saving list of available packages...')
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
            cmd = "COLUMNS=2000 apt-opkg list | grep -E 'enigma2-plugin-extensions-|enigma2-plugin-systemplugins-|enigma2-skin-|enigma2-cams-|nodejs-module-|kernel-|exfat|ntfs-|ostende|gemini|gp4|dreamarabia' > " + dpkg_list_filename
            self.container = eConsoleAppContainer()
            self.container_conn = self.container.appClosed.connect(self.ondpkgListClose)
            self.container.execute(cmd)
        return

    def ondpkgListClose(self, status):
        self.container_conn = None
        os_system('touch %s' % dpkg_ready_filename)
        if os_path.exists(dpkg_busy_filename):
            os_remove(dpkg_busy_filename)
        self['info'].setText('Checking for available updates...')
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
        config.plugins.TSUpdater.UpdateAvailable.value = self.upgradable_nr
        config.plugins.TSUpdater.save()
        configfile.save()
        self.getdpkgLastUpdate()
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

    def getfreespace(self):
        self['fspace'].setText(getFreeSpace())
        return

    def shownews(self):
        if self.downloading == True:
            cmd = "echo '%s'" % self.newsdata
            title = 'TSimage_5.0 Feed Updates'
            info = _('Getting feed news, please wait...')
            self.session.open(TSConsole, cmd, title, info)
        return

    def getdpkgLastUpdate(self, retval=None):
        if not os_path.exists(dpkg_ready_filename):
            print '[MultiIpk RessourcesCheck] resources busy...'
            cmd = 'echo\n'
            self.container = eConsoleAppContainer()
            self.container_conn = self.container.appClosed.connect(self.getdpkgLastUpdate)
            self.container.execute(cmd)
        else:
            self.container = eConsoleAppContainer()
            cmd = 'ls -e ' + dpkg_ready_filename + ' | awk \'{printf "%s %s %s %s",$6,$7,$8,$9}\''
            self.container_conn = self.container.appClosed.connect(self.ondpkgLastUpdateClose)
            self.container_data = self.container.dataAvail.connect(self.getData)
            self.container.execute(cmd)
        return

    def ondpkgLastUpdateClose(self, retval=None):
        self.container_conn = None
        self['info2'].setText('Available update: %d package(s)' % config.plugins.TSUpdater.UpdateAvailable.value)
        self.upgradable_nr = config.plugins.TSUpdater.UpdateAvailable.value
        if not self.upgradable_nr == 0:
            self['key_green'].show()
            self['key_info'].show()
        else:
            self['key_green'].hide()
            self['key_info'].hide()
        self['key_red'].show()
        self['key_blue'].show()
        self.is_dpkg_busy = False
        return

    def getData(self, data):
        if data:
            self['info'].setText(_('Last apt update: %s') % data)
        return

    def errorLoadConn(self, error=None):
        if error is not None:
            self['waiting'].setText(str(error.getErrorMessage()))
        return

    def downloadxmlpage(self):
        if NEWS_URL and NEWS_URL.strip():
            try:
                getPage(NEWS_URL).addCallback(self.gotPageLoad).addErrback((lambda _: self.gotPageLoad('')))
            except Exception:
                self.gotPageLoad('')

        else:
            self.gotPageLoad('')
        return

    def gotPageLoad(self, data=None):
        self.newsdata = data or 'No server news available.'
        self.names = []
        self.mainNames = []
        self.namesList = []
        self.namesPicons = []
        self.namesPiconsList = []
        self.names.append('Plugins')
        self.namesList.append(('enigma2 Plugins', self.downlIcon))
        self.names.append('System Plugins')
        self.namesList.append(('System Plugins', self.downlIcon))
        self.names.append('Skins')
        self.namesList.append(('enigma2 Skins', self.downlIcon))
        self.names.append('ostende')
        self.namesList.append(('Ostende Skins', self.downlIcon))
        self.names.append('Dream-Arabia')
        self.namesList.append(('Dream-Arabia Feed', self.downlIcon))
        self.names.append('Gemini')
        self.namesList.append(('Gemini Feed', self.downlIcon))
        self.names.append('Filesystems')
        self.namesList.append(('Filesystems', self.downlIcon))
        self.names.append('Kernel')
        self.namesList.append(('Kernel', self.downlIcon))
        self['key_yellow'].show()
        self['key_blue'].show()
        self['list'].setList(self.namesList)
        self['waiting'].setText('')
        self.downloading = True
        if not os_path.exists(dpkg_ready_filename) and not os_path.exists(dpkg_busy_filename):
            self.dpkgupdate()
        else:
            self.getdpkgLastUpdate()
        return

    def showUpgradableInfo(self):
        if not self.upgradable_nr == 0:
            self.session.open(showUpgradeInfo)
        return

    def exitclicked(self):
        if not self.is_dpkg_busy:
            if os_path.exists(dpkg_busy_filename):
                os_remove(dpkg_busy_filename)
            self.close(True)
        return

    def okClicked(self):
        if self.downloading == True:
            self.mainOkClicked()
        else:
            self.close
        return

    def mainOkClicked(self):
        selection = self['list'].getCurrent()[0]
        if selection == 'enigma2 Plugins':
            self.session.openWithCallback(self.getfreespace, IpkgList, '', selection, True)
        elif selection == 'System Plugins':
            self.session.openWithCallback(self.getfreespace, IpkgList, '', selection, True)
        elif selection == 'Ostende Skins':
            self.session.openWithCallback(self.getfreespace, IpkgList, '', selection, True)
        elif selection == 'enigma2 Skins':
            self.session.openWithCallback(self.getfreespace, IpkgList, '', selection, True)
        elif selection == 'Dream-Arabia Feed':
            self.session.openWithCallback(self.getfreespace, IpkgList, '', selection, True)
        elif selection == 'Gemini Feed':
            self.session.openWithCallback(self.getfreespace, IpkgList, '', selection, True)
        elif selection == 'Filesystems':
            self.session.openWithCallback(self.getfreespace, IpkgList, '', selection, True)
        elif selection == 'Kernel':
            self.session.openWithCallback(self.getfreespace, IpkgList, '', selection, True)
        return


class showUpgradeInfo(Screen):
    skin_1280 = '<screen name="showUpgradeInfo" position="center,77" size="920,600" title="">\n    <widget name="waiting" position="20,15" zPosition="4" size="880,550" font="Regular;22" transparent="1" halign="center" valign="center" />\n    <widget source="upgradeinfo" render="Listbox" position="40,25" size="850,400" scrollbarMode="showOnDemand" transparent="1" zPosition="2">\n        <convert type="TemplatedMultiContent">\n            {"template": [\n                MultiContentEntryText(pos = (70, 0), size = (750, 30), font=0, flags = RT_HALIGN_LEFT, text = 0),\n                MultiContentEntryText(pos = (70, 27), size = (750, 22), font=1, flags = RT_HALIGN_LEFT, text = 1),\n                MultiContentEntryPixmapAlphaTest(pos = (3, 1), size = (48, 48), png = 2)\n            ],\n            "fonts": [gFont("Regular", 24), gFont("Regular", 18)],\n            "itemHeight": 50}\n        </convert>\n    </widget>\n    <eLabel position="20,445" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff" />\n    <widget name="info" position="20,450" zPosition="4" size="880,30" font="Regular;22" foregroundColor="yellow" transparent="1" halign="center" valign="center" />\n    <eLabel position="20,485" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff" />\n    <widget name="fspace" position="20,490" zPosition="4" size="880,30" font="Regular;22" foregroundColor="yellow" transparent="1" halign="center" valign="center" />\n    <eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff" />\n    <ePixmap name="red" position="50,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" transparent="1" alphatest="blend" />\n    <ePixmap name="green" position="260,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_green.png" transparent="1" alphatest="blend" />\n    <widget name="key_red" position="50,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" />\n    <widget name="key_green" position="260,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" />\n</screen>'
    skin_1920 = '<screen name="showUpgradeInfo" position="center,200" size="1300,720" title="Addons Manager">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png" position="375,640" size="200,40" alphatest="blend" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green-big.png" position="725,640" size="200,40" alphatest="blend" />\n    <widget name="key_red" position="375,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#940d0d" transparent="1" />\n    <widget name="key_green" position="725,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#2d872d" transparent="1" />\n    <widget name="info" position="20,560" size="1260,40" foregroundColor="yellow" backgroundColor="background" font="Regular;28" valign="center" halign="center" transparent="1" zPosition="1" />\n    <widget name="waiting" position="20,20" size="1260,600" foregroundColor="foreground" backgroundColor="background" font="Regular;32" valign="center" halign="center" transparent="1" zPosition="1" />\n    <widget source="upgradeinfo" render="Listbox" position="20,20" size="1260,520" zPosition="2" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background" transparent="1">\n        <convert type="TemplatedMultiContent">\n            {"template": [\n                MultiContentEntryText(pos = (65, 0), size = (1000, 40), flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 0),\n                MultiContentEntryText(pos = (65, 40), size = (1000, 25), flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 1),\n                MultiContentEntryPixmapAlphaBlend(pos = (5, 11), size = (48, 48), png = 2)\n            ],\n            "fonts": [gFont("Regular", 28), gFont("Regular", 20)],\n            "itemHeight": 70}\n        </convert>\n    </widget>\n</screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session):
        Screen.__init__(self, session)
        self.upgradeIcon = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/upgrade.png'))
        self['upgradeinfo'] = List([])
        self['key_red'] = Button(_('Back'))
        self['key_green'] = Button(_('Upgrade'))
        self['setupActions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': (self.dpkgupgrade), 
           'cancel': (self.close), 
           'red': (self.close), 
           'green': (self.dpkgupgrade)})
        self['waiting'] = Label('')
        self['info'] = Label('')
        self['fspace'] = Label(getFreeSpace())
        self.onLayoutFinish.append(self.getUpgradeInfo)
        self.onShown.append(self.setWindowTitle)
        return

    def setWindowTitle(self):
        self.setTitle(_('Ugradable packages'))
        return

    def dpkgupgrade(self):
        if not self.upgradable_nr == 0:
            self.session.openWithCallback(self.runUpgrade, MessageBox, _('Do you want to update your Dreambox?') + '\n' + _('\nAfter pressing OK, please wait!'))
        return

    def runUpgrade(self, result):
        if result:
            skin_path = '/usr/lib/enigma2/python/Plugins'
            self.session.open(UpdatePlugin, skin_path)
        return

    def getUpgradeInfo(self):
        if os_path.exists(dpkg_ugradable_filename):
            f = open(dpkg_ugradable_filename, 'r')
            line = 'dummy'
            upgradeList = []
            while line:
                line = f.readline()
                s = line.split(' - ')
                if len(s) == 3:
                    pkgname = s[0].strip()
                    akt_ver = s[1].strip()
                    up_ver = s[2].strip()
                    upgradeList.append((pkgname, akt_ver + ' --> ' + up_ver, self.upgradeIcon))

            f.close()
        else:
            self['waiting'].setText('No upgrade info available !')
        self['upgradeinfo'].setList(upgradeList)
        self.upgradable_nr = len(upgradeList)
        self['info'].setText(_('%d packages available for update') % self.upgradable_nr)
        return


class IpkgList(Screen):
    skin_1280 = '<screen name="IpkgList" position="center,77" size="920,600" title="Addons Manager">\n    <widget source="menu" render="Listbox" position="20,15" size="880,352" scrollbarMode="showOnDemand" transparent="1" zPosition="1">\n        <convert type="TemplatedMultiContent">\n            {"template": [\n                MultiContentEntryPixmapAlphaBlend(pos = (8, 8), size = (16, 16), png = 1),\n                MultiContentEntryText(pos = (35, 0), size = (650, 32), font=0, flags = RT_HALIGN_LEFT| RT_VALIGN_CENTER, text = 0),\n                MultiContentEntryPixmapAlphaBlend(pos = (3, 3), size = (26, 26), png = 2)\n            ],\n            "fonts": [gFont("Regular", 23)],\n            "itemHeight": 32}\n        </convert>\n    </widget>\n    <widget name="waiting" position="20,15" zPosition="4" size="880,416" font="Regular;22" transparent="1" halign="center" valign="center" />\n    <widget name="pkginfo" position="20,415" zPosition="4" size="880,108" font="Regular;18" transparent="1" halign="left" />\n    <eLabel position="20,410" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff" />\n    <widget name="fspace" position="20,350" zPosition="4" size="880,80" font="Regular;22" foregroundColor="yellow" transparent="1" halign="center" valign="center" />\n    <eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff" />\n    <ePixmap name="red" position="50,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" transparent="1" alphatest="blend" />\n    <ePixmap name="green" position="260,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_green.png" transparent="1" alphatest="blend" />\n    <ePixmap name="yellow" position="470,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_yellow.png" transparent="1" alphatest="blend" />\n    <ePixmap name="blue" position="680,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_blue.png" transparent="1" alphatest="blend" />\n    <ePixmap name="infokey" position="840,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_info.png" transparent="1" alphatest="blend" />\n    <eLabel name="key_red" text="Back" position="50,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" />\n    <widget name="key_green" position="260,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" />\n    <widget name="key_yellow" position="470,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;20" transparent="1" />\n    <widget name="key_blue" position="680,550" size="150,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" />\n</screen>'
    skin_1920 = '<screen name="IpkgList" position="center,200" size="1300,720" title="Addons Manager">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png" position="50,640" size="200,40" alphatest="blend" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green-big.png" position="360,640" size="200,40" alphatest="blend" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/yellow-big.png" position="670,640" size="200,40" alphatest="blend" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/blue-big.png" position="980,640" size="200,40" alphatest="blend" />\n    <eLabel name="key_red" text="Back" position="50,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#940d0d" transparent="1" />\n    <widget name="key_green" position="360,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#2d872d" transparent="1" />\n    <widget name="key_yellow" position="670,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#bba502" transparent="1" />\n    <widget name="key_blue" position="980,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#18188b" transparent="1" />\n    <ePixmap name="key_info" position="1190,636" size="48,48" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_info-big.png" transparent="1" alphatest="blend" />\n    <widget name="pkginfo" position="40,490" size="1000,140" foregroundColor="foreground" backgroundColor="background" font="Regular;22" valign="top" halign="left" transparent="1" zPosition="1" />\n    <widget name="fspace" position="20,440" size="1260,40" foregroundColor="yellow" backgroundColor="background" font="Regular;28" valign="center" halign="center" transparent="1" zPosition="1" />\n    <widget name="waiting" position="20,20" size="1260,600" foregroundColor="foreground" backgroundColor="background" font="Regular;32" valign="center" halign="center" transparent="1" zPosition="1" />\n    <eLabel position="10,480" cornerRadius="40" zPosition="4" size="1280,1" backgroundColor="foreground" />\n    <widget source="menu" render="Listbox" position="20,20" size="1260,400" zPosition="2" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background" transparent="1">\n        <convert type="TemplatedMultiContent">\n            {"template": [\n                MultiContentEntryText(pos = (45, 0), size = (1000, 40), flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 0),\n                MultiContentEntryPixmapAlphaBlend(pos = (7, 7), size = (26, 26), png = 1),\n                MultiContentEntryPixmapAlphaBlend(pos = (0, 0), size = (40, 40), png = 2)\n            ],\n            "fonts": [gFont("Regular", 30)],\n            "itemHeight": 40}\n        </convert>\n    </widget>\n</screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session, xmlparse, selection, imagefeed=False):
        self.imagefeed = imagefeed
        Screen.__init__(self, session)
        self.greenStatus = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green.png'))
        self.blueStatus = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/blue.png'))
        self.greyStatus = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/grey.png'))
        self.installIcon = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/install.png'))
        self.removeIcon = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/remove.png'))
        self.updateIcon = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/update.png'))
        self.xmlparse = xmlparse
        self.selection = selection
        self['key_red'] = Button(_('Back'))
        self['key_yellow'] = Button(_('Preview'))
        self['key_blue'] = Button(_('Description'))
        self['key_green'] = Button(_('Execute'))
        self['key_info'] = Button(_('pkg info'))
        self['info'] = Label('')
        self['waiting'] = Label(' ')
        self['pkginfo'] = Label(' ')
        self['fspace'] = Label(getFreeSpace())
        self['menu'] = List([])
        self['actions'] = ActionMap([
         'SetupActions', 'EPGSelectActions'], {'ok': (self.selclicked), 
           'cancel': (self.close), 
           'yellow': (self.preview), 
           'timerAdd': (self.selgreen), 
           'blue': (self.desc), 
           'info': (self.showPkgkInfo)}, -2)
        self['key_green'].hide()
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self.metapreview = False
        self.itempreview = False
        self.itemdes = False
        self.ipklist = []
        self.onShown.append(self.setWindowTitle)
        if os_path.exists(dpkg_busy_filename):
            print '[MultiIpk startRessourcesCheck] resources busy...'
            self.onCheckClose()
        else:
            self.timer = eTimer()
            self.timer_conn = self.timer.timeout.connect(self.createImagefeedIpklist)
            self.timer.start(500, 1)
            self['menu'].onSelectionChanged.append(self.selectionChanged)
        return

    def onCheckClose(self, result=True):
        if os_path.exists(dpkg_busy_filename):
            cmd = 'echo'
            self['info'].setText(' ')
            self['waiting'].setText(_('Updating plugins list, please wait...'))
            self.container = eConsoleAppContainer()
            self.container_conn = self.container.appClosed.connect(self.onCheckClose)
            self.container.execute(cmd)
        else:
            self['waiting'].setText(' ')
            self.timer = eTimer()
            self.timer_conn = self.timer.timeout.connect(self.createImagefeedIpklist)
            self.timer.start(200, 1)
            self['menu'].onSelectionChanged.append(self.selectionChanged)
        return

    def setWindowTitle(self):
        self.setTitle(self.selection)
        if not os_path.exists(dpkg_busy_filename) and len(self.ipklist) > 0:
            self.updateOLED(self.selection, self.ipklist[0][0])
        return

    def createSummary(self):
        return TSAddonsManagerSummary

    def updateOLED(self, text0, text1):
        try:
            self.summaries.setText(text0, text1, 1)
        except Exception:
            pass

        return

    def showPkgkInfo(self):
        if os_path.exists(dpkg_busy_filename) or not os_path.exists(dpkg_ready_filename):
            return
        cindex = self['menu'].getIndex()
        if cindex < 0 or cindex >= len(self.ipklist):
            return
        pkg_name = self.ipklist[cindex][5].replace('Package: ', '')
        cmd = 'COLUMNS=2000 apt-opkg info ' + pkg_name
        info = _('Getting full package info, please wait...')
        title = _('Package info')
        self.session.open(TSConsole, cmd, title, info)
        return

    def createImagefeedIpklist(self):
        self.installList = []
        self.removeList = []
        self.ipklist = []
        self.dpkgpack_list, self.dpkgversion_list, self.dpkgdesc_list, self.dpkgdepends_list, self.dpkgstatus_list = self.createDpkgList()
        sel = (self.selection or '').strip().lower()
        if sel in ('enigma2 plugins', 'plugins'):
            cmd = 'cat ' + dpkg_list_filename + ' | grep "enigma2-plugin-extensions-" | awk \'{printf "%s_%s\\n",$1,$3}\''
            self._runStreamingBuild(cmd, _('Getting %s list, please wait...') % self.selection)
            return
        if sel in ('system plugins', 'systemplugins'):
            cmd = 'cat ' + dpkg_list_filename + ' | grep "enigma2-plugin-systemplugins-" | awk \'{printf "%s_%s\\n",$1,$3}\''
            self._runStreamingBuild(cmd, _('Getting %s list, please wait...') % self.selection)
            return
        if sel in ('enigma2 skins', 'skins', 'ts skins'):
            cmd = 'cat ' + dpkg_list_filename + ' | grep "enigma2-skin-" | awk \'{printf "%s_%s\\n",$1,$3}\' > ' + dpkg_tmplist_filename
            os_system(cmd)
            self.readImagefeedList()
            self['menu'].setList(self.ipklist)
            self.selectionChanged()
            return
        if sel in ('ostende skins', 'ostende'):
            cmd = 'cat ' + dpkg_list_filename + ' | grep -E "^enigma2-skin-.*ostende|^ostende" | awk \'{printf "%s_%s\\n",$1,$3}\' > ' + dpkg_tmplist_filename
            os_system(cmd)
            self.readImagefeedList()
            self['menu'].setList(self.ipklist)
            self.selectionChanged()
            return
        if sel in ('dream-arabia feed', 'dream-arabia', 'dream arabia feed'):
            cmd = 'cat ' + dpkg_list_filename + ' | grep -E "^dreamarabia" | awk \'{printf "%s_%s\\n",$1,$3}\' > ' + dpkg_tmplist_filename
            os_system(cmd)
            self.readImagefeedList()
            self['menu'].setList(self.ipklist)
            self.selectionChanged()
            return
        if sel in ('gemini feed', 'gemini', 'gp4'):
            cmd = 'cat ' + dpkg_list_filename + ' | grep -E "^(gemini|libgemini|packagegroup-gemini|gp4)" | awk \'{printf "%s_%s\\n",$1,$3}\''
            self._runStreamingBuild(cmd, _('Getting %s list, please wait...') % self.selection)
            return
        if sel == 'filesystems':
            cmd = 'cat ' + dpkg_list_filename + ' | grep -E "sshfs|ifuse|exfat|ntfs" | awk \'{printf "%s_%s\\n",$1,$3}\' > ' + dpkg_tmplist_filename
            os_system(cmd)
            self.readImagefeedList()
            self['menu'].setList(self.ipklist)
            self.selectionChanged()
            return
        if sel == 'kernel':
            cmd = 'cat ' + dpkg_list_filename + ' | grep "kernel-" | awk \'{printf "%s_%s\\n",$1,$3}\''
            self._runStreamingBuild(cmd, _('Getting %s list, please wait...') % self.selection)
            return
        self['waiting'].setText(_('No packages found in this category.'))
        self['menu'].setList([])
        return

    def _runStreamingBuild(self, cmd, wait_text):
        self.count = 0
        self.cache = None
        self.container_conn = None
        self.container_data = None
        self['waiting'].setText(wait_text)
        self.container = eConsoleAppContainer()
        self.container_conn = self.container.appClosed.connect(self.ongetIpkgListClose)
        self.container_data = self.container.dataAvail.connect(self.cmdData)
        self.container.execute(cmd)
        return

    def ongetIpkgListClose(self, retval=None):
        self.container_data = None
        self.container_conn = None
        self['waiting'].setText('')
        self['menu'].setList(self.ipklist)
        self.selectionChanged()
        return

    def readImagefeedList(self):
        try:
            fm = open(dpkg_tmplist_filename)
        except IOError:
            self['waiting'].setText(_('No packages found.'))
            self.ipklist = []
            self.count = 0
            return

        line = 'dummy'
        self.ipklist = []
        self.count = 0
        while line:
            line = fm.readline().replace('\n', '')
            if line == '':
                continue
            if line.rfind('dbg') != -1 or line.rfind('dev') != -1:
                continue
            if line.startswith('enigma2-plugin-'):
                self.addIpkg(line, boxarch, 'plugin')
            elif line.startswith('enigma2-skin-'):
                self.addIpkg(line, 'all', 'skin')
            elif line.startswith('nodejs-module-'):
                self.addIpkg(line, 'all', 'nodejs')
            elif line.startswith('kernel-'):
                self.addIpkg(line, hostname, 'kernel')
            elif line.startswith('gemini') or line.startswith('libgemini') or line.startswith('packagegroup-gemini') or line.startswith('gp4'):
                self.addIpkg(line, boxarch, 'plugin')
            elif line.rfind('doc') == -1 and not line.startswith('libntfs') and not line.startswith('ntfsprogs'):
                self.addIpkg(line, boxarch, 'filesystems')

        fm.close()
        return

    def cmdData(self, data):
        if self.cache is None:
            self.cache = data
        else:
            self.cache += data
        if '\n' not in data:
            return
        else:
            splitcache = self.cache.split('\n')
            if self.cache[-1] == '\n':
                iteration = splitcache
                self.cache = None
            else:
                iteration = splitcache[:-1]
                self.cache = splitcache[-1]
            for line in iteration:
                if not line:
                    continue
                if line.rfind('dbg') != -1 or line.rfind('dev') != -1 or line.rfind('-meta') != -1:
                    continue
                if line.startswith('enigma2-plugin-'):
                    self.addIpkg(line, boxarch, 'plugin')
                elif line.startswith('enigma2-skin-'):
                    self.addIpkg(line, 'all', 'skin')
                elif line.startswith('nodejs-module-'):
                    self.addIpkg(line, 'all', 'nodejs')
                elif line.startswith('kernel-'):
                    self.addIpkg(line, hostname, 'kernel')
                elif line.startswith('gemini') or line.startswith('libgemini') or line.startswith('packagegroup-gemini') or line.startswith('gp4'):
                    self.addIpkg(line, boxarch, 'plugin')
                elif line.rfind('doc') == -1 and not line.startswith('libntfs') and not line.startswith('ntfsprogs'):
                    self.addIpkg(line, boxarch, 'filesystems')

            return

    def createDpkgList(self):
        fname = '/var/lib/dpkg/status'
        dpkgList = []
        dpkgVersion = []
        dpkgDepends = []
        dpkgDesc = []
        dpkgStatus = []
        for line in open(fname, 'r').readlines():
            if line.startswith('Package:'):
                if len(dpkgDesc) < len(dpkgList):
                    dpkgDesc.append('Description: N/A')
                if len(dpkgDepends) < len(dpkgList):
                    dpkgDepends.append('Depends:')
                if len(dpkgVersion) < len(dpkgList):
                    dpkgVersion.append('Version:')
                dpkgList.append(line.replace('Package: ', '').strip())
            if line.startswith('Status:'):
                dpkgStatus.append(line.replace('Status: ', '').strip())
            if line.startswith('Version:'):
                dpkgVersion.append(line.replace('Version: ', '').strip())
            if line.startswith('Description:'):
                dpkgDesc.append(line.strip())
            if line.startswith('Depends:'):
                dpkgDepends.append(line.strip())

        return (
         dpkgList, dpkgVersion, dpkgDesc, dpkgDepends, dpkgStatus)

    def addIpkg(self, data, arch, metaprefix):
        sp = data.split('_', 2)
        url = distro_feed + arch.replace('mipsel', debarchname) + '/'
        fullname = url + data + '_' + arch + '.deb'
        ipkversion = str(sp[1]).strip()
        if len(sp) <= 1:
            return
        if sp[1].find(':') != -1:
            idx = sp[1].find(':')
            sp[1] = sp[1][idx + 1:]
            data = sp[0] + '_' + sp[1]
            fullname = url + data + '_' + arch + '.deb'
        pkg, ver, desc, dep, processmode, metadata, prev = getipkinfos(data, ipkversion, self.dpkgpack_list, self.dpkgversion_list, self.dpkgdesc_list, self.dpkgdepends_list, self.dpkgstatus_list)
        if self.count > 0 and pkg == self.ipklist[self.count - 1][5]:
            processmode = 'spring'
        if metaprefix == 'plugin':
            sp[0] = sp[0].replace('enigma2-plugin-extensions-', '')
            sp[0] = sp[0].replace('enigma2-plugin-systemplugins-', '')
        if metaprefix == 'skin':
            sp[0] = sp[0].replace('enigma2-skin-ts-', 'ts-')
            sp[0] = sp[0].replace('enigma2-skin-', '')
        if metaprefix == 'nodejs':
            sp[0] = sp[0].replace('nodejs-module-', '')
        metafilename = '/usr/share/meta/' + metaprefix + '_' + sp[0] + '.xml'
        if os_path.exists(metafilename):
            metadata = True
        item = sp[0].strip()
        if len(item) <= 1 or item in ('-reviewed', 'namev', 'kernel-based'):
            return
        else:
            self.count += 1
            if processmode == 'install':
                self.ipklist.append((item, self.greyStatus, None, processmode, fullname, pkg, ver, desc, dep, metadata, prev))
            elif processmode == 'update':
                self.ipklist.append((item, self.blueStatus, None, processmode, fullname, pkg, ver, desc, dep, metadata, prev))
            elif processmode == 'remove':
                self.ipklist.append((item, self.greenStatus, None, processmode, fullname, pkg, ver, desc, dep, metadata, prev))
            return

    def preview(self):
        if not self.itempreview or os_path.exists(dpkg_busy_filename):
            return
        idx = self['menu'].getIndex()
        if idx < 0 or idx >= len(self.ipklist):
            return
        try:
            urlserver = self.ipklist[idx][10]
            if urlserver and urlserver.endswith('.deb'):
                self.session.open(PreviewScreen, urlserver.replace('.deb', '.jpg'))
        except Exception:
            return

        return

    def checkPreview(self, metafilename):
        try:
            xmlmeta = ''
            preview_url = 'N/A'
            f = open(metafilename, 'r')
            line = 'dummy'
            while line:
                line = f.readline()
                xmlmeta += line

            f.close()
            xmlmeta = xmlmeta.strip()
            xmlmeta = minidom.parseString(xmlmeta)
            infos = xmlmeta.getElementsByTagName('info')
            for info in infos:
                try:
                    screenshot = info.getElementsByTagName('screenshot')[0]
                    preview_url = screenshot.getAttribute('src').encode('utf8').strip() or 'N/A'
                except Exception:
                    preview_url = 'N/A'

        except Exception:
            print '[No preview file !]'
            preview_url = 'N/A'

        return preview_url

    def selectionChanged(self):
        if not self.ipklist:
            self['pkginfo'].setText('')
            self['info'].setText(_('No packages in this category.'))
            return
        cindex = self['menu'].getIndex()
        if cindex < 0 or cindex >= len(self.ipklist):
            return
        pkg = self.ipklist[cindex][5]
        ver = self.ipklist[cindex][6]
        desc = self.ipklist[cindex][7]
        dep = self.ipklist[cindex][8]
        metadata = self.ipklist[cindex][9]
        plugin_name = self.ipklist[cindex][0]
        self.updateOLED(self.selection, plugin_name)
        self['pkginfo'].setText('%s\n%s\n%s\n%s' % (pkg, ver, desc, dep))
        fullname = self.ipklist[cindex][4]
        endstr = fullname[-2:] if len(fullname) >= 2 else ''
        if self.ipklist[cindex][2] is not None:
            self['info'].setText(_('Press OK to select for reset'))
        elif self.ipklist[cindex][1] == self.greyStatus:
            self['info'].setText(_('Press OK to select for install'))
        elif self.ipklist[cindex][1] == self.greenStatus:
            self['info'].setText(_('Press OK to select for remove'))
        elif self.ipklist[cindex][1] == self.blueStatus:
            self['info'].setText(_('Press OK to select for update'))
        self.pngtext = self.ipklist[cindex][3]
        if endstr == '-p':
            self['key_yellow'].show()
            self['key_blue'].hide()
            self.itempreview = True
            self.itemdes = False
            self.metapreview = False
        elif endstr == '-d':
            self['key_yellow'].hide()
            self['key_blue'].show()
            self.itempreview = False
            self.itemdes = True
            self.metapreview = False
        elif endstr == '-b':
            self['key_yellow'].show()
            self['key_blue'].show()
            self.itempreview = True
            self.itemdes = True
            self.metapreview = False
        else:
            self['key_yellow'].hide()
            self['key_blue'].hide()
            self.itempreview = False
            self.itemdes = False
            self.metapreview = False
        sel = (self.selection or '').strip().lower()
        if sel in ('enigma2 plugins', 'plugins', 'system plugins', 'systemplugins'):
            if metadata:
                metafilename = '/usr/share/meta/' + 'plugin_' + plugin_name + '.xml'
                self['key_blue'].show()
                self.metapreview = True
                self.previewChanged(metafilename)
        elif sel in ('enigma2 skins', 'skins', 'ts skins', 'ostende skins', 'ostende'):
            metafilename = '/usr/share/meta/' + 'skin_' + plugin_name + '.xml'
            if metadata:
                self['key_blue'].hide()
                self.metapreview = False
                self.previewChanged(metafilename)
        return

    def previewChanged(self, metafilename):
        cindex = self['menu'].getIndex()
        if cindex < 0 or cindex >= len(self.ipklist):
            return
        prev = self.checkPreview(metafilename)
        if prev != 'N/A':
            self['key_yellow'].show()
            self.ipklist[cindex] = (
             self.ipklist[cindex][0],
             self.ipklist[cindex][1],
             self.ipklist[cindex][2],
             self.ipklist[cindex][3],
             self.ipklist[cindex][4],
             self.ipklist[cindex][5],
             self.ipklist[cindex][6],
             self.ipklist[cindex][7],
             self.ipklist[cindex][8],
             self.ipklist[cindex][9],
             prev)
            self.itempreview = True
        return

    def updateInstall(self, status):
        self['fspace'].setText(getFreeSpace())
        self['key_green'].hide()
        self['menu'].setList([])
        self.timer_conn = self.timer.timeout.connect(self.createImagefeedIpklist)
        self.timer.start(200, 1)
        return

    def updateLists(self):
        self.installNameList = []
        self.removeNameList = []
        self.installList = []
        self.removeList = []
        for idx in range(len(self.ipklist)):
            if self.ipklist[idx][2] in (self.installIcon, self.updateIcon):
                self.installNameList.append(self.ipklist[idx][0])
                self.installList.append(self.ipklist[idx][4])
            elif self.ipklist[idx][2] == self.removeIcon:
                self.removeNameList.append(self.ipklist[idx][0])
                self.removeList.append(self.ipklist[idx][4])

        if self.removeList or self.installList:
            self['key_green'].show()
        else:
            self['key_green'].hide()
        return

    def selgreen(self):
        if os_path.exists(dpkg_busy_filename):
            return
        if self.removeList or self.installList:
            self.session.openWithCallback(self.updateInstall, TSGetMultiipk, self.installNameList, self.removeNameList, self.installList, self.removeList)
        return

    def selclicked(self):
        idx = self['menu'].getIndex()
        if idx < 0 or idx >= len(self.ipklist):
            return
        processmode = self.ipklist[idx][3]
        if processmode == 'install':
            self.ipklist[idx] = (
             self.ipklist[idx][0], self.ipklist[idx][1], self.installIcon, 'remove+', self.ipklist[idx][4], self.ipklist[idx][5], self.ipklist[idx][6], self.ipklist[idx][7], self.ipklist[idx][8], self.ipklist[idx][9], self.ipklist[idx][10])
            self['info'].setText(_('Press OK to select for reset'))
        elif processmode == 'remove':
            self.ipklist[idx] = (
             self.ipklist[idx][0], self.ipklist[idx][1], self.removeIcon, 'install+', self.ipklist[idx][4], self.ipklist[idx][5], self.ipklist[idx][6], self.ipklist[idx][7], self.ipklist[idx][8], self.ipklist[idx][9], self.ipklist[idx][10])
            self['info'].setText(_('Press OK to select for reset'))
        elif processmode == 'update':
            self.ipklist[idx] = (
             self.ipklist[idx][0], self.ipklist[idx][1], self.updateIcon, 'update+', self.ipklist[idx][4], self.ipklist[idx][5], self.ipklist[idx][6], self.ipklist[idx][7], self.ipklist[idx][8], self.ipklist[idx][9], self.ipklist[idx][10])
            self['info'].setText(_('Press OK to select for remove'))
        elif processmode == 'update+':
            self.ipklist[idx] = (
             self.ipklist[idx][0], self.ipklist[idx][1], self.removeIcon, 'update++', self.ipklist[idx][4], self.ipklist[idx][5], self.ipklist[idx][6], self.ipklist[idx][7], self.ipklist[idx][8], self.ipklist[idx][9], self.ipklist[idx][10])
            self['info'].setText(_('Press OK to select for reset'))
        elif processmode == 'install+':
            self.ipklist[idx] = (
             self.ipklist[idx][0], self.ipklist[idx][1], None, 'remove', self.ipklist[idx][4], self.ipklist[idx][5], self.ipklist[idx][6], self.ipklist[idx][7], self.ipklist[idx][8], self.ipklist[idx][9], self.ipklist[idx][10])
            self['info'].setText(_('Press OK to select for remove'))
        elif processmode == 'remove+':
            self.ipklist[idx] = (
             self.ipklist[idx][0], self.ipklist[idx][1], None, 'install', self.ipklist[idx][4], self.ipklist[idx][5], self.ipklist[idx][6], self.ipklist[idx][7], self.ipklist[idx][8], self.ipklist[idx][9], self.ipklist[idx][10])
            self['info'].setText(_('Press OK to select for install'))
        elif processmode == 'update++':
            self.ipklist[idx] = (
             self.ipklist[idx][0], self.ipklist[idx][1], None, 'update', self.ipklist[idx][4], self.ipklist[idx][5], self.ipklist[idx][6], self.ipklist[idx][7], self.ipklist[idx][8], self.ipklist[idx][9], self.ipklist[idx][10])
            self['info'].setText(_('Press OK to select for update'))
        self.updateLists()
        self['menu'].updateList(self.ipklist)
        return

    def desc(self):
        if not self.metapreview:
            return
        idx = self['menu'].getIndex()
        if idx < 0 or idx >= len(self.ipklist):
            return
        pluginname = self.ipklist[idx][0]
        self.session.open(metaDescScreen, pluginname)
        return


class metaDescScreen(Screen):
    skin_1280 = '<screen name="metaDescScreen" position="center,77" size="920,600" title="">\n    <widget name="pkgname" position="30,10" size="530,35" font="Regular;28" transparent="1" zPosition="2" />\n    <widget name="author" position="30,45" size="530,30" font="Regular;22" transparent="1" zPosition="2" />\n    <widget name="desc" position="30,78" size="530,540" font="Regular;24" transparent="1" zPosition="2" />\n    <widget name="preview" position="580,10" size="320,256" transparent="1" zPosition="2" alphatest="blend" />\n</screen>'
    skin_1920 = '<screen name="metaDescScreen" position="center,200" size="1300,720" title="TS Console">\n    <widget name="pkgname" position="20,15" zPosition="4" size="1260,50" font="Regular;30" transparent="1" halign="left" valign="center" />\n    <widget name="author" position="20,55" zPosition="4" size="1260,30" font="Regular;22" transparent="1" halign="left" valign="center" />\n    <widget name="desc" position="20,90" size="780,530" zPosition="2" font="Regular;28" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n    <widget name="preview" position="830,10" size="450,360" transparent="1" zPosition="2" alphatest="blend" />\n</screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session, pluginname):
        Screen.__init__(self, session)
        self.pluginname = pluginname
        self['pkgname'] = Label('')
        self['author'] = Label('')
        self['desc'] = Label('')
        self['preview'] = Pixmap()
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': (self.close), 'cancel': (self.close), 'red': (self.close)}, -1)
        self.timer = eTimer()
        self.timer_conn = self.timer.timeout.connect(self.downloadxmlmeta)
        self.timer.start(200, 1)
        self.picload = ePicLoad()
        self.picload_conn = self.picload.PictureData.connect(self.showPic)
        self.onLayoutFinish.append(self.setConf)
        self.onShown.append(self.setWindowTitle)
        return

    def setWindowTitle(self):
        self.setTitle(_('Description'))
        return

    def handleToc(self, infos):
        for info in infos:
            author = info.getElementsByTagName('author')[0]
            author_str = 'author: %s' % getText(author.childNodes)
            author_str = author_str.encode('utf8').strip()
            try:
                desc = info.getElementsByTagName('description')[0]
            except:
                desc = info.getElementsByTagName('shortdescription')[0]

            desc_str = '%s' % getText(desc.childNodes).encode('utf8')
            sp = desc_str.split('\n')
            desc_str = ''
            for i in range(len(sp)):
                desc_str = desc_str + sp[i].strip()

            name = info.getElementsByTagName('name')[0]
            name_str = getText(name.childNodes)
            name_str = name_str.encode('utf8').strip()
            try:
                screenshot = info.getElementsByTagName('screenshot')[0]
                screenshot_str = screenshot.getAttribute('src').encode('utf8').strip()
                if screenshot_str == '':
                    screenshot_str = 'N/A'
            except:
                screenshot_str = 'N/A'

            return (
             name_str, author_str, desc_str, screenshot_str)

        return

    def downloadxmlmeta(self):
        try:
            metafilename = '/usr/share/meta/' + 'plugin_' + self.pluginname + '.xml'
            xmlmeta = ''
            f = open(metafilename, 'r')
            line = 'dummy'
            while line:
                line = f.readline()
                xmlmeta = xmlmeta + line

            f.close()
            xmlmeta = xmlmeta.strip()
            xmlmeta = minidom.parseString(xmlmeta)
            infos = xmlmeta.getElementsByTagName('info')
            name, author, desc, preview_url = self.handleToc(infos)
            self['pkgname'].setText(name)
            self['author'].setText(author)
            self['desc'].setText(desc)
            self.preview_path = '/tmp/plugin_preview.jpg'
            downloadPage(preview_url, self.preview_path).addCallback(self.getPreview).addErrback(self.errorload)
        except:
            print '[No metadata file !]'
            self['pkgname'].setText('')
            self['author'].setText('')
            self['desc'].setText('')
            self['desc'].setText('')

        return

    def getPreview(self, data):
        if os_path.exists(self.preview_path):
            self.picload.startDecode(self.preview_path)
        return

    def setConf(self):
        self['preview'].instance.setPixmap(gPixmapPtr())
        self['preview'].hide()
        sc = AVSwitch().getFramebufferScale()
        self._aspectRatio = eSize(sc[0], sc[1])
        self._scaleSize = self['preview'].instance.size()
        params = (self._scaleSize.width(), self._scaleSize.height(), sc[0], sc[1], False, 1, '#00000000')
        self.picload.setPara(params)
        return

    def showPic(self, picInfo=''):
        self.timer.stop()
        self.timer_conn = None
        ptr = self.picload.getData()
        if ptr != None:
            self['preview'].instance.setPixmap(ptr)
            self['preview'].show()
        return

    def errorload(self, error):
        print '[Plugin preview]:', error
        return


class PreviewScreen(Screen):
    skin_1280 = '<screen name="PreviewScreen" position="center,center" size="1280,720" title=" " flags="wfNoBorder">\n    <widget name="myPic" position="0,0" size="1280,720" zPosition="1" alphatest="blend" />\n    <widget name="info" position="0,0" zPosition="4" size="1280,720" font="Regular;24" backgroundColor="background" foregroundColor="foreground" halign="center" valign="center" transparent="1" />\n</screen>'
    skin_1920 = '<screen name="PreviewScreen" position="0,0" size="1920,1080" title="Preview" flags="wfNoBorder">\n    <widget name="myPic" position="0,0" size="1920,1080" zPosition="1" alphatest="blend" />\n    <widget name="info" position="0,0" zPosition="4" size="1920,1080" font="Regular;32" backgroundColor="background" foregroundColor="foreground" halign="center" valign="center" transparent="1" />\n</screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session, url=None):
        Screen.__init__(self, session)
        self.setTitle(_('Preview'))
        self.url = url
        self.path = '/tmp/addons_preview.jpg'
        self.Scale = AVSwitch().getFramebufferScale()
        self['myPic'] = Pixmap()
        self['info'] = Label()
        self['myActionMap'] = ActionMap(['SetupActions'], {'ok': (self.cancel), 'cancel': (self.cancel)}, -1)
        self['info'].setText(_('Downloading preview, please wait..\n press exit to cancel'))
        self.PicLoad = ePicLoad()
        self.PicLoad_conn = self.PicLoad.PictureData.connect(self.DecodePicture)
        self.onLayoutFinish.append(self.download)
        return

    def download(self):
        downloadPage(self.url, self.path).addCallback(self.downloadDone).addErrback(self.downloadError)
        return

    def downloadError(self, error):
        print '[PreviewScreen]: download Error', error
        self['info'].setText('Download Failure: preview not available !\n press OK to exit')
        return

    def downloadDone(self, status):
        self.ShowPicture()
        return

    def ShowPicture(self):
        if fileExists(self.path):
            self.PicLoad.setPara([self['myPic'].instance.size().width(),
             self['myPic'].instance.size().height(),
             self.Scale[0],
             self.Scale[1],
             0,
             1,
             'background'])
            self.PicLoad.startDecode(self.path)
        return

    def DecodePicture(self, PicInfo=''):
        if fileExists(self.path):
            self['info'].setText('')
            ptr = self.PicLoad.getData()
            self['myPic'].instance.setPixmap(ptr)
        return

    def cancel(self):
        if fileExists(self.path):
            os_remove(self.path)
        self.close(None)
        return


return
