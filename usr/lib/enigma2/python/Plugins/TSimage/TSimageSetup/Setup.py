# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/TSimageSetup/Setup.py
# Compiled at: 2025-09-16 20:39:05
from Components.Button import Button
from Components.Label import Label
from Components.Sources.List import List
from Components.Pixmap import Pixmap
from Components.AVSwitch import AVSwitch
from Tools.LoadPixmap import LoadPixmap
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Tools.Directories import fileExists, SCOPE_LANGUAGE, SCOPE_PLUGINS, SCOPE_CURRENT_PLUGIN, resolveFilename
from enigma import eSize, eTimer, ePicLoad, gPixmapPtr, getDesktop
from twisted.web.client import downloadPage, getPage
from xml.dom import Node, minidom
from Components.ConfigList import ConfigList, ConfigListScreen
from Components.config import config, ConfigInteger, ConfigSubsection, ConfigText, ConfigSelection, ConfigYesNo, getConfigListEntry, configfile
from Plugins.TSimage.TSimagePanel.multInstaller import TSGetMultiipk
from TSyWeatherSetup import TSyWeatherEntries
from Plugins.TSimage.TSimagePanel.addonsManager import PreviewScreen
from PermanentClock import *
from Components.Language import language
from os import environ, statvfs, system as os_system, path as os_path, remove as os_remove
import gettext, xml.etree.ElementTree as ET
try:
    from Screens.VirtualKeyBoard import VirtualKeyBoard
except Exception:
    VirtualKeyBoard = None

try:
    from Screens.InputBox import InputBox
except Exception:
    InputBox = None

try:
    basestring
except NameError:
    basestring = (
     str, bytes)

def _as_str(x):
    try:
        if isinstance(x, basestring):
            return x
        else:
            return str(x)

    except Exception:
        return str(x)

    return


def _iter_children(node):
    d = getattr(node, 'content', None)
    if d is None:
        d = getattr(node, 'dict', None)
    if isinstance(d, dict):
        return d.items()
    else:
        return []
        return


def _sanitize_node(path, node, changes):
    try:
        getch = getattr(node, 'getChoices', None)
        choices = list(getch()) if callable(getch) else getattr(node, 'choices', None)
        if choices:
            fixed = []
            need_fix = False
            for c in choices:
                if isinstance(c, (list, tuple)) and len(c) >= 2:
                    v, t = c[0], c[1]
                else:
                    v, t = c, c
                sv, st = _as_str(v), _as_str(t)
                if sv != v or st != t or not isinstance(v, basestring):
                    need_fix = True
                fixed.append((sv, st))

            if need_fix:
                setch = getattr(node, 'setChoices', None)
                if callable(setch):
                    setch(fixed)
                    changes.append(path + ' :: choices normalized')
            if hasattr(node, 'value'):
                try:
                    node.value = _as_str(node.value)
                    changes.append(path + ' :: value normalized')
                except Exception:
                    pass

    except Exception:
        pass

    for k, child in _iter_children(node):
        _sanitize_node(path + '.' + k, child, changes)

    return


def sanitize_all_config():
    changes = []
    _sanitize_node('config', config, changes)
    try:
        with open('/tmp/config_sanitize.log', 'w') as f:
            f.write(('\n').join(changes) if changes else 'no changes\n')
    except Exception:
        pass

    return changes


def _scan_config_for_bad(out, node, path):
    bad = False
    try:
        vts = getattr(node, 'valueToString', None)
        if callable(vts):
            res = vts(getattr(node, 'value', None))
            if not isinstance(res, basestring):
                bad = True
    except Exception:
        bad = True

    try:
        getch = getattr(node, 'getChoices', None)
        choices = list(getch()) if callable(getch) else getattr(node, 'choices', None)
        if choices:
            for c in choices:
                v = c[0] if isinstance(c, (list, tuple)) and c else c
                if not isinstance(v, basestring):
                    bad = True
                    break

    except Exception:
        pass

    if bad:
        cls = node.__class__.__name__
        val = getattr(node, 'value', None)
        out.append('%s :: %s value=%r (%s)' % (path, cls, val, type(val).__name__))
    for k, child in _iter_children(node):
        _scan_config_for_bad(out, child, path + '.' + k)

    return


def _dump_bad_config_report():
    items = []
    try:
        _scan_config_for_bad(items, config, 'config')
    except Exception as e:
        items.append('SCAN-ERROR: %s' % e)

    try:
        with open('/tmp/config_bad.txt', 'w') as f:
            if items:
                f.write(('\n').join(items) + '\n')
            else:
                f.write('no suspects found\n')
    except Exception:
        pass

    return items


try:
    sanitize_all_config()
except Exception:
    pass

def _scan_config(node, path, out):
    """
    Recursively scan config tree and log leaves that can't stringify cleanly
    or have non-string choices (common cause of the pickle TypeError).
    """
    try:
        children = getattr(node, 'content', None)
        if children is None:
            children = getattr(node, 'dict', None)
    except Exception:
        children = None

    if isinstance(children, dict) and children:
        for k, v in children.items():
            _scan_config(v, '%s.%s' % (path, k), out)

        return
    bad = False
    val = getattr(node, 'value', None)
    try:
        v2s = getattr(node, 'valueToString', None)
        if callable(v2s):
            s = v2s(val)
            if not isinstance(s, basestring):
                bad = True
    except Exception:
        bad = True

    try:
        ch = getattr(node, 'choices', None)
        if ch:
            for c in list(ch):
                v = c[0] if isinstance(c, (list, tuple)) and c else c
                if not isinstance(v, basestring):
                    bad = True
                    break

    except Exception:
        pass

    if bad:
        out.append('%s :: value=%r (%s)' % (path, val, type(val).__name__))
    return


def _dump_bad_config_report():
    """
    Write a quick report to /tmp/config_bad.txt and return the list.
    """
    out = []
    try:
        _scan_config(config, 'config', out)
    except Exception as e:
        out.append('SCAN-ERROR: %s' % e)

    try:
        if out:
            with open('/tmp/config_bad.txt', 'w') as f:
                f.write(('\n').join(out) + '\n')
    except Exception:
        pass

    return out


def _choices_from_list(seq):
    """
    Build ConfigSelection choices from any iterable, coercing values to strings.
    Each entry is (value, text) and both are strings.
    """
    out = []
    for x in seq:
        s = _as_str(x)
        out.append((s, s))

    return out


path_extplugins = ('/usr/share/enigma2/' + config.skin.primary_skin.value).replace('skin.xml', '/modules/skin_extplugins.xml')
path_tspanel = ('/usr/share/enigma2/' + config.skin.primary_skin.value).replace('skin.xml', '/modules/skin_tspanel.xml')

def localeInit():
    lang = language.getLanguage()
    environ['LANGUAGE'] = lang[:2]
    gettext.bindtextdomain('enigma2', resolveFilename(SCOPE_LANGUAGE))
    gettext.textdomain('enigma2')
    gettext.bindtextdomain('TSimageSetup', '%s%s' % (resolveFilename(SCOPE_PLUGINS), 'TSimage/TSimageSetup/locale/'))
    return


def _(txt):
    t = gettext.dgettext('TSimageSetup', txt)
    if t == txt:
        t = gettext.gettext(txt)
    return t


localeInit()
language.addCallback(localeInit)
VERSION = 'v6.0'
DATE = '24.08.2025'
PREVIEW_PATH = '/tmp/plugin_preview.jpg'
SKIN_PREVIEW_PATH = '/tmp/skin_preview.png'
iconpanel_conf = '/etc/enigma2/icon_panel.conf'
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


def getChoices(list_str):
    choices = []
    for item in list_str:
        s = _as_str(item)
        choices.append((s, _(s)))

    return choices


def checkProcessmode(item):
    idx_0 = -1
    idx = 0
    iconpanel_set = 'Icons_000'
    iconpanel_sel = item
    if fileExists(iconpanel_conf):
        f = open(iconpanel_conf, 'r')
        iconpanel_set = f.readline().strip()
        s = iconpanel_set.split('_')
        if len(s) > 1:
            try:
                idx = int(s[1])
            except:
                idx = 0

        f.close()
    if iconpanel_set == iconpanel_sel:
        return ('remove', idx)
    else:
        return (
         'install', idx_0)

    return


config.plugins.TSPanel = ConfigSubsection()
config.plugins.TSPanel.Type = ConfigSelection(default='icons', choices=[('icons', _('Icons')), ('list', _('List'))])
config.plugins.SecondInfoBar = ConfigSubsection()
config.plugins.SecondInfoBar.TimeOut = ConfigInteger(default=6, limits=(0, 30))
config.plugins.SecondInfoBar.Mode = ConfigSelection(default='sib', choices=[('nothing', _('Not enabled')),
 (
  'sib', _('Show Second-InfoBar')),
 (
  'sibepg', _('Show Second-InfoBar EPG')),
 (
  'epglist', _('Show EPG-List/MerlinEPG')),
 (
  'subsrv', _('Show Subservices')),
 (
  'onlysib', _('Show ONLY Second-InfoBar'))])
config.plugins.SecondInfoBar.HideNormalIB = ConfigYesNo(default=False)
config.plugins.TSSkinSetup = ConfigSubsection()
config.plugins.TSSkinSetup.neutrino = ConfigYesNo(default=False)
config.plugins.TSSkinSetup.TSiMediaPanelenabled = ConfigYesNo(default=True)
config.plugins.TSSkinSetup.piconSet1 = ConfigText(default='/data/picon', fixed_size=False)
config.plugins.TSSkinSetup.piconSet2 = ConfigText(default='/media/usb/picon', fixed_size=False)
config.plugins.TSSkinSetup.piconSet3 = ConfigText(default='/media/cf/picon', fixed_size=False)
config.plugins.TSSkinSetup.piconSet4 = ConfigText(default='/media/hdd/picon', fixed_size=False)
config.plugins.TSSkinSetup.piconSet5 = ConfigText(default='/usr/share/enigma2/picon', fixed_size=False)
config.plugins.TSSkinSetup.picon1Path = ConfigSelection(default=config.plugins.TSSkinSetup.piconSet1.value, choices=[config.plugins.TSSkinSetup.piconSet1.value,
 config.plugins.TSSkinSetup.piconSet2.value,
 config.plugins.TSSkinSetup.piconSet3.value,
 config.plugins.TSSkinSetup.piconSet4.value,
 config.plugins.TSSkinSetup.piconSet5.value])
config.plugins.TSSkinSetup.picon2Path = ConfigSelection(default=config.plugins.TSSkinSetup.piconSet1.value, choices=[config.plugins.TSSkinSetup.piconSet1.value,
 config.plugins.TSSkinSetup.piconSet2.value,
 config.plugins.TSSkinSetup.piconSet3.value,
 config.plugins.TSSkinSetup.piconSet4.value,
 config.plugins.TSSkinSetup.piconSet5.value])
config.plugins.TSSkinSetup.typewriter = ConfigYesNo(default=False)
config.plugins.TSSkinSetup.typingSpeed = ConfigInteger(default=300, limits=(100, 999))
config.plugins.TSSkinSetup.runningText = ConfigYesNo(default=False)
config.plugins.TSSkinSetup.runningStartTime = ConfigSelection(default='5', choices=[79, 80, 81, 82, 78, 83, 84, 85, 86, 87])
config.plugins.TSSkinSetup.runningRepeat = ConfigSelection(default='1', choices=[79, 80, 81, 82, 78])
config.plugins.TSSkinSetup.piconOledSwitchTime = ConfigInteger(default=7, limits=(0, 60))
config.plugins.TSSkinSetup.piconOledEnabled = ConfigYesNo(default=False)
config.plugins.TSSkinSetup.piconOledPath = ConfigText(default='/data/picon_oled', fixed_size=False)
config.plugins.TSSkinSetup.CaidsColoredBackgroud = ConfigYesNo(default=True)
config.plugins.TSSkinSetup.positionClock = ConfigSelection(default='<>', choices=['<>', '<>'])
config.plugins.PermanentClock.enabled = ConfigYesNo(default=False)
config.plugins.PermanentClock.position_x = ConfigInteger(default=590)
config.plugins.PermanentClock.position_y = ConfigInteger(default=35)
config.plugins.TSWeather = ConfigSubsection()
config.plugins.TSWeather.locationIndex = ConfigInteger(default=0)
config.plugins.TSWeather.locationList = ConfigText(default='bredene', fixed_size=False)
config.plugins.TSWeather.woeidList = ConfigText(default='', fixed_size=False)
config.plugins.TSWeather.tempUnit = ConfigSelection(default='Celsius', choices=[('Celsius', _('Celsius')), ('Fahrenheit', _('Fahrenheit'))])
config.plugins.TSWeather.satMap = ConfigSelection(default='europesat', choices=[
 (
  'europesat', _('Europe')),
 (
  'germany_sat', _('Germany')),
 (
  'france_sat', _('France')),
 (
  'italy_sat', _('Italy')),
 (
  'uksat', _('UK')),
 (
  'scand_sat', _('Scandinavia')),
 (
  'euro-africasat', _('Europe-Africa')),
 (
  'africasat', _('Africa')),
 (
  'mideastsat', _('Middle East')),
 (
  'russia_sat', _('Russia')),
 (
  'afghan_sat', _('Afghanistan')),
 (
  'india_sat', _('India')),
 (
  'indian_oce_sat', _('Indian Ocean')),
 (
  'asiasat', _('Asia')),
 (
  'cen_asiasat', _('Central Asia')),
 (
  'east_asiasat', _('East Asia')),
 (
  'japan_sat', _('Japan')),
 (
  'aussiesat', _('Australia')),
 (
  'new_zealsat', _('New Zealand')),
 (
  'canadasat', _('North America')),
 (
  'cenamersat', _('Central America')),
 (
  'caribsat', _('Caribbean')),
 (
  'gomex_sat', _('Gulf of Mexico')),
 (
  'mexsat', _('Mexico')),
 (
  'brazil_sat', _('Brazil')),
 (
  'nwbrazilsat', _('Northwest Brazil')),
 (
  'nebrazilsat', _('Northeast Brazil')),
 (
  'sbrazilsat', _('South Brazil')),
 (
  'colomven_sat', _('Venezuela')),
 (
  'sat_argent', _('Argentina')),
 (
  'atl_oce_sat', _('Atlantic Ocean')),
 (
  'pac_oce_sat', _('Pacific Ocean')),
 (
  'pacglobsat', _('Pacific Global')),
 (
  'goesdisk', _('Western Hemisphere'))])
cities_s = [x for x in config.plugins.TSWeather.locationList.value.split('|') if x]
cityChoices = getChoices(cities_s) if len(cities_s) != 0 else [(config.plugins.TSWeather.locationList.value, config.plugins.TSWeather.locationList.value)]
woeid_s = [x for x in config.plugins.TSWeather.woeidList.value.split('|') if x]
woeidChoices = getChoices(woeid_s) if len(woeid_s) != 0 else [(config.plugins.TSWeather.woeidList.value, config.plugins.TSWeather.woeidList.value)]
_loc_idx = config.plugins.TSWeather.locationIndex.value
if not 0 <= _loc_idx < len(cityChoices):
    _loc_idx = 0
config.plugins.TSWeather.location = ConfigSelection(default=_as_str(cityChoices[_loc_idx][0]), choices=cityChoices)
config.plugins.TSWeather.woeid = ConfigSelection(default=_as_str(woeidChoices[_loc_idx][0]), choices=woeidChoices)

class TSSkinSetup(ConfigListScreen, Screen):
    desktopSize = getDesktop(0).size()
    if desktopSize.width() == 1920:
        skin = '\n        <screen name="TSSkinSetup" position="center,200" size="1300,720" title="TSimage Setup">\n            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png"    position="50,640"  size="200,40" alphatest="blend" />\n            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green-big.png"  position="360,640" size="200,40" alphatest="blend" />\n            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/yellow-big.png" position="670,640" size="200,40" alphatest="blend" />\n            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/blue-big.png"   position="980,640" size="200,40" alphatest="blend" />\n            <widget name="key_red"    position="50,640"  size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" transparent="1" />\n            <widget name="key_green"  position="360,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" transparent="1" />\n            <widget name="key_yellow" position="670,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" transparent="1" />\n            <widget name="key_blue"   position="980,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" transparent="1" />\n            <widget name="key_ok"     position="1220,636" size="48,48" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_ok-big.png" transparent="1" alphatest="blend" />\n            <widget name="config"     position="20,30" size="1260,600" zPosition="2" itemHeight="40" enableWrapAround="1" scrollbarMode="showOnDemand" transparent="1" />\n        </screen>\n        '
    else:
        skin = '\n        <screen name="TSSkinSetup" position="center,77" size="920,600" title="TSimage Setup">\n            <widget name="config" position="20,20" size="880,490" enableWrapAround="1" scrollbarMode="showOnDemand" transparent="1" zPosition="1" />\n            <eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff" />\n            <ePixmap name="red"    position="70,545"  zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png"    transparent="1" alphatest="blend" />\n            <ePixmap name="green"  position="280,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_green.png"  transparent="1" alphatest="blend" />\n            <ePixmap name="yellow" position="490,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_yellow.png" transparent="1" alphatest="blend" />\n            <ePixmap name="blue"   position="700,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_blue.png"   transparent="1" alphatest="blend" />\n            <widget name="key_red"    position="70,550"  size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" />\n            <widget name="key_green"  position="280,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" />\n            <widget name="key_yellow" position="490,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" />\n            <widget name="key_blue"   position="690,550" size="150,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" />\n            <widget name="key_ok"     position="870,550" size="30,30" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_ok.png" transparent="1" alphatest="blend" />\n        </screen>\n        '

    def __init__(self, session):
        Screen.__init__(self, session)
        if config.plugins.TSPanel.Type.value == 'list' or os_path.exists('/usr/share/enigma2/' + config.skin.primary_skin.value.replace('skin.xml', 'tsimage/icons/')):
            self['setupActions'] = ActionMap([
             'SetupActions', 'ColorActions'], {'ok': (self.keyOk), 'cancel': (self.keycancel), 'red': (self.keycancel), 'green': (self.keySave), 
               'yellow': (self.skinEdit), 'save': (self.keySave)}, -2)
            self['key_blue'] = Button(' ')
        else:
            self['setupActions'] = ActionMap([
             'SetupActions', 'ColorActions'], {'ok': (self.keyOk), 'cancel': (self.keycancel), 'red': (self.keycancel), 'green': (self.keySave), 
               'yellow': (self.skinEdit), 'blue': (self.panelIconsDown), 'save': (self.keySave)}, -2)
            self['key_blue'] = Button(_('Panel icons'))
        self['key_ok'] = Pixmap()
        self['key_green'] = Button(_('Save'))
        self['key_red'] = Button(_('Cancel'))
        if os_path.exists('/usr/share/enigma2/' + config.skin.primary_skin.value.replace('skin.xml', 'themes.xml')):
            self['key_yellow'] = Button(_('Skin themes'))
        else:
            self['key_yellow'] = Button(_('Skin options'))
        self.list = []
        ConfigListScreen.__init__(self, self.list, session=self.session)
        self['config'].onSelectionChanged.append(self.selectionChanged)
        self.fistNeutrinostatus = config.plugins.TSSkinSetup.neutrino.value
        self.fistSIBstatus = config.plugins.SecondInfoBar.Mode.value
        self.fistMediaPanelstatus = config.plugins.TSSkinSetup.TSiMediaPanelenabled.value
        self.firstTempUnit = config.plugins.TSWeather.tempUnit.value
        self.firstLocation = config.plugins.TSWeather.location.value
        self.firstWoeid = config.plugins.TSWeather.woeid.value
        self.createSetup()
        self.setTitle(_('TSimage Setup'))
        return

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.checkListentrys()
        return

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.checkListentrys()
        return

    def selectionChanged(self):
        cur = self['config'].getCurrent()
        show_ok = False
        if cur and len(cur) >= 2:
            ce = cur[1]
            if ce in (config.plugins.TSSkinSetup.positionClock,
             config.plugins.TSSkinSetup.picon1Path,
             config.plugins.TSSkinSetup.picon2Path,
             config.plugins.TSWeather.location):
                show_ok = True
        self['key_ok'].show() if show_ok else self['key_ok'].hide()
        return

    def checkListentrys(self):
        cur = self['config'].getCurrent()
        if not cur:
            return
        else:
            ce = cur[1]
            if ce == config.plugins.TSWeather.location:
                woeids = config.plugins.TSWeather.woeid.getChoices()
                index = config.plugins.TSWeather.location.getIndex()
                val = woeids[index][0] if 0 <= index < len(woeids) else '0'
                config.plugins.TSWeather.woeid.value = _as_str(val)
                config.plugins.TSWeather.locationIndex.value = index
            if ce == config.plugins.SecondInfoBar.Mode or cur == getattr(self, 'picon1path', None) or cur == getattr(self, 'picon2path', None) or ce == config.plugins.TSSkinSetup.typewriter or ce == config.plugins.TSSkinSetup.runningText or ce == config.plugins.TSSkinSetup.piconOledEnabled or ce == config.plugins.PermanentClock.enabled:
                self.createSetup()
            if ce == config.plugins.TSSkinSetup.positionClock:
                try:
                    from Plugins.Extensions.PermanentClock.PermanentClock import pClock, PermanentClockPositioner
                    if pClock.dialog is None:
                        pClock.gotSession(self.session)
                    pClock.dialog.hide()
                    self.session.openWithCallback(self.positionerCallback, PermanentClockPositioner)
                except Exception:
                    pass

            return

    def positionerCallback(self, callback=None):
        try:
            from Plugins.Extensions.PermanentClock.PermanentClock import pClock
            pClock.showHide()
        except Exception:
            pass

        return

    def createSetup(self):
        l = []
        l.append(getConfigListEntry(_('TS Panel type'), config.plugins.TSPanel.Type))
        l.append(getConfigListEntry(_('Enable media panel on pvr/video button'), config.plugins.TSSkinSetup.TSiMediaPanelenabled))
        l.append(getConfigListEntry(_('Enable permenant clock'), config.plugins.PermanentClock.enabled))
        if config.plugins.PermanentClock.enabled.value:
            l.append(getConfigListEntry(_('Change permanent clock position'), config.plugins.TSSkinSetup.positionClock))
        if config.skin.primary_skin.value != 'hd_glass16/skin.xml':
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/Pauli/plugin.pyo'):
                l.append(getConfigListEntry(_('Enable Neutrino Keymap'), config.plugins.TSSkinSetup.neutrino))
            l.append(getConfigListEntry(_('Second-InfoBar working mode'), config.plugins.SecondInfoBar.Mode))
            if config.plugins.SecondInfoBar.Mode.value != 'nothing':
                l.append(getConfigListEntry(_('Second-InfoBar Timeout [sec] (0=wait for OK)'), config.plugins.SecondInfoBar.TimeOut))
                l.append(getConfigListEntry(_('Hide Infobar if Second-InfoBar shown'), config.plugins.SecondInfoBar.HideNormalIB))
            self.picon1path = getConfigListEntry(_('Picon infobar path'), config.plugins.TSSkinSetup.picon1Path)
            l.append(self.picon1path)
            self.picon2path = getConfigListEntry(_('Picon channel selection path'), config.plugins.TSSkinSetup.picon2Path)
            l.append(self.picon2path)
            l.append(getConfigListEntry(_('Enable picon LCD/Oled'), config.plugins.TSSkinSetup.piconOledEnabled))
            if config.plugins.TSSkinSetup.piconOledEnabled.value:
                l.append(getConfigListEntry(_('Picon LCD/Oled switch time [0-60 sec] (0=disabled)'), config.plugins.TSSkinSetup.piconOledSwitchTime))
                l.append(getConfigListEntry(_('Picon LCD/Oled path'), config.plugins.TSSkinSetup.piconOledPath))
            l.append(getConfigListEntry(_('Enable typewriter in infobar'), config.plugins.TSSkinSetup.typewriter))
            if config.plugins.TSSkinSetup.typewriter.value:
                l.append(getConfigListEntry(_('Typewriter speed [msec]'), config.plugins.TSSkinSetup.typingSpeed))
            l.append(getConfigListEntry(_('Enable running text in extended description'), config.plugins.TSSkinSetup.runningText))
            if config.plugins.TSSkinSetup.runningText.value:
                l.append(getConfigListEntry(_('Running text start time [sec]'), config.plugins.TSSkinSetup.runningStartTime))
                l.append(getConfigListEntry(_('Repeat running text'), config.plugins.TSSkinSetup.runningRepeat))
            l.append(getConfigListEntry(_('Enable CAIDs colored background'), config.plugins.TSSkinSetup.CaidsColoredBackgroud))
        l.append(getConfigListEntry(_('Weather City'), config.plugins.TSWeather.location))
        l.append(getConfigListEntry(_('Weather Unit'), config.plugins.TSWeather.tempUnit))
        l.append(getConfigListEntry(_('Weather satellite map'), config.plugins.TSWeather.satMap))
        self.list = l
        self['config'].setList(self.list)
        return

    def keySave(self):
        try:
            config.plugins.TSWeather.locationIndex.save()
            config.plugins.TSWeather.woeid.save()
        except Exception:
            pass

        for entry in self['config'].list or []:
            try:
                ce = entry[1]
                ce.save()
            except Exception:
                pass

        try:
            configfile.save()
        except TypeError:
            print '[TSimageSetup] configfile.save() TypeError, continuing (see /tmp/config_bad.txt if present)'
            try:
                from Screens.MessageBox import MessageBox
                self.session.open(MessageBox, _('A bad config entry (from another plugin) prevented saving all settings.\nI wrote a suspect list to /tmp/config_bad.txt.\nYour TSimage changes are applied for this session.'), MessageBox.TYPE_INFO, timeout=6)
            except Exception:
                pass

        from os import system as os_system
        if self.fistNeutrinostatus and not config.plugins.TSSkinSetup.neutrino.value:
            os_system('touch /tmp/.neutrinooff')
        if not self.fistNeutrinostatus and config.plugins.TSSkinSetup.neutrino.value:
            os_system('touch /tmp/.neutrinoon')
        if self.fistSIBstatus == 'onlysib' and config.plugins.SecondInfoBar.Mode.value != 'onlysib':
            os_system('touch /tmp/.sibonlyoff')
        if self.fistSIBstatus != 'onlysib' and config.plugins.SecondInfoBar.Mode.value == 'onlysib':
            os_system('touch /tmp/.sibonlyon')
        if self.fistMediaPanelstatus and not config.plugins.TSSkinSetup.TSiMediaPanelenabled.value:
            os_system('touch /tmp/.mediaoff')
        if not self.fistMediaPanelstatus and config.plugins.TSSkinSetup.TSiMediaPanelenabled.value:
            os_system('touch /tmp/.mediaon')
        if self.fistSIBstatus == 'sibepg' and config.plugins.SecondInfoBar.Mode.value == 'sib':
            os_system('touch /tmp/.sibepgoff')
        if self.fistSIBstatus == 'sib' and config.plugins.SecondInfoBar.Mode.value == 'sibepg':
            os_system('touch /tmp/.sibepgon')
        if self.firstWoeid != config.plugins.TSWeather.woeid.value or self.firstLocation != config.plugins.TSWeather.location.value or self.firstTempUnit != config.plugins.TSWeather.tempUnit.value:
            try:
                from Components.WeatherYahoo import weatheryahoo
                weatheryahoo.getData(config.plugins.TSWeather.woeid.value)
            except Exception:
                pass

        self.close(True)
        return

    def keyOk(self):
        cur = self['config'].getCurrent()
        if not cur:
            return
        ce = cur[1]
        if ce == config.plugins.TSSkinSetup.positionClock:
            self.checkListentrys()
        elif config.skin.primary_skin.value != 'hd_glass16/skin.xml' and (ce == config.plugins.TSSkinSetup.picon1Path or ce == config.plugins.TSSkinSetup.picon2Path):
            try:
                from Plugins.TSimage.TSimagePanel.something import TSiPiconEdit
                self.session.open(TSiPiconEdit)
            except Exception:
                pass

        elif ce == config.plugins.TSWeather.location:
            self.changeCity()
        return

    def changeCity(self):
        current = config.plugins.TSWeather.location.value
        title = _('Enter city name')
        try:
            from Screens.VirtualKeyBoard import VirtualKeyBoard
            self.session.openWithCallback(self._cityEntered, VirtualKeyBoard, title=title, text=current)
        except Exception:
            try:
                from Screens.InputBox import InputBox
                self.session.openWithCallback(self._cityEntered, InputBox, title=title, text=current)
            except Exception:
                pass

        return

    def _cityEntered(self, newname=None):
        if not newname:
            return
        name = newname.strip()
        if not name:
            return
        cities = [x for x in (config.plugins.TSWeather.locationList.value or '').split('|') if x]
        if name not in cities:
            cities.append(name)
            config.plugins.TSWeather.locationList.value = ('|').join(_as_str(c) for c in cities)
        wlist = [x for x in (config.plugins.TSWeather.woeidList.value or '').split('|') if x]
        while len(wlist) < len(cities):
            wlist.append('0')

        config.plugins.TSWeather.woeidList.value = ('|').join(_as_str(w) for w in wlist)
        locs = getChoices(cities)
        config.plugins.TSWeather.location.setChoices(locs)
        config.plugins.TSWeather.location.setValue(_as_str(name))
        config.plugins.TSWeather.location.save()
        woeids = getChoices(wlist)
        config.plugins.TSWeather.woeid.setChoices(woeids)
        idx = config.plugins.TSWeather.location.getIndex()
        config.plugins.TSWeather.locationIndex.value = idx
        config.plugins.TSWeather.woeid.value = _as_str(woeids[idx][0])
        config.plugins.TSWeather.woeid.save()
        configfile.save()
        try:
            from Components.WeatherYahoo import weatheryahoo
            weatheryahoo.getData(name)
        except Exception:
            pass

        self.firstLocation = name
        self.createSetup()
        return

    def updateCity(self, index, locations, woeids):
        config.plugins.TSWeather.location.setChoices(locations)
        config.plugins.TSWeather.location.setValue(locations[index][0])
        config.plugins.TSWeather.location.save()
        config.plugins.TSWeather.woeid.setChoices(woeids)
        config.plugins.TSWeather.woeid.setValue(woeids[index][0])
        config.plugins.TSWeather.woeid.save()
        configfile.save()
        try:
            from Components.WeatherYahoo import weatheryahoo
            weatheryahoo.getData(config.plugins.TSWeather.woeid.value)
        except Exception:
            pass

        self.firstWoeid = config.plugins.TSWeather.woeid.value
        self.firstLocation = config.plugins.TSWeather.location.value
        self.createSetup()
        return

    def keycancel(self):
        try:
            from Plugins.Extensions.PermanentClock.PermanentClock import pClock
            if pClock.dialog is None:
                pClock.gotSession(self.session)
            pClock.showHide()
        except Exception:
            pass

        self.keyCancel()
        return

    def skinEdit(self):
        self.session.open(TSiSkinThemes)
        return

    def panelIconsDown(self):
        self.session.open(PanelIconslist)
        return

    def positionerCallback(self, callback=None):
        pClock.showHide()
        return


class TSiSkinThemes(ConfigListScreen, Screen):
    skin_1280 = '\n    <screen name="TSiSkinThemes" position="center,77" size="920,600" title="TSimage Setup">\n        <widget name="config" position="20,20" size="880,490" enableWrapAround="1" scrollbarMode="showOnDemand" transparent="1" zPosition="1" />\n        <eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff" />\n        <ePixmap name="red"   position="250,540" size="140,40" zPosition="1" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" transparent="1" alphatest="on" />\n        <ePixmap name="green" position="460,540" size="140,40" zPosition="1" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_green.png" transparent="1" alphatest="on" />\n        <widget name="waiting" position="20,0" size="880,550" font="Regular;22" transparent="1" halign="center" valign="center" />\n        <widget name="key_red" position="250,550" size="140,40" zPosition="2" font="Regular;20" transparent="1" halign="center" valign="center" />\n        <widget name="key_green" position="460,550" size="140,40" zPosition="2" font="Regular;20" transparent="1" halign="center" valign="center" />\n    </screen>\n    '
    skin_1920 = '\n    <screen name="TSiSkinThemes" position="center,200" size="1300,720" title="TSimage Setup">\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png"   position="375,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green-big.png" position="725,640" size="200,40" alphatest="blend" />\n        <widget name="key_red"   position="375,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n        <widget name="key_green" position="725,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n        <widget name="waiting" position="20,30" size="1260,600" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n        <widget name="config"  position="20,30" size="1260,600" zPosition="2" itemHeight="40" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n    </screen>\n    '
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session):
        Screen.__init__(self, session)
        self['setupActions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': (self.keySave), 
           'cancel': (self.keyCancel), 'red': (self.keyCancel), 'green': (self.keySave)}, -2)
        self['key_green'] = Button(_('Save'))
        self['key_red'] = Button(_('Cancel'))
        self['waiting'] = Label()
        self['preview'] = Pixmap()
        self.list = []
        self.filename = '/usr/share/enigma2/' + config.skin.primary_skin.value.replace('skin.xml', 'themes.xml')
        ConfigListScreen.__init__(self, self.list, session=self.session)
        self.theme_active_index = 0
        self.theme_old_index = 0
        self.sub_actVal = 'N/A'
        self.titleOffset_actVal = '0,0'
        self.screentype_actVal = '1'
        self.colorthemes_list = []
        self.theme_type = []
        self.theme_choices = []
        self.theme_bsWindow = []
        self.theme_titleOffset = []
        self.theme_screentype = []
        self.theme_screenenable = []
        self.line_list_tspanel = []
        self.line_list_extplugins = []
        self.selectioncolor_choices_list = [
         'N/A']
        self.screen_type = None
        self.icons_type = 'icons'
        self.theme_screen_blocks = []
        self.infobar_mode = None
        self.chanselect_mode = None
        self.infobar_selected_by_theme = {}
        self.chanselect_selected_by_theme = {}
        self.timer = eTimer()
        if os_path.exists(self.filename):
            self.timer_conn = self.timer.timeout.connect(self.LoadThemesXml)
            self.setTitle(_('Skin themes'))
            self['waiting'].setText(_('Loading themes, please wait...'))
        else:
            self.timer_conn = self.timer.timeout.connect(self.LoadSkinXml)
            self.setTitle(_('Skin options'))
            self['waiting'].setText(_('Loading skin, please wait...'))
        self.timer.start(200, 1)
        self.picload = ePicLoad()
        self.picload_conn = self.picload.PictureData.connect(self.showPic)
        self.onLayoutFinish.append(self.setConf)
        return

    def _get_block_bounds(self, line_list, screen_name):
        start = -1
        depth = 0
        for i, ln in enumerate(line_list):
            il = ln.strip()
            if start < 0:
                if il.startswith('<screen ') and 'name="%s"' % screen_name in il:
                    start = i
                    depth = 1
            else:
                if il.startswith('<screen '):
                    depth += 1
                if il.startswith('</screen>'):
                    depth -= 1
                    if depth == 0:
                        return (start, i)

        return (-1, -1)

    def _strip_marked_block_for_screen(self, body_lines, screen_name):
        start_idx = end_idx = -1
        for i, ln in enumerate(body_lines):
            if 'THEME-INSERT-START:%s' % screen_name in ln:
                start_idx = i
            if 'THEME-INSERT-END:%s' % screen_name in ln:
                end_idx = i

        if start_idx >= 0 and end_idx > start_idx:
            return body_lines[:start_idx] + body_lines[end_idx + 1:]
        return body_lines

    def _inject_screen_block(self, line_list, screen_name, insert_lines):
        b = self._get_block_bounds(line_list, screen_name)
        if b[0] < 0:
            return line_list
        head = line_list[:b[0]]
        body = line_list[b[0]:b[1] + 1]
        tail = line_list[b[1] + 1:]
        body = self._strip_marked_block_for_screen(body, screen_name)
        if not insert_lines:
            return head + body + tail
        insert_at = 1
        if screen_name == 'InfoBar':
            for i, ln in enumerate(body):
                if '<!--/* TSUpdater -->' in ln:
                    insert_at = i + 1
                    break

        marked = [
         '    <!-- THEME-INSERT-START:%s -->\n' % screen_name]
        for ln in insert_lines:
            s = ln
            if not isinstance(s, basestring):
                try:
                    s = s.decode('utf-8')
                except Exception:
                    s = str(s)

            if not s.endswith('\n'):
                s += '\n'
            if not s.startswith(' '):
                s = '    ' + s
            marked.append(s)

        marked.append('    <!-- THEME-INSERT-END:%s -->\n' % screen_name)
        body[insert_at:insert_at] = marked
        return head + body + tail

    def LoadThemesXml(self):
        self.selectioncolor_name = []
        self.selectioncolor_choices_list = []
        self.themes = ET.parse(self.filename)
        k = -1
        for colortheme in self.themes.findall('colortheme'):
            k += 1
            found = False
            self.color_choices = []
            self.selectioncolor_choices = []
            self.skinParamtersNames = []
            self.skinThemeValues = []
            self.theme_choices.append((colortheme.get('name'), _(colortheme.get('name'))))
            self.theme_type.append(colortheme.get('type'))
            self.theme_bsWindow.append(colortheme.get('bsWindow') or 'N/A')
            self.theme_titleOffset.append(colortheme.get('titleOffset') or 'N/A')
            self.theme_screentype.append(colortheme.get('screenType') or 'N/A')
            self.theme_screenenable.append(colortheme.get('enableScreentypeSelection') in ('1',
                                                                                           'Yes',
                                                                                           'yes',
                                                                                           'True',
                                                                                           'true'))
            if colortheme.get('value') == 'active':
                self.theme_active_index = k
                self.theme_old_index = k
            for selectioncolorname in colortheme.findall('.//selectioncolors'):
                found = True
                self.selectioncolor_name.append(selectioncolorname.get('name'))

            if not found:
                self.selectioncolor_name.append('N/A')
                self.selectioncolor_choices.append(('N/A', _('N/A')))
            else:
                for selectioncolor in colortheme.findall('.//selectioncolor'):
                    self.selectioncolor_choices.append((selectioncolor.get('value'), _(selectioncolor.get('name'))))

            default_selcolor = self.selectioncolor_choices[0][0]
            for color in colortheme.findall('.//color'):
                if color.get('name') == self.selectioncolor_name[-1]:
                    default_selcolor = color.get('value')
                self.color_choices.append((color.get('value'), _(color.get('name'))))
                self.skinParamtersNames.append('<color name="%s"' % color.get('name'))
                self.skinThemeValues.append('%s' % color.get('value'))

            self.selectioncolor_choices_list.append(ConfigSelection(self.selectioncolor_choices, default=default_selcolor))
            self.colorthemes_list.append((self.skinParamtersNames, self.skinThemeValues))
            screen_blocks = {}
            screens_node = colortheme.find('./screens')
            if screens_node is not None:
                for s in screens_node.findall('screen'):
                    sname = (s.get('name') or '').strip()
                    if not sname:
                        continue
                    mode = (s.get('value') or '').strip().lower() or 'default'
                    wcfg = s.find('./widget[@name="renderer"]')
                    if wcfg is not None and (wcfg.get('value') or '').strip():
                        mode = (wcfg.get('value') or '').strip().lower()
                    lines = []
                    for child in list(s):
                        if child.tag == 'widget' and (child.get('name') or '') == 'renderer':
                            continue
                        try:
                            xml = ET.tostring(child)
                            if not isinstance(xml, basestring):
                                xml = xml.decode('utf-8')
                        except Exception:
                            xml = ''

                        if xml:
                            if not xml.endswith('\n'):
                                xml += '\n'
                            lines.append(xml)

                    if sname not in screen_blocks:
                        screen_blocks[sname] = {}
                    screen_blocks[sname][mode] = lines

            self.theme_screen_blocks.append(screen_blocks)

        if k != -1:
            self.LoadSkinXml()
        else:
            self['waiting'].setText('No skin themes found. Please check your themes.xml file !')
        return

    def LoadSkinXml(self):
        f = open('/usr/share/enigma2/' + config.skin.primary_skin.value, 'r')
        line = 'dummy line'
        self.line_list = []
        self.screennameList = []
        self.screennumberList = []
        if len(self.theme_screentype) > 0:
            self.screennumberList.append(self.theme_screentype[self.theme_active_index])
        while line:
            line = f.readline()
            iline = line.strip()
            if iline.startswith('<sub name="Subtitle_TTX"'):
                s = iline.split(' ')
                value = s[2].split(';')
                self.sub_actVal = value[1].replace('"', '')
            if len(self.theme_titleOffset) > 0:
                if iline.startswith('<title offset=') and self.theme_titleOffset[self.theme_active_index] != 'N/A':
                    s = iline.split(' ')
                    value = s[1].split('=')
                    self.titleOffset_actVal = value[1].replace('"', '')
            if len(self.theme_screentype) > 0:
                if iline.startswith('<screen name="#') and self.theme_screentype[self.theme_active_index] != 'N/A':
                    value = iline.split('#')[1]
                    tmp = value.split('-')
                    if len(tmp) > 1:
                        if tmp[0] not in self.screennameList:
                            self.screennameList.append(tmp[0])
                        if tmp[1] not in self.screennumberList:
                            self.screennumberList.append(tmp[1])
                self.screentype_actVal = self.theme_screentype[self.theme_active_index]
            self.line_list.append(line)

        f.close()
        self.screennumberList.sort()
        self['waiting'].setText('')
        self.timer.stop()
        self.theme_choices_list = []
        if self.theme_choices:
            if self.selectioncolor_name[self.theme_active_index] != 'N/A':
                selectioncolor_active_value = self.colorthemes_list[self.theme_active_index][1][0]
                self.selectioncolor_choices_list[self.theme_active_index].setValue(selectioncolor_active_value)
                self.selectioncolor_choices_list[self.theme_active_index].save()
            self.theme_choices_list = ConfigSelection(self.theme_choices, default=self.theme_choices[self.theme_active_index][0])
        size_choices = []
        if self.sub_actVal != 'N/A':
            for i in range(10, 75):
                size_choices.append((str(i), str(i)))

        else:
            size_choices.append(('N/A', 'N/A'))
        self.sub_fontsize = ConfigSelection(default=self.sub_actVal, choices=size_choices)
        if len(self.theme_screentype) > 0:
            self.screen_type = ConfigSelection(default=self.theme_screentype[self.theme_active_index], choices=self.screennumberList)
        if os_path.exists(path_tspanel):
            f = open(path_tspanel, 'r')
            self.line_list_tspanel = f.readlines()
            f.close()
        if os_path.exists(path_extplugins):
            f = open(path_extplugins, 'r')
            self.line_list_extplugins = f.readlines()
            f.close()
        self.createSetup()
        return

    def WriteSkinXml(self, filename, line_list):
        if not os_path.exists(filename):
            return
        f = open(filename, 'w')
        k = 0
        old_panel_path = 'dummy'
        new_panel_path = 'dummy'
        change_path = False
        skinParameterList = self.colorthemes_list[self.theme_active_index][0] if self.colorthemes_list else []
        if self.theme_old_index != self.theme_active_index:
            if self.theme_bsWindow:
                old_panel_path = self.theme_bsWindow[self.theme_old_index]
                new_panel_path = self.theme_bsWindow[self.theme_active_index]
            if os_path.exists('/usr/share/enigma2/' + new_panel_path):
                change_path = True
        for line in line_list:
            newline = line
            iline = line.strip()
            if k < len(skinParameterList) and iline.startswith('<color name="'):
                skinParameter = '<color name="%s"' % iline.split('"')[1]
                if skinParameter in skinParameterList:
                    if skinParameter.find(self.selectioncolor_name[self.theme_active_index]) != -1:
                        if self.selectioncolor_name[self.theme_active_index] != 'N/A':
                            newline = line.replace(iline, '%s value="%s" />' % (
                             skinParameter, self.selectioncolor_choices_list[self.theme_active_index].value))
                    else:
                        idx = self.colorthemes_list[self.theme_active_index][0].index(skinParameter)
                        newline = line.replace(iline, '%s value="%s" />' % (
                         skinParameter, self.colorthemes_list[self.theme_active_index][1][idx]))
                    k += 1
            if iline.startswith('<sub name="Subtitle_') and self.sub_actVal != 'N/A':
                newline = line.replace(';%s"' % self.sub_actVal, ';%s"' % self.sub_fontsize.value)
            if self.theme_titleOffset and self.theme_titleOffset[self.theme_active_index] != 'N/A':
                if iline.startswith('<title offset='):
                    newline = line.replace('"%s"' % self.titleOffset_actVal, '"%s"' % self.theme_titleOffset[self.theme_active_index])
            if self.theme_screentype:
                for screenname in self.screennameList:
                    if iline.startswith('<screen name="#%s-%s#"' % (screenname, self.screen_type.value)) and self.screentype_actVal != self.screen_type.value and self.screentype_actVal != 'N/A':
                        newline = line.replace('name="#%s-%s#"' % (screenname, self.screen_type.value), 'name="%s"' % screenname)
                    if iline.startswith('<screen name="%s"' % screenname) and self.screentype_actVal != self.screen_type.value and self.screentype_actVal != 'N/A':
                        newline = line.replace('name="%s"' % screenname, 'name="#%s-%s#"' % (screenname, self.screentype_actVal))

            if change_path and iline.find(old_panel_path) != -1:
                newline = line.replace(old_panel_path, new_panel_path)
            f.write('%s' % newline)

        f.close()
        return

    def WriteThemesXml(self):
        path = '/usr/share/enigma2/' + config.skin.primary_skin.value.replace('skin.xml', 'themes.xml')
        if not os_path.exists(path):
            return
        if self.theme_type[self.theme_active_index] == 'Light':
            self.icons_type = 'icons_h'
        elif self.theme_type[self.theme_active_index] == 'Dark':
            self.icons_type = 'icons_d'
        for colortheme in self.themes.findall('colortheme'):
            if colortheme.get('name') == self.theme_choices_list.value:
                colortheme.set('value', 'active')
                if self.theme_screentype[self.theme_active_index] != 'N/A':
                    colortheme.set('screenType', self.screen_type.value)
                for color in colortheme.findall('.//color'):
                    if color.get('name') == self.selectioncolor_name[self.theme_active_index]:
                        color.set('value', self.selectioncolor_choices_list[self.theme_active_index].value)

            else:
                colortheme.set('value', 'inactive')

        self.updateIconsPath()
        self.themes.write(self.filename)
        return

    def createSetup(self):
        self.list = []
        if os_path.exists('/usr/share/enigma2/' + config.skin.primary_skin.value.replace('skin.xml', 'themes.xml')):
            self.list.append(getConfigListEntry(_('Theme name'), self.theme_choices_list))
            if self.selectioncolor_name[self.theme_active_index] != 'N/A':
                self.list.append(getConfigListEntry(_('Selection color'), self.selectioncolor_choices_list[self.theme_active_index]))
            if self.theme_screentype[self.theme_active_index] != 'N/A' and self.theme_screenenable[self.theme_active_index]:
                self.list.append(getConfigListEntry(_('Screen type'), self.screen_type))
            try:
                blocks = self.theme_screen_blocks[self.theme_active_index]
            except Exception:
                blocks = {}

            ib_modes = sorted(list(blocks.get('InfoBar', {}).keys())) if isinstance(blocks, dict) else []
            if ib_modes:
                choices = [
                 (
                  'default', _('default'))] + [(m, m) for m in ib_modes]
                prev = self.infobar_selected_by_theme.get(self.theme_active_index, 'default')
                valid_values = [v for v, _lbl in choices]
                if prev not in valid_values:
                    prev = 'default'
                self.infobar_mode = ConfigSelection(default=prev, choices=choices)
                self.list.append(getConfigListEntry(_('InfoBar renderer'), self.infobar_mode))
            else:
                self.infobar_mode = None
            cs_modes = sorted(list(blocks.get('ChannelSelection', {}).keys())) if isinstance(blocks, dict) else []
            if cs_modes:
                choices = [
                 (
                  'default', _('default'))] + [(m, m) for m in cs_modes]
                prev = self.chanselect_selected_by_theme.get(self.theme_active_index, 'default')
                valid_values = [v for v, _lbl in choices]
                if prev not in valid_values:
                    prev = 'default'
                self.chanselect_mode = ConfigSelection(default=prev, choices=choices)
                self.list.append(getConfigListEntry(_('ChannelSelection renderer'), self.chanselect_mode))
            else:
                self.chanselect_mode = None
            self.getPreview()
        self.list.append(getConfigListEntry(_('Subtitles font size'), self.sub_fontsize))
        self['config'].setList(self.list)
        return

    def getPreview(self):
        preview_sufix = ''
        if self.selectioncolor_choices_list[self.theme_active_index].getText() != _('N/A'):
            preview_sufix = '_' + self.selectioncolor_choices_list[self.theme_active_index].getText()
        if self.screen_type.value in ('1', 'N/A'):
            path = '/usr/share/enigma2/' + self.theme_bsWindow[self.theme_active_index] + '/preview' + preview_sufix + '.png'
        else:
            path = '/usr/share/enigma2/' + self.theme_bsWindow[self.theme_active_index] + '/preview_' + self.screen_type.value + preview_sufix + '.png'
        if os_path.exists(path):
            self.picload.startDecode(path)
        else:
            preview_url = path.replace('/usr/share/enigma2/' + self.theme_bsWindow[self.theme_active_index] + '/preview', 'http://tunisia-dreambox.info/tsimage-feed/unstable/4.0/preview/' + self.theme_bsWindow[self.theme_active_index])
            downloadPage(preview_url, SKIN_PREVIEW_PATH).addCallback(self.showPreview).addErrback(self.errorload)
        return

    def errorload(self, error):
        print '[Skin Theme preview]:', error
        return

    def showPreview(self, data):
        if os_path.exists(SKIN_PREVIEW_PATH):
            self.picload.startDecode(SKIN_PREVIEW_PATH)
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
        ptr = self.picload.getData()
        if ptr is not None:
            self['preview'].instance.setPixmap(ptr)
            self['preview'].show()
        return

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.checkListentry_left()
        return

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.checkListentry_right()
        return

    def keySave(self):
        if self['waiting'].text == _('Saving changes, please wait...'):
            return
        if self.theme_choices:
            self.theme_choices_list.save()
            self.selectioncolor_choices_list[self.theme_active_index].save()
        self['config'].setList([])
        self['waiting'].setText(_('Saving changes, please wait...'))
        self['key_green'].hide()
        self['key_red'].hide()
        self['preview'].hide()
        self.timer_conn = self.timer.timeout.connect(self.onSave)
        self.timer.start(200, 1)
        return

    def onSave(self):
        ll_main = self.line_list[:]
        ll_ts = self.line_list_tspanel[:] if self.line_list_tspanel else self.line_list_tspanel
        ll_ext = self.line_list_extplugins[:] if self.line_list_extplugins else self.line_list_extplugins
        blocks = {}
        if self.theme_screen_blocks and self.theme_active_index < len(self.theme_screen_blocks):
            blocks = self.theme_screen_blocks[self.theme_active_index] or {}
        selected_ib = self.infobar_mode.value if self.infobar_mode is not None else self.infobar_selected_by_theme.get(self.theme_active_index, 'default')
        selected_cs = self.chanselect_mode.value if self.chanselect_mode is not None else self.chanselect_selected_by_theme.get(self.theme_active_index, 'default')
        self.infobar_selected_by_theme[self.theme_active_index] = selected_ib or 'default'
        self.chanselect_selected_by_theme[self.theme_active_index] = selected_cs or 'default'
        ib_modes = blocks.get('InfoBar', {}) if isinstance(blocks, dict) else {}
        cs_modes = blocks.get('ChannelSelection', {}) if isinstance(blocks, dict) else {}
        ib_lines = ib_modes.get(selected_ib, []) if selected_ib and selected_ib != 'default' else []
        cs_lines = cs_modes.get(selected_cs, []) if selected_cs and selected_cs != 'default' else []
        ll_main = self._inject_screen_block(ll_main, 'InfoBar', ib_lines)
        ll_main = self._inject_screen_block(ll_main, 'ChannelSelection', cs_lines)
        if isinstance(ll_ts, list) and ll_ts:
            ll_ts = self._inject_screen_block(ll_ts, 'InfoBar', ib_lines)
            ll_ts = self._inject_screen_block(ll_ts, 'ChannelSelection', cs_lines)
        if isinstance(ll_ext, list) and ll_ext:
            ll_ext = self._inject_screen_block(ll_ext, 'InfoBar', ib_lines)
            ll_ext = self._inject_screen_block(ll_ext, 'ChannelSelection', cs_lines)
        self.WriteSkinXml('/usr/share/enigma2/' + config.skin.primary_skin.value, ll_main)
        self.WriteSkinXml(path_tspanel, ll_ts if isinstance(ll_ts, list) else self.line_list_tspanel)
        self.WriteSkinXml(path_extplugins, ll_ext if isinstance(ll_ext, list) else self.line_list_extplugins)
        self.WriteThemesXml()
        self.close(True)
        return

    def checkListentry_right(self):
        if self['config'].getCurrent()[1] == self.theme_choices_list:
            if self.infobar_mode is not None:
                self.infobar_selected_by_theme[self.theme_active_index] = self.infobar_mode.value
            if self.chanselect_mode is not None:
                self.chanselect_selected_by_theme[self.theme_active_index] = self.chanselect_mode.value
            if self.theme_active_index < len(self.theme_choices) - 1:
                self.theme_active_index += 1
            else:
                self.theme_active_index = 0
            if self.theme_screentype[self.theme_active_index] != 'N/A':
                self.screen_type.value = self.theme_screentype[self.theme_active_index]
            self.createSetup()
        elif self['config'].getCurrent()[1] == self.screen_type:
            self.getPreview()
        elif self['config'].getCurrent()[1] == (self.selectioncolor_choices_list[self.theme_active_index] if self.selectioncolor_choices_list else None):
            self.getPreview()
        return

    def checkListentry_left(self):
        if self['config'].getCurrent()[1] == self.theme_choices_list:
            if self.infobar_mode is not None:
                self.infobar_selected_by_theme[self.theme_active_index] = self.infobar_mode.value
            if self.chanselect_mode is not None:
                self.chanselect_selected_by_theme[self.theme_active_index] = self.chanselect_mode.value
            if self.theme_active_index > 0:
                self.theme_active_index -= 1
            else:
                self.theme_active_index = len(self.theme_choices) - 1
            if self.theme_screentype[self.theme_active_index] != 'N/A':
                self.screen_type.value = self.theme_screentype[self.theme_active_index]
            self.createSetup()
        elif self['config'].getCurrent()[1] == self.screen_type:
            self.getPreview()
        elif self['config'].getCurrent()[1] == (self.selectioncolor_choices_list[self.theme_active_index] if self.selectioncolor_choices_list else None):
            self.getPreview()
        return

    def updateIconsPath(self):
        path = '/usr/share/enigma2/' + config.skin.primary_skin.value.replace('/skin.xml', '')
        if self.icons_type == 'icons_d':
            if os_path.exists('%s/icons_d' % path):
                os_system('mv %s/icons %s/icons_h' % (path, path))
                os_system('mv %s/icons_d %s/icons' % (path, path))
            if os_path.exists('%s/menu_d' % path):
                os_system('mv %s/menu %s/menu_h' % (path, path))
                os_system('mv %s/menu_d %s/menu' % (path, path))
            if os_path.exists('%s/tsimage/menu_d' % path):
                os_system('mv %s/tsimage/menu %s/tsimage/menu_h' % (path, path))
                os_system('mv %s/tsimage/menu_d %s/tsimage/menu' % (path, path))
            if os_path.exists('%s/buttons/key_menu_d' % path):
                os_system('mv %s/buttons/key_menu.png %s/buttons/key_menu_h.png' % (path, path))
                os_system('mv %s/buttons/key_menu_d.png %s/buttons/key_menu.png' % (path, path))
            if os_path.exists('%s/buttons/key_info_d' % path):
                os_system('mv %s/buttons/key_info.png %s/buttons/key_info_h.png' % (path, path))
                os_system('mv %s/buttons/key_info_d.png %s/buttons/key_info.png' % (path, path))
            if os_path.exists('%s/buttons/key_pvr_d' % path):
                os_system('mv %s/buttons/key_pvr.png %s/buttons/key_pvr_h.png' % (path, path))
                os_system('mv %s/buttons/key_pvr_d.png %s/buttons/key_pvr.png' % (path, path))
            if os_path.exists('%s/marker_d.png' % path):
                os_system('mv %s/marker.png %s/marker_h.png' % (path, path))
                os_system('mv %s/marker_d.png %s/marker.png' % (path, path))
            if os_path.exists('%s/bouquet_d.png' % path):
                os_system('mv %s/bouquet.png %s/bouquet_h.png' % (path, path))
                os_system('mv %s/bouquet_d.png %s/bouquet.png' % (path, path))
            if os_path.exists('%s/picon_default_d.png' % path):
                os_system('mv %s/picon_default.png %s/picon_default_h.png' % (path, path))
                os_system('mv %s/picon_default_d.png %s/picon_default.png' % (path, path))
            if os_path.exists('%s/skin_default/icons/folder_d.png' % path):
                os_system('mv %s/skin_default/icons/folder.png %s/skin_default/icons/folder_h.png' % (path, path))
                os_system('mv %s/skin_default/icons/folder_d.png %s/skin_default/icons/folder.png' % (path, path))
            os_system('touch /tmp/.changedcolor')
        elif self.icons_type == 'icons_h':
            if os_path.exists('%s/icons_h' % path):
                os_system('mv %s/icons %s/icons_d' % (path, path))
                os_system('mv %s/icons_h %s/icons' % (path, path))
            if os_path.exists('%s/menu_h' % path):
                os_system('mv %s/menu %s/menu_d' % (path, path))
                os_system('mv %s/menu_h %s/menu' % (path, path))
            if os_path.exists('%s/tsimage/menu_h' % path):
                os_system('mv %s/tsimage/menu %s/tsimage/menu_d' % (path, path))
                os_system('mv %s/tsimage/menu_h %s/tsimage/menu' % (path, path))
            if os_path.exists('%s/buttons/key_menu_h' % path):
                os_system('mv %s/buttons/key_menu.png %s/buttons/key_menu_d.png' % (path, path))
                os_system('mv %s/buttons/key_menu_h.png %s/buttons/key_menu.png' % (path, path))
            if os_path.exists('%s/buttons/key_info_h' % path):
                os_system('mv %s/buttons/key_info.png %s/buttons/key_info_d.png' % (path, path))
                os_system('mv %s/buttons/key_info_h.png %s/buttons/key_info.png' % (path, path))
            if os_path.exists('%s/buttons/key_pvr_h' % path):
                os_system('mv %s/buttons/key_pvr.png %s/buttons/key_pvr_d.png' % (path, path))
                os_system('mv %s/buttons/key_pvr_h.png %s/buttons/key_pvr.png' % (path, path))
            if os_path.exists('%s/marker_h.png' % path):
                os_system('mv %s/marker.png %s/marker_d.png' % (path, path))
                os_system('mv %s/marker_h.png %s/marker.png' % (path, path))
            if os_path.exists('%s/bouquet_h.png' % path):
                os_system('mv %s/bouquet.png %s/bouquet_d.png' % (path, path))
                os_system('mv %s/bouquet_h.png %s/bouquet.png' % (path, path))
            if os_path.exists('%s/picon_default_h.png' % path):
                os_system('mv %s/picon_default.png %s/picon_default_d.png' % (path, path))
                os_system('mv %s/picon_default_h.png %s/picon_default.png' % (path, path))
            if os_path.exists('%s/skin_default/icons/folder_h.png' % path):
                os_system('mv %s/skin_default/icons/folder.png %s/skin_default/icons/folder_d.png' % (path, path))
                os_system('mv %s/skin_default/icons/folder_h.png %s/skin_default/icons/folder.png' % (path, path))
            os_system('touch /tmp/.changedcolor')
        if self.theme_active_index != self.theme_old_index and not os_path.exists('/tmp/.changedcolor'):
            os_system('touch /tmp/.changedcolor')
        return


class TSiPiconEdit(ConfigListScreen, Screen):
    skin_1280 = '\n\n        \t<screen name="TSiPiconEdit" position="center,77" size="920,600" title="TSimage Setup" >\n                <widget name="config" position="20,20" size="880,490" enableWrapAround="1" scrollbarMode="showOnDemand" transparent="1" zPosition="1" />\n                <eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\n\t        <ePixmap name="red"    position="250,540"   zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" transparent="1" alphatest="on" />\n\t        <ePixmap name="green"  position="460,540" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_green.png" transparent="1" alphatest="on" />\n        \t<widget name="key_red" position="250,550" size="140,40" valign="center" halign="center" zPosition="2"  font="Regular;20" transparent="1" /> \n        \t<widget name="key_green" position="460,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;20" transparent="1" /> \n                </screen>'
    skin_1920 = '    <screen name="TSiPiconEdit" position="center,200" size="1300,720" title="TSimage Setup">\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png" position="375,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green-big.png" position="725,640" size="200,40" alphatest="blend" />\n        <widget name="key_red" position="375,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#940d0d" transparent="1" />\n        <widget name="key_green" position="725,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#2d872d" transparent="1" />\n        <widget name="config" position="20,30" size="1260,600" zPosition="2" itemHeight="40" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background"  transparent="1" />\n    </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session):
        Screen.__init__(self, session)
        self['setupActions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': (self.keySave), 'cancel': (self.keyCancel), 'red': (self.keyCancel), 'green': (self.keySave)}, -2)
        self['key_green'] = Button(_('Save'))
        self['key_red'] = Button(_('Cancel'))
        self.list = []
        ConfigListScreen.__init__(self, self.list, session=self.session)
        self.createSetup()
        self.setTitle(_('Edit Picon Path'))
        return

    def createSetup(self):
        self.list = []
        self.list.append(getConfigListEntry(_('Picon set') + ' 1:', config.plugins.TSSkinSetup.piconSet1))
        self.list.append(getConfigListEntry(_('Picon set') + ' 2:', config.plugins.TSSkinSetup.piconSet2))
        self.list.append(getConfigListEntry(_('Picon set') + ' 3:', config.plugins.TSSkinSetup.piconSet3))
        self.list.append(getConfigListEntry(_('Picon set') + ' 4:', config.plugins.TSSkinSetup.piconSet4))
        self.list.append(getConfigListEntry(_('Picon set') + ' 5:', config.plugins.TSSkinSetup.piconSet5))
        self['config'].setList(self.list)
        return

    def updatePathSelection(self):
        piconSet = [
         config.plugins.TSSkinSetup.piconSet1.value,
         config.plugins.TSSkinSetup.piconSet2.value,
         config.plugins.TSSkinSetup.piconSet3.value,
         config.plugins.TSSkinSetup.piconSet4.value,
         config.plugins.TSSkinSetup.piconSet5.value]
        config.plugins.TSSkinSetup.picon1Path.setChoices(piconSet)
        config.plugins.TSSkinSetup.picon1Path.setValue(self.picon1_old)
        config.plugins.TSSkinSetup.picon2Path.setChoices(piconSet)
        config.plugins.TSSkinSetup.picon2Path.setValue(self.picon2_old)
        config.plugins.TSSkinSetup.picon1Path.save()
        config.plugins.TSSkinSetup.picon2Path.save()
        return

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        return

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        return

    def keySave(self):
        self.picon1_old = config.plugins.TSSkinSetup.picon1Path.value
        self.picon2_old = config.plugins.TSSkinSetup.picon2Path.value
        for x in self['config'].list:
            x[1].save()

        configfile.save()
        self.updatePathSelection()
        self.close(True)
        return


class PanelIconslist(Screen):
    skin_1280 = '\n        \t<screen name="PanelIconslist" position="center,77" size="920,600" title="Panel icons list" >\n                <widget source="menu" render="Listbox" position="20,20" size="880,128" enableWrapAround="1" scrollbarMode="showOnDemand" transparent="1" zPosition="1" >\n\t\t                <convert type="TemplatedMultiContent">\n\t\t\t\t\t{"template": [\n\t\t\t\t\t                MultiContentEntryPixmapAlphaBlend(pos = (8, 8), size = (16, 16), png = 1), # Status Icon,\n\t\t\t\t\t\t\tMultiContentEntryText(pos = (35, 0), size = (615, 32), font=0, flags = RT_HALIGN_LEFT| RT_VALIGN_CENTER, text = 0),\n                                                ],\n\t\t\t\t\t"fonts": [gFont("Regular", 23)],\n\t\t\t\t\t"itemHeight": 32\n\t\t\t\t\t}\n\t\t\t\t</convert>\n                </widget>  \n  \t\t<widget name="preview" position="210,160" size="500,281" zPosition="5" backgroundColor="transpBlack" alphatest="blend" transparent="1" />               \n                <widget name="waiting" position="20,15" zPosition="4" size="880,416" font="Regular;22" transparent="1" halign="center" valign="center" />\n                <widget name="fspace" position="20,450" zPosition="4" size="880,80" font="Regular;22" foregroundColor="yellow" transparent="1" halign="center" valign="center" />\n                <eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\n\t        <ePixmap name="red"    position="170,540"   zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" transparent="1" alphatest="on" />\n\t        <ePixmap name="green"  position="380,540" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_green.png" transparent="1" alphatest="on" />\n\t        <ePixmap name="yellow" position="590,540" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_yellow.png" transparent="1" alphatest="on" /> \n        \t<widget name="key_red" position="170,550" size="140,40" valign="center" halign="center" zPosition="2"  font="Regular;20" transparent="1" /> \n        \t<widget name="key_green" position="380,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;20" transparent="1" /> \n                <widget name="key_yellow" position="590,555" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;20" transparent="1" />\n                </screen>'
    skin_1920 = '    <screen name="PanelIconslist" position="center,200" size="1300,720" title="Panel icons list">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png" position="50,640" size="200,40" alphatest="blend" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green-big.png" position="360,640" size="200,40" alphatest="blend" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/yellow-big.png" position="670,640" size="200,40" alphatest="blend" />\n    <widget name="key_red" position="50,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#940d0d" transparent="1" />\n    <widget name="key_green" position="360,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#2d872d" transparent="1" />\n    <widget name="key_yellow" position="670,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#bba502" transparent="1" />\n\n    <widget name="preview" position="780,20" size="500,281" transparent="1" zPosition="1" />    <widget name="fspace" position="0,570" size="1260,60" foregroundColor="yellow" backgroundColor="background" font="Regular;28" valign="center" halign="center" transparent="1" zPosition="1" />\n\n    <widget source="menu" render="Listbox" position="20,20" size="720,520" zPosition="2" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background"  transparent="1" >\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (35, 0), size = (650, 40), flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 0) ,\n    MultiContentEntryPixmapAlphaBlend(pos = (12, 12), size = (16, 16), png = 1),\n    ],\n    "fonts": [gFont("Regular", 30)],\n    "itemHeight": 40\n    }\n    </convert>\n    </widget>\n    </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session):
        Screen.__init__(self, session)
        self.greenStatus = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green.png'))
        self.greyStatus = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/grey.png'))
        self['setupActions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': (self.downloadIconSet), 'cancel': (self.close), 'red': (self.close), 'green': (self.downloadIconSet), 
           'yellow': (self.preview)}, -2)
        self['key_red'] = Button(_('Back'))
        self['key_green'] = Button(_('Download'))
        self['key_yellow'] = Button(_('Preview'))
        self['waiting'] = Label(_('Downloading Panel icons sets, please wait...'))
        self['fspace'] = Label('')
        self['preview'] = Pixmap()
        self['menu'] = List([])
        self['menu'].onSelectionChanged.append(self.selectionChanged)
        self['key_green'].hide()
        self['key_yellow'].hide()
        self.itempreview = False
        self.iteminstall = False
        self.oindex = -1
        self.getfreespace()
        self.picload = ePicLoad()
        self.picload_conn = self.picload.PictureData.connect(self.showPic)
        self.onLayoutFinish.append(self.setConf)
        self.onLayoutFinish.append(self.createPanelIconslist)
        self.setTitle(_('Select Panel icons set'))
        return

    def createPanelIconslist(self):
        selectedserverurl = 'https://raw.githubusercontent.com/fairbird/TSipanel-pyhon3/main/TSipanel.xml'
        getPage(selectedserverurl.encode('utf-8')).addCallback(self.gotPageLoad).addErrback(self.errorLoadConn)
        return

    def errorLoadConn(self, error=None):
        if error is not None:
            self['waiting'].setText(str(error.getErrorMessage()))
        return

    def gotPageLoad(self, data=None):
        if data is not None:
            xmlstr = minidom.parseString(data)
            self.iconslist = []
            idx = 0
            for plugins in xmlstr.getElementsByTagName('plugins'):
                if str(plugins.getAttribute('cont').encode('utf8')) == 'Icons-Panel-FHD':
                    for plugin in plugins.getElementsByTagName('plugin'):
                        item = plugin.getAttribute('name').encode('utf8')
                        fullname = item
                        x = item.strip()
                        endstr = x[-2:]
                        if endstr == '-p':
                            item = x[:-2]
                        elif endstr == '-d':
                            item = x[:-2]
                        elif endstr == '-b':
                            item = x[:-2]
                        urlserver = str(plugin.getElementsByTagName('url')[0].childNodes[0].data)
                        processmode, idx = checkProcessmode(item)
                        if processmode == 'install':
                            self.iconslist.append((item,
                             self.greyStatus,
                             None,
                             processmode,
                             fullname,
                             urlserver))
                        elif processmode == 'remove':
                            self.oindex = idx
                            self.iconslist.append((item,
                             self.greenStatus,
                             None,
                             processmode,
                             fullname,
                             urlserver))

                    break

            self.iconslist.sort()
            self['menu'].setList(self.iconslist)
            if self.oindex != -1:
                self['menu'].setIndex(self.oindex)
                self.selectionChanged(False)
            self['waiting'].setText('')
        else:
            self['waiting'].setText('Error processing server addons data')
        return

    def getfreespace(self):
        fspace = freespace()
        self['fspace'].setText(fspace)
        return

    def selectionChanged(self, getIndex=True):
        if getIndex:
            cindex = self['menu'].getIndex()
        else:
            cindex = self.oindex
        fullname = self.iconslist[cindex][4]
        urlserver = self.iconslist[cindex][5]
        processmode = self.iconslist[cindex][3]
        if processmode == 'remove':
            self.iteminstall = False
            self['key_green'].hide()
            self.oindex = cindex
        else:
            self.iteminstall = True
            self['key_green'].show()
        endstr = fullname[-2:]
        if endstr == '-p':
            self['key_yellow'].show()
            self.itempreview = True
            preview_url = urlserver.replace('.tar.gz', '.jpg')
            if os_path.exists(PREVIEW_PATH):
                os_remove(PREVIEW_PATH)
            downloadPage(preview_url, PREVIEW_PATH).addCallback(self.getPreview).addErrback(self.errorload)
        else:
            self['key_yellow'].hide()
            self.itempreview = False
        return

    def preview(self):
        if self.itempreview:
            cindex = self['menu'].getIndex()
            urlserver = self.iconslist[cindex][5]
            picUrlserver = urlserver.replace('.tar.gz', '.jpg')
            self.session.open(PreviewScreen, picUrlserver)
        return

    def downloadIconSet(self):
        if self.iteminstall:
            self.cindex = self['menu'].getIndex()
            item = self.iconslist[self.cindex][0]
            urlserver = self.iconslist[self.cindex][5]
            self.session.openWithCallback(self.updateInstall, TSGetMultiipk, [item], [], [urlserver], [], '', False, True)
        return

    def updateInstall(self, status):
        if os_path.exists('/tmp/.restart_e2'):
            os_remove('/tmp/.restart_e2')
        cmd = 'echo ' + self.iconslist[self.cindex][0] + ' > ' + iconpanel_conf
        os_system(cmd)
        self.iconslist[self.oindex] = (self.iconslist[self.oindex][0],
         self.greyStatus,
         None,
         'install',
         self.iconslist[self.oindex][4],
         self.iconslist[self.oindex][5])
        self.iconslist[self.cindex] = (self.iconslist[self.cindex][0],
         self.greenStatus,
         None,
         'remove',
         self.iconslist[self.cindex][4],
         self.iconslist[self.cindex][5])
        self['menu'].updateList(self.iconslist)
        self.oindex = self.cindex
        self.getfreespace()
        self.selectionChanged()
        return

    def getPreview(self, data):
        if os_path.exists(PREVIEW_PATH):
            self.picload.startDecode(PREVIEW_PATH)
        return

    def setConf(self):
        self['preview'].instance.setPixmap(gPixmapPtr())
        self['preview'].hide()
        sc = AVSwitch().getFramebufferScale()
        self._aspectRatio = eSize(sc[0], sc[1])
        self._scaleSize = self['preview'].instance.size()
        params = (self._scaleSize.width(),
         self._scaleSize.height(),
         sc[0],
         sc[1],
         False,
         1,
         '#00000000')
        self.picload.setPara(params)
        return

    def showPic(self, picInfo=''):
        ptr = self.picload.getData()
        if ptr != None:
            self['preview'].instance.setPixmap(ptr)
            self['preview'].show()
        return

    def errorload(self, error):
        print '[Plugin preview]:',
        print error
        return


return
