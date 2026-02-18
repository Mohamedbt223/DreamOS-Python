# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/TSEcmInfo.py
# Compiled at: 2013-11-10 15:41:40
from enigma import iServiceInformation, iPlayableService
from os import popen as os_popen
from Components.Converter.Converter import Converter
from Components.Element import cached
from Tools.Directories import fileExists
from Poll import Poll

class TSEcmInfo(Poll, Converter, object):

    def __init__(self, type):
        Poll.__init__(self)
        Converter.__init__(self, type)
        self.poll_interval = 2000
        self.poll_enabled = True
        return

    @cached
    def getText(self):
        ecminfo = 'No ECM Info.'
        if self.source.service and self.source.service.info():
            if fileExists('/tmp/ecm.info'):
                cmd = 'cat /tmp/ecm.info'
                ecminfo = self.getCmdOutput(cmd)
        return ecminfo

    text = property(getText)

    def changed(self, what):
        if what[0] == self.CHANGED_SPECIFIC and what[1] == iPlayableService.evUpdatedInfo or what[0] == self.CHANGED_POLL:
            Converter.changed(self, what)
        return

    def getCmdOutput(self, cmd):
        pipe = os_popen('{ ' + cmd + '; } 2>&1', 'r')
        text = pipe.read()
        pipe.close()
        if text[-1:] == '\n':
            text = text[:-1]
        return text


return
