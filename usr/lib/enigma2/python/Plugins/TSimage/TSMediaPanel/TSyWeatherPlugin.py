# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/TSMediaPanel/TSyWeatherPlugin.py
# Compiled at: 2025-09-16 21:31:13
from __future__ import print_function
from Components.Button import Button
from Components.Label import Label
from Components.AVSwitch import AVSwitch
from enigma import eTimer, ePicLoad
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Pixmap import Pixmap
from Components.config import config, configfile, ConfigSubsection, ConfigText, ConfigSelection
from Plugins.TSimage.TSimageSetup.TSyWeatherSetup import TSyWeatherEntries
from Components.WeatherYahoo import weatheryahoo
from Tools.Directories import fileExists, SCOPE_LANGUAGE, SCOPE_PLUGINS, resolveFilename
from Components.Language import language
from enigma import getDesktop
from Tools.Downloader import downloadWithProgress
from os import environ, path as os_path, makedirs as os_makedirs, unlink as os_unlink
import gettext
try:
    unicode
except NameError:
    unicode = str

def _b(v):
    if v is None:
        return ''
    else:
        try:
            if isinstance(v, unicode):
                return v.encode('utf-8', 'ignore')
            else:
                return str(v)

        except Exception:
            try:
                return str(v)
            except Exception:
                return ''

        return


DEG = _b(u'\u')

def localeInit():
    lang = language.getLanguage()
    environ['LANGUAGE'] = lang[:2]
    gettext.bindtextdomain('enigma2', resolveFilename(SCOPE_LANGUAGE))
    gettext.textdomain('enigma2')
    gettext.bindtextdomain('TSyWeatherPlugin', '%s%s' % (resolveFilename(SCOPE_PLUGINS), 'TSimage/TSMediaPanel/locale/'))
    return


def _(txt):
    t = gettext.dgettext('TSyWeatherPlugin', txt)
    if t == txt:
        t = gettext.gettext(txt)
    return _b(t)


localeInit()
language.addCallback(localeInit)
VERSION = 'v2.0'
DATE = '24.08.2025'
daykeys = ('1', '2', '3', '4')
pluginPrintname = '[TSyWeatherPlugin Ver. %s]' % VERSION
CACHE_PATH = '/var/cache/TSyWeather/'
if os_path.exists(CACHE_PATH) is False:
    try:
        os_makedirs(CACHE_PATH, 493)
    except:
        pass

THUMB_PATH = resolveFilename(SCOPE_PLUGINS) + 'TSimage/TSMediaPanel/thumbs/'
SLIDETIME = 1
INFOLINE = True
LOOP = True
SLIDE_NR = 5

def getScale():
    return AVSwitch().getFramebufferScale()


desktopSize = getDesktop(0).size()
if not hasattr(config, 'plugins'):
    config.plugins = ConfigSubsection()
if not hasattr(config.plugins, 'TSWeather'):
    config.plugins.TSWeather = ConfigSubsection()
TSW = config.plugins.TSWeather
if not hasattr(TSW, 'locationList'):
    TSW.locationList = ConfigText(default='Antwerp', fixed_size=False)
if not hasattr(TSW, 'woeidList'):
    TSW.woeidList = ConfigText(default='51.2211,4.3997', fixed_size=False)
if not hasattr(TSW, 'locationIndex'):
    TSW.locationIndex = ConfigSelection(default='0', choices=[57, 58, 59, 60, 61])

def _split_pipe(s):
    s = s or ''
    parts = [p for p in s.split('|') if p != '']
    return parts


def _get_locations_and_ids():
    names = _split_pipe(TSW.locationList.value)
    ids = _split_pipe(TSW.woeidList.value)
    L = min(len(names), len(ids))
    if L == 0:
        names, ids = [
         'Antwerp'], ['51.2211,4.3997']
        L = 1
    locs = [(_b(names[i]), _b(names[i])) for i in range(L)]
    wids = [(_b(ids[i]), _b(ids[i])) for i in range(L)]
    return (
     locs, wids)


def _save_locations_and_ids(locs, wids, idx):
    if not locs or not wids:
        return
    loc_str = locs[0][0]
    wid_str = wids[0][0]
    for i in range(1, len(locs)):
        loc_str += '|' + locs[i][0]
        wid_str += '|' + wids[i][0]

    TSW.locationList.value = loc_str
    TSW.woeidList.value = wid_str
    TSW.locationList.save()
    TSW.woeidList.save()
    TSW.locationIndex.value = str(idx)
    TSW.locationIndex.save()
    configfile.save()
    return


class TSyWeatherPlugin(Screen):
    skin_1280 = '<screen name="TSyWeatherPlugin" position="center,center" size="560,590" flags="wfNoBorder">\n   \t<widget name="city" position="20,10" size="450,50" font="Regular; 40" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" noWrap="1" transparent="1" />\n\t<widget name="country" position="25,54" size="450,30" font="Regular; 21" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" noWrap="1" transparent="1" />\n\t<widget source="global.CurrentTime" render="Label" position="340,10" size="200,50" font="Regular; 40" halign="right" backgroundColor="background" foregroundColor="foreground" transparent="1" valign="center">\n  \t\t<convert type="ClockToText">Default</convert>\n\t</widget>\n\t<widget source="global.CurrentTime" render="Label" position="140,54" size="400,29" font="Regular; 19" halign="right" backgroundColor="background" foregroundColor="foreground" transparent="1">\n  \t\t<convert type="ClockToText">Format: %A, %e. %B</convert>\n\t</widget>\n\t<widget source="session.TSyWeather" render="TSyWeatherPixmap" position="10,90" size="60,60" zPosition="10"  transparent="1" alphatest="blend" >\n  \t\t<convert type="TSyWeather">weathericon,current</convert>\n\t</widget>\n\t<widget name="currenttext" position="75,95" size="250,60" font="Regular; 25" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n\t<widget name="high_today" position="20,150" size="100,40" font="Regular; 21" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n\t<widget name="low_today" position="105,150" size="100,40" font="Regular; 21" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n\t<widget name="currenttemp" position="20,180" size="250,130" font="Regular; 120" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" noWrap="1" />\n\t\t\n\t<widget name="windpic" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSMediaPanel/weather_icons/24.png" position="340,95" size="52,52" zPosition="1" alphatest="blend" />\n\t<widget name="windtext" position="395,105" size="80,25" font="Regular; 21" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n\t<widget name="windspeed" position="395,127" size="180,25" font="Regular; 18" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" noWrap="1" />\n\t<widget name="visibility" position="340,160" size="230,25" font="Regular; 18" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n\t<widget name="humidity" position="340,185" size="230,25" font="Regular; 18" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n\t<widget name="barometer" position="340,210" size="230,25" font="Regular; 18" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n\t<widget name="sunrisepic" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSMediaPanel/weather_icons/sunrise.png" position="340,243" size="30,30" zPosition="1" alphatest="blend" />\n\t<widget name="sunsetpic" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSMediaPanel/weather_icons/sunset.png" position="490,243" size="30,30" zPosition="1" alphatest="blend" />\n\t<widget name="sunrise" position="325,275" size="60,25" font="Regular; 18" zPosition="10" halign="center" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n\t<widget name="sunset" position="475,275" size="60,25" font="Regular; 18" zPosition="10" halign="center" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n\t<widget name="forecast" position="20,345" size="520,40" font="Regular; 25" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n\t<widget name="weekday1" position="20,385" size="150,40" font="Regular; 20" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n\t<widget source="session.TSyWeather" render="TSyWeatherPixmap" position="250,385" size="40,40" zPosition="10"  transparent="1" alphatest="blend" >\n\t  <convert type="TSyWeather">weathericon,day1</convert>\n\t</widget>\n\t<widget name="high_day1" position="430,390" size="230,25" font="Regular; 20" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n\t<widget name="low_day1" position="500,390" size="230,25" font="Regular; 20" zPosition="10" halign="left" valign="center" foregroundColor="#1677d2" backgroundColor="background" transparent="1" />\n\t<widget name="line1" position="20,430" size="520,1" zPosition="1" backgroundColor="foreground" pixmap="/usr/share/enigma2/skin_default/div-h.png" />\n\t<widget name="weekday2" position="20,435" size="150,40" font="Regular; 20" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n\t<widget source="session.TSyWeather" render="TSyWeatherPixmap" position="250,435" size="40,40" zPosition="10"  transparent="1" alphatest="blend" >\n\t  <convert type="TSyWeather">weathericon,day2</convert>\n\t</widget>\n\t<widget name="high_day2" position="430,440" size="230,25" font="Regular; 20" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n\t<widget name="low_day2" position="500,440" size="230,25" font="Regular; 20" zPosition="10" halign="left" valign="center" foregroundColor="#1677d2" backgroundColor="background" transparent="1" />\n\t<widget name="line2" position="20,480" size="520,1" zPosition="1" backgroundColor="foreground" pixmap="/usr/share/enigma2/skin_default/div-h.png" />\n\t<widget name="weekday3" position="20,485" size="150,40" font="Regular; 20" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n\t<widget source="session.TSyWeather" render="TSyWeatherPixmap" position="250,485" size="40,40" zPosition="10"  transparent="1" alphatest="blend" >\n\t  <convert type="TSyWeather">weathericon,day3</convert>\n\t</widget>\n\t<widget name="high_day3" position="430,490" size="230,25" font="Regular; 20" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n\t<widget name="low_day3" position="500,490" size="230,25" font="Regular; 20" zPosition="10" halign="left" valign="center" foregroundColor="#1677d2" backgroundColor="background" transparent="1" />\n\t<widget name="line3" position="20,530" size="520,1" zPosition="1" backgroundColor="foreground" pixmap="/usr/share/enigma2/skin_default/div-h.png" />\n\t<widget name="weekday4" position="20,535" size="150,40" font="Regular; 20" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n\t<widget source="session.TSyWeather" render="TSyWeatherPixmap" position="250,535" size="40,40" zPosition="10"  transparent="1" alphatest="blend" >\n \t <convert type="TSyWeather">weathericon,day4</convert>\n\t</widget>\n\t<widget name="high_day4" position="430,540" size="230,25" font="Regular; 20" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n\t<widget name="low_day4" position="500,540" size="230,25" font="Regular; 20" zPosition="10" halign="left" valign="center" foregroundColor="#1677d2" backgroundColor="background" transparent="1" />\n\t<widget name="statustext" position="0,0" zPosition="1" size="550,590" foregroundColor="foreground" backgroundColor="background" font="Regular;20" halign="center" valign="center" transparent="1"/>\n\t</screen>'
    skin_1920 = '    <screen name="TSyWeatherPlugin" position="center,center" size="840,886" flags="wfNoBorder">\n    <widget name="city" position="30,20" size="620,70" font="Regular; 60" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" noWrap="1" transparent="1" />\n    <widget name="country" position="30,70" size="620,65" font="Regular; 32" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" noWrap="1" transparent="1" />\n    <widget source="global.CurrentTime" render="Label" position="610,20" size="200,70" font="Regular; 60" halign="right" backgroundColor="background" foregroundColor="foreground" transparent="1" valign="center">\n    <convert type="ClockToText">Default</convert>\n    </widget>\n    <widget source="global.CurrentTime" render="Label" position="390,70" size="420,65" font="Regular; 32" halign="right" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1">\n    <convert type="ClockToText">Format: %A, %e. %B</convert>\n    </widget>\n    <widget source="session.TSyWeather" render="TSyWeatherPixmap" position="30,150" size="96,96" zPosition="10"  transparent="1" alphatest="blend" >\n    <convert type="TSyWeather">weathericon,current</convert>\n    </widget>\n    <widget name="currenttext" position="132,150" size="400,96" font="Regular; 40" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n    <widget name="high_today" position="30,250" size="135,50" font="Regular; 32" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n    <widget name="low_today" position="165,250" size="125,50" font="Regular; 32" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n    <widget name="currenttemp" position="30,300" size="455,180" font="Regular; 150" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" noWrap="1" />\n    <widget name="windpic" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSMediaPanel/weather_icons/24.png" position="520,177" size="52,52" zPosition="1" alphatest="blend" />\n    <widget name="windtext" position="575,185" size="120,40" font="Regular; 32" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n    <widget name="windspeed" position="575,227" size="250,35" font="Regular; 27" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" noWrap="1" />\n    <widget name="visibility" position="520,262" size="300,35" font="Regular; 27" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n    <widget name="humidity" position="520,297" size="300,35" font="Regular; 27" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n    <widget name="barometer" position="520,332" size="340,35" font="Regular; 27" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n    <widget name="sunrisepic" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSMediaPanel/weather_icons/sunrise.png" position="520,380" size="30,30" zPosition="1" alphatest="blend" />\n    <widget name="sunsetpic" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSMediaPanel/weather_icons/sunset.png" position="760,380" size="30,30" zPosition="1" alphatest="blend" />\n    <widget name="sunrise" position="490,410" size="90,40" font="Regular; 27" zPosition="10" halign="center" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n    <widget name="sunset" position="730,410" size="90,40" font="Regular; 27" zPosition="10" halign="center" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n    <widget name="forecast" position="30,505" size="520,50" font="Regular; 36" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n    <widget name="weekday1" position="30,570" size="200,64" font="Regular; 30" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n    <widget source="session.TSyWeather" render="TSyWeatherPixmap" position="380,570" size="64,64" zPosition="10"  transparent="1" alphatest="blend" >\n    <convert type="TSyWeather">weathericon,day1</convert>\n    </widget>\n    <widget name="high_day1" position="650,570" size="230,64" font="Regular; 30" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n    <widget name="low_day1" position="750,570" size="230,64" font="Regular; 30" zPosition="10" halign="left" valign="center" foregroundColor="#1677d2" backgroundColor="background" transparent="1" />\n    <widget name="line1" position="30,640" size="780,1" zPosition="1" backgroundColor="foreground" pixmap="/usr/share/enigma2/skin_default/div-h.png" />\n    <widget name="weekday2" position="30,645" size="200,64" font="Regular; 30" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n    <widget source="session.TSyWeather" render="TSyWeatherPixmap" position="380,645" size="64,64" zPosition="10"  transparent="1" alphatest="blend" >\n    <convert type="TSyWeather">weathericon,day2</convert>\n    </widget>\n    <widget name="high_day2" position="650,645" size="230,64" font="Regular; 30" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n    <widget name="low_day2" position="750,645" size="230,64" font="Regular; 30" zPosition="10" halign="left" valign="center" foregroundColor="#1677d2" backgroundColor="background" transparent="1" />\n    <widget name="line2" position="30,715" size="780,1" zPosition="1" backgroundColor="foreground" pixmap="/usr/share/enigma2/skin_default/div-h.png" />\n    <widget name="weekday3" position="30,720" size="200,64" font="Regular; 30" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n    <widget source="session.TSyWeather" render="TSyWeatherPixmap" position="380,720" size="64,64" zPosition="10"  transparent="1" alphatest="blend" >\n    <convert type="TSyWeather">weathericon,day3</convert>\n    </widget>\n    <widget name="high_day3" position="650,720" size="230,64" font="Regular; 30" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n    <widget name="low_day3" position="750,720" size="230,64" font="Regular; 30" zPosition="10" halign="left" valign="center" foregroundColor="#1677d2" backgroundColor="background" transparent="1" />\n    <widget name="line3" position="30,790" size="780,1" zPosition="1" backgroundColor="foreground" pixmap="/usr/share/enigma2/skin_default/div-h.png" />\n    <widget name="weekday4" position="30,795" size="200,64" font="Regular; 30" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n    <widget source="session.TSyWeather" render="TSyWeatherPixmap" position="380,795" size="64,64" zPosition="10"  transparent="1" alphatest="blend" >\n    <convert type="TSyWeather">weathericon,day4</convert>\n    </widget>\n    <widget name="high_day4" position="650,795" size="230,64" font="Regular; 30" zPosition="10" halign="left" valign="center" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n    <widget name="low_day4" position="750,795" size="230,64" font="Regular; 30" zPosition="10" halign="left" valign="center" foregroundColor="#1677d2" backgroundColor="background" transparent="1" />\n    <widget name="statustext" position="0,0" zPosition="20" size="840,906" foregroundColor="foreground" backgroundColor="background" font="Regular;30" halign="center" valign="center" transparent="1"/>\n    </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session):
        Screen.__init__(self, session)
        self['setupActions'] = ActionMap(['WizardActions',
         'DirectionActions',
         'ColorActions',
         'EPGSelectActions'], {'back': (self.exit), 
           'ok': (self.exit), 'input_date_time': (self.yWeatherEntries), 
           'info': (self.satPics), 
           'right': (self.nextCity), 
           'left': (self.previousCity)}, -2)
        self['city'] = Button('')
        self['country'] = Button('')
        self['high_today'] = Button('')
        self['low_today'] = Button('')
        self['currenttemp'] = Button('')
        self['currenttext'] = Button('')
        self['windtext'] = Button('')
        self['windspeed'] = Button('')
        self['humidity'] = Button('')
        self['visibility'] = Button('')
        self['barometer'] = Button('')
        self['sunrise'] = Button('')
        self['sunset'] = Button('')
        for skey in daykeys:
            self['high_day%s' % skey] = Button('')
            self['low_day%s' % skey] = Button('')
            self['weekday%s' % skey] = Button('')
            if skey != '4':
                self['line%s' % skey] = Pixmap()

        self['forecast'] = Button('')
        self['statustext'] = Label('')
        self['windpic'] = Pixmap()
        self['sunrisepic'] = Pixmap()
        self['sunsetpic'] = Pixmap()
        self.errortext = None
        self.locations, self.woeids = _get_locations_and_ids()
        try:
            self.index = int(TSW.locationIndex.value or '0')
        except:
            self.index = 0

        self.index = max(0, min(self.index, len(self.woeids) - 1))
        self.lang = language.getLanguage()
        weatheryahoo.resetData()
        self.onLayoutFinish.append(self.getWeather)
        self.setTitle(_('TSWeather'))
        return

    def clearField(self):
        self['statustext'].setText(_('Getting weather information...'))
        self['city'].hide()
        self['country'].hide()
        self['high_today'].hide()
        self['low_today'].hide()
        self['currenttemp'].hide()
        self['currenttext'].hide()
        self['windtext'].hide()
        self['windspeed'].hide()
        self['humidity'].hide()
        self['visibility'].hide()
        self['barometer'].hide()
        self['sunrise'].hide()
        self['sunset'].hide()
        self['forecast'].hide()
        for skey in daykeys:
            self['low_day%s' % skey].hide()
            self['high_day%s' % skey].hide()
            self['weekday%s' % skey].hide()
            if skey != '4':
                self['line%s' % skey].hide()

        self['windpic'].hide()
        self['sunrisepic'].hide()
        self['sunsetpic'].hide()
        return

    def getWeather(self):
        self.clearField()
        token = self.woeids[self.index][0]
        weatheryahoo.getData(token, self.getWeatherDataCallback)
        return

    def updateWeather(self):
        if len(self.woeids) > 1:
            self.clearField()
            weatheryahoo.resetData()
        token = self.woeids[self.index][0]
        weatheryahoo.getData(token, self.getWeatherDataCallback)
        return

    def getWeatherDataCallback(self, result, errortext):
        self.errortext = errortext
        self['statustext'].setText(_b(errortext) if errortext else '')
        if errortext is None:
            self['forecast'].setText(_('Forecast'))
            self['windtext'].setText(_('Wind'))
            self['city'].setText(_b(weatheryahoo.weatherData.city))
            country = ''
            if weatheryahoo.weatherData.region:
                country = _b(weatheryahoo.weatherData.region) + _b(', ')
            if weatheryahoo.weatherData.country:
                country = country + _b(weatheryahoo.weatherData.country)
            self['country'].setText(country)
            today = weatheryahoo.weatherData.weatherItems.get('-1')
            if today:
                self['sunrise'].setText(self.convertTime(today.sunrise))
                self['sunset'].setText(self.convertTime(today.sunset))
                self['humidity'].setText(_('Humidity %s %s') % (_b(today.humidity), _b('%')))
                visibility = today.visibility or _b('--')
                self['visibility'].setText(_('Visibility %s %s') % (_b(visibility), _b(today.unitdistance)))
                self['barometer'].setText(_('Barometer %s %s') % (_b(today.pressure), _b(today.unitpressure)))
                self['high_today'].setText(_(u'H: ').decode('utf-8').encode('utf-8') + _b(today.high) + DEG + _b(today.unittemperature))
                self['low_today'].setText(_(u'L: ').decode('utf-8').encode('utf-8') + _b(today.low) + DEG + _b(today.unittemperature))
                self['currenttemp'].setText(_b(today.temperature) + DEG)
                self['currenttext'].setText(_b(today.skytext))
                windline = _b(today.windspeed)
                if windline:
                    windline = windline + _b(' ') + _b(today.unitspeed) + _b(' ') + _b(today.winddirection)
                self['windspeed'].setText(windline)
            self['city'].show()
            self['country'].show()
            self['high_today'].show()
            self['low_today'].show()
            self['currenttemp'].show()
            self['currenttext'].show()
            self['sunrisepic'].show()
            self['sunsetpic'].show()
            self['windpic'].show()
            self['windtext'].show()
            self['windspeed'].show()
            self['humidity'].show()
            self['visibility'].show()
            self['barometer'].show()
            self['sunrise'].show()
            self['sunset'].show()
            self['forecast'].show()
            for skey in daykeys:
                item = weatheryahoo.weatherData.weatherItems.get(skey)
                if not item:
                    continue
                self['low_day%s' % skey].setText(_b(item.low) + DEG + _b(today.unittemperature))
                self['high_day%s' % skey].setText(_b(item.high) + DEG + _b(today.unittemperature))
                if self.lang == 'ar_AE':
                    self['weekday%s' % skey].setText(_b('x ') + _b(item.day))
                else:
                    self['weekday%s' % skey].setText(_b(item.day))
                self['low_day%s' % skey].show()
                self['high_day%s' % skey].show()
                self['weekday%s' % skey].show()
                if skey != '4':
                    self['line%s' % skey].show()

        return

    def convertTime(self, time_str):
        try:
            time_str = _b(time_str)
            parts = time_str.split(' ')
            clk = parts[0].split(':')
            hh = int(clk[0])
            mm = clk[1]
            if len(parts) > 1 and parts[1].lower() == 'pm' and hh != 12:
                hh += 12
            if len(parts) > 1 and parts[1].lower() == 'am' and hh == 12:
                hh = 0
            return _b('%02d:%s' % (hh, mm))
        except:
            return _b('--:--')

        return

    def yWeatherEntries(self):
        self.session.openWithCallback(self.updateConfig, TSyWeatherEntries, TSW.locationIndex.value, self.locations, self.woeids)
        return

    def updateConfig(self, index, locations, woeids):
        if woeids and self.woeids != woeids:
            self.locations = locations
            self.woeids = woeids
        try:
            self.index = int(index)
        except:
            self.index = 0

        _save_locations_and_ids(self.locations, self.woeids, self.index)
        self.updateWeather()
        return

    def nextCity(self):
        if len(self.woeids) != 0:
            if self.index < len(self.woeids) - 1:
                self.index += 1
            else:
                self.index = 0
            _save_locations_and_ids(self.locations, self.woeids, self.index)
            self.updateWeather()
        return

    def previousCity(self):
        if len(self.woeids) != 0:
            if self.index > 0:
                self.index -= 1
            else:
                self.index = len(self.woeids) - 1
            _save_locations_and_ids(self.locations, self.woeids, self.index)
            self.updateWeather()
        return

    def exit(self):
        if self.errortext is None and self.woeids:
            weatheryahoo.getData(self.woeids[self.index][0])
        self.close()
        return

    def satPics(self):
        if self['statustext'].getText():
            self.session.openWithCallback(self.reloadWeather, animationLoader)
        return

    def reloadWeather(self, reval):
        if reval:
            weatheryahoo.getData(self.woeids[self.index][0], self.getWeatherDataCallback)
        return


class animationLoader(Screen):
    skin_1280 = '\n\t        <screen name="animationLoader" position="center,605" size="150,40" title="Loading animation..." flags="wfNoBorder" >\n\t\t<widget name="status" position="0,0" size="150,40" font="Regular;18" foregroundColor="foreground" backgroundColor="background" halign="center" valign="center" noWrap="1" transparent="1" />\n\t        </screen>'
    skin_1920 = '\n\t        <screen name="animationLoader" position="center,908" size="225,60" title="Loading animation..." flags="wfNoBorder" >\n\t\t<widget name="status" position="0,0" size="225,60" font="Regular;27" foregroundColor="foreground" backgroundColor="background" halign="center" valign="center" noWrap="1" transparent="1" />\n\t        </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session):
        self.skin = animationLoader.skin
        Screen.__init__(self, session)
        self['actions'] = ActionMap(['OkCancelActions'], {'cancel': (self.abort)}, -1)
        self['status'] = Label(_('Loading...') + ' 0%')
        try:
            self.sat = config.plugins.TSWeather.satMap.value
        except:
            self.sat = 'uksat'

        self.idx = 1
        self.picfilelist = []
        self.errormessage = ''
        self.progressprevious = 0
        self.downloader = None
        self.onLayoutFinish.append(self.tryNextPicture)
        return

    def progress(self, current, total):
        try:
            p = int(100 * (float(current) / float(total)) / float(SLIDE_NR))
        except:
            p = 0

        if p == int(100 / SLIDE_NR) - 1 and self.idx == SLIDE_NR:
            p = p + 1
        if p == int(100 / SLIDE_NR) - 2 and self.idx == SLIDE_NR:
            p = p + 2
        self['status'].setText(_('Loading... ') + ' ' + str(self.progressprevious + p) + '%')
        return

    def responseCompleted(self, data=None):
        self.progressprevious = int(100 / SLIDE_NR) * self.idx
        self['status'].setText(_('Loading... ') + ' ' + str(self.progressprevious) + '%')
        self.downloader = None
        self.picfilelist.append(CACHE_PATH + '%sL.jpg' % self.idx)
        if self.idx == SLIDE_NR:
            self.idx = 1
            self['status'].setText('Loading... 100%')
            self.session.openWithCallback(self.Close, WeatherinMotion, 0, self.picfilelist)
        else:
            self.idx = self.idx + 1
            self.tryNextPicture()
        return

    def responseFailed(self, failure_instance=None, error_message=''):
        print('[TS downloader] Download failed.')
        self.error_message = error_message
        if error_message == '' and failure_instance is not None:
            try:
                self.error_message = failure_instance.getErrorMessage()
            except:
                self.error_message = 'Download failed'

        self['status'].setText('Failed to load!')
        return

    def tryNextPicture(self):
        if self.idx <= SLIDE_NR:
            url = 'http://image.weather.com/looper/archive/' + self.sat + '_720x486/' + str(self.idx) + 'L.jpg'
            if self.sat == 'afghan_sat':
                url = url.replace('720x486', '720_usen')
            if self.sat == 'uksat':
                url = url.replace('720x486', '600x405')
            self.downloader = downloadWithProgress(url, CACHE_PATH + str(self.idx) + 'L.jpg')
            self.downloader.addProgress(self.progress)
            self.downloader.start().addCallback(self.responseCompleted).addErrback(self.responseFailed)
        return

    def abort(self):
        if self.downloader is not None:
            try:
                self.downloader.stop()
            except:
                pass

            self['status'].setText(_('Aborting...'))
        for file in self.picfilelist:
            if fileExists(file):
                os_unlink(file)

        self.close(False)
        return

    def Close(self, retval):
        self.close(True)
        return


class WeatherinMotion(Screen):

    def __init__(self, session, pindex, picfilelist):
        self.pindex = pindex
        self.picfilelist = picfilelist
        self.startslide = True
        print(pluginPrintname, 'Starting weather in motion...')
        self.textcolor = 'foreground'
        self.bgcolor = 'background'
        space = 5
        size_w = 730
        size_h = 526
        self.skin = '<screen position="center,center" size="' + str(size_w) + ',' + str(size_h) + '" flags="wfNoBorder" >         \t<!--eLabel position="0,0" zPosition="0" size="' + str(size_w) + ',' + str(size_h) + '" backgroundColor="' + self.bgcolor + '" /> -->         \t<widget name="pic" position="' + str(space) + ',' + str(space + 30) + '" size="' + str(size_w - space * 2) + ',' + str(size_h - space * 2 - 30) + '" zPosition="1" alphatest="blend" />         \t<widget name="pause_icon" position="' + str(space + 5) + ',' + str(space + 7) + '" size="20,20" zPosition="2" pixmap="' + THUMB_PATH + 'ico_mp_pause.png"  alphatest="blend" />         \t<widget name="play_icon" position="' + str(space + 5) + ',' + str(space + 7) + '" size="20,20" zPosition="2" pixmap="' + THUMB_PATH + 'ico_mp_play.png"  alphatest="blend" />         \t<widget name="file" position="' + str(space + 25) + ',' + str(space + 0) + '" size="' + str(size_w - space * 2 - 50) + ',30" font="Regular;20" halign="left" valign="center" foregroundColor="' + self.textcolor + '" zPosition="2" noWrap="1" transparent="1" />         \t<widget source="Title" render="Label" position="' + str(space + 25) + ',' + str(space + 0) + '" size="' + str(size_w - space * 2 - 50) + ',30" font="Regular;20" halign="center" valign="center" foregroundColor="' + self.textcolor + '" zPosition="2" noWrap="1" transparent="1" />         \t<widget source="global.CurrentTime" render="Label" position="' + str(space + 25) + ',' + str(space + 0) + '" size="' + str(size_w - space * 2 - 30) + ',30" font="Regular;20" halign="right" valign="center" foregroundColor="' + self.textcolor + '" zPosition="2" noWrap="1" transparent="1" >         \t    <convert type="ClockToText">Default</convert>                 </widget>         \t<widget name="status" position="' + str(space) + ',' + str(space + 30) + '" size="' + str(size_w - space * 2) + ',' + str(size_h - space * 2 - 30) + '" font="Regular;20" halign="center" valign="center" foregroundColor="' + self.textcolor + '" zPosition="2" noWrap="1" transparent="1" />         \t</screen>'
        Screen.__init__(self, session)
        self['actions'] = ActionMap(['OkCancelActions', 'MediaPlayerActions', 'DirectionActions'], {'cancel': (self.Exit), 
           'ok': (self.PlayPause), 'right': (self.nextPic), 
           'left': (self.prevPic), 'stop': (self.Exit), 
           'pause': (self.PlayPause), 'play': (self.PlayPause), 'previous': (self.prevPic), 
           'next': (self.nextPic)}, -1)
        self['pic'] = Pixmap()
        self['play_icon'] = Pixmap()
        self['pause_icon'] = Pixmap()
        self.idx = 1
        self['status'] = Label(_('Loading animation...'))
        self['file'] = Label('(%d/5)' % self.idx)
        self.lastindex = self.pindex
        self.currPic = []
        self.shownow = True
        self.onLayoutFinish.append(self.loadPics)
        self.onShown.append(self.setWindowTitle)
        return

    def setWindowTitle(self):
        self.setTitle(_('Weather in motion'))
        return

    def loadPics(self):
        self.maxentry = len(self.picfilelist) - 1
        self.pindex = self.pindex
        if self.pindex < 0:
            self.pindex = 0
        self.picload = ePicLoad()
        self.picload_conn = self.picload.PictureData.connect(self.finish_decode)
        self.slideTimer = eTimer()
        self.slideTimer_conn = self.slideTimer.timeout.connect(self.slidePic)
        if self.maxentry >= 0:
            self.setPicloadConf()
        if self.startslide:
            self.PlayPause()
        return

    def setPicloadConf(self):
        sc = getScale()
        self.picload.setPara([self['pic'].instance.size().width(),
         self['pic'].instance.size().height(),
         sc[0], sc[1], 0, 1, self.bgcolor])
        if not INFOLINE:
            self['file'].hide()
        self.start_decode()
        return

    def ShowPicture(self):
        if self.shownow and len(self.currPic):
            self.shownow = False
            self['file'].setText(self.currPic[0])
            self.lastindex = self.currPic[1]
            self['pic'].instance.setPixmap(self.currPic[2])
            self.currPic = []
            self.next()
            self.start_decode()
        return

    def finish_decode(self, picInfo=''):
        ptr = self.picload.getData()
        if ptr is not None:
            text = ''
            self['status'].setText('')
            try:
                text = '(' + str(self.pindex + 1) + '/' + str(self.maxentry + 1) + ') '
            except:
                pass

            self.currPic = [
             text, self.pindex, ptr]
            self.ShowPicture()
        else:
            self['play_icon'].hide()
            self['pause_icon'].hide()
        return

    def start_decode(self):
        self.picload.startDecode(self.picfilelist[self.pindex])
        return

    def next(self):
        self.pindex += 1
        if self.pindex > self.maxentry:
            self.pindex = 0
        return

    def prev(self):
        self.pindex -= 1
        if self.pindex < 0:
            self.pindex = self.maxentry
        return

    def slidePic(self):
        if not LOOP and self.lastindex == self.maxentry:
            self.PlayPause()
        self.shownow = True
        self['play_icon'].show()
        self['pause_icon'].hide()
        self.ShowPicture()
        return

    def PlayPause(self):
        if self.slideTimer.isActive():
            self.slideTimer.stop()
            self['play_icon'].hide()
            self['pause_icon'].show()
        else:
            self['play_icon'].show()
            self['pause_icon'].hide()
            self.slideTimer.start(SLIDETIME * 1000)
            self.nextPic()
        return

    def prevPic(self):
        self.currPic = []
        self.pindex = self.lastindex
        self.prev()
        self.start_decode()
        self.shownow = True
        self['pause_icon'].show()
        self['play_icon'].hide()
        return

    def nextPic(self):
        self.shownow = True
        self.ShowPicture()
        return

    def Exit(self):
        try:
            if self.picload is not None:
                del self.picload
        except:
            pass

        for file in self.picfilelist:
            if fileExists(file):
                os_unlink(file)

        self.close(self.lastindex)
        return


return
