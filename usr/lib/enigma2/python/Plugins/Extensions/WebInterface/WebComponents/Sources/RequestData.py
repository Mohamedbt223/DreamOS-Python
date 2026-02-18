# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebComponents/Sources/RequestData.py
# Compiled at: 2025-09-18 23:33:40
from Components.Sources.Source import Source

class RequestData(Source):
    """
                a source for requestinformations like the adress that the client requested to reache the box
        """
    HOST = 0
    PORT = 1
    METHOD = 2
    PATH = 3
    PROTOCOL = 4
    REMOTEADRESS = 5
    REMOTEPORT = 6
    REMOTETYPE = 7
    URI = 8

    def __init__(self, request, what=None):
        Source.__init__(self)
        self.request = request
        self.what = what
        return

    def handleCommand(self, cmd):
        return

    def getHTML(self, id):
        if self.what is self.HOST:
            return self.request.getRequestHostname()
        else:
            if self.what is self.PORT:
                return str(self.request.host.port)
            if self.what is self.METHOD:
                return self.request.method
            if self.what is self.PATH:
                return self.request.path
            if self.what is self.PROTOCOL:
                if self.request.isSecure():
                    return 'https'
                return 'http'
            if self.what is self.REMOTEADRESS:
                return self.request.client.ip
            if self.what is self.REMOTEPORT:
                return str(self.request.client.port)
            if self.what is self.REMOTETYPE:
                return self.request.client.type
            if self.what is self.URI:
                return self.request.uri
            return 'N/A'

        return


return
