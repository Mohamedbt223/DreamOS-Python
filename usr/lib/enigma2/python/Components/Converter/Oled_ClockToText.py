# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/Oled_ClockToText.py
# Compiled at: 2017-08-01 20:14:45
from Converter import Converter
from time import localtime, strftime
from Components.Element import cached
from Components.config import config, ConfigSubsection, ConfigText, ConfigSelection
import locale
strclock = [
 (
  '1', _('HH:MM')),
 (
  '2', _('HH:MM:SS'))]
config.plugins.displayskin = ConfigSubsection()
config.plugins.displayskin.oled_clock = ConfigSelection(default='2', choices=strclock)

class Oled_ClockToText(Converter, object):
    DEFAULT = 0
    WITH_SECONDS = 1
    IN_MINUTES = 2
    DATE = 3
    FORMAT = 4
    AS_LENGTH = 5
    TIMESTAMP = 6
    OLED_DEFAULT = 7

    def __init__(self, type):
        Converter.__init__(self, type)
        if type == 'WithSeconds':
            self.type = self.WITH_SECONDS
            self.isAnimated = False
        if type == 'oled_default':
            self.type = self.OLED_DEFAULT
            self.isAnimated = False
        elif type == 'InMinutes':
            self.type = self.IN_MINUTES
        elif type == 'Date':
            self.type = self.DATE
        elif type == 'AsLength':
            self.type = self.AS_LENGTH
        elif type == 'Timestamp':
            self.type = self.TIMESTAMP
            self.isAnimated = False
        elif str(type).find('Format') != -1:
            self.type = self.FORMAT
            self.fmt_string = type[7:]
            self.isAnimated = False
        else:
            self.type = self.DEFAULT
        return

    @cached
    def getText(self):
        time = self.source.time
        if time is None:
            return ''
        else:
            if self.type == self.IN_MINUTES:
                return '%d min' % (time / 60)
            if self.type == self.AS_LENGTH:
                return '%d:%02d' % (time / 60, time % 60)
            if self.type == self.TIMESTAMP:
                return str(time)
            t = localtime(time)
            if self.type == self.WITH_SECONDS:
                return '%2d:%02d:%02d' % (t.tm_hour, t.tm_min, t.tm_sec)
            if self.type == self.DEFAULT:
                return '%02d:%02d' % (t.tm_hour, t.tm_min)
            if self.type == self.OLED_DEFAULT:
                try:
                    if config.plugins.displayskin.oled_clock.value == '2':
                        return '%2d:%02d:%02d' % (t.tm_hour, t.tm_min, t.tm_sec)
                    else:
                        return '%02d:%02d' % (t.tm_hour, t.tm_min)

                except:
                    return '%02d:%02d' % (t.tm_hour, t.tm_min)

            elif self.type == self.DATE:
                return strftime('%a, %x', t)
            if self.type == self.FORMAT:
                spos = self.fmt_string.find('%')
                if spos > -1:
                    s1 = self.fmt_string[:spos]
                    s2 = strftime(self.fmt_string[spos:], t)
                    return str(s1 + s2)
                return strftime(self.fmt_string, t)
            else:
                return '???'
            return

    text = property(getText)


return
