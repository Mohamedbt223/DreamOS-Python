# uncompyle6 version 3.9.0
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.8.10 (default, Nov 22 2023, 10:22:35) 
# [GCC 9.4.0]
# Embedded file name: /usr/lib/enigma2/python/Components/WeatherYahoo.py
# Compiled at: 2025-08-21 18:06:06
from __future__ import print_function
import sys, json, time
from time import localtime, strftime
from datetime import datetime
PY3 = sys.version_info[0] >= 3
if PY3:
    text_type = str
    binary_type = bytes
else:
    text_type = unicode
    binary_type = str
try:
    from urllib import quote as urlquote
except Exception:
    from urllib.parse import quote as urlquote

from twisted.web.client import getPage
try:
    from Components.config import config
except Exception:
    config = None

def _s(v):
    try:
        if isinstance(v, text_type):
            return v
        else:
            if isinstance(v, binary_type):
                try:
                    return v.decode('utf-8', 'ignore')
                except Exception:
                    return text_type(v)

            return text_type(v)

    except Exception:
        if not PY3:
            return ''
        return ''


def _to_bytes(u):
    if isinstance(u, binary_type):
        return u
    try:
        return _s(u).encode('utf-8', 'ignore')
    except Exception:
        return binary_type(u)


def _quote_name(name):
    return urlquote((PY3 or _s(name).encode)('utf-8') if 1 else _s(name))


def _unit_flag():
    try:
        u = _s(config.plugins.TSWeather.tempUnit.value).lower()
        if u.startswith('f'):
            return ('fahrenheit', 'F')
        return ('celsius', 'C')
    except Exception:
        return ('celsius', 'C')


def _city():
    try:
        return _s(config.plugins.TSWeather.location.value).strip()
    except Exception:
        return ''


def _parse_coords(val):
    try:
        s = _s(val).strip()
        if ',' in s:
            lat, lon = s.split(',', 1)
            return (
             float(lat.strip()), float(lon.strip()))
    except Exception:
        pass

    return (None, None)


def _abbr_day(iso_date):
    try:
        dt = datetime.strptime(_s(iso_date), '%Y-%m-%d')
        return ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][dt.weekday()]
    except Exception:
        return _s(iso_date)


def _compass(deg):
    try:
        d = float(deg) % 360.0
    except Exception:
        return ''

    dirs = [
     'N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 
     'S', 
     'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    i = int((d + 11.25) / 22.5) % 16
    return dirs[i]


def _fmt_ampm(iso_ts):
    try:
        t = datetime.strptime(_s(iso_ts).replace('Z', ''), '%Y-%m-%dT%H:%M')
        h = t.hour
        m = t.minute
        ampm = 'am' if h < 12 else 'pm'
        h12 = h % 12
        if h12 == 0:
            h12 = 12
        return '%d:%02d %s' % (h12, m, ampm)
    except Exception:
        return '---'


WMO_TO_TEXT = {0: 'Clear', 
   1: 'Mainly clear', 2: 'Partly cloudy', 3: 'Cloudy', 45: 'Fog', 
   48: 'Rime fog', 51: 'Light drizzle', 
   53: 'Drizzle', 55: 'Heavy drizzle', 56: 'Freezing drizzle', 
   57: 'Freezing drizzle', 61: 'Light rain', 
   63: 'Rain', 65: 'Heavy rain', 66: 'Freezing rain', 
   67: 'Heavy freezing rain', 71: 'Light snow', 
   73: 'Snow', 75: 'Heavy snow', 77: 'Snow grains', 
   80: 'Rain showers', 
   81: 'Rain showers', 82: 'Violent rain showers', 85: 'Snow showers', 
   86: 'Snow showers', 95: 'Thunderstorm', 
   96: 'Thunderstorm w/ hail', 99: 'Thunderstorm w/ hail'}
WMO_TO_YAHOO = {0: 32, 
   1: 34, 2: 30, 3: 26, 45: 20, 
   48: 20, 51: 9, 
   53: 9, 55: 9, 56: 8, 
   57: 8, 61: 11, 
   63: 12, 65: 12, 66: 10, 
   67: 10, 71: 16, 
   73: 16, 75: 16, 77: 13, 
   80: 11, 
   81: 12, 82: 12, 85: 16, 
   86: 16, 95: 3, 
   96: 3, 99: 3}

class _ItemsDict(dict):

    def has_key(self, k):
        return k in self

    def __unicode__(self):
        return ''

    def __str__(self):
        return ''


class _Item(object):

    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)

    def __getattr__(self, name):
        return ''

    if not PY3:

        def __unicode__(self):
            return ''

    def __str__(self):
        return ''


class _WeatherData(object):

    def __init__(self):
        self.city = ''
        self.region = ''
        self.country = ''
        self.degreetype = 'C'
        self.weatherItems = _ItemsDict()

    if not PY3:

        def __unicode__(self):
            return ''

    def __str__(self):
        return ''


class _WeatherWrapper(object):

    def __init__(self):
        self.weatherData = _WeatherData()
        self.callbacksAllIconsDownloaded = []
        self.callbacksDataUpdated = []
        self._pending_cb = None
        self.last_ok = 0
        return

    def resetData(self):
        unit_chr = _unit_flag()[1]
        self.weatherData = _WeatherData()
        self.weatherData.degreetype = unit_chr

    def getData(self, token=None, callback=None):
        """token may be None, 'lat,lon', city text, or legacy WOEID (ignored)."""
        self._pending_cb = callback
        lat, lon = _parse_coords(token)
        if lat is not None and lon is not None:
            self._fetch(lat, lon, token_city=None)
            return
        else:
            name = _s(token).strip()
            if name and not name.isdigit() and ',' not in name:
                self._geocode_and_fetch(name)
            else:
                name = _city()
                if not name:
                    self._fetch(0.0, 0.0, token_city='')
                else:
                    self._geocode_and_fetch(name)
            return

    def downloadAllWeatherIcons(self, *a, **k):
        self._notify_icons_ready()

    def _notify_icons_ready(self):
        for cb in list(self.callbacksAllIconsDownloaded):
            try:
                cb()
            except Exception:
                pass

    def _notify_data_updated(self):
        for cb in list(self.callbacksDataUpdated):
            try:
                cb()
            except Exception:
                pass

    def _finish_ok(self):
        self._notify_icons_ready()
        self._notify_data_updated()
        cb, self._pending_cb = self._pending_cb, None
        if cb:
            try:
                cb(True, None)
            except Exception:
                pass

        return

    def _finish_err(self, msg):
        self._notify_icons_ready()
        cb, self._pending_cb = self._pending_cb, None
        if cb:
            try:
                cb(None, _s(msg) or 'Weather fetch failed')
            except Exception:
                pass

        return

    def _geocode_and_fetch(self, name):
        url = 'https://geocoding-api.open-meteo.com/v1/search?count=1&language=en&name=' + _quote_name(name)

        def _ok(body):
            meta = {}
            try:
                if isinstance(body, binary_type):
                    body = body.decode('utf-8', 'ignore')
                js = json.loads(body)
                r = (js.get('results') or [])[0]
                lat = float(r['latitude'])
                lon = float(r['longitude'])
                meta = {'city': r.get('name') or name, 'country': r.get('country') or '', 
                   'region': r.get('admin1') or ''}
            except Exception as e:
                print('[Weather] Geocoding failed for "%s": %s' % (name, e))
                lat, lon = (0.0, 0.0)
                meta = {'city': name, 'country': '', 'region': ''}

            self._fetch(lat, lon, token_city=meta.get('city') or name, meta=meta)

        def _err(err):
            print('[Weather] Geocoding error for "%s": %s' % (name, err))
            self._fetch(0.0, 0.0, token_city=name, meta={'city': name, 'country': '', 'region': ''})

        try:
            getPage(_to_bytes(url)).addCallback(_ok).addErrback(_err)
        except Exception as e:
            print('[Weather] getPage exception (geocode):', e)
            self._fetch(0.0, 0.0, token_city=name, meta={'city': name, 'country': '', 'region': ''})

    def _fetch(self, lat, lon, token_city, meta=None):
        unit_api, unit_chr = _unit_flag()
        url = 'https://api.open-meteo.com/v1/forecast?latitude=%s&longitude=%s&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,wind_direction_10m,pressure_msl&daily=weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset&timezone=auto&temperature_unit=%s&windspeed_unit=kmh' % (
         lat, lon, unit_api)

        def _ok(body):
            try:
                if isinstance(body, binary_type):
                    body = body.decode('utf-8', 'ignore')
                js = json.loads(body)
            except Exception as e:
                print('[Weather] JSON parse error:', e)
                self._finish_err('Weather data parse error')
                return

            cur = js.get('current') or js.get('current_weather') or {}
            daily = js.get('daily') or {}
            wcode = cur.get('weather_code') or cur.get('weathercode')
            temp = cur.get('temperature_2m') or cur.get('temperature')
            rh = cur.get('relative_humidity_2m')
            wind = cur.get('wind_speed_10m') or cur.get('windspeed')
            wdir = cur.get('wind_direction_10m') or cur.get('winddirection')
            pres = cur.get('pressure_msl')
            text = WMO_TO_TEXT.get(wcode, 'N/A')
            ycode = WMO_TO_YAHOO.get(wcode, 3200)
            times = daily.get('time') or []
            dcode = daily.get('weather_code') or daily.get('weathercode') or []
            tmax = daily.get('temperature_2m_max') or []
            tmin = daily.get('temperature_2m_min') or []
            sunrise = daily.get('sunrise') or []
            sunset = daily.get('sunset') or []
            wd = _WeatherData()
            wd.city = _s((meta or {}).get('city') or token_city or _city())
            wd.country = _s((meta or {}).get('country') or '')
            wd.region = _s((meta or {}).get('region') or '')
            wd.degreetype = _s(unit_chr)
            items = _ItemsDict()
            hi0 = '' if not tmax or tmax[0] is None else str(int(round(tmax[0])))
            lo0 = '' if not tmin or tmin[0] is None else str(int(round(tmin[0])))
            sr0 = _fmt_ampm(sunrise[0]) if sunrise else '---'
            ss0 = _fmt_ampm(sunset[0]) if sunset else '---'
            items['-1'] = _Item(sunrise=_s(sr0), sunset=_s(ss0), temperature=_s('' if temp is None else int(round(temp))), unittemperature=_s(unit_chr), high=_s(hi0), low=_s(lo0), humidity=_s('' if rh is None else int(round(rh))), visibility='', unitdistance='km', windspeed=_s('' if wind is None else int(round(wind))), unitspeed='km/h', winddirection=_s('' if wdir is None else _compass(wdir)), pressure=_s('' if pres is None else int(round(pres))), unitpressure='hPa', day=_s(_abbr_day(times[0]) if times else ''), shortday=_s(_abbr_day(times[0]) if times else ''), stand=_s(strftime('%H:%M', localtime(int(time.time())))), skytext=_s(text), skycodeText=_s(text), code=_s(ycode), iconFilename=_s('/usr/share/enigma2/TSimage/weather/%s.png' % (ycode,)))
            for i in range(0, min(4, len(times))):
                code_i = WMO_TO_YAHOO.get(dcode[i], 3200) if i < len(dcode) else 3200
                hi = '' if i >= len(tmax) or tmax[i] is None else str(int(round(tmax[i])))
                lo = '' if i >= len(tmin) or tmin[i] is None else str(int(round(tmin[i])))
                items[str(i + 1)] = _Item(high=_s(hi), low=_s(lo), unittemperature=_s(unit_chr), day=_s(_abbr_day(times[i])), shortday=_s(_abbr_day(times[i])), skytext=_s(WMO_TO_TEXT.get(dcode[i], 'N/A') if i < len(dcode) else 'N/A'), skycodeText=_s(WMO_TO_TEXT.get(dcode[i], 'N/A') if i < len(dcode) else 'N/A'), code=_s(code_i), iconFilename=_s('/usr/share/enigma2/TSimage/weather/%s.png' % (code_i,)))

            for k, it in list(items.items()):
                try:
                    for attr, val in list(it.__dict__.items()):
                        if not isinstance(val, text_type):
                            setattr(it, attr, _s(val))

                except Exception:
                    pass

            wd.weatherItems = items
            self.weatherData = wd
            self.last_ok = int(time.time())
            self._finish_ok()
            return

        def _err(err):
            print('[Weather] fetch error:', err)
            self._finish_err('Weather fetch error')

        try:
            getPage(_to_bytes(url)).addCallback(_ok).addErrback(_err)
        except Exception as e:
            print('[Weather] getPage exception (forecast):', e)
            self._finish_err('Weather request failed')


weatheryahoo = _WeatherWrapper()