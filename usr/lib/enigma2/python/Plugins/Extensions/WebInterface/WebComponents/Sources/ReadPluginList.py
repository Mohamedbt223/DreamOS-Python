# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebComponents/Sources/ReadPluginList.py
# Compiled at: 2025-09-18 23:33:40
from Components.Sources.Source import Source
from Components.PluginComponent import plugins
from Tools.Directories import resolveFilename, SCOPE_PLUGINS

class ReadPluginList(Source):

    def __init__(self, session):
        Source.__init__(self)
        self.session = session
        return

    def command(self):
        print '[WebComponents.ReadPluginList] readPluginList'
        plugins.readPluginList(resolveFilename(SCOPE_PLUGINS))
        return (True, _('List of Plugins has been read'))

    result = property(command)


return
