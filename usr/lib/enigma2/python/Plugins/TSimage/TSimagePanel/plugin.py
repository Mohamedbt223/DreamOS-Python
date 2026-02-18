# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/plugin.py
# Compiled at: 2025-09-17 11:40:03
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Plugins.Plugin import PluginDescriptor
from Tools.HardwareInfo import HardwareInfo
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from Tools import Notifications
from enigma import ePicLoad, getDesktop
from Tools.LoadPixmap import LoadPixmap
from Screens.Standby import TryQuitMainloop, inTryQuitMainloop
from Components.Pixmap import Pixmap, MovingPixmap
from Components.ActionMap import ActionMap
from Components.Sources.StaticText import StaticText
from Components.AVSwitch import AVSwitch
from Components.Sources.List import List
from Components.Label import Label
import os
from Tools.Directories import createDir, pathExists
from os import environ, listdir, popen as os_popen, system as os_system, path as os_path, remove as os_remove
from Components.config import config, configfile, ConfigYesNo
from GlobalActions import globalActionMap
from keymapparser import readKeymap
from Tools.TSTools import getCmdOutput
from Components.TSUpdater import TSUpdater
from Plugins.TSimage.CamsManager.plugin import TSSoftcamsManager
from addonsManager import ServerGroups
from Screens.HarddiskSetup import HarddiskDriveSelection
from filesexplorer import FileExplorerII
from Plugins.TSimage.TSimageSetup.Setup import TSSkinSetup
from feeds import TSFeedScreenList
from epgSetup import TSEpgSetup, EPGdbBackupAutoStartTimer
from Plugins.SystemPlugins.SkinSelector.plugin import SkinSelector
from Screens.About import About
from TSInfos.TSGeneralInfo import TSGeneralInfo
from TSInfos.TSDevicesInfo import TSDevicesInfo
from TSInfos.TSKernelModules import TSKernelModules
from TSInfos.TSProcessList import TSProcessList
from TSInfos.TSMounts import TSMounts
from TSInfos.TSShowSettings import TSShowSettings
from TSInfos.TSCustomCmd import TSCustomCmd
from Stools.uninstaller import TSiMenuscrn
from Stools.SetBackupRestore import TSBackupSettings
from Stools.setloader import TSiServersScreen
from Stools.TSsatEditor.satedithd import SatellitesEditor
from Stools.ScreenGrabber.ScreenGrabber import TSiScreenGrabberSetup, TSiScreenGrabberView
from Stools.languageone import TSilangScreen
from Stools.swap import TSiswapScreen
from Stools.cronmanager import TSiCronScreen
from Components.Language import language
import gettext
from Components.config import ConfigYesNo
if os_path.exists('/usr/lib/enigma2/python/Plugins/Extensions/PluginSort/plugin.pyo'):
    from Plugins.Extensions.PluginSort.plugin import SortingPluginBrowser as PluginBrowser
else:
    from Screens.PluginBrowser import PluginBrowser
try:
    _ = config.plugins.TSPanel
except Exception:
    pass

if not hasattr(config.plugins.TSPanel, 'autostartCam'):
    config.plugins.TSPanel.autostartCam = ConfigYesNo(default=True)

def _(txt):
    t = gettext.dgettext('TSimagePanel', txt)
    if t == txt:
        t = gettext.gettext(txt)
    return t


desktopSize = getDesktop(0).size()
Notifications.notificationQueue.registerDomain('AddonsManager', _('Addons manager'), Notifications.ICON_TIMER)
Notifications.notificationQueue.registerDomain('TSPanel', _('Switch type'), Notifications.ICON_TIMER)
tsupdater = None
EPGdbBackupautoStartTimer = None
DEFAULT_ICONSPATH = '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/panelbuttons/'
DEFAULT_FRAMEPATH = '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/'
SKIN_ICONSPATH = '/usr/share/enigma2/' + config.skin.primary_skin.value.replace('skin.xml', 'tsimage/icons/')
DEFAULT_MENUPATH = '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/menu/'
SKIN_MENUPATH = '/usr/share/enigma2/' + config.skin.primary_skin.value.replace('skin.xml', 'tsimage/menu/')
TSPANEL_LABELS = [_('Softcams'),
 _('Addons'),
 _('Tools'),
 _('Device manager'),
 _('Files explorer'),
 _('TSimage setup'),
 _('Information'),
 _('RSS reader'),
 _('EPG setup')]
TSPANEL_ICONS = [77, 
 78, 
 79, 
 80, 
 81, 
 82, 
 83, 
 84, 
 85]
TSINFOS_LABELS = [_('Image information'),
 _('General Info'),
 _('Devices Info'),
 _('Kernel Modules'),
 _('Process List'),
 _('Mountpoints'),
 _('E2 Settings'),
 _('Custom Script'),
 _('About')]
TSINFOS_ICONS = [95, 
 96, 
 97, 
 98, 
 99, 
 100, 
 101, 
 102, 
 103]
TSTOOLS_LABELS = [_('Uninstaller'),
 _('Flash & Backup'),
 _('Settings backup'),
 _('Settings loader'),
 _('Satellites manager'),
 _('Screen grabber'),
 _('Language manager'),
 _('Swap manager'),
 _('Cron manager')]
TSTOOLS_ICONS = [113, 
 114, 
 115, 
 116, 
 117, 
 118, 
 119, 
 120, 
 121]
_cam_autostart_timer = None

def _read_last_cam_name():
    try:
        with open('/etc/clist.list', 'r') as f:
            return f.read().strip()
    except Exception:
        return

    return


def _read_last_cam_script_hint():
    try:
        with open('/etc/lastcam.script', 'r') as f:
            s = f.read().strip()
            if s:
                return s
            return
    except Exception:
        return

    return


def _osd_of_script(fpath):
    try:
        with open(fpath, 'r') as fh:
            for line in fh:
                s = line.strip()
                if not s.startswith('OSD'):
                    continue
                parts = s.split('=', 1)
                if len(parts) != 2:
                    continue
                val = parts[1].strip().strip('"').strip("'")
                return val

    except Exception:
        pass

    return


def _normalize_name(s):
    return ('').join(ch for ch in s.lower() if ch.isalnum())


def _find_cam_script(target_name):
    path = '/usr/script/cam/'
    try:
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    except Exception:
        files = []

    hint = _read_last_cam_script_hint()
    if hint and hint in files:
        return hint
    for fname in files:
        fpath = os.path.join(path, fname)
        osd = _osd_of_script(fpath)
        if osd and osd == target_name:
            return fname

    tn = _normalize_name(target_name or '')
    best = None
    for fname in files:
        base = os.path.splitext(fname)[0]
        if tn and (tn in _normalize_name(base) or _normalize_name(base) in tn):
            best = fname
            break
        osd = _osd_of_script(os.path.join(path, fname))
        if osd and (tn in _normalize_name(osd) or _normalize_name(osd) in tn):
            best = fname
            break

    return best


_cam_t_stop = None
_cam_t_start = None
_cam_ctx = {'last': None, 'script': None}

def _start_with_verbs(fpath, last, verbs=(
 'cam_up', 'start', 'cam_res', 'restart')):
    for verb in verbs:
        rc = os_system('%s %s >/dev/null 2>&1' % (fpath, verb))
        if rc == 0:
            print "[TSPanel] cam start OK via '%s' (last=%s)" % (verb, last)
            return True

    return False


def _stop_with_verbs(fpath):
    for verb in ('cam_down', 'stop', 'cam_kill'):
        rc = os_system('%s %s >/dev/null 2>&1' % (fpath, verb))
        if rc == 0:
            print "[TSPanel] cam stop OK via '%s'" % verb
            return True

    return False


def _stop_fallback_initd():
    for svc in ('softcam', 'oscam', 'ncam', 'gcam'):
        initd = '/etc/init.d/%s' % svc
        if os_path.exists(initd):
            os_system('%s stop >/dev/null 2>&1' % initd)
            print '[TSPanel] cam stop via %s' % initd
            return True

    return False


def _start_fallback_initd():
    for svc in ('softcam', 'oscam', 'ncam', 'gcam'):
        initd = '/etc/init.d/%s' % svc
        if os_path.exists(initd):
            os_system('%s start >/dev/null 2>&1 &' % initd)
            print '[TSPanel] cam start via %s' % initd
            return True

    return False


def _cam_stop_phase():
    """Timer callback #1: resolve script, STOP it, then arm START timer."""
    global _cam_ctx
    global _cam_t_start
    last = _read_last_cam_name()
    if not last or not last.strip():
        print '[TSPanel] No last cam recorded; skipping autostart'
        return
    else:
        script = _find_cam_script(last.strip())
        if not script:
            print "[TSPanel] Could not map last cam '%s' to a script; trying init.d stop" % last
            if not _stop_fallback_initd():
                print '[TSPanel] stop fallback failed; aborting'
                return
            _cam_ctx['last'], _cam_ctx['script'] = last, None
        else:
            fpath = '/usr/script/cam/%s' % script
            try:
                if not os.access(fpath, os.X_OK):
                    os.chmod(fpath, 493)
            except Exception:
                pass

            if not _stop_with_verbs(fpath):
                if not _stop_fallback_initd():
                    print '[TSPanel] stop verbs/init.d failed for script=%s' % script
            _cam_ctx['last'], _cam_ctx['script'] = last, script
        try:
            from enigma import eTimer
            t2 = eTimer()
            try:
                t2.timeout.connect(_cam_start_phase)
            except Exception:
                t2.callback.append(_cam_start_phase)

            t2.start(1500, True)
            _cam_t_start = t2
            print '[TSPanel] Armed cam START in 1500 ms (last=%s, script=%s)' % (_cam_ctx['last'], _cam_ctx['script'])
        except Exception as e:
            print '[TSPanel] Failed to arm START phase: %s' % e

        return


def _cam_start_phase():
    """Timer callback #2: START the cam (script verbs first, then init.d)."""
    last, script = _cam_ctx.get('last'), _cam_ctx.get('script')
    if not last:
        print '[TSPanel] START phase: no context; abort'
        return
    if script:
        fpath = '/usr/script/cam/%s' % script
        try:
            if not os.access(fpath, os.X_OK):
                os.chmod(fpath, 493)
        except Exception:
            pass

        if _start_with_verbs(fpath, last):
            return
        print '[TSPanel] start verbs failed for script=%s; trying init.d' % script
    if _start_fallback_initd():
        return
    print '[TSPanel] Autostart cam FAILED (last=%s, script=%s)' % (last, script)
    return


def _schedule_cam_autostart(delay_ms=12000):
    """Public entry: schedules STOP phase; START is chained automatically."""
    global _cam_t_stop
    try:
        from enigma import eTimer
        t = eTimer()
        try:
            t.timeout.connect(_cam_stop_phase)
        except Exception:
            t.callback.append(_cam_stop_phase)

        t.start(delay_ms, True)
        _cam_t_stop = t
        print '[TSPanel] Scheduled cam STOP→START in %d ms' % delay_ms
    except Exception as e:
        print '[TSPanel] Failed to schedule cam autostart: %s' % e

    return


class TSPanelSummary(Screen):
    if '820' in HardwareInfo().get_device_name():
        skin = '\n        <screen position="0,0" size="96,64" id="2">\n            <widget name="text0" position="1,0" size="94,30" font="Regular;13" halign="center" valign="center"/>\n            <eLabel position="2,30" size="92,1" backgroundColor="#e16f00"/>\n            <widget name="text1" position="1,34" size="94,30" font="Regular;14" halign="center" valign="center"/>\n        </screen>\n        '
    elif '7080' in HardwareInfo().get_device_name():
        skin = '\n        <screen position="0,0" size="132,64">\n            <widget name="text0" position="6,0" size="120,30" font="Regular;13" halign="center" valign="center"/>\n            <eLabel position="2,30" size="128,1" backgroundColor="white"/>\n            <widget name="text1" position="6,34" size="120,30" font="Regular;14" halign="center" valign="center"/>\n        </screen>\n        '
    elif 'two' in HardwareInfo().get_device_name():
        skin = '<screen position="0,0" size="264,128">\n            <widget name="text0" position="6,0" size="252,30" font="Regular;17" halign="center" valign="center"/>\n            <eLabel position="2,30" size="260,1" backgroundColor="white"/>\n            <widget name="text1" position="6,34" size="252,30" font="Regular;14" halign="center" valign="center"/>\n        </screen>\n        '
    elif '900' in HardwareInfo().get_device_name() or '920' in HardwareInfo().get_device_name():
        skin = '<screen position="0,0" size="400,240" id="3">\n            <ePixmap pixmap="/usr/share/enigma2/skin_default/display_bg.png" position="0,0" size="400,240" zPosition="-1"/>\n            <widget name="text0" position="10,0" size="380,75" font="Display;48" halign="center" valign="center" transparent="1"/>\n            <eLabel position="10,85" size="380,2" backgroundColor="white"/>\n            <widget name="text1" position="0,85" size="400,155" font="Display;58" halign="center" valign="center" transparent="1"/>\n        </screen>\n        '

    def __init__(self, session, parent):
        Screen.__init__(self, session)
        self['text0'] = Label('')
        self['text1'] = Label('')
        return

    def setText(self, text, line=1):
        if line == 0:
            self['text0'].setText(text)
        elif line == 1:
            self['text1'].setText(text)
        return


class TSPanelList(Screen):
    skin_1280 = '<screen name="TSPanelList" position="center,center" title="TSimage Panel" size="380,470">\n        <widget source="list" render="Listbox" position="10,10" size="360,450" scrollbarMode="showOnDemand" enableWrapAround="1" transparent="1">\n            <convert type="TemplatedMultiContent">\n                {"templates":\n                    {"default": (50,[\n                        MultiContentEntryText(pos=(70,0), size=(280,50), font=0, flags=RT_HALIGN_LEFT|RT_VALIGN_CENTER, text=1),\n                        MultiContentEntryPixmapAlphaBlend(pos=(10,5), size=(40,40), png=0)\n                    ])},\n                 "fonts": [gFont("Regular",25)],\n                 "itemHeight": 50\n                }\n            </convert>\n        </widget>\n    </screen>\n    '
    skin_1920 = '<screen name="TSPanelList" position="center,200" size="1300,720" title="TSPanel">\n        <widget source="list" render="Listbox" enableWrapAround="1" position="20,20" size="820,605" zPosition="1" foregroundColor="foreground" backgroundColor="background" scrollbarMode="showNever" transparent="1">\n            <convert type="TemplatedMultiContent">\n                {"template": [ MultiContentEntryText(pos=(20,7), size=(645,40), flags=RT_HALIGN_LEFT, text=1) ],\n                 "fonts": [gFont("Regular",34)],\n                 "itemHeight": 55\n                }\n            </convert>\n        </widget>\n\n        <widget source="list" render="Listbox" position="945,160" size="250,250" zPosition="1" foregroundColor="foreground" backgroundColor="background" selectionDisabled="1" scrollbarMode="showNever" transparent="1">\n            <convert type="TemplatedMultiContent">\n                {"template": [ MultiContentEntryPixmapAlphaBlend(pos=(0,0), size=(250,250), png=0) ],\n                 "fonts": [gFont("Regular",34)],\n                 "itemHeight": 250\n                }\n            </convert>\n        </widget>\n\n        <widget source="global.CurrentTime" render="Label" position="840,50" size="460,70" font="Regular;65" halign="center" foregroundColor="foreground" backgroundColor="background" transparent="1">\n            <convert type="ClockToText">Default</convert>\n        </widget>\n\n        <widget source="session.CurrentService" render="Label" position="850,480" size="440,100" font="Regular;38" halign="center" foregroundColor="foreground" backgroundColor="background" transparent="1">\n            <convert type="ServiceName">Name</convert>\n        </widget>\n    </screen>\n    '
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session, title='TS Panel', labelsList=TSPANEL_LABELS, iconsnameList=TSPANEL_ICONS, startindex=0):
        Screen.__init__(self, session)
        self.labelsList = labelsList or []
        self.iconsnameList = iconsnameList or []
        self.title = title or 'TS Panel'
        self.startindex = int(startindex or 0)
        self.setTitle(self.title)
        if self.title in ('TS Panel', 'TSimage Panel', 'TSPanel'):
            self.openSelected = self.openSelected_main
        elif self.title == 'TS Infos':
            self.openSelected = self.openSelected_info
        elif self.title == 'TS Tools':
            self.openSelected = self.openSelected_tools
        else:
            self.openSelected = self.openSelected_main
        self['actions'] = ActionMap([
         'SetupActions'], {'cancel': (self.quit), 'ok': (self.openSelected)}, -2)
        l = []
        count = min(len(self.labelsList), len(self.iconsnameList))
        for idx in range(count):
            l.append(self.buildListEntry(self.labelsList[idx], self.iconsnameList[idx]))

        self['list'] = List(l)
        self['list'].onSelectionChanged.append(self.selectionChanged)
        self.onLayoutFinish.append(self.setIndex)
        self.onShow.append(self.updateSummaries)
        return

    def updateSummaries(self):
        if hasattr(self, 'summaries'):
            self.summaries.setText(self.title, 0)
            cur = self['list'].getCurrent()
            if cur:
                self.summaries.setText(cur[1], 1)
        return

    def selectionChanged(self):
        if hasattr(self, 'summaries'):
            cur = self['list'].getCurrent()
            if cur:
                self.summaries.setText(cur[1], 1)
        return

    def setIndex(self):
        self['list'].setIndex(self.startindex)
        return

    def buildListEntry(self, description, image):
        if os_path.exists(SKIN_MENUPATH + image):
            pixmap = LoadPixmap(cached=True, path='%s%s' % (SKIN_MENUPATH, image))
        else:
            pixmap = LoadPixmap(cached=True, path='%s%s' % (DEFAULT_MENUPATH, image))
        return (
         pixmap, description)

    def openSelected_main(self):
        index = self['list'].getIndex()
        if index == 0:
            self.session.open(TSSoftcamsManager)
        elif index == 1:
            self.session.openWithCallback(self.checkAddonsRestart, ServerGroups)
        elif index == 2:
            self.session.openWithCallback(self.onTSToolsClose, TSPanelList, 'TS Tools', TSTOOLS_LABELS, TSTOOLS_ICONS)
        elif index == 3:
            self.session.open(HarddiskDriveSelection)
        elif index == 4:
            self.session.open(FileExplorerII)
        elif index == 5:
            self.session.openWithCallback(self.checkSetupRestart, TSSkinSetup)
        elif index == 6:
            self.session.open(TSPanelList, 'TS Infos', TSINFOS_LABELS, TSINFOS_ICONS)
        elif index == 7:
            self.session.open(TSFeedScreenList)
        elif index == 8:
            self.session.open(TSEpgSetup)
        return

    def openSelected_info(self):
        index = self['list'].getIndex()
        if index == 0:
            self.session.open(About)
        elif index == 1:
            self.session.open(TSGeneralInfo)
        elif index == 2:
            self.session.open(TSDevicesInfo)
        elif index == 3:
            self.session.open(TSKernelModules)
        elif index == 4:
            self.session.open(TSProcessList)
        elif index == 5:
            self.session.open(TSMounts)
        elif index == 6:
            self.session.open(TSShowSettings)
        elif index == 7:
            self.session.open(TSCustomCmd)
        elif index == 8:
            self.session.open(AboutScreen)
        return

    def openSelected_tools(self):
        index = self['list'].getIndex()
        if index == 0:
            self.session.open(TSiMenuscrn)
        elif self.index == 1:
            if os_path.exists('/usr/lib/enigma2/python/Plugins/Extensions/backupflashe/plugin.pyo'):
                from Plugins.Extensions.backupflashe.plugin import full_main
                self.session.open(full_main)
            else:
                self.session.open(MessageBox, 'backupflashe not found!', MessageBox.TYPE_INFO)
        elif index == 2:
            self.session.open(TSBackupSettings)
        elif index == 3:
            self.session.open(TSiServersScreen)
        elif index == 4:
            self.session.open(SatellitesEditor)
        elif index == 5:
            self.session.openWithCallback(self.checkGrabberReboot, TSiScreenGrabberSetup)
        elif index == 6:
            self.session.openWithCallback(self.checkLanguageReboot, TSilangScreen)
        elif index == 7:
            self.session.open(TSiswapScreen)
        elif index == 8:
            self.session.open(TSiCronScreen)
        return

    def updatePanel(self):
        if config.plugins.TSPanel.Type.value == 'icons':
            Notifications.AddNotification(TSPanelIcons, 'TS Panel', TSPANEL_LABELS, TSPANEL_ICONS, 5, domain='TSPanel')
            self.close()
        return

    def checkSetupRestart(self, result=True):
        if os_path.exists('/tmp/.sibonlyoff'):
            os_remove('/tmp/.sibonlyoff')
            self.session.openWithCallback(self.restartGUI, MessageBox, _('GUI needs a restart to disable show only SecondInfobar.\nDo you want to Restart the GUI now?'), MessageBox.TYPE_YESNO, -1, False, True, True, None, _('Restart GUI now?'))
        elif os_path.exists('/tmp/.sibonlyon'):
            os_remove('/tmp/.sibonlyon')
            self.session.openWithCallback(self.restartGUI, MessageBox, _('GUI needs a restart to enable show only SecondInfobar.\nDo you want to Restart the GUI now?'), MessageBox.TYPE_YESNO, -1, False, True, True, None, _('Restart GUI now?'))
        elif os_path.exists('/tmp/.sibepgoff'):
            os_remove('/tmp/.sibepgoff')
            self.session.openWithCallback(self.restartGUI, MessageBox, _('GUI needs a restart to disable SecondInfobar EPG.\nDo you want to Restart the GUI now?'), MessageBox.TYPE_YESNO, -1, False, True, True, None, _('Restart GUI now?'))
        elif os_path.exists('/tmp/.sibepgon'):
            os_remove('/tmp/.sibepgon')
            self.session.openWithCallback(self.restartGUI, MessageBox, _('GUI needs a restart to enable SecondInfobar EPG.\nDo you want to Restart the GUI now?'), MessageBox.TYPE_YESNO, -1, False, True, True, None, _('Restart GUI now?'))
        elif os_path.exists('/tmp/.neutrinooff'):
            os_remove('/tmp/.neutrinooff')
            self.session.openWithCallback(self.restartGUI, MessageBox, _('GUI needs a restart to disable Neutrino Keymap.\nDo you want to Restart the GUI now?'), MessageBox.TYPE_YESNO, -1, False, True, True, None, _('Restart GUI now?'))
        elif os_path.exists('/tmp/.neutrinoon'):
            os_remove('/tmp/.neutrinoon')
            self.session.openWithCallback(self.restartGUI, MessageBox, _('GUI needs a restart to enable Neutrino Keymap.\nDo you want to Restart the GUI now?'), MessageBox.TYPE_YESNO, -1, False, True, True, None, _('Restart GUI now?'))
        elif os_path.exists('/tmp/.mediaoff'):
            os_remove('/tmp/.mediaoff')
            self.session.openWithCallback(self.restartGUI, MessageBox, _('GUI needs a restart to disable tsmedia panel.\nDo you want to Restart the GUI now?'), MessageBox.TYPE_YESNO, -1, False, True, True, None, _('Restart GUI now?'))
        elif os_path.exists('/tmp/.mediaon'):
            os_remove('/tmp/.mediaon')
            self.session.openWithCallback(self.restartGUI, MessageBox, _('GUI needs a restart to enable tsmedia panel.\nDo you want to Restart the GUI now?'), MessageBox.TYPE_YESNO, -1, False, True, True, None, _('Restart GUI now?'))
        elif os_path.exists('/tmp/.changedcolor'):
            os_remove('/tmp/.changedcolor')
            self.session.openWithCallback(self.restartGUI, MessageBox, _('GUI needs a restart to change skin colors.\nDo you want to Restart the GUI now?'), MessageBox.TYPE_YESNO, -1, False, True, True, None, _('Restart GUI now?'))
        else:
            self.updatePanel()
        return

    def checkAddonsRestart(self, result=True):
        if os_path.exists('/tmp/.newskin'):
            os_remove('/tmp/.newskin')
            restartbox = self.session.openWithCallback(self.selectSkin, MessageBox, _('New skin installed.') + '\n' + _('Do you want to select a skin?'), MessageBox.TYPE_YESNO)
            restartbox.setTitle(_('Select new skin now?'))
        elif os_path.exists('/tmp/.restart_e2'):
            os_remove('/tmp/.restart_e2')
            restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _('GUI needs a restart to reload plugins.\nDo you want to Restart the GUI now?'), MessageBox.TYPE_YESNO)
            restartbox.setTitle(_('Restart GUI now?'))
        return

    def selectSkin(self, answer):
        if answer:
            Notifications.AddNotification(SkinSelector, domain='AddonsManager')
            self.close()
        elif os_path.exists('/tmp/.restart_e2'):
            os_remove('/tmp/.restart_e2')
            restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _('GUI needs a restart to reload plugins.\nDo you want to Restart the GUI now?'), MessageBox.TYPE_YESNO)
            restartbox.setTitle(_('Restart GUI now?'))
        return

    def onTSToolsClose(self, result=True):
        if os_path.exists('/tmp/.newsettings'):
            os_remove('/tmp/.newsettings')
            self.close()
        elif os_path.exists('/tmp/.newlang'):
            os_remove('/tmp/.newlang')
            self.close()
        return

    def checkLanguageReboot(self, result=True):
        if os_path.exists('/tmp/.newlang'):
            restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _('GUI needs a restart to load new language\nDo you want to Restart the GUI now?'), MessageBox.TYPE_YESNO)
            restartbox.setTitle(_('Restart GUI now?'))
        return

    def checkGrabberReboot(self, result=True):
        if os_path.exists('/tmp/.newsettings'):
            restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _('GUI needs a restart to load changes\nDo you want to Restart the GUI now?'), MessageBox.TYPE_YESNO)
            restartbox.setTitle(_('Restart GUI now?'))
        return

    def restartGUI(self, answer):
        if os_path.exists('/tmp/.mediaoff'):
            os_remove('/tmp/.mediaoff')
        if os_path.exists('/tmp/.mediaon'):
            os_remove('/tmp/.mediaon')
        if os_path.exists('/tmp/.changedcolor'):
            os_remove('/tmp/.changedcolor')
        if os_path.exists('/tmp/.neutrinooff'):
            os_remove('/tmp/.neutrinooff')
        if os_path.exists('/tmp/.neutrinoon'):
            os_remove('/tmp/.neutrinoon')
        if answer and not inTryQuitMainloop:
            Notifications.AddNotification(TryQuitMainloop, 3, domain='AddonsManager')
            self.close()
        elif not answer:
            if os_path.exists('/tmp/.newlang'):
                os_remove('/tmp/.newlang')
            if os_path.exists('/tmp/.newsettings'):
                os_remove('/tmp/.newsettings')
            self.updatePanel()
        return

    def quit(self):
        if os_path.exists('/tmp/.dpkg_busy'):
            os_remove('/tmp/.dpkg_busy')
        self.close()
        return

    def createSummary(self):
        return TSPanelSummary


class TSPanelIcons(Screen):
    skin_1280 = '<screen name="TSPanelIcons" position="center,77" title=" " size="920,600">\n        <widget name="frame" position="0,0" size="145,145" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/pic_frame.png" zPosition="1" alphatest="blend"/>\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/images/tsimagelogo.png" position="695,230" zPosition="2" alphatest="blend" transparent="1" size="260,262"/>\n        <eLabel text="PANEL" position="670,380" font="Regular;45" valign="center" halign="center" zPosition="2" foregroundColor="#00398e" transparent="1" size="207,70"/>\n\n        <widget source="label0" render="Label" position="10,175" size="195,25" font="Regular;20" zPosition="2" transparent="1" noWrap="1" halign="center" valign="center"/>\n        <widget name="thumb0" position="40,25" size="128,128" zPosition="2" transparent="1" alphatest="blend"/>\n\n        <widget source="label1" render="Label" position="225,175" size="195,25" font="Regular;20" zPosition="2" transparent="1" noWrap="1" halign="center" valign="center"/>\n        <widget name="thumb1" position="255,25" size="128,128" zPosition="2" transparent="1" alphatest="blend"/>\n\n        <widget source="label2" render="Label" position="440,175" size="195,25" font="Regular;20" zPosition="2" transparent="1" noWrap="1" halign="center" valign="center"/>\n        <widget name="thumb2" position="470,25" size="128,128" zPosition="2" transparent="1" alphatest="blend"/>\n\n        <widget source="label3" render="Label" position="10,365" size="195,25" font="Regular;20" zPosition="2" transparent="1" noWrap="1" halign="center" valign="center"/>\n        <widget name="thumb3" position="40,215" size="128,128" zPosition="2" transparent="1" alphatest="blend"/>\n\n        <widget source="label4" render="Label" position="225,365" size="195,25" font="Regular;20" zPosition="2" transparent="1" noWrap="1" halign="center" valign="center"/>\n        <widget name="thumb4" position="255,215" size="128,128" zPosition="2" transparent="1" alphatest="blend"/>\n\n        <widget source="label5" render="Label" position="440,365" size="195,25" font="Regular;20" zPosition="2" transparent="1" noWrap="1" halign="center" valign="center"/>\n        <widget name="thumb5" position="470,215" size="128,128" zPosition="2" transparent="1" alphatest="blend"/>\n\n        <widget source="label6" render="Label" position="10,555" size="195,25" font="Regular;20" zPosition="2" transparent="1" noWrap="1" halign="center" valign="center"/>\n        <widget name="thumb6" position="40,405" size="128,128" zPosition="2" transparent="1" alphatest="blend"/>\n\n        <widget source="label7" render="Label" position="225,555" size="195,25" font="Regular;20" zPosition="2" transparent="1" noWrap="1" halign="center" valign="center"/>\n        <widget name="thumb7" position="255,405" size="128,128" zPosition="2" transparent="1" alphatest="blend"/>\n\n        <widget source="label8" render="Label" position="440,555" size="195,25" font="Regular;20" zPosition="2" transparent="1" noWrap="1" halign="center" valign="center"/>\n        <widget name="thumb8" position="470,405" size="128,128" zPosition="2" transparent="1" alphatest="blend"/>\n    </screen>\n    '
    skin_1920 = '<screen name="TSPanelIcons" position="center,200" size="1300,720" title="TSPanel">\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/images/tsimagelogo2.png" position="945,160" size="250,243" zPosition="-1" alphatest="blend"/>\n\n        <widget source="label0" render="Label" position="45,178" size="200,70" font="Regular;26" zPosition="2" halign="center" valign="center" transparent="1"/>\n        <widget source="label1" render="Label" position="275,178" size="200,70" font="Regular;26" zPosition="2" halign="center" valign="center" transparent="1"/>\n        <widget source="label2" render="Label" position="505,178" size="200,70" font="Regular;26" zPosition="2" halign="center" valign="center" transparent="1"/>\n\n        <widget source="label3" render="Label" position="45,397" size="200,70" font="Regular;26" zPosition="2" halign="center" valign="center" transparent="1"/>\n        <widget source="label4" render="Label" position="275,397" size="200,70" font="Regular;26" zPosition="2" halign="center" valign="center" transparent="1"/>\n        <widget source="label5" render="Label" position="505,397" size="200,70" font="Regular;26" zPosition="2" halign="center" valign="center" transparent="1"/>\n\n        <widget source="label6" render="Label" position="45,616" size="200,70" font="Regular;26" zPosition="2" halign="center" valign="center" transparent="1"/>\n        <widget source="label7" render="Label" position="275,616" size="200,70" font="Regular;26" zPosition="2" halign="center" valign="center" transparent="1"/>\n        <widget source="label8" render="Label" position="505,616" size="200,70" font="Regular;26" zPosition="2" halign="center" valign="center" transparent="1"/>\n\n        <widget name="thumb0" position="80,38" size="130,130" zPosition="2" alphatest="blend"/>\n        <widget name="thumb1" position="310,38" size="130,130" zPosition="2" alphatest="blend"/>\n        <widget name="thumb2" position="540,38" size="130,130" zPosition="2" alphatest="blend"/>\n\n        <widget name="thumb3" position="80,257" size="130,130" zPosition="2" alphatest="blend"/>\n        <widget name="thumb4" position="310,257" size="130,130" zPosition="2" alphatest="blend"/>\n        <widget name="thumb5" position="540,257" size="130,130" zPosition="2" alphatest="blend"/>\n\n        <widget name="thumb6" position="80,476" size="130,130" zPosition="2" alphatest="blend"/>\n        <widget name="thumb7" position="310,476" size="130,130" zPosition="2" alphatest="blend"/>\n        <widget name="thumb8" position="540,476" size="130,130" zPosition="2" alphatest="blend"/>\n\n        <widget name="frame" position="70,38" size="150,150" zPosition="3" alphatest="blend"/>\n\n        <widget source="global.CurrentTime" render="Label" position="840,50" size="460,70" font="Regular;65" halign="center" foregroundColor="foreground" backgroundColor="background" transparent="1">\n            <convert type="ClockToText">Default</convert>\n        </widget>\n\n        <widget source="session.CurrentService" render="Label" position="850,480" size="440,100" font="Regular;38" halign="center" foregroundColor="foreground" backgroundColor="background" transparent="1">\n            <convert type="ServiceName">Name</convert>\n        </widget>\n    </screen>\n    '
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session, title='TS Panel', labelsList=TSPANEL_LABELS, iconsnameList=TSPANEL_ICONS, startindex=0):
        Screen.__init__(self, session)
        self.labelsList = labelsList
        self.iconsnameList = iconsnameList
        self.title = title
        self.startindex = startindex
        self.setTitle(self.title)
        self.thumbsC = 9
        for idx in range(self.thumbsC):
            self['label%d' % idx] = StaticText('')
            self['thumb%d' % idx] = Pixmap()

        self['frame'] = MovingPixmap()
        if title == 'TS Panel':
            self.KeyOk = self.KeyOk_main
            self.def_iconspath = '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/panelbuttons/'
        elif title == 'TS Infos':
            self.skin = self.skin.replace('<eLabel text="PANEL"', '<eLabel text="INFOS"')
            self.KeyOk = self.KeyOk_info
            self.def_iconspath = '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/infobuttons/'
        elif title == 'TS Tools':
            self.skin = self.skin.replace('<eLabel text="PANEL"', '<eLabel text="TOOLS"')
            self.KeyOk = self.KeyOk_tools
            self.def_iconspath = '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/Stools/toolsbuttons/'
        self['actions'] = ActionMap([
         'OkCancelActions', 'ColorActions', 'DirectionActions', 'MovieSelectionActions'], {'cancel': (self.quit), 'ok': (self.KeyOk), 
           'left': (self.key_left), 
           'right': (self.key_right), 
           'up': (self.key_up), 
           'down': (self.key_down)}, -1)
        self.onLayoutFinish.append(self.showPanel)
        self.onShow.append(self.updateSummaries)
        return

    def updateSummaries(self):
        try:
            self.summaries.setText(self.title, 0)
            idx = getattr(self, 'index', 0)
            self.summaries.setText(self['label%d' % idx].getText(), 1)
        except Exception:
            pass

        return

    def checkEntry(self, image, def_path=DEFAULT_ICONSPATH):
        if os_path.exists(SKIN_ICONSPATH + image):
            path = '%s%s' % (SKIN_ICONSPATH, image)
        else:
            path = '%s%s' % (def_path, image)
        return path

    def moveFrame(self):
        self['frame'].moveTo(self.positionList[self.index][0], self.positionList[self.index][1], 1)
        self['frame'].startMoving()
        return

    def showPanel(self):
        self.positionList = []
        sc = AVSwitch().getFramebufferScale()
        self.picload = ePicLoad()
        self.picload.setPara([self['thumb0'].instance.size().width(),
         self['thumb0'].instance.size().height(),
         sc[0],
         sc[1],
         True,
         1,
         'background'])
        offsetX = 10
        offsetY = 10
        self.thumbsX = 0
        for idx in range(self.thumbsC):
            frame_pos = self['thumb%d' % idx].getPosition()
            self.positionList.append((frame_pos[0] - offsetX, frame_pos[1] - offsetY))
            if frame_pos[1] == self.positionList[0][1] + offsetY:
                self.thumbsX += 1
            self['thumb%d' % idx].instance.setPixmapFromFile(self.checkEntry(self.iconsnameList[idx], self.def_iconspath))
            self['label%d' % idx].setText(self.labelsList[idx])

        self['frame'].setPosition(self.positionList[self.startindex][0], self.positionList[self.startindex][1])
        self['frame'].instance.setPixmapFromFile(self.checkEntry('pic_frame.png', DEFAULT_FRAMEPATH))
        self.index = self.startindex
        self.maxentry = len(self.positionList) - 1
        return

    def key_left(self):
        if self.thumbsX == 1:
            self.index = 0
        else:
            self.index -= 1
            if self.index < 0:
                self.index = self.maxentry
        self.moveFrame()
        self.summaries.setText(self['label%d' % self.index].getText(), 1)
        return

    def key_right(self):
        if self.thumbsX == 1:
            self.index = self.maxentry
        else:
            self.index += 1
            if self.index > self.maxentry:
                self.index = 0
        self.moveFrame()
        self.summaries.setText(self['label%d' % self.index].getText(), 1)
        return

    def key_up(self):
        self.index -= self.thumbsX
        if self.index < 0:
            self.index = self.maxentry
        self.moveFrame()
        self.summaries.setText(self['label%d' % self.index].getText(), 1)
        return

    def key_down(self):
        self.index += self.thumbsX
        if self.index > self.maxentry:
            self.index = 0
        self.moveFrame()
        self.summaries.setText(self['label%d' % self.index].getText(), 1)
        return

    def KeyOk_main(self):
        self.old_index = self.index
        if self.index == 0:
            self.session.open(TSSoftcamsManager)
        elif self.index == 1:
            self.session.openWithCallback(self.checkAddonsRestart, ServerGroups)
        elif self.index == 2:
            self.session.openWithCallback(self.onTSToolsClose, TSPanelIcons, 'TS Tools', TSTOOLS_LABELS, TSTOOLS_ICONS)
        elif self.index == 3:
            self.session.open(HarddiskDriveSelection)
        elif self.index == 4:
            self.session.open(FileExplorerII)
        elif self.index == 5:
            self.session.openWithCallback(self.checkSetupRestart, TSSkinSetup)
        elif self.index == 6:
            self.session.open(TSPanelIcons, 'TS Infos', TSINFOS_LABELS, TSINFOS_ICONS)
        elif self.index == 7:
            self.session.open(TSFeedScreenList)
        elif self.index == 8:
            self.session.open(TSEpgSetup)
        return

    def KeyOk_info(self):
        if self.index == 0:
            self.session.open(About)
        elif self.index == 1:
            self.session.open(TSGeneralInfo)
        elif self.index == 2:
            self.session.open(TSDevicesInfo)
        elif self.index == 3:
            self.session.open(TSKernelModules)
        elif self.index == 4:
            self.session.open(TSProcessList)
        elif self.index == 5:
            self.session.open(TSMounts)
        elif self.index == 6:
            self.session.open(TSShowSettings)
        elif self.index == 7:
            self.session.open(TSCustomCmd)
        elif self.index == 8:
            self.session.open(AboutScreen)
        return

    def KeyOk_tools(self):
        self.old_index = self.index
        if self.index == 0:
            self.session.open(TSiMenuscrn)
        elif self.index == 1:
            if os_path.exists('/usr/lib/enigma2/python/Plugins/Extensions/backupflashe/plugin.pyo'):
                from Plugins.Extensions.backupflashe.plugin import full_main
                self.session.open(full_main)
            else:
                self.session.open(MessageBox, 'backupflashe not found!', MessageBox.TYPE_INFO)
        elif self.index == 2:
            self.session.open(TSBackupSettings)
        elif self.index == 3:
            self.session.open(TSiServersScreen)
        elif self.index == 4:
            self.session.open(SatellitesEditor)
        elif self.index == 5:
            self.session.openWithCallback(self.checkGrabberReboot, TSiScreenGrabberSetup)
        elif self.index == 6:
            self.session.openWithCallback(self.checkLanguageReboot, TSilangScreen)
        elif self.index == 7:
            self.session.open(TSiswapScreen)
        elif self.index == 8:
            self.session.open(TSiCronScreen)
        return

    def updatePanel(self, status=True):
        if config.plugins.TSPanel.Type.value == 'list':
            Notifications.AddNotification(TSPanelList, 'TS Panel', TSPANEL_LABELS, TSPANEL_ICONS, 5, domain='TSPanel')
            self.close(self.index)
        else:
            self['frame'].instance.setPixmapFromFile(self.checkEntry('pic_frame.png', DEFAULT_FRAMEPATH))
            for idx in range(self.thumbsC):
                self['thumb%d' % idx].instance.setPixmapFromFile(self.checkEntry(self.iconsnameList[idx], self.def_iconspath))
                self['label%d' % idx].setText(self.labelsList[idx])

        return

    def checkSetupRestart(self, result=True):
        if os_path.exists('/tmp/.sibonlyoff'):
            os_remove('/tmp/.sibonlyoff')
            restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _('GUI needs a restart to disable show only SecondInfobar.\nDo you want to Restart the GUI now?'), MessageBox.TYPE_YESNO)
            restartbox.setTitle(_('Restart GUI now?'))
        elif os_path.exists('/tmp/.sibonlyon'):
            os_remove('/tmp/.sibonlyon')
            restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _('GUI needs a restart to enable show only SecondInfobar.\nDo you want to Restart the GUI now?'), MessageBox.TYPE_YESNO)
            restartbox.setTitle(_('Restart GUI now?'))
        elif os_path.exists('/tmp/.sibepgoff'):
            os_remove('/tmp/.sibepgoff')
            restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _('GUI needs a restart to disable SecondInfobar EPG.\nDo you want to Restart the GUI now?'), MessageBox.TYPE_YESNO)
            restartbox.setTitle(_('Restart GUI now?'))
        elif os_path.exists('/tmp/.sibepgon'):
            os_remove('/tmp/.sibepgon')
            restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _('GUI needs a restart to enable SecondInfobar EPG.\nDo you want to Restart the GUI now?'), MessageBox.TYPE_YESNO)
            restartbox.setTitle(_('Restart GUI now?'))
        elif os_path.exists('/tmp/.neutrinooff'):
            os_remove('/tmp/.neutrinooff')
            restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _('GUI needs a restart to disable Neutrino Keymap.\nDo you want to Restart the GUI now?'), MessageBox.TYPE_YESNO)
            restartbox.setTitle(_('Restart GUI now?'))
        elif os_path.exists('/tmp/.neutrinoon'):
            os_remove('/tmp/.neutrinoon')
            restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _('GUI needs a restart to enable Neutrino Keymap.\nDo you want to Restart the GUI now?'), MessageBox.TYPE_YESNO)
            restartbox.setTitle(_('Restart GUI now?'))
        elif os_path.exists('/tmp/.mediaoff'):
            os_remove('/tmp/.mediaoff')
            restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _('GUI needs a restart to disable tsmedia panel.\nDo you want to Restart the GUI now?'), MessageBox.TYPE_YESNO)
            restartbox.setTitle(_('Restart GUI now?'))
        elif os_path.exists('/tmp/.mediaon'):
            os_remove('/tmp/.mediaon')
            restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _('GUI needs a restart to enable tsmedia panel.\nDo you want to Restart the GUI now?'), MessageBox.TYPE_YESNO)
            restartbox.setTitle(_('Restart GUI now?'))
        elif os_path.exists('/tmp/.changedcolor'):
            os_remove('/tmp/.changedcolor')
            restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _('GUI needs a restart to change skin colors.\nDo you want to Restart the GUI now?'), MessageBox.TYPE_YESNO)
            restartbox.setTitle(_('Restart GUI now?'))
        else:
            self.updatePanel()
        return

    def checkAddonsRestart(self, result=True):
        if os_path.exists('/tmp/.newskin'):
            os_remove('/tmp/.newskin')
            restartbox = self.session.openWithCallback(self.selectSkin, MessageBox, _('New skin installed.') + '\n' + _('Do you want to select a skin?'), MessageBox.TYPE_YESNO)
            restartbox.setTitle(_('Select new skin now?'))
        elif os_path.exists('/tmp/.restart_e2'):
            os_remove('/tmp/.restart_e2')
            restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _('GUI needs a restart to reload plugins.\nDo you want to Restart the GUI now?'), MessageBox.TYPE_YESNO)
            restartbox.setTitle(_('Restart GUI now?'))
        return

    def selectSkin(self, answer):
        if answer:
            Notifications.AddNotification(SkinSelector, domain='AddonsManager')
            self.close(self.index)
        elif os_path.exists('/tmp/.restart_e2'):
            os_remove('/tmp/.restart_e2')
            restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _('GUI needs a restart to reload plugins.\nDo you want to Restart the GUI now?'), MessageBox.TYPE_YESNO)
            restartbox.setTitle(_('Restart GUI now?'))
        return

    def onTSToolsClose(self, result=True):
        if os_path.exists('/tmp/.newsettings'):
            os_remove('/tmp/.newsettings')
            self.close(self.index)
        elif os_path.exists('/tmp/.newlang'):
            os_remove('/tmp/.newlang')
            self.close(self.index)
        return

    def checkLanguageReboot(self, result=True):
        if os_path.exists('/tmp/.newlang'):
            restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _('GUI needs a restart to load new language\nDo you want to Restart the GUI now?'), MessageBox.TYPE_YESNO)
            restartbox.setTitle(_('Restart GUI now?'))
        return

    def checkGrabberReboot(self, result=True):
        if os_path.exists('/tmp/.newsettings'):
            restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _('GUI needs a restart to load changes\nDo you want to Restart the GUI now?'), MessageBox.TYPE_YESNO)
            restartbox.setTitle(_('Restart GUI now?'))
        return

    def restartGUI(self, answer):
        if os_path.exists('/tmp/.mediaoff'):
            os_remove('/tmp/.mediaoff')
        if os_path.exists('/tmp/.mediaon'):
            os_remove('/tmp/.mediaon')
        if os_path.exists('/tmp/.changedcolor'):
            os_remove('/tmp/.changedcolor')
        if os_path.exists('/tmp/.neutrinooff'):
            os_remove('/tmp/.neutrinooff')
        if os_path.exists('/tmp/.neutrinoon'):
            os_remove('/tmp/.neutrinoon')
        if answer and not inTryQuitMainloop:
            Notifications.AddNotification(TryQuitMainloop, 3, domain='AddonsManager')
            self.close(self.index)
        elif not answer:
            if os_path.exists('/tmp/.newlang'):
                os_remove('/tmp/.newlang')
            if os_path.exists('/tmp/.newsettings'):
                os_remove('/tmp/.newsettings')
            self.updatePanel()
        return

    def quit(self):
        del self.picload
        if os_path.exists('/tmp/.dpkg_busy'):
            os_remove('/tmp/.dpkg_busy')
        self.close(self.index)
        return

    def createSummary(self):
        return TSPanelSummary


def Plugins(**kwargs):
    list = []
    list.append(PluginDescriptor(where=[PluginDescriptor.WHERE_SESSIONSTART, PluginDescriptor.WHERE_AUTOSTART], fnc=TSPanelAutostart))
    list.append(PluginDescriptor(name='TS Panel', description='TSimage Bleu Panel by colombo555', icon='tsimagelogo.png', where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=showPanel))
    return list


def showPanel(session, **kwargs):
    if config.plugins.TSPanel.Type.value == 'list':
        session.open(TSPanelList)
    elif config.plugins.TSPanel.Type.value == 'icons':
        session.open(TSPanelIcons)
    return


def _sanitize_config_text_values():
    try:
        from Components.config import config, ConfigSubsection, ConfigElement, ConfigText, ConfigSelection
        try:
            from Components.config import ConfigSelectionNumber
        except Exception:

            class ConfigSelectionNumber(object):
                pass

        try:
            basestring
        except NameError:
            basestring = (
             str, unicode)

        seen = set()

        def _walk(node, path='config'):
            if id(node) in seen:
                return
            else:
                seen.add(id(node))
                for name in dir(node):
                    if name.startswith('_') or name in ('save', 'load', 'pickle', 'getSavedValue'):
                        continue
                    try:
                        child = getattr(node, name)
                    except Exception:
                        continue

                    if isinstance(child, ConfigSubsection):
                        _walk(child, '%s.%s' % (path, name))
                        continue
                    if isinstance(child, ConfigElement):
                        clsname = child.__class__.__name__
                        val = getattr(child, 'value', None)
                        if isinstance(child, (ConfigText, ConfigSelection, ConfigSelectionNumber)):
                            if not isinstance(val, basestring):
                                try:
                                    child.value = '' if val is None else str(val)
                                    print '[CFG SAN] %s (%s) coerced non-string value=%r' % (
                                     '%s.%s' % (path, name), clsname, val)
                                except Exception as e:
                                    print '[CFG SAN] failed to coerce %s: %s' % (
                                     '%s.%s' % (path, name), e)

                return
                return

        _walk(config)
        print '[CFG SAN] text-like config values sanitized'
    except Exception as e:
        print '[CFG SAN] skipped: %s' % e

    return


def TSPanelAutostart(reason, session=None, **kwargs):
    global EPGdbBackupautoStartTimer
    global tsupdater
    if reason != 0:
        return
    else:
        _sanitize_config_text_values()
        if session is not None:
            if tsupdater is None:
                tsupdater = TSUpdater()
                if config.plugins.TSUpdater.boot.value:
                    print '[TSUpdater] autostart'
                    tsupdater.dpkgUpdate()
                else:
                    tsupdater.cleantmp()
                    print '[TSUpdater] apt update at boot: disabled'
            if EPGdbBackupautoStartTimer is None:
                print '[EPGdbBackup] Start epg backup check'
                EPGdbBackupautoStartTimer = EPGdbBackupAutoStartTimer(session)
            if config.plugins.TSSwapmanager.activateonboot.value:
                outline = getCmdOutput("cat /proc/swaps | grep %s/swapfile | awk '{print $1}'" % config.plugins.TSSwapmanager.mountpoint.value)
                if outline == '':
                    print '[TSSwapmanager] swapfile autostart...'
                    cmd = 'swapon %s/swapfile' % config.plugins.TSSwapmanager.mountpoint.value
                    os_system(cmd)
                    print '[TSSwapmanager] %s/swapfile enabled' % config.plugins.TSSwapmanager.mountpoint.value
            else:
                print '[TSSwapmanager] swapfile autostart: disabled'
            try:
                _schedule_cam_autostart(delay_ms=8000)
            except Exception as e:
                print '[TSPanel] Cam autostart setup failed: %s' % e

            if pathExists('/etc/issue.net'):
                try:
                    issue = open('/etc/issue.net', 'r').read()
                    if issue:
                        if issue.find('TSimage') < 0:
                            text = '+-------------------------------+\n'
                            text += '|                               |\n'
                            text += '|         TSimage 2025          |\n'
                            text += '|           [Ostende]           |\n'
                            text += '|                               |\n'
                            text += '+-------------------------------+\n'
                            open('/etc/issue.net', 'w').write(text)
                except Exception as e:
                    print '[TSPanel] issue failed: %s' % e

            if not pathExists('/root/.profile'):
                try:
                    text = 'TERM=xterm\n'
                    text += 'alias ls="ls --color"'
                    open('/root/.profile', 'w').write(text)
                except Exception as e:
                    print '[TSPanel] profile failed: %s' % e

        return
        return


def showext(self):
    self.onOpenSession()
    self.session.open(PluginBrowser)
    return


def showTSiPanel(self):
    self.onOpenSession()
    if config.plugins.TSPanel.Type.value == 'list':
        self.session.open(TSPanelList)
    elif config.plugins.TSPanel.Type.value == 'icons':
        self.session.open(TSPanelIcons)
    return


def ScreenGrabberGlobalAction(self):
    global globalActionMap
    rcbutton = config.plugins.ScreenGrabber.scut.value
    ScreenGrabber_keymap = '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/Stools/ScreenGrabber/keymaps/' + rcbutton + '_keymap.xml'
    if os_path.exists(ScreenGrabber_keymap):
        readKeymap(ScreenGrabber_keymap)
        globalActionMap.actions['ShowScreenGrabber'] = self.ScreenGrabberView
    else:
        self.session.open(MessageBox, 'file %s not found!' % ScreenGrabber_keymap, MessageBox.TYPE_ERROR)
    return


def ScreenGrabberView(self):
    self.onOpenSession()
    self.session.open(TSiScreenGrabberView)
    return


def onOpenSession(self):
    if self.shown:
        self.hide()
    try:
        if self.SIBdialog.shown:
            self.SIBdialog.hide()
        elif self.SIBEPGdialog.shown:
            self.SIBEPGdialog.hide()
    except:
        print '[InfobarBar onOpenSession] warning: no SecondInfoBar found !'

    return


class AboutScreen(Screen):
    skin_1280 = '<screen position="center,77" size="920,600" title="">\n        <widget name="logo" position="720,15" size="150,164" alphatest="blend" transparent="1"/>\n        <widget name="about" position="20,15" size="890,570" font="Regular;22" zPosition="2" backgroundColor="background" transparent="1" noWrap="1" halign="left"/>\n        <eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"/>\n        <ePixmap name="red" position="70,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" transparent="1" alphatest="blend"/>\n        <widget name="key_red" position="70,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" backgroundColor="background" transparent="1"/>\n    </screen>\n    '
    skin_1920 = '<screen name="AboutScreen" position="center,200" size="1300,720" title="About">\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/images/tsimagelogo2.png" position="945,160" size="250,243" zPosition="-1" alphatest="blend"/>\n        <widget font="Regular;28" name="about" position="30,30" size="830,920" foregroundColor="foreground" backgroundColor="background" transparent="1"/>\n        <!--widget name="logo" position="680,10" size="150,164" alphatest="blend" transparent="1" /-->\n        <widget source="global.CurrentTime" render="Label" position="840,50" size="460,70" font="Regular;65" halign="center" foregroundColor="foreground" backgroundColor="background" transparent="1">\n            <convert type="ClockToText">Default</convert>\n        </widget>\n        <widget source="session.CurrentService" render="Label" position="850,480" size="440,100" font="Regular;38" halign="center" foregroundColor="foreground" backgroundColor="background" transparent="1">\n            <convert type="ServiceName">Name</convert>\n        </widget>\n    </screen>\n    '
    if getDesktop(0).size().width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session):
        Screen.__init__(self, session)
        text = b'TSimage 6.0 \xa9 2012-2025\n'
        text += 'http://www.tunisia-sat.com\n\n'
        text += 'developed by: \n\n'
        text += '-[Ostende] (image builder) \n\n'
        text += 'In memory of: \n\n'
        text += '-colombo555 (main developer and image builder)\n'
        text += '-SIOUD (scripts developer)\n'
        text += '-mfaraj57 (developer)[R.I.P]\n'
        text += '-sangoku (beta tester)\n'
        text += '-tounsi9_4 (server)\n'
        text += '-merdas (member)\n'
        text += '-sami73 (member)\n'
        self['about'] = Label(text)
        self['logo'] = Pixmap()
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': (self.close), 'cancel': (self.close), 'red': (self.close)}, -1)
        self['key_red'] = Label(_('Close'))
        self.onFirstExecBegin.append(self.setImages)
        self.onShown.append(self.setWindowTitle)
        return

    def setImages(self):
        self['logo'].instance.setPixmapFromFile('/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/images/tsimagelogo.png')
        return

    def setWindowTitle(self):
        self.setTitle(_('About') + ' TSimage')
        return


return
