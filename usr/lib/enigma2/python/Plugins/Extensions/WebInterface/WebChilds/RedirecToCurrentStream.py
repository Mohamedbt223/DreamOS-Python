# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebChilds/RedirecToCurrentStream.py
# Compiled at: 2025-09-18 23:33:39
from twisted.web import resource, server
from ServiceReference import ServiceReference

class RedirecToCurrentStreamResource(resource.Resource):
    """
                used to redirect the client to the streamproxy with the current service tuned on TV
        """

    def __init__(self, session):
        resource.Resource.__init__(self)
        self.session = session
        return

    def render(self, request):
        currentServiceRef = self.session.nav.getCurrentlyPlayingServiceReference()
        if currentServiceRef is not None:
            sref = currentServiceRef.toString()
        else:
            sref = 'N/A'
        request.redirect('http://%s:8001/%s' % (request.getHost().host, sref))
        request.finish()
        return server.NOT_DONE_YET


return
