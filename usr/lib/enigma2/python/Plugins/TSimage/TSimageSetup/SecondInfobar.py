# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/TSimageSetup/SecondInfobar.py
# Compiled at: 2016-11-22 07:46:06
""" TS SeconInfobar v4.2 by colombo555 """
from Screens.InfoBarGenerics import InfoBarPlugins, InfoBarShowHide, InfoBarAudioSelection, InfoBarMenu, InfoBarChannelSelection, InfoBarEPG, InfoBarExtensions, InfoBarPiP, InfoBarNumberZap, NumberZap
from Components.Harddisk import harddiskmanager
from Components.PluginComponent import plugins
from Plugins.Plugin import PluginDescriptor
from Screens.ChoiceBox import ChoiceBox
from Components.Sources.Boolean import Boolean
from Components.Sources.HbbtvApplication import HbbtvApplication
from Screens.InfoBar import InfoBar
from Screens.EpgSelection import EPGSelection
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.ActionMap import ActionMap
from Components.config import config, configfile
from Tools.Directories import fileExists, SCOPE_LANGUAGE, SCOPE_PLUGINS, resolveFilename
from enigma import eTimer, eEPGCache, getDesktop, eServiceCenter, eServiceReference
from tsimage import getpaneltitle
from Screens.EventView import EventViewEPGSelect
from ServiceReference import ServiceReference
from Screens.Menu import MainMenu, mdom
from Screens.AudioSelection import AudioSelection
from Tools.BoundFunction import boundFunction
from Screens.ChannelSelection import ChannelSelection
from Screens.PluginBrowser import PluginBrowser
from Plugins.TSimage.TSimagePanel.plugin import showTSiPanel, showext, ScreenGrabberView, ScreenGrabberGlobalAction
from tsimage import getpaneltitle
if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/MerlinEPG/plugin.pyo'):
    from Plugins.Extensions.MerlinEPG.plugin import Merlin_PGII
    MerlinEPGaviable = True
else:
    MerlinEPGaviable = False
from Components.Language import language
from os import environ
import gettext

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
VERSION = 'v4.2'
DATE = '30.07.2016'
STATE_HIDDEN = 0
STATE_HIDING = 1
STATE_SHOWING = 2
STATE_SHOWN = 3
SIBbase__init__ = None
SIB_StartOnlyOneTime = False
VZ_MODE = '-1'
desktopSize = getDesktop(0).size()

class SecondInfoBar(Screen):
    skin_1280 = '\n\t\t<screen flags="wfNoBorder" name="SecondInfoBar" position="center,350" size="720,200" title="Second Infobar">\n\t\t\t<eLabel text="Your skin does not support SecondInfoBar !!!" position="0,0" size="720,200" font="Regular;22" halign="center" valign="center"/>\n\t\t</screen>'
    skin_1920 = '    <screen name="SecondInfoBar" position="0,827" size="1920,295" title="Second Infobar" flags="wfNoBorder">\n        <eLabel text="Your skin does not support SecondInfoBar !!!" position="0,0" size="1920,295" font="Regular;32" halign="center" valign="center"/>\n        </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/HbbTV/plugin.pyo'):
            self['HbbtvApplication'] = HbbtvApplication()
        else:
            self['HbbtvApplication'] = Boolean(fixed=0)
            self['HbbtvApplication'].name = ''
        self['RecordingPossible'] = Boolean(fixed=harddiskmanager.HDDCount() > 0 and config.misc.rcused.value == 1)
        self['TimeshiftPossible'] = self['RecordingPossible']
        self['ShowAudioOnYellow'] = Boolean(fixed=config.misc.rcused.value == 0)
        self['ShowTimeshiftOnYellow'] = Boolean(fixed=config.misc.rcused.value == 1)
        self['ShowEventListOnYellow'] = Boolean(fixed=config.misc.rcused.value == 2)
        self['ShowRecordOnRed'] = Boolean(fixed=config.misc.rcused.value == 1)
        self['ExtensionsAvailable'] = Boolean(fixed=1)
        self['PendingNotification'] = Boolean(fixed=0)
        return


class SecondInfoBarEPG(Screen):
    skin_1280 = '\n\t\t<screen flags="wfNoBorder" name="SecondInfoBarEPG" position="center,350" size="720,200" title="Second Infobar">\n\t\t\t<eLabel text="Your skin does not support SecondInfoBarEPG !!!" position="0,0" size="720,200" font="Regular;22" halign="center" valign="center"/>\n\t\t</screen>'
    skin_1920 = '    <screen name="SecondInfoBar" position="0,827" size="1920,295" title="Second Infobar" flags="wfNoBorder">\n        <eLabel text="Your skin does not support SecondInfoBarEPG !!!" position="0,0" size="1920,295" font="Regular;32" halign="center" valign="center"/>\n        </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/HbbTV/plugin.pyo'):
            self['HbbtvApplication'] = HbbtvApplication()
        else:
            self['HbbtvApplication'] = Boolean(fixed=0)
            self['HbbtvApplication'].name = ''
        self['RecordingPossible'] = Boolean(fixed=harddiskmanager.HDDCount() > 0 and config.misc.rcused.value == 1)
        self['TimeshiftPossible'] = self['RecordingPossible']
        self['ShowAudioOnYellow'] = Boolean(fixed=config.misc.rcused.value == 0)
        self['ShowTimeshiftOnYellow'] = Boolean(fixed=config.misc.rcused.value == 1)
        self['ShowEventListOnYellow'] = Boolean(fixed=config.misc.rcused.value == 2)
        self['ShowRecordOnRed'] = Boolean(fixed=config.misc.rcused.value == 1)
        self['ExtensionsAvailable'] = Boolean(fixed=1)
        self['PendingNotification'] = Boolean(fixed=0)
        return


def SIBautostart(reason, **kwargs):
    global SIBbase__init__
    if 'session' in kwargs:
        print '[TSyWeatherPlugin] autostart'
        session = kwargs['session']
        from Components.Sources.TSyWeather import TSyWeather
        session.screen['TSyWeather'] = TSyWeather()
        if not config.skin.primary_skin.value == 'hd_glass16/skin.xml':
            print '[SIB] autostart'
            if SIBbase__init__ is None:
                SIBbase__init__ = InfoBarPlugins.__init__
            InfoBarPlugins.__init__ = InfoBarPlugins__init__
            if not fileExists('/usr/lib/enigma2/python/Plugins/SystemPlugins/NumberZapExt/plugin.pyo'):
                InfoBarNumberZap.keyNumberGlobal = keyNumberGlobal
                InfoBarNumberZap.onOpenSession = onOpenSession
            InfoBarPlugins.switch = switch
            InfoBarPlugins.swOff = swOff
            InfoBarChannelSelection.switchChannelUp = switchChannelUp
            InfoBarChannelSelection.switchChannelDown = switchChannelDown
            InfoBarChannelSelection.zapUp = zapUp
            InfoBarChannelSelection.zapDown = zapDown
            InfoBarChannelSelection.historyNext = historyNext
            InfoBarChannelSelection.historyBack = historyBack
            InfoBarChannelSelection.openServiceList = openServiceList
            InfoBarChannelSelection.onOpenSession = onOpenSession
            InfoBarMenu.mainMenu = mainMenu
            InfoBarMenu.onOpenSession = onOpenSession
            InfoBarAudioSelection.audioSelection = audioSelection
            InfoBarAudioSelection.onOpenSession = onOpenSession
            InfoBarEPG.openEventView = openEventView
            InfoBarEPG.showEventInfoPlugins = showEventInfoPlugins
            InfoBarEPG.onOpenSession = onOpenSession
            print '[ScreenGrabber] autostart'
            if not config.plugins.ScreenGrabber.items.value == 'Disabled':
                print '[ScreenGrabber] enabled on: ', config.plugins.ScreenGrabber.scut.getValue()
                InfoBarPlugins.ScreenGrabberView = ScreenGrabberView
                InfoBarPlugins.ScreenGrabberGlobalAction = ScreenGrabberGlobalAction
            else:
                print '[ScreenGrabber] disabled '
            print '[TSPanel] Keymap blue --> TSPanel'
            print '[TSPanel] Keymap green --> Plugin browser'
            InfoBarPlugins.blue = showTSiPanel
            InfoBarPlugins.green = showext
            InfoBarPlugins.onOpenSession = onOpenSession
    return


def InfoBarPlugins__init__(self):
    global SIB_StartOnlyOneTime
    global VZ_MODE
    if not SIB_StartOnlyOneTime:
        SIB_StartOnlyOneTime = True
        self['TSiPanelActions'] = ActionMap(['TSiPanelActions'], {'TSiPanel': (self.blue), 'showextensions': (self.green)}, -1)
        if not config.plugins.ScreenGrabber.items.value == 'Disabled':
            self.ScreenGrabberGlobalAction()
        if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/VirtualZap/plugin.pyo') or fileExists('/usr/lib/enigma2/python/Plugins/Extensions/VirtualZap/plugin.pyc'):
            try:
                VZ_MODE = config.plugins.virtualzap.mode.value
            except:
                VZ_MODE = '-1'

        else:
            VZ_MODE = '-1'
        if VZ_MODE == '1':
            self['SIBActions'] = ActionMap(['SIBwithVZActions'], {'ok_but': (self.switch), 'exit_but': (self.swOff)}, -1)
        else:
            self['SIBActions'] = ActionMap(['SIBActions'], {'ok_but': (self.switch), 'exit_but': (self.swOff)}, -1)
        self.hideTimer = eTimer()
        self.hideTimer_conn = self.hideTimer.timeout.connect(self.swOff)
        if config.usage.infobar_timeout.index:
            self.hideTimer.start(config.usage.infobar_timeout.index * 1000, True)
        self.SIBtimer = eTimer()
        self.SIBtimer_conn = self.SIBtimer.timeout.connect(self.swOff)
        self.SIBdialog = self.session.instantiateDialog(SecondInfoBar)
        if config.plugins.SecondInfoBar.Mode.value == 'sibepg':
            self.session.deleteDialog(self.SIBdialog)
            self.SIBdialog = self.session.instantiateDialog(SecondInfoBarEPG)
        self.SIBdialog.shown = False
        if config.plugins.SecondInfoBar.Mode.value == 'onlysib':
            self.onHide.append((lambda : self.SIBdialog.hide()))
            self.onShow.append((lambda : self.SIBdialog.show()))

        def CheckSIBtimer():
            if self.SIBtimer.isActive():
                self.SIBtimer.stop()
            return

        self.SIBdialog.onHide.append(CheckSIBtimer)
    else:
        InfoBarPlugins.__init__ = InfoBarPlugins.__init__
        InfoBarPlugins.blue = None
        InfoBarPlugins.green = None
        InfoBarPlugins.ScreenGrabberView = None
        InfoBarPlugins.ScreenGrabberGlobalAction = None
        InfoBarPlugins.switch = None
        InfoBarPlugins.swOff = None
    from Components.WeatherYahoo import weatheryahoo
    self.onLayoutFinish.append(weatheryahoo.getData)
    SIBbase__init__(self)
    return


def onOpenSession(self):
    try:
        self.hideTimer.stop()
    except:
        print '[InfobarBar onOpenSession] warning: no hideTimer found !'

    if self.shown:
        self.hide()
    try:
        if self.SIBdialog.shown:
            self.SIBdialog.hide()
    except:
        print '[InfobarBar onOpenSession] warning: no SecondInfoBar found !'

    return


def keyNumberGlobal(self, number):
    self.onOpenSession()
    if number == 0:
        if isinstance(self, InfoBarPiP) and self.pipHandles0Action():
            self.pipDoHandle0Action()
        else:
            self.servicelist.recallPrevService()
    elif self.has_key('TimeshiftActions') and not self.timeshift_enabled:
        self.session.openWithCallback(self.numberEntered, NumberZap, number)
    return


def switchChannelUp(self):
    self.onOpenSession()
    self.servicelist.moveUp()
    self.session.execDialog(self.servicelist)
    return


def switchChannelDown(self):
    self.onOpenSession()
    self.servicelist.moveDown()
    self.session.execDialog(self.servicelist)
    return


def zapUp(self):
    self.onOpenSession()
    if self.servicelist.inBouquet():
        prev = self.servicelist.getCurrentSelection()
        if prev:
            prev = prev.toString()
            while True:
                if config.usage.quickzap_bouquet_change.value:
                    if self.servicelist.atBegin():
                        self.servicelist.prevBouquet()
                self.servicelist.moveUp()
                cur = self.servicelist.getCurrentSelection()
                if not cur or not cur.flags & 64 or cur.toString() == prev:
                    break

    else:
        self.servicelist.moveUp()
    self.servicelist.zap()
    return


def zapDown(self):
    self.onOpenSession()
    if self.servicelist.inBouquet():
        prev = self.servicelist.getCurrentSelection()
        if prev:
            prev = prev.toString()
            while True:
                if config.usage.quickzap_bouquet_change.value and self.servicelist.atEnd():
                    self.servicelist.nextBouquet()
                else:
                    self.servicelist.moveDown()
                cur = self.servicelist.getCurrentSelection()
                if not cur or not cur.flags & 64 or cur.toString() == prev:
                    break

    else:
        self.servicelist.moveDown()
    self.servicelist.zap()
    return


def historyBack(self):
    self.onOpenSession()
    self.servicelist.historyBack()
    return


def historyNext(self):
    self.onOpenSession()
    self.servicelist.historyNext()
    return


def openServiceList(self):
    self.onOpenSession()
    self.session.execDialog(self.servicelist)
    return


def mainMenu(self):
    self.onOpenSession()
    print 'loading mainmenu XML...'
    menu = mdom.getroot()
    self.session.infobar = self
    self.session.openWithCallback(self.mainMenuClosed, MainMenu, menu)
    return


def audioSelection(self):
    self.onOpenSession()
    self.session.openWithCallback(self.audioSelected, AudioSelection, infobar=self)
    return


def openEventView(self):
    ref = self.session.nav.getCurrentlyPlayingServiceReference()
    self.getNowNext()
    epglist = self.epglist
    if not epglist:
        epg = eEPGCache.getInstance()
        ptr = ref and ref.valid() and epg.lookupEventTime(ref, -1)
        if ptr:
            epglist.append(ptr)
            ptr = epg.lookupEventTime(ref, ptr.getBeginTime(), +1)
            if ptr:
                epglist.append(ptr)
    else:
        self.is_now_next = True
    self.onOpenSession()
    if epglist:
        self.eventView = self.session.openWithCallback(self.closed, EventViewEPGSelect, self.epglist[0], ServiceReference(ref), self.eventViewCallback, self.openSingleServiceEPG, self.openMultiServiceEPG, self.openSimilarList)
        self.dlg_stack.append(self.eventView)
    else:
        print 'no epg for the service avail.. so we show multiepg instead of eventinfo'
        self.openMultiServiceEPG(False)
    return


def showEventInfoPlugins(self):
    self.onOpenSession()
    list = [(p.name, boundFunction(self.runPlugin, p)) for p in plugins.getPlugins(where=PluginDescriptor.WHERE_EVENTINFO)]
    if list:
        list.append((_('show single service EPG...'), self.openSingleServiceEPG))
        if config.misc.epgcache_outdated_timespan.value:
            list.append((_('show outdated service EPG...'), self.openOutdatedSingleServiceEPG))
        list.append((_('Multi EPG'), self.openMultiServiceEPG))
        self.session.openWithCallback(self.EventInfoPluginChosen, ChoiceBox, title=_('Please choose an extension...'), list=list, skin_name='EPGExtensionsList')
    else:
        self.openSingleServiceEPG()
    return


def switch(self):
    if isinstance(self, InfoBar):
        if config.plugins.SecondInfoBar.Mode.value == 'sib' or config.plugins.SecondInfoBar.Mode.value == 'sibepg':
            if not self.shown and not self.SIBdialog.shown:
                self.SIBdialog.neverAnimate()
                self.toggleShow()
            elif self.shown and not self.SIBdialog.shown:
                if config.plugins.SecondInfoBar.HideNormalIB.value:
                    self.hide()
                self.SIBdialog.show()
                SIBidx = config.plugins.SecondInfoBar.TimeOut.value
                if SIBidx > 0:
                    self.SIBtimer.start(SIBidx * 1000, True)
            elif not self.shown and self.SIBdialog.shown:
                self.SIBdialog.hide()
            elif self.shown and self.SIBdialog.shown:
                self.hide()
                self.SIBdialog.hide()
            else:
                self.toggleShow()
        elif config.plugins.SecondInfoBar.Mode.value == 'epglist':
            if self.shown:
                if MerlinEPGaviable:
                    self.session.open(Merlin_PGII, self.servicelist)
                else:
                    self.session.open(EPGSelection, self.session.nav.getCurrentlyPlayingServiceReference())
            else:
                self.toggleShow()
        elif config.plugins.SecondInfoBar.Mode.value == 'subsrv':
            if self.shown:
                service = self.session.nav.getCurrentService()
                subservices = service and service.subServices()
                if subservices.getNumberOfSubservices() > 0:
                    self.subserviceSelection()
                else:
                    self.toggleShow()
            else:
                self.toggleShow()
        else:
            self.toggleShow()
    return


def swOff(self):
    if isinstance(self, InfoBar):
        if not (self.shown or self.SIBdialog.shown) and VZ_MODE == '2':
            self.newHide()
        else:
            self.hide()
            self.SIBdialog.hide()
    return


return
