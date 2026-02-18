# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/Oled_ConverterRotator.py
# Compiled at: 2020-08-06 17:48:48
from Components.Converter.Converter import Converter
from Components.Converter.Oled_Poll import Oled_Poll
from Components.Element import cached

class Oled_ConverterRotator(Oled_Poll, Converter, object):
    """Static Text Converter Rotator"""

    def __init__(self, type):
        Oled_Poll.__init__(self)
        Converter.__init__(self, type)
        self.mainstream = None
        self.sourceList = []
        self.sourceIndex = -1
        if type and type.isdigit():
            self.poll_interval = int(type) * 1000
        return

    def poll(self):
        self.sourceIndex = (self.sourceIndex + 1) % len(self.sourceList)
        self.downstream_elements.changed((self.CHANGED_POLL,))
        return

    def doSuspend(self, suspended):
        if self.mainstream and len(self.sourceList) != 0:
            if suspended:
                self.poll_enabled = False
            else:
                self.sourceIndex = len(self.sourceList) - 1
                self.poll_enabled = True
                self.poll()
        return

    @cached
    def getText(self):
        result = ''
        if self.poll_enabled:
            prev_source = self.sourceList[self.sourceIndex][0].source
            self.sourceList[self.sourceIndex][0].source = self.mainstream
            result = self.sourceList[self.sourceIndex][0].text or ''
            self.sourceList[self.sourceIndex][0].source = prev_source
        return result

    text = property(getText)

    def changed(self, what, parent=None):
        if what[0] == self.CHANGED_DEFAULT and not len(self.sourceList):
            upstream = self.source
            while upstream:
                self.sourceList.insert(0, (upstream, hasattr(upstream, 'poll_enabled')))
                upstream = upstream.source

            if len(self.sourceList):
                self.mainstream = self.sourceList.pop(0)[0]
        self.downstream_elements.changed(what)
        return


return
