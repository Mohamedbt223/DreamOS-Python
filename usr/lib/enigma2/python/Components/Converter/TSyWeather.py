# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/TSyWeather.py
# Compiled at: 2025-09-16 17:52:22
from Components.Converter.Converter import Converter
from Components.Element import cached

class TSyWeather(Converter, object):
    CURRENT = -1
    CITY = 0
    DAY1 = 1
    DAY2 = 2
    DAY3 = 3
    DAY4 = 4
    DAY5 = 5
    TEMPERATURE_HIGH = 6
    TEMPERATURE_LOW = 7
    TEMPERATURE_TEXT = 8
    TEMPERATURE_CURRENT = 9
    WEEKDAY = 10
    SHORTWEEKDAY = 11
    STAND = 12
    SUNRISE = 13
    SUNSET = 14
    HUMIDITY = 15
    WINDSPEED = 16
    ICON = 17
    TEMPERATURE_HIGH_LOW = 18
    PATH = 19
    CODETEXT = 20
    UNIT = 21
    COUNTRY = 22
    VISIBILITY = 23
    PRESSURE = 24
    TEMPERATURE_CURRENT_UNIT = 25

    def __init__(self, type):
        Converter.__init__(self, type)
        self.index = None
        self.mode = None
        self.path = None
        self.extension = None
        if type == 'city':
            self.mode = self.CITY
        elif type == 'country':
            self.mode = self.COUNTRY
        elif type == 'stand':
            self.mode = self.STAND
        elif type == 'unit':
            self.mode = self.UNIT
        elif type == 'sunrise':
            self.mode = self.SUNRISE
        elif type == 'sunset':
            self.mode = self.SUNSET
        elif type == 'temperature_current':
            self.mode = self.TEMPERATURE_CURRENT
        elif type == 'temperature_current_unit':
            self.mode = self.TEMPERATURE_CURRENT_UNIT
        elif type == 'humidity':
            self.mode = self.HUMIDITY
        elif type == 'visibility':
            self.mode = self.VISIBILITY
        elif type == 'windspeed':
            self.mode = self.WINDSPEED
        elif type == 'pressure':
            self.mode = self.PRESSURE
        else:
            if 'weathericon' in type:
                self.mode = self.ICON
            elif 'codetext' in type:
                self.mode = self.CODETEXT
            elif 'temperature_high_low' in type:
                self.mode = self.TEMPERATURE_HIGH_LOW
            elif 'temperature_high' in type:
                self.mode = self.TEMPERATURE_HIGH
            elif 'temperature_low' in type:
                self.mode = self.TEMPERATURE_LOW
            elif 'temperature_text' in type:
                self.mode = self.TEMPERATURE_TEXT
            elif 'weekday_short' in type:
                self.mode = self.SHORTWEEKDAY
            elif 'weekday' in type:
                self.mode = self.WEEKDAY
            if self.mode is not None:
                dd = type.split(',')
                if len(dd) >= 2:
                    self.index = self.getIndex(dd[1])
                if self.mode == self.ICON and len(dd) == 4:
                    self.path = dd[2]
                    self.extension = dd[3]
        return

    def _safe(self, v):
        if v is None or v == 'None':
            return ''
        try:
            if isinstance(v, unicode):
                return v.encode('utf-8', 'ignore')
            else:
                return str(v)

        except Exception:
            return ''

        return

    def getIndex(self, key):
        if key == 'current':
            return self.CURRENT
        if key == 'day1':
            return self.DAY1
        if key == 'day2':
            return self.DAY2
        if key == 'day3':
            return self.DAY3
        if key == 'day4':
            return self.DAY4
        if key == 'day5':
            return self.DAY5
        return

    @cached
    def getText(self):
        m = self.mode
        s = self.source
        if m == self.CITY:
            return self._safe(s.getCity())
        else:
            if m == self.COUNTRY:
                return self._safe(s.getCountry())
            if m == self.STAND:
                return self._safe(s.getStand())
            if m == self.UNIT:
                return self._safe(s.getUnit())
            if m == self.SUNRISE:
                return self._safe(s.getSunrise())
            if m == self.SUNSET:
                return self._safe(s.getSunset())
            if m == self.TEMPERATURE_CURRENT:
                return self._safe(s.getTemperature_Current())
            if m == self.TEMPERATURE_CURRENT_UNIT:
                return self._safe(s.getTemperature_Current()) + self._safe(s.getUnit())
            if m == self.CODETEXT and self.index is not None:
                return self._safe(s.getCodeText(self.index))
            if m == self.HUMIDITY:
                return self._safe(s.getHumidity())
            if m == self.VISIBILITY:
                return self._safe(s.getVisibility())
            if m == self.WINDSPEED:
                return self._safe(s.getWindspeed())
            if m == self.PRESSURE:
                return self._safe(s.getPressure())
            if m == self.TEMPERATURE_HIGH and self.index is not None:
                return self._safe(s.getTemperature_High(self.index))
            if m == self.TEMPERATURE_LOW and self.index is not None:
                return self._safe(s.getTemperature_Low(self.index))
            if m == self.TEMPERATURE_HIGH_LOW and self.index is not None:
                return self._safe(s.getTemperature_High_Low(self.index))
            if m == self.TEMPERATURE_TEXT and self.index is not None:
                return self._safe(s.getTemperature_Text(self.index))
            if m == self.SHORTWEEKDAY and self.index is not None:
                return self._safe(s.getShortWeekday(self.index))
            if m == self.WEEKDAY and self.index is not None:
                return self._safe(s.getWeekday(self.index))
            return ''

    text = property(getText)

    @cached
    def getIconFilename(self):
        if self.mode == self.ICON and self.index in (self.CURRENT, self.DAY1, self.DAY2, self.DAY3, self.DAY4, self.DAY5):
            if self.path is not None and self.extension is not None:
                return self.path + self._safe(self.source.getCode(self.index)) + '.' + self.extension
            return self.source.getWeatherIconFilename(self.index) or ''
        else:
            return ''

    iconfilename = property(getIconFilename)


return
