# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Components/Sources/TSyWeather.py
# Compiled at: 2025-08-21 17:11:09
import sys
from Source import Source
from Components.WeatherYahoo import weatheryahoo
from Components.config import config
PY3 = sys.version_info[0] >= 3
try:
    unicode
except NameError:
    unicode = str

def _u(x):
    if isinstance(x, unicode):
        return x
    try:
        return x.decode('utf-8', 'ignore')
    except Exception:
        try:
            return unicode(x)
        except Exception:
            return u''

    return


def _out(x):
    """Return text in the exact type Enigma expects:
       - Py2: bytes (utf-8)
       - Py3: str
    """
    if PY3:
        if isinstance(x, str):
            return x
        return str(x)
    if isinstance(x, unicode):
        return x.encode('utf-8', 'ignore')
    if isinstance(x, str):
        return x
    try:
        return unicode(x).encode('utf-8', 'ignore')
    except Exception:
        return ''

    return


DEG = u'\u'

class TSyWeather(Source):

    def __init__(self):
        Source.__init__(self)
        weatheryahoo.callbacksAllIconsDownloaded.append(self._onAnyUpdate)
        weatheryahoo.callbacksDataUpdated.append(self._onAnyUpdate)
        weatheryahoo.getData()
        return

    def _onAnyUpdate(self, *a, **k):
        self.changed((self.CHANGED_ALL,))
        return

    def _item(self, key):
        try:
            d = weatheryahoo.weatherData.weatherItems
            k = unicode(key)
            if d.has_key(k):
                return d[k]
            return
        except Exception:
            return

        return

    def getCity(self):
        city = _u(getattr(weatheryahoo.weatherData, 'city', u'')) or _u(getattr(config.plugins.TSWeather.location, 'value', u''))
        return _out(city)

    def getCountry(self):
        reg = _u(getattr(weatheryahoo.weatherData, 'region', u''))
        c = _u(getattr(weatheryahoo.weatherData, 'country', u''))
        txt = reg + u', ' + c if reg and c else c or u''
        return _out(txt)

    def getSunrise(self):
        it = self._item(-1)
        return _out(_u(getattr(it, 'sunrise', u'n/a')) if it else u'n/a')

    def getSunset(self):
        it = self._item(-1)
        return _out(_u(getattr(it, 'sunset', u'n/a')) if it else u'n/a')

    def getTemperature_High(self, key):
        it = self._item(key)
        cur = self._item(-1)
        if not it:
            return _out(u'n/a')
        val = _u(getattr(it, 'high', u''))
        if not val:
            return _out(u'n/a')
        unit = _u(getattr(cur, 'unittemperature', u'C')) if cur else u'C'
        return _out(u'%s%s%s' % (val, DEG, unit))

    def getTemperature_Low(self, key):
        it = self._item(key)
        cur = self._item(-1)
        if not it:
            return _out(u'n/a')
        val = _u(getattr(it, 'low', u''))
        if not val:
            return _out(u'n/a')
        unit = _u(getattr(cur, 'unittemperature', u'C')) if cur else u'C'
        return _out(u'%s%s%s' % (val, DEG, unit))

    def getTemperature_High_Low(self, key):
        hi = _u(self.getTemperature_High(key))
        lo = _u(self.getTemperature_Low(key))
        if hi == u'n/a' and lo == u'n/a':
            return _out(u'n/a')
        return _out(u'%s - %s' % (hi, lo))

    def getTemperature_Text(self, key):
        it = self._item(key)
        return _out(_u(getattr(it, 'skytext', u'n/a')) if it else u'n/a')

    def getTemperature_Current(self):
        it = self._item(-1)
        return _out(_u(getattr(it, 'temperature', u'n/a')) if it else u'n/a')

    def getHumidity(self):
        it = self._item(-1)
        return _out(_u(getattr(it, 'humidity', u'n/a')) if it else u'n/a')

    def getVisibility(self):
        it = self._item(-1)
        if not it:
            return _out(u'n/a')
        vis = _u(getattr(it, 'visibility', u''))
        unit = _u(getattr(it, 'unitdistance', u''))
        out = (vis + u' ' + unit).strip() or (u'-- ' + unit if unit else u'n/a')
        return _out(out)

    def getWindspeed(self):
        it = self._item(-1)
        if not it:
            return _out(u'n/a')
        spd = _u(getattr(it, 'windspeed', u''))
        unit = _u(getattr(it, 'unitspeed', u''))
        wdr = _u(getattr(it, 'winddirection', u''))
        parts = [p for p in (spd, unit, wdr) if p]
        return _out((u' ').join(parts) if parts else u'n/a')

    def getPressure(self):
        it = self._item(-1)
        if not it:
            return _out(u'n/a')
        val = _u(getattr(it, 'pressure', u''))
        unit = _u(getattr(it, 'unitpressure', u''))
        out = (val + u' ' + unit).strip() or u'n/a'
        return _out(out)

    def getWeekday(self, key):
        it = self._item(key)
        return _out(_u(getattr(it, 'day', u'n/a')) if it else u'n/a')

    def getShortWeekday(self, key):
        it = self._item(key)
        return _out(_u(getattr(it, 'shortday', u'')) + u'.' if it else u'n/a')

    def getStand(self):
        it = self._item(-1)
        return _out(_u(getattr(it, 'stand', u'n/a')) if it else u'n/a')

    def getWeatherIconFilename(self, key):
        it = self._item(key)
        return _out(_u(getattr(it, 'iconFilename', u'')) if it else u'')

    def getCode(self, key):
        it = self._item(key)
        return _out(_u(getattr(it, 'code', u'')) if it else u'')

    def getCodeText(self, key):
        it = self._item(key)
        return _out(_u(getattr(it, 'skycodeText', u'')) if it else u'(')

    def getUnit(self):
        try:
            unit = _u(weatheryahoo.weatherData.degreetype)
            unit = u'F' if unit.upper().startswith(u'F') else u'C'
        except Exception:
            unit = u'C'

        return _out(DEG + unit)

    def destroy(self):
        try:
            weatheryahoo.callbacksAllIconsDownloaded.remove(self._onAnyUpdate)
        except Exception:
            pass

        try:
            weatheryahoo.callbacksDataUpdated.remove(self._onAnyUpdate)
        except Exception:
            pass

        Source.destroy(self)
        return


return
