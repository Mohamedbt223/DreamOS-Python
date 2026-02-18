# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/TSRotator.py
from Converter import Converter
from Poll import Poll
from Components.Element import cached
from time import strftime
from Components.config import config

class TSRotator(Poll, Converter, object):
    """Static Text Converter Rotator"""

    def __init__(self, type):
        Poll.__init__(self)
        Converter.__init__(self, type)
        self.mainstream = None
        self.sourceList = []
        self.sourceIndex = -1
        if int(config.plugins.TSSkinSetup.piconOledSwitchTime.value) != 0:
            self.poll_interval = int(config.plugins.TSSkinSetup.piconOledSwitchTime.value) * 1000
        else:
            self.poll_interval = int(config.plugins.TSSkinSetup.piconOledSwitchTime.value + 1) * 1000
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
            if int(config.plugins.TSSkinSetup.piconOledSwitchTime.value) != 0:
                self.poll_interval = int(config.plugins.TSSkinSetup.piconOledSwitchTime.value) * 1000
                prev_source = self.sourceList[self.sourceIndex][0].source
                self.sourceList[self.sourceIndex][0].source = self.mainstream
                result = self.sourceList[self.sourceIndex][0].text or ''
                self.sourceList[self.sourceIndex][0].source = prev_source
            else:
                self.poll_interval = int(config.plugins.TSSkinSetup.piconOledSwitchTime.value + 18000) * 1000
                prev_source = self.sourceList[self.sourceIndex][0].source
                self.sourceList[self.sourceIndex][0].source = self.mainstream
                result = self.sourceList[self.sourceIndex][0].text or ''
                self.sourceList[self.sourceIndex][0].source = prev_source
        return result

    text = property(getText)

    def changed(self, what, parent=None):
        if config.plugins.TSSkinSetup.piconOledEnabled.value:
            if int(config.plugins.TSSkinSetup.piconOledSwitchTime.value) != 0:
                self.poll_interval = int(config.plugins.TSSkinSetup.piconOledSwitchTime.value) * 1000
            else:
                self.poll_interval = int(config.plugins.TSSkinSetup.piconOledSwitchTime.value + 1) * 1000
            self.poll_enabled = True
        else:
            self.poll_enabled = False
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
