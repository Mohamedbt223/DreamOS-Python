# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/Oled_DatumToText.py
# Compiled at: 2025-09-12 20:46:41
from Converter import Converter
from time import localtime, strftime
from Components.Element import cached
from Components.config import config

class Oled_DatumToText(Converter, object):
    DEFAULT = 0
    WITH_SECONDS = 1
    IN_MINUTES = 2
    DATE = 3
    FORMAT = 4
    AS_LENGTH = 5
    TIMESTAMP = 6

    def __init__(self, type):
        Converter.__init__(self, type)
        if type == 'WithSeconds':
            self.type = self.WITH_SECONDS
        elif type == 'InMinutes':
            self.type = self.IN_MINUTES
        elif type == 'Date':
            self.type = self.DATE
        elif type == 'AsLength':
            self.type = self.AS_LENGTH
        elif type == 'Timestamp':
            self.type = self.TIMESTAMP
        elif str(type).find('Format') != -1:
            self.type = self.FORMAT
            self.fmt_string = type[7:]
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
            if self.type == self.DATE:
                backstring = strftime('%A %d. %B %Y', t)
                if config.osd.language.value == 'de_DE':
                    backstring = backstring.replace('Monday', 'Montag')
                    backstring = backstring.replace('Tuesday', 'Dienstag')
                    backstring = backstring.replace('Wednesday', 'Mittwoch')
                    backstring = backstring.replace('Thursday', 'Donnerstag')
                    backstring = backstring.replace('Friday', 'Freitag')
                    backstring = backstring.replace('Saturday', 'Samstag')
                    backstring = backstring.replace('Sunday', 'Sonntag')
                    backstring = backstring.replace('January', 'Januar')
                    backstring = backstring.replace('February', 'Februar')
                    backstring = backstring.replace('March', 'März')
                    backstring = backstring.replace('April', 'April')
                    backstring = backstring.replace('May', 'Mai')
                    backstring = backstring.replace('June', 'Juni')
                    backstring = backstring.replace('July', 'Juli')
                    backstring = backstring.replace('October', 'Oktober')
                    backstring = backstring.replace('December', 'Dezember')
                return backstring
            if self.type == self.FORMAT:
                spos = self.fmt_string.find('%')
                apos = self.fmt_string.find('%a')
                aapos = self.fmt_string.find('%A')
                bpos = self.fmt_string.find('%b')
                bbpos = self.fmt_string.find('%B')
                if spos > 0:
                    s1 = self.fmt_string[:spos]
                    s2 = strftime(self.fmt_string[spos:], t)
                    backstring = str(s1 + s2)
                    if config.osd.language.value == 'de_DE':
                        if apos > -1:
                            backstring = backstring.replace('Mon', 'Mo')
                            backstring = backstring.replace('Tue', 'Di')
                            backstring = backstring.replace('Wed', 'Mi')
                            backstring = backstring.replace('Thu', 'Do')
                            backstring = backstring.replace('Fri', 'Fr')
                            backstring = backstring.replace('Sat', 'Sa')
                            backstring = backstring.replace('Sun', 'So')
                        if aapos > -1:
                            backstring = backstring.replace('Monday', 'Montag')
                            backstring = backstring.replace('Tuesday', 'Dienstag')
                            backstring = backstring.replace('Wednesday', 'Mittwoch')
                            backstring = backstring.replace('Thursday', 'Donnerstag')
                            backstring = backstring.replace('Friday', 'Freitag')
                            backstring = backstring.replace('Saturday', 'Samstag')
                            backstring = backstring.replace('Sunday', 'Sonntag')
                        if bpos > -1:
                            backstring = backstring.replace('Mar', 'Mrz')
                            backstring = backstring.replace('May', 'Mai')
                            backstring = backstring.replace('June', 'Jun')
                            backstring = backstring.replace('July', 'Jul')
                            backstring = backstring.replace('Sept', 'Sep')
                            backstring = backstring.replace('Oct', 'Okt')
                            backstring = backstring.replace('Dec', 'Dez')
                        if bbpos > -1:
                            backstring = backstring.replace('January', 'Januar')
                            backstring = backstring.replace('February', 'Februar')
                            backstring = backstring.replace('March', 'März')
                            backstring = backstring.replace('April', 'April')
                            backstring = backstring.replace('May', 'Mai')
                            backstring = backstring.replace('June', 'Juni')
                            backstring = backstring.replace('July', 'Juli')
                            backstring = backstring.replace('October', 'Oktober')
                            backstring = backstring.replace('December', 'Dezember')
                    return backstring
                backstring = strftime(self.fmt_string, t)
                if config.osd.language.value == 'de_DE':
                    if apos > -1:
                        backstring = backstring.replace('Mon', 'Mo')
                        backstring = backstring.replace('Tue', 'Di')
                        backstring = backstring.replace('Wed', 'Mi')
                        backstring = backstring.replace('Thu', 'Do')
                        backstring = backstring.replace('Fri', 'Fr')
                        backstring = backstring.replace('Sat', 'Sa')
                        backstring = backstring.replace('Sun', 'So')
                    if aapos > -1:
                        backstring = backstring.replace('Monday', 'Montag')
                        backstring = backstring.replace('Tuesday', 'Dienstag')
                        backstring = backstring.replace('Wednesday', 'Mittwoch')
                        backstring = backstring.replace('Thursday', 'Donnerstag')
                        backstring = backstring.replace('Friday', 'Freitag')
                        backstring = backstring.replace('Saturday', 'Samstag')
                        backstring = backstring.replace('Sunday', 'Sonntag')
                    if bpos > -1:
                        backstring = backstring.replace('Mar', 'Mrz')
                        backstring = backstring.replace('May', 'Mai')
                        backstring = backstring.replace('June', 'Jun')
                        backstring = backstring.replace('July', 'Jul')
                        backstring = backstring.replace('Sept', 'Sep')
                        backstring = backstring.replace('Oct', 'Okt')
                        backstring = backstring.replace('Dec', 'Dez')
                    if bbpos > -1:
                        backstring = backstring.replace('January', 'Januar')
                        backstring = backstring.replace('February', 'Februar')
                        backstring = backstring.replace('March', 'März')
                        backstring = backstring.replace('April', 'April')
                        backstring = backstring.replace('May', 'Mai')
                        backstring = backstring.replace('June', 'Juni')
                        backstring = backstring.replace('July', 'Juli')
                        backstring = backstring.replace('October', 'Oktober')
                        backstring = backstring.replace('December', 'Dezember')
                return backstring
            else:
                return '???'
            return

    text = property(getText)


return
