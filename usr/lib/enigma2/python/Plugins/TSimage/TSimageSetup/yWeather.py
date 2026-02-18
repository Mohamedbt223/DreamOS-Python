# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/TSimageSetup/yWeather.py
# Compiled at: 2016-11-22 07:46:06
from xml.etree.cElementTree import fromstring as cet_fromstring
from twisted.internet import defer
from twisted.web.client import getPage, downloadPage
from enigma import eEnv
from os import path as os_path, mkdir as os_mkdir, remove as os_remove, listdir as os_listdir
from math import ceil
from xml.dom.minidom import parseString
from Components.config import config
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE, SCOPE_SKIN
from os import environ
import gettext

def localeInit():
    lang = language.getLanguage()
    environ['LANGUAGE'] = lang[:2]
    gettext.bindtextdomain('enigma2', resolveFilename(SCOPE_LANGUAGE))
    gettext.textdomain('enigma2')
    gettext.bindtextdomain('yWeather', '%s%s' % (resolveFilename(SCOPE_PLUGINS), 'TSimage/TSimageSetup/locale/'))
    return


def _(txt):
    t = gettext.dgettext('yWeather', txt)
    if t == txt:
        t = gettext.gettext(txt)
    return t


localeInit()
language.addCallback(localeInit)
QUERY_URL = 'http://query.yahooapis.com/v1/public/yql?'
WEATHER_URL = 'http://weather.yahooapis.com/forecastrss?'
WEATHER_NS = 'http://xml.weather.yahoo.com/ns/rss/1.0'
YWEATHER_ICONS_PATH = '%s%s' % (resolveFilename(SCOPE_PLUGINS), 'TSimage/TSMediaPanel/weather_icons/')

class WeatherIconItem():

    def __init__(self, url='', filename='', index=-1, error=False):
        self.url = url
        self.filename = filename
        self.index = index
        self.error = error
        return


class yWeatherItem():

    def __init__(self):
        self.temperature = ''
        self.skytext = ''
        self.humidity = ''
        self.visibility = ' '
        self.windspeed = ''
        self.pressure = ''
        self.sunrise = ''
        self.sunset = ''
        self.skycode = ''
        self.skycodeText = ''
        self.stand = ''
        self.day = ''
        self.shortday = ''
        self.low = ''
        self.high = ''
        self.unittemperature = ''
        self.unitdistance = ''
        self.unitpressure = ''
        self.unitspeed = ''
        self.winddirection = ''
        self.iconFilename = ''
        return


class yWeather():
    ERROR = 0
    OK = 1

    def __init__(self):
        path = '/etc/enigma2/weather_icons/'
        extension = self.checkIconExtension(path)
        if extension is None:
            path = os_path.dirname(resolveFilename(SCOPE_SKIN, config.skin.primary_skin.value)) + '/weather_icons/'
            extension = self.checkIconExtension(path)
        if extension is None:
            path = YWEATHER_ICONS_PATH
            extension = '.png'
        self.setIconPath(path)
        self.setIconExtension(extension)
        self.initialize()
        return

    def checkIconExtension(self, path):
        filename = None
        extension = None
        if os_path.exists(path):
            try:
                filename = os_listdir(path)[0]
            except:
                filename = None

        if filename is not None:
            try:
                extension = os_path.splitext(filename)[1].lower()
            except:
                pass

        return extension

    def initialize(self):
        self.locationcode = ''
        self.city = ''
        self.region = ''
        self.country = ''
        self.degreetype = ''
        self.imagerelativeurl = 'http://l.yimg.com/a/i/us/we/52/'
        self.url = ''
        self.weatherItems = {}
        self.callback = None
        self.callbackShowIcon = None
        self.callbackAllIconsDownloaded = None
        return

    def cancel(self):
        self.callback = None
        self.callbackShowIcon = None
        return

    def setIconPath(self, iconpath):
        if not os_path.exists(iconpath):
            os_mkdir(iconpath)
        self.iconpath = iconpath
        return

    def setIconExtension(self, iconextension):
        self.iconextension = iconextension
        return

    def getWeatherData(self, locationcode, callback, callbackShowIcon, callbackAllIconsDownloaded=None):
        self.initialize()
        self.locationcode = locationcode
        self.callback = callback
        self.callbackShowIcon = callbackShowIcon
        self.callbackAllIconsDownloaded = callbackAllIconsDownloaded
        if config.plugins.TSWeather.tempUnit.value == 'Fahrenheit':
            self.degreetype = 'F'
            unit = 'f'
        else:
            self.degreetype = 'C'
            unit = 'c'
        url = 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid=' + str(self.locationcode) + '%20and%20u="' + str(unit) + '"&format=xml'
        getPage(url).addCallback(self.xmlCallback).addErrback(self.error)
        return

    def getDefaultWeatherData(self, callback=None, callbackAllIconsDownloaded=None):
        locationcode = config.plugins.TSWeather.woeid.value
        self.getWeatherData(locationcode, callback, None, callbackAllIconsDownloaded)
        return

    def error(self, error=None):
        errormessage = ''
        if error is not None:
            errormessage = str(error.getErrorMessage())
            if self.callback is not None:
                self.callback(self.ERROR, errormessage)
        return

    def errorIconDownload(self, error=None, item=None):
        item.error = True
        if os_path.exists(item.filename):
            os_remove(item.filename)
        return

    def finishedIconDownload(self, result, item):
        if not item.error:
            self.showIcon(item.index, item.filename)
        return

    def showIcon(self, index, filename):
        if self.callbackShowIcon is not None:
            self.callbackShowIcon(index, filename)
        return

    def finishedAllDownloadFiles(self, result):
        if self.callbackAllIconsDownloaded is not None:
            self.callbackAllIconsDownloaded()
        return

    def ConvertDay(self, day):
        weekday = ''
        if day == _('Sun'):
            weekday = _('Sunday')
        if day == _('Mon'):
            weekday = _('Monday')
        if day == _('Tue'):
            weekday = _('Tuesday')
        if day == _('Wed'):
            weekday = _('Wednesday')
        if day == _('Thu'):
            weekday = _('Thursday')
        if day == _('Fri'):
            weekday = _('Friday')
        if day == _('Sat'):
            weekday = _('Saturday')
        return weekday

    def ConvertCondition(self, c):
        c = int(c)
        condition = '('
        if c == 0 or c == 1 or c == 2:
            condition = 'S'
        elif c == 3 or c == 4:
            condition = 'Z'
        elif c == 5 or c == 6 or c == 7 or c == 18:
            condition = 'U'
        elif c == 8 or c == 10 or c == 25:
            condition = 'G'
        elif c == 9:
            condition = 'Q'
        elif c == 11 or c == 12 or c == 40:
            condition = 'R'
        elif c == 13 or c == 14 or c == 15 or c == 16 or c == 41 or c == 46 or c == 42 or c == 43:
            condition = 'W'
        elif c == 17 or c == 35:
            condition = 'X'
        elif c == 19:
            condition = 'F'
        elif c == 20 or c == 21 or c == 22:
            condition = 'L'
        elif c == 23 or c == 24:
            condition = 'S'
        elif c == 26 or c == 44:
            condition = 'N'
        elif c == 27 or c == 29:
            condition = 'I'
        elif c == 28 or c == 30:
            condition = 'H'
        elif c == 31 or c == 33:
            condition = 'C'
        elif c == 32 or c == 34:
            condition = 'B'
        elif c == 36:
            condition = 'B'
        elif c == 37 or c == 38 or c == 39 or c == 45 or c == 47:
            condition = '0'
        else:
            condition = ')'
        return str(condition)

    def windDeg2txt(self, deg):
        if deg > 348.75 or deg <= 11.25:
            wind_dir_txt = 'N'
        elif deg > 11.25 and deg <= 33.75:
            wind_dir_txt = 'NNE'
        elif deg > 33.75 and deg <= 56.25:
            wind_dir_txt = 'NE'
        elif deg > 56.25 and deg <= 78.75:
            wind_dir_txt = 'ENE'
        elif deg > 78.75 and deg <= 101.25:
            wind_dir_txt = 'E'
        elif deg > 101.25 and deg <= 123.75:
            wind_dir_txt = 'ESE'
        elif deg > 101.25 and deg <= 123.75:
            wind_dir_txt = 'SE'
        elif deg > 123.75 and deg <= 146.25:
            wind_dir_txt = 'SE'
        elif deg > 146.25 and deg <= 168.75:
            wind_dir_txt = 'SSE'
        elif deg > 168.75 and deg <= 191.25:
            wind_dir_txt = 'S'
        elif deg > 191.25 and deg <= 213.75:
            wind_dir_txt = 'SSW'
        elif deg > 213.75 and deg <= 236.25:
            wind_dir_txt = 'SW'
        elif deg > 236.25 and deg <= 258.75:
            wind_dir_txt = 'WSW'
        elif deg > 258.75 and deg <= 281.25:
            wind_dir_txt = 'W'
        elif deg > 281.25 and deg <= 303.75:
            wind_dir_txt = 'WNW'
        elif deg > 303.75 and deg <= 326.25:
            wind_dir_txt = 'NW'
        elif deg > 326.25 and deg <= 348.75:
            wind_dir_txt = 'NNW'
        return wind_dir_txt

    def getCklFormat(self, time_str, suffix=None):
        time = time_str.split(':')
        if suffix is None:
            suffix = time[1][-2:]
        hh = time[0]
        mn = time[1].replace(suffix, '')
        if int(mn) < 10:
            mn = '0%s' % mn
        if suffix == 'pm':
            hh = str(int(hh) + 12)
        elif suffix == 'am':
            if int(hh) < 10:
                hh = '0%s' % hh
        return hh + ':' + mn

    def roundValue(self, value):
        if value.find('.') != -1:
            roundValue = str(round(float(value), 1))
        else:
            roundValue = value
        return roundValue

    def resetData(self):
        self.initialize()
        weatherItems = yWeatherItem()
        items = (-1, 1, 2, 3, 4)
        for item in items:
            self.showIcon(item, '')
            self.weatherItems[str(item)] = weatherItems

        self.finishedAllDownloadFiles(None)
        return

    def xmlCallback(self, xmlstring):
        IconDownloadList = []
        dom = parseString(xmlstring)
        currentWeather = yWeatherItem()
        structure = (('location', ('city', 'region', 'country')),
         (
          'units', ('temperature', 'distance', 'pressure', 'speed')),
         (
          'wind', ('chill', 'direction', 'speed')),
         (
          'atmosphere', ('humidity', 'visibility', 'pressure', 'rising')),
         (
          'astronomy', ('sunrise', 'sunset')),
         (
          'condition', ('text', 'code', 'temp', 'date')))
        element = dom.getElementsByTagNameNS(WEATHER_NS, 'location')[0]
        self.city = str(element.getAttribute('city'))
        self.region = str(element.getAttribute('region'))
        self.country = str(element.getAttribute('country'))
        element = dom.getElementsByTagNameNS(WEATHER_NS, 'astronomy')[0]
        currentWeather.sunrise = self.getCklFormat(str(element.getAttribute('sunrise')))
        currentWeather.sunset = self.getCklFormat(str(element.getAttribute('sunset')))
        element = dom.getElementsByTagNameNS(WEATHER_NS, 'atmosphere')[0]
        currentWeather.pressure = self.roundValue(str(element.getAttribute('pressure')))
        currentWeather.humidity = str(element.getAttribute('humidity'))
        currentWeather.visibility = str(element.getAttribute('visibility'))
        element = dom.getElementsByTagNameNS(WEATHER_NS, 'units')[0]
        currentWeather.unittemperature = str(element.getAttribute('temperature'))
        currentWeather.unitdistance = str(element.getAttribute('distance'))
        currentWeather.unitpressure = str(element.getAttribute('pressure'))
        currentWeather.unitspeed = str(element.getAttribute('speed'))
        element = dom.getElementsByTagNameNS(WEATHER_NS, 'wind')[0]
        currentWeather.windspeed = str(element.getAttribute('speed'))
        direction = float(str(element.getAttribute('direction')))
        currentWeather.winddirection = self.windDeg2txt(direction)
        element = dom.getElementsByTagNameNS(WEATHER_NS, 'condition')[0]
        currentWeather.temperature = str(element.getAttribute('temp'))
        currentWeather.skytext = str(element.getAttribute('text'))
        currentWeather.skycode = str(element.getAttribute('code'))
        date = str(element.getAttribute('date')).split(' ')
        currentWeather.stand = self.getCklFormat(date[4], date[5])
        currentWeather.skycodeText = self.ConvertCondition(currentWeather.skycode)
        filename = '%s%s%s' % (self.iconpath, currentWeather.skycode, self.iconextension)
        currentWeather.iconFilename = filename
        if not os_path.exists(filename):
            url = '%s%s.gif' % (self.imagerelativeurl, currentWeather.skycode)
            filename = '%s%s.gif' % (self.iconpath, currentWeather.skycode)
            if not os_path.exists(filename):
                IconDownloadList.append(WeatherIconItem(url=url, filename=filename, index=-1))
            else:
                self.showIcon(-1, filename)
        else:
            self.showIcon(-1, filename)
        element = dom.getElementsByTagNameNS(WEATHER_NS, 'forecast')
        currentWeather.high = str(element[0].getAttribute('high'))
        currentWeather.low = str(element[0].getAttribute('low'))
        if int(currentWeather.temperature) > int(currentWeather.high):
            currentWeather.high = currentWeather.temperature
        if int(currentWeather.temperature) < int(currentWeather.low):
            currentWeather.low = currentWeather.temperature
        currentWeather.shortday = _(str(element[0].getAttribute('day')))
        currentWeather.day = self.ConvertDay(currentWeather.shortday)
        self.weatherItems[str(-1)] = currentWeather
        index = 1
        for idx in range(len(element) - 1):
            index = idx + 1
            weather = yWeatherItem()
            weather.high = str(element[index].getAttribute('high'))
            weather.low = str(element[index].getAttribute('low'))
            weather.skytext = str(element[index].getAttribute('text'))
            weather.skycode = str(element[index].getAttribute('code'))
            weather.skycodeText = self.ConvertCondition(weather.skycode)
            weather.shortday = _(str(element[index].getAttribute('day')))
            weather.day = self.ConvertDay(weather.shortday)
            filename = '%s%s%s' % (self.iconpath, weather.skycode, self.iconextension)
            weather.iconFilename = filename
            if not os_path.exists(filename):
                url = '%s%s.gif' % (self.imagerelativeurl, weather.skycode)
                filename = '%s%s.gif' % (self.iconpath, weather.skycode)
                if not os_path.exists(filename):
                    IconDownloadList.append(WeatherIconItem(url=url, filename=filename, index=index))
                else:
                    self.showIcon(index, filename)
            else:
                self.showIcon(index, filename)
            self.weatherItems[str(index)] = weather

        if len(IconDownloadList) != 0:
            ds = defer.DeferredSemaphore(tokens=len(IconDownloadList))
            downloads = [ds.run(download, item).addErrback(self.errorIconDownload, item).addCallback(self.finishedIconDownload, item) for item in IconDownloadList]
            finished = defer.DeferredList(downloads).addErrback(self.error).addCallback(self.finishedAllDownloadFiles)
        else:
            self.finishedAllDownloadFiles(None)
        if self.callback is not None:
            self.callback(self.OK, None)
        return


def download(item):
    return downloadPage(item.url, file(item.filename, 'wb'))


return
