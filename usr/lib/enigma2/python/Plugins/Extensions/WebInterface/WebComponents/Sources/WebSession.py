# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebComponents/Sources/WebSession.py
# Compiled at: 2025-09-18 23:33:40
from Components.Sources.Source import Source
import uuid

class WebSession(Source):

    def __init__(self, request):
        Source.__init__(self)
        self.request = request
        return

    def getText(self):
        return self.request.enigma2_session.id

    text = property(getText)


return
