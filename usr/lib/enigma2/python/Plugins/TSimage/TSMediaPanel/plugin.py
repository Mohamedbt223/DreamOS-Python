# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/TSMediaPanel/plugin.py
# Compiled at: 2025-09-16 21:20:39
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.InfoBarGenerics import InfoBarPlugins
from Plugins.Plugin import PluginDescriptor
from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from Components.Label import Label
from Components.ConfigList import ConfigListScreen
from Components.PluginComponent import plugins
from Components.PluginList import PluginList, PluginEntryComponent
from Components.Sources.StaticText import StaticText
from Components.Pixmap import Pixmap, MovingPixmap
from Components.config import config, getConfigListEntry, ConfigSubsection, ConfigSelection
from Tools.Directories import fileExists, pathExists, resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from Tools.LoadPixmap import LoadPixmap
from Tools.HardwareInfo import HardwareInfo
from enigma import RT_HALIGN_LEFT, eListboxPythonMultiContent, gFont, ePicLoad, eSize, getDesktop
from Components.AVSwitch import AVSwitch
from os import environ, system as os_system, listdir as os_listdir, path as os_path
from Components.Language import language
import gettext
DEFAULT_ICONSPATH = '/usr/lib/enigma2/python/Plugins/TSimage/TSMediaPanel/mediabuttons/'
DEFAULT_FRAMEPATH = '/usr/lib/enigma2/python/Plugins/TSimage/TSMediaPanel/'
SKIN_ICONSPATH = '/usr/share/enigma2/' + config.skin.primary_skin.value.replace('skin.xml', 'tsimage/icons/mediabuttons/')
TSMEDIA_ICONS = [27, 
 28, 
 29, 
 30, 
 31, 
 32, 
 33, 
 34, 
 35, 
 36, 
 37]

def localeInit():
    lang = language.getLanguage()
    environ['LANGUAGE'] = lang[:2]
    gettext.bindtextdomain('enigma2', resolveFilename(SCOPE_LANGUAGE))
    gettext.textdomain('enigma2')
    gettext.bindtextdomain('TSMediaPanel', '%s%s' % (resolveFilename(SCOPE_PLUGINS), 'TSimage/TSMediaPanel/locale/'))
    return


def _(txt):
    t = gettext.dgettext('TSMediaPanel', txt)
    if t == txt:
        t = gettext.gettext(txt)
    return t


desktopSize = getDesktop(0).size()
localeInit()
language.addCallback(localeInit)
EMbaseInfoBarPlugins__init__ = None
EMStartOnlyOneTime = False
EMsession = None
InfoBar_instance = None
config.plugins.TSMediaPanel = ConfigSubsection()
config.plugins.TSMediaPanel.music = ConfigSelection(default='mediacenter', choices=[('no', _('Disabled')), ('mediacenter', _('MediaCenter')), ('merlinmp', _('MerlinMusicPlayer')), ('musiccenter', _('MusicCenter'))])
config.plugins.TSMediaPanel.files = ConfigSelection(default='filesexplorer', choices=[('no', _('Disabled')),
 (
  'filebrowser', _('Filebrowser')),
 (
  'filesexplorer', _('FilesExplorer')),
 (
  'tuxcom', _('TuxCom'))])
config.plugins.TSMediaPanel.weather = ConfigSelection(default='yWeather', choices=[('no', _('Disabled')),
 (
  'yWeather', _('TSyWeatherPlugin')),
 (
  'weather', _('WeatherPlugin')),
 (
  'foreca', _('Foreca'))])
config.plugins.TSMediaPanel.pictures = ConfigSelection(default='yes', choices=[('no', _('Disabled')), ('yes', _('Enabled'))])
config.plugins.TSMediaPanel.mytube = ConfigSelection(default='no', choices=[('no', _('Disabled')), ('yes', _('Enabled'))])
config.plugins.TSMediaPanel.vlc = ConfigSelection(default='no', choices=[('no', _('Disabled')), ('yes', _('Enabled'))])
config.plugins.TSMediaPanel.dvd = ConfigSelection(default='no', choices=[('no', _('Disabled')), ('yes', _('Enabled'))])
config.plugins.TSMediaPanel.iradio = ConfigSelection(default='no', choices=[('no', _('Disabled')), ('yes', _('Enabled'))])
config.plugins.TSMediaPanel.iptv = ConfigSelection(default='iptvplayer', choices=[('no', _('Disabled')), ('iptvplayer', _('IPTVPlayer')), ('mediaportal', _('MediaPortal')), ('tsmedia', _('TSMedia'))])
config.plugins.TSMediaPanel.timers = ConfigSelection(default='no', choices=[('no', _('Disabled')), ('yes', _('Enabled'))])

class TSMediaPanel(Screen):
    skin_1280 = ('\n<screen name="TSMediaPanel" position="0,540" title="TSimage Panel" size="1280,170" flags="wfNoBorder">\n    <widget name="frame" position="0,0" size="96,96" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSMediaPanel/frame.png" zPosition="1" alphatest="blend"/>\n    <widget source="label0" render="Label" position="0,135" size="175,20" font="Regular;20" zPosition="2" transparent="1" noWrap="1" halign="center" valign="center"/>\n    <widget name="thumb0" position="40,25" size="96,96" zPosition="2" transparent="1" alphatest="blend"/>\n\n    <widget source="label1" render="Label" position="110,135" size="175,20" font="Regular;20" zPosition="2" transparent="1" noWrap="1" halign="center" valign="center"/>\n    <widget name="thumb1" position="150,25" size="96,96" zPosition="2" transparent="1" alphatest="blend"/>\n\n    <widget source="label2" render="Label" position="220,135" size="175,20" font="Regular;20" zPosition="2" transparent="1" noWrap="1" halign="center" valign="center"/>\n    <widget name="thumb2" position="260,25" size="96,96" zPosition="2" transparent="1" alphatest="blend"/>\n\n    <widget source="label3" render="Label" position="330,135" size="175,20" font="Regular;20" zPosition="2" transparent="1" noWrap="1" halign="center" valign="center"/>\n    <widget name="thumb3" position="370,25" size="96,96" zPosition="2" transparent="1" alphatest="blend"/>\n\n    <widget source="label4" render="Label" position="440,135" size="175,20" font="Regular;20" zPosition="2" transparent="1" noWrap="1" halign="center" valign="center"/>\n    <widget name="thumb4" position="480,25" size="96,96" zPosition="2" transparent="1" alphatest="blend"/>\n\n    <widget source="label5" render="Label" position="550,135" size="175,20" font="Regular;20" zPosition="2" transparent="1" noWrap="1" halign="center" valign="center"/>\n    <widget name="thumb5" position="590,25" size="96,96" zPosition="2" transparent="1" alphatest="blend"/>\n\n    <widget source="label6" render="Label" position="660,135" size="175,20" font="Regular;20" zPosition="2" transparent="1" noWrap="1" halign="center" valign="center"/>\n    <widget name="thumb6" position="700,25" size="96,96" zPosition="2" transparent="1" alphatest="blend"/>\n\n    <widget source="label7" render="Label" position="770,135" size="175,20" font="Regular;20" zPosition="2" transparent="1" noWrap="1" halign="center" valign="center"/>\n    <widget name="thumb7" position="810,25" size="96,96" zPosition="2" transparent="1" alphatest="blend"/>\n\n    <widget source="label8" render="Label" position="880,135" size="175,20" font="Regular;20" zPosition="2" transparent="1" noWrap="1" halign="center" valign="center"/>\n    <widget name="thumb8" position="920,25" size="96,96" zPosition="2" transparent="1" alphatest="blend"/>\n\n    <widget source="label9" render="Label" position="990,135" size="175,20" font="Regular;20" zPosition="2" transparent="1" noWrap="1" halign="center" valign="center"/>\n    <widget name="thumb9" position="1030,25" size="96,96" zPosition="2" transparent="1" alphatest="blend"/>\n\n    <widget source="label10" render="Label" position="1100,135" size="175,20" font="Regular;20" zPosition="2" transparent="1" noWrap="1" halign="center" valign="center"/>\n    <widget name="thumb10" position="1140,25" size="96,96" zPosition="2" transparent="1" alphatest="blend"/>\n</screen>\n').strip()
    skin_1920 = ('\n<screen name="TSMediaPanel" position="0,920" title="TSMedia Panel" size="1920,160" flags="wfNoBorder">\n    <widget name="frame" position="0,15" size="100,100" zPosition="1" alphatest="blend"/>\n    <widget source="label0" render="Label" position="20,120" size="140,30" font="Regular;25" zPosition="2" transparent="1" noWrap="1" halign="center" valign="center"/>\n    <widget name="thumb0" position="40,15" size="100,100" zPosition="2" transparent="1" alphatest="blend"/>\n\n    <widget source="label1" render="Label" position="160,120" size="140,30" font="Regular;25" zPosition="2" transparent="1" noWrap="1" halign="center" valign="center"/>\n    <widget name="thumb1" position="180,15" size="100,100" zPosition="2" transparent="1" alphatest="blend"/>\n\n    <widget source="label2" render="Label" position="300,120" size="140,30" font="Regular;25" zPosition="2" transparent="1" noWrap="1" halign="center" valign="center"/>\n    <widget name="thumb2" position="320,15" size="100,100" zPosition="2" transparent="1" alphatest="blend"/>\n\n    <widget source="label3" render="Label" position="440,120" size="140,30" font="Regular;25" zPosition="2" transparent="1" noWrap="1" halign="center" valign="center"/>\n    <widget name="thumb3" position="460,15" size="100,100" zPosition="2" transparent="1" alphatest="blend"/>\n\n    <widget source="label4" render="Label" position="580,120" size="140,30" font="Regular;25" zPosition="2" transparent="1" noWrap="1" halign="center" valign="center"/>\n    <widget name="thumb4" position="600,15" size="100,100" zPosition="2" transparent="1" alphatest="blend"/>\n\n    <widget source="label5" render="Label" position="720,120" size="140,30" font="Regular;25" zPosition="2" transparent="1" noWrap="1" halign="center" valign="center"/>\n    <widget name="thumb5" position="740,15" size="100,100" zPosition="2" transparent="1" alphatest="blend"/>\n\n    <widget source="label6" render="Label" position="860,120" size="140,30" font="Regular;25" zPosition="2" transparent="1" noWrap="1" halign="center" valign="center"/>\n    <widget name="thumb6" position="880,15" size="100,100" zPosition="2" transparent="1" alphatest="blend"/>\n\n    <widget source="label7" render="Label" position="1000,120" size="140,30" font="Regular;25" zPosition="2" transparent="1" noWrap="1" halign="center" valign="center"/>\n    <widget name="thumb7" position="1020,15" size="100,100" zPosition="2" transparent="1" alphatest="blend"/>\n\n    <widget source="label8" render="Label" position="1140,120" size="140,30" font="Regular;25" zPosition="2" transparent="1" noWrap="1" halign="center" valign="center"/>\n    <widget name="thumb8" position="1160,15" size="100,100" zPosition="2" transparent="1" alphatest="blend"/>\n\n    <widget source="label9" render="Label" position="1280,120" size="140,30" font="Regular;25" zPosition="2" transparent="1" noWrap="1" halign="center" valign="center"/>\n    <widget name="thumb9" position="1300,15" size="100,100" zPosition="2" transparent="1" alphatest="blend"/>\n\n    <widget source="label10" render="Label" position="1420,120" size="140,30" font="Regular;25" zPosition="2" transparent="1" noWrap="1" halign="center" valign="center"/>\n    <widget name="thumb10" position="1440,15" size="100,100" zPosition="2" transparent="1" alphatest="blend"/>\n</screen>\n').strip()
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session):
        self.thumbsX = 11
        self.thumbsY = 1
        self.thumbsC = 11
        Screen.__init__(self, session)
        self.title = 'Media Panel'
        self.setTitle(self.title)
        self['actions'] = ActionMap(['WizardActions',
         'MenuActions',
         'InfobarActions',
         'ColorActions'], {'back': (self.Exit), 'ok': (self.KeyOk), 'menu': (self.MPContextMenu), 
           'showMovies': (self.Exit), 
           'left': (self.key_left), 
           'right': (self.key_right), 
           'up': (self.key_up), 
           'down': (self.key_down)}, -1)
        self['frame'] = MovingPixmap()
        for idx in range(self.thumbsC):
            self['label%d' % idx] = StaticText()
            self['thumb%d' % idx] = Pixmap()

        self.maxentry = self.thumbsC - 1
        self.index = 0
        self.onLayoutFinish.append(self.setPicloadConf)
        self.onShow.append(self.updateSummaries)
        return

    def updateSummaries(self):
        self.summaries.setText(self.title, 0)
        self.summaries.setText(self['label%d' % self.index].getText(), 1)
        return

    def checkEntry(self, image, def_path=DEFAULT_ICONSPATH):
        if os_path.exists(SKIN_ICONSPATH + image):
            path = '%s%s' % (SKIN_ICONSPATH, image)
        else:
            path = '%s%s' % (def_path, image)
        return path

    def setPicloadConf(self):
        self.picload = ePicLoad()
        sc = AVSwitch().getFramebufferScale()
        self._aspectRatio = eSize(sc[0], sc[1])
        self._scaleSize = self['thumb0'].instance.size()
        params = (self._scaleSize.width(),
         self._scaleSize.height(),
         sc[0],
         sc[1],
         config.pic.cache.value,
         int(config.pic.resize.value),
         '#00000000')
        self.picload.setPara(params)
        self.getConfig()
        self.initFrame()
        self.paintFrame()
        return

    def initFrame(self):
        self.positionlist = []
        for idx in range(self.thumbsC):
            if not self.labelIdx_list[idx] == -1:
                new_pos = self.Thumbnail_list[self.labelIdx_list[idx]]
                self['thumb%d' % idx].setPosition(new_pos[0], new_pos[1])
                self.positionlist.append((new_pos[0], new_pos[1]))
                self['thumb%d' % idx].instance.setPixmapFromFile(self.checkEntry(TSMEDIA_ICONS[idx]))
                self['label%d' % self.labelIdx_list[idx]].setText(self.label_list[idx][0])

        frame_pos = self['thumb0'].getPosition()
        self['frame'].setPosition(frame_pos[0], frame_pos[1])
        self['frame'].instance.setPixmapFromFile(self.checkEntry('frame.png', DEFAULT_FRAMEPATH))
        return

    def paintFrame(self):
        if self.maxentry < self.index or self.index < 0:
            return
        pos = self.positionlist[self.index]
        self['frame'].moveTo(pos[0], pos[1], 1)
        self['frame'].startMoving()
        return

    def getConfig(self):
        self.labelIdx_list = []
        self.Thumbnail_list = []
        self.Label_list = []
        self.label_list = []
        count = 0
        self.labelIdx_list.append(count)
        self.Thumbnail_list.append(self['thumb0'].getPosition())
        self.Label_list.append(self['label0'].getText())
        self.label_list.append((_('Movies'), 'PLAYMOVIES'))
        self.Thumbnail_list.append(self['thumb1'].getPosition())
        self.Label_list.append(self['label1'].getText())
        self.label_list.append((_('Music'), 'MUSIC'))
        if config.plugins.TSMediaPanel.music.value == 'no':
            self.labelIdx_list.append(-1)
            self['thumb1'].hide()
            self['label1'].setText('')
        else:
            count = count + 1
            self.labelIdx_list.append(count)
        self.Thumbnail_list.append(self['thumb2'].getPosition())
        self.Label_list.append(self['label2'].getText())
        self.label_list.append((_('Pictures'), 'PICTURES'))
        if config.plugins.TSMediaPanel.pictures.value == 'no':
            self.labelIdx_list.append(-1)
            self['thumb2'].hide()
            self['label2'].setText('')
        else:
            count = count + 1
            self.labelIdx_list.append(count)
        self.Thumbnail_list.append(self['thumb3'].getPosition())
        self.Label_list.append(self['label3'].getText())
        self.label_list.append((_('Timer '), 'TIMER'))
        if config.plugins.TSMediaPanel.timers.value == 'no':
            self.labelIdx_list.append(-1)
            self['thumb3'].hide()
            self['label3'].setText('')
        else:
            count = count + 1
            self.labelIdx_list.append(count)
        self.Thumbnail_list.append(self['thumb4'].getPosition())
        self.Label_list.append(self['label4'].getText())
        self.label_list.append((_('Files'), 'FILES'))
        if config.plugins.TSMediaPanel.files.value == 'no':
            self.labelIdx_list.append(-1)
            self['thumb4'].hide()
            self['label4'].setText('')
        else:
            count = count + 1
            self.labelIdx_list.append(count)
        self.Thumbnail_list.append(self['thumb5'].getPosition())
        self.Label_list.append(self['label5'].getText())
        self.label_list.append((_('DVD'), 'DVD'))
        if config.plugins.TSMediaPanel.dvd.value == 'no':
            self.labelIdx_list.append(-1)
            self['thumb5'].hide()
            self['label5'].setText('')
        else:
            count = count + 1
            self.labelIdx_list.append(count)
        self.Thumbnail_list.append(self['thumb6'].getPosition())
        self.Label_list.append(self['label6'].getText())
        self.label_list.append((_('IPTV'), 'IPTV'))
        if config.plugins.TSMediaPanel.iptv.value == 'no':
            self.labelIdx_list.append(-1)
            self['thumb6'].hide()
            self['label6'].setText('')
        else:
            count = count + 1
            self.labelIdx_list.append(count)
        self.Thumbnail_list.append(self['thumb7'].getPosition())
        self.Label_list.append(self['label7'].getText())
        self.label_list.append((_('NetRadio'), 'INTERNETRADIO'))
        if config.plugins.TSMediaPanel.iradio.value == 'no':
            self.labelIdx_list.append(-1)
            self['thumb7'].hide()
            self['label7'].setText('')
        else:
            count = count + 1
            self.labelIdx_list.append(count)
        self.Thumbnail_list.append(self['thumb8'].getPosition())
        self.Label_list.append(self['label8'].getText())
        self.label_list.append((_('MyTube'), 'MYTUBE'))
        if config.plugins.TSMediaPanel.mytube.value == 'no':
            self.labelIdx_list.append(-1)
            self['thumb8'].hide()
            self['label8'].setText('')
        else:
            count = count + 1
            self.labelIdx_list.append(count)
        self.Thumbnail_list.append(self['thumb9'].getPosition())
        self.Label_list.append(self['label9'].getText())
        self.label_list.append((_('VLC'), 'VLC'))
        if config.plugins.TSMediaPanel.vlc.value == 'no':
            self.labelIdx_list.append(-1)
            self['thumb9'].hide()
            self['label9'].setText('')
        else:
            count = count + 1
            self.labelIdx_list.append(count)
        self.Thumbnail_list.append(self['thumb10'].getPosition())
        self.Label_list.append(self['label10'].getText())
        self.label_list.append((_('Weather'), 'WEATHER'))
        if config.plugins.TSMediaPanel.weather.value == 'no':
            self.labelIdx_list.append(-1)
            self['thumb10'].hide()
            self['label10'].setText('')
        else:
            count = count + 1
            self.labelIdx_list.append(count)
        self.maxentry = count
        return

    def key_left(self):
        self.index -= 1
        if self.index < 0:
            self.index = self.maxentry
        self.summaries.setText(self['label%d' % self.index].getText(), 1)
        self.paintFrame()
        return

    def key_right(self):
        self.index += 1
        if self.index > self.maxentry:
            self.index = 0
        self.summaries.setText(self['label%d' % self.index].getText(), 1)
        self.paintFrame()
        return

    def key_up(self):
        self.index -= self.thumbsX
        if self.index < 0:
            self.index = self.maxentry
        self.summaries.setText(self['label%d' % self.index].getText(), 1)
        self.paintFrame()
        return

    def key_down(self):
        self.index += self.thumbsX
        if self.index > self.maxentry:
            self.index = 0
        self.summaries.setText(self['label%d' % self.index].getText(), 1)
        self.paintFrame()
        return

    def KeyOk(self):
        sel = self['label%d' % self.index].getText()
        self.goEntry(sel)
        return

    def goEntry(self, entry):
        self.close(entry)
        return

    def ClosecallbackFunc(self, answer=True):
        self.close()
        return

    def MPContextMenu(self):
        self.session.openWithCallback(self.Exit, TSMediaPanelConfig)
        return

    def createSummary(self):
        return TSMediaPanelSummary

    def callbackView(self, val=0):
        self.index = val
        if self.old_index != self.index:
            self.paintFrame()
        return

    def Exit(self):
        del self.picload
        self.close(self.index)
        return


def TSMediaPanelAutostart(reason, **kwargs):
    global EMbaseInfoBarPlugins__init__
    global EMsession
    if 'session' in kwargs:
        EMsession = kwargs['session']
        if EMbaseInfoBarPlugins__init__ is None:
            EMbaseInfoBarPlugins__init__ = InfoBarPlugins.__init__
        InfoBarPlugins.__init__ = InfoBarPlugins__init__
        InfoBarPlugins.pvr = pvr
        InfoBarPlugins.onOpenSession = onOpenSession
    return


def InfoBarPlugins__init__(self):
    global EMStartOnlyOneTime
    global InfoBar_instance
    if not EMStartOnlyOneTime:
        EMStartOnlyOneTime = True
        InfoBar_instance = self
        self['TSMediaPanelActions'] = ActionMap(['TSMediaPanelActions'], {'video_but': (self.pvr)}, -1)
        print '[TSMediaPanel] enabled on : pvr_key'
    else:
        InfoBarPlugins.__init__ = InfoBarPlugins.__init__
        InfoBarPlugins.pvr = None
        print '[TSMediaPanel] disabled'
    EMbaseInfoBarPlugins__init__(self)
    return


def pvr(self):
    self.onOpenSession()
    self.session.openWithCallback(MPcallbackFunc, TSMediaPanel)
    return


def notEasy(session, **kwargs):
    self.onOpenSession()
    session.openWithCallback(MPcallbackFunc, TSMediaPanel)
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


def MPcallbackFunc(answer):
    if EMsession is None:
        return
    else:
        if answer == _('Movies'):
            if InfoBar_instance:
                InfoBar_instance.showMovies()
        elif answer == _('Pictures'):
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/PicturePlayer/plugin.pyo'):
                from Plugins.Extensions.PicturePlayer.plugin import picshow
                EMsession.open(picshow)
            else:
                EMsession.open(MessageBox, text=_('Picture player is not installed!'), type=MessageBox.TYPE_ERROR)
        elif answer == _('Music'):
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/MerlinMusicPlayer2/plugin.pyo') and config.plugins.TSMediaPanel.music.value == 'merlinmp':
                from Plugins.Extensions.MerlinMusicPlayer2.plugin import iDream
                servicelist = None
                EMsession.open(iDream, servicelist)
            elif fileExists('/usr/lib/enigma2/python/Plugins/Extensions/MediaCenter/plugin.pyo') and config.plugins.TSMediaPanel.music.value == 'mediacenter':
                from Plugins.Extensions.MediaCenter.plugin import main
                main(EMsession)
            elif fileExists('/usr/lib/enigma2/python/Plugins/Extensions/MusicCenter/plugin.pyo') and config.plugins.TSMediaPanel.music.value == 'musiccenter':
                from Plugins.Extensions.MusicCenter.plugin import MusicCenterstart
                MusicCenterstart(EMsession)
            else:
                EMsession.open(MessageBox, text=_('No Music Player installed!'), type=MessageBox.TYPE_ERROR)
        elif answer == _('IPTV'):
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/plugin.pyo') and config.plugins.TSMediaPanel.iptv.value == 'iptvplayer':
                from Plugins.Extensions.IPTVPlayer.plugin import main
                main(EMsession)
            elif fileExists('/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal/plugin.pyo') and config.plugins.TSMediaPanel.iptv.value == 'mediaportal':
                from Plugins.Extensions.MediaPortal.plugin import MPmain
                MPmain(EMsession)
            elif fileExists('/usr/lib/enigma2/python/Plugins/Extensions/TSmedia/plugin.pyo') and config.plugins.TSMediaPanel.iptv.value == 'tsmedia':
                from Plugins.Extensions.TSmedia.plugin import main
                main(EMsession)
            else:
                EMsession.open(MessageBox, text=_('No IPTV Player installed!'), type=MessageBox.TYPE_ERROR)
        elif answer == _('Files'):
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/Tuxcom/plugin.pyo') and config.plugins.TSMediaPanel.files.value == 'tuxcom':
                from Plugins.Extensions.Tuxcom.plugin import TuxComStarter
                EMsession.open(TuxComStarter)
            elif fileExists('/usr/lib/enigma2/python/Plugins/Extensions/DreamExplorer/plugin.pyo') and config.plugins.TSMediaPanel.files.value == 'dreamexplorer':
                from Plugins.Extensions.DreamExplorer.plugin import DreamExplorerII
                EMsession.open(DreamExplorerII)
            elif fileExists('/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/filesexplorer.pyo') and config.plugins.TSMediaPanel.files.value == 'filesexplorer':
                from Plugins.TSimage.TSimagePanel.filesexplorer import FileExplorerII
                EMsession.open(FileExplorerII)
            elif fileExists('/usr/lib/enigma2/python/Plugins/Extensions/Filebrowser/plugin.pyo') and config.plugins.TSMediaPanel.files.value == 'filebrowser':
                from Plugins.Extensions.Filebrowser.plugin import FilebrowserScreen
                EMsession.open(FilebrowserScreen)
            else:
                EMsession.open(MessageBox, text=_('No File Manager installed!'), type=MessageBox.TYPE_ERROR)
        elif answer == _('Weather'):
            if config.plugins.TSMediaPanel.weather.value == 'yWeather':
                from TSyWeatherPlugin import TSyWeatherPlugin
                EMsession.open(TSyWeatherPlugin)
            elif fileExists('/usr/lib/enigma2/python/Plugins/Extensions/WeatherPlugin/plugin.pyo') and config.plugins.TSMediaPanel.weather.value == 'weather':
                from Plugins.Extensions.WeatherPlugin.plugin import MSNWeatherPlugin
                EMsession.open(MSNWeatherPlugin)
            elif fileExists('/usr/lib/enigma2/python/Plugins/Extensions/Foreca/plugin.pyo') and config.plugins.TSMediaPanel.weather.value == 'foreca':
                from Plugins.Extensions.Foreca.plugin import ForecaPreview
                EMsession.open(ForecaPreview)
            else:
                EMsession.open(MessageBox, text=_('No Weather Plugin installed!'), type=MessageBox.TYPE_ERROR)
        elif answer == _('DVD'):
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/DVDPlayer/plugin.pyo'):
                from Plugins.Extensions.DVDPlayer.plugin import DVDPlayer
                EMsession.open(DVDPlayer)
            else:
                EMsession.open(MessageBox, text=_('DVDPlayer Plugin is not installed!'), type=MessageBox.TYPE_ERROR)
        elif answer == _('TSMedia'):
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/TSmedia/plugin.pyo'):
                from Plugins.Extensions.TSmedia.plugin import TSmediaPanelscreen1
                EMsession.open(TSmediaPanelscreen1)
            else:
                EMsession.open(MessageBox, text=_('TSMedia Plugin is not installed!'), type=MessageBox.TYPE_ERROR)
        elif answer == _('MyTube'):
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/MyTube/plugin.pyo'):
                from Plugins.Extensions.MyTube.plugin import MyTubeMain
                MyTubeMain(EMsession)
            else:
                EMsession.open(MessageBox, text=_('MyTube Plugin is not installed!'), type=MessageBox.TYPE_ERROR)
        elif answer == _('NetRadio'):
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/InternetRadio/plugin.pyo'):
                from Plugins.Extensions.InternetRadio.InternetRadioScreen import InternetRadioScreen
                EMsession.open(InternetRadioScreen)
            else:
                EMsession.open(MessageBox, text=_('InternetRadio Plugin is not installed!'), type=MessageBox.TYPE_ERROR)
        elif answer == _('VLC'):
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/VlcPlayer/plugin.pyo'):
                from Plugins.Extensions.VlcPlayer.plugin import main
                main(EMsession)
            else:
                EMsession.open(MessageBox, text=_('VLC Player is not installed!'), type=MessageBox.TYPE_ERROR)
        elif answer == _('Timer '):
            from Screens.TimerEdit import TimerEditList
            EMsession.open(TimerEditList)
        return
        return


class TSMediaPanelConfig(ConfigListScreen, Screen):
    skin_1280 = '\n        \t<screen name="TSMediaPanelConfig" position="center,77" size="920,600" title="TS Media panel settings" >\n                <widget name="config" position="20,20" size="880,490" scrollbarMode="showOnDemand" transparent="1" zPosition="1" />\n                <eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\n\t        <ePixmap name="red"    position="170,540"   zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" transparent="1" alphatest="on" />\n\t        <ePixmap name="green"  position="380,540" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_green.png" transparent="1" alphatest="on" />\n\t        <!--ePixmap name="yellow" position="590,540" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_yellow.png" transparent="1" alphatest="on" /> --> \n        \t<eLabel text="Cancel" position="170,550" size="140,40" valign="center" halign="center" zPosition="2"  backgroundColor="background" foregroundColor="#ffffff" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" /> \n        \t<eLabel text="Save" position="380,550" size="140,40" valign="center" halign="center" zPosition="2" backgroundColor="background" foregroundColor="#ffffff" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" /> \n                <!--eLabel text="Plugins" position="590,555" size="140,40" valign="center" halign="center" zPosition="2" backgroundColor="background" foregroundColor="#ffffff" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" /> -->\n                </screen>'
    skin_1920 = '    <screen name="TSAddonsSetup" position="center,200" size="1300,720" title="Addons Manager Setup">\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png" position="375,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green-big.png" position="725,640" size="200,40" alphatest="blend" />\n        <eLabel name="key_red" text="Cancel" position="375,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#940d0d" transparent="1" />\n        <eLabel name="key_green" text="Save" position="725,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#2d872d" transparent="1" />\n        <widget name="config" position="20,30" size="1260,600" zPosition="2" itemHeight="40" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background"  transparent="1" />\n        </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session):
        Screen.__init__(self, session)
        self.setTitle(_('TS Media panel settings'))
        self.session = session
        list = []
        list.append(getConfigListEntry(_('Music player'), config.plugins.TSMediaPanel.music))
        list.append(getConfigListEntry(_('Files browser'), config.plugins.TSMediaPanel.files))
        list.append(getConfigListEntry(_('Timer'), config.plugins.TSMediaPanel.timers))
        list.append(getConfigListEntry(_('PicturePlayer'), config.plugins.TSMediaPanel.pictures))
        list.append(getConfigListEntry(_('DVD player'), config.plugins.TSMediaPanel.dvd))
        list.append(getConfigListEntry(_('IPTV Plugin'), config.plugins.TSMediaPanel.iptv))
        list.append(getConfigListEntry(_('InternetRadio Player'), config.plugins.TSMediaPanel.iradio))
        list.append(getConfigListEntry(_('YouTube Player'), config.plugins.TSMediaPanel.mytube))
        list.append(getConfigListEntry(_('VLC Player'), config.plugins.TSMediaPanel.vlc))
        list.append(getConfigListEntry(_('Weather Plugin'), config.plugins.TSMediaPanel.weather))
        ConfigListScreen.__init__(self, list)
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'green': (self.save), 'red': (self.exit), 'cancel': (self.exit)}, -1)
        return

    def save(self):
        for x in self['config'].list:
            x[1].save()

        self.close()
        return

    def exit(self):
        for x in self['config'].list:
            x[1].cancel()

        self.close()
        return


class TSMediaPanelSummary(Screen):
    if '820' in HardwareInfo().get_device_name():
        skin = '\n\t\t\t<screen position="0,0" size="96,64" id="2">\n\t\t\t\t<widget name="text0" position="1,0" size="94,30" font="Regular;13" halign="center" valign="center"/>\n                                <eLabel position="2,30" size="92,1" backgroundColor="#e16f00"/> \n\t\t\t\t<widget name="text1" position="1,34" size="94,30" font="Regular;14" halign="center" valign="center"/>\n\t\t\t</screen>'
    else:
        skin = '\n\t\t\t<screen position="0,0" size="132,64">\n\t\t\t\t<widget name="text0" position="6,0" size="120,30" font="Regular;13" halign="center" valign="center"/>\n\t\t\t\t<eLabel position="2,30" size="128,1" backgroundColor="white" /> \n\t\t\t\t<widget name="text1" position="6,34" size="120,30" font="Regular;14" halign="center" valign="center"/>\n\t\t\t</screen>'

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


return
