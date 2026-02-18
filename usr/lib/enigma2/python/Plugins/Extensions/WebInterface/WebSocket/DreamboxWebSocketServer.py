# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebSocket/DreamboxWebSocketServer.py
# Compiled at: 2025-09-18 23:33:40
from DreamboxServerProtocol import DreamboxServerProtocol
from autobahn.twisted.websocket import WebSocketServerFactory
from autobahn.twisted.resource import WebSocketResource

class DreamboxWebSocketServer:

    def __init__(self):
        self.session = None
        self._sessions = set()
        self._factory = WebSocketServerFactory(url=None, debug=False, debugCodePaths=False)
        self._factory.setProtocolOptions(autoPingInterval=15, autoPingTimeout=3)
        self._factory.protocol = DreamboxServerProtocol
        self.root = WebSocketResource(self._factory)
        DreamboxServerProtocol.server = None
        return

    def addSession(self, session):
        self._sessions.add(session)
        return

    def removeSession(self, session):
        self._sessions.remove(session)
        return

    def checkSession(self, session):
        return session in self._sessions

    def start(self, session):
        self._session = session
        DreamboxServerProtocol.server = self
        DreamboxServerProtocol.session = session
        return


webSocketServer = DreamboxWebSocketServer()
return
