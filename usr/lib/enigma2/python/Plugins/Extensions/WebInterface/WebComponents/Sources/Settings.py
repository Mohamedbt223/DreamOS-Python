# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebComponents/Sources/Settings.py
# Compiled at: 2025-09-18 23:33:40
from Components.config import config
from Components.Sources.Source import Source

class Settings(Source):

    def __init__(self, session):
        self.cmd = []
        self.session = session
        Source.__init__(self)
        return

    def handleCommand(self, cmd):
        self.cmd = cmd
        return

    def do_func(self):
        result = []
        self.pickle_this('config', config.saved_value, result)
        return result

    def pickle_this(self, prefix, topickle, result):
        for key, val in topickle.items():
            name = prefix + '.' + key
            if isinstance(val, dict):
                self.pickle_this(name, val, result)
            elif isinstance(val, tuple):
                result.append((name, val[0]))
            else:
                result.append((name, val))

        return

    list = property(do_func)
    lut = {'Name': 0, 'Value': 1}


return
