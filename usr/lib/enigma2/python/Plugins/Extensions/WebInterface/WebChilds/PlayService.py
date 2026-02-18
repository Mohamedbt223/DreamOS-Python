# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebChilds/PlayService.py
# Compiled at: 2025-09-18 23:33:39
from enigma import eServiceReference
from twisted.web import resource, http, server
from os import path as os_path

class ServiceplayerResource(resource.Resource):

    def __init__(self, session):
        resource.Resource.__init__(self)
        self.session = session
        self.oldservice = None
        return

    def render(self, request):
        if 'file' in request.args:
            output = self.playFile(request.args['file'][0])
        elif 'url' in request.args:
            output = self.playURL(request.args['url'][0])
        elif 'stop' in request.args:
            output = self.stopServicePlay()
        else:
            output = (
             True, 'unknown command')
        request.setResponseCode(http.OK)
        return output[1]

    def playFile(self, path):
        print '[ServiceplayerResource] playing file', path
        if os_path.exists(path) is not True:
            return (False, 'given path is not existing, %s' % path)
        else:
            sref = '4097:0:0:0:0:0:0:0:0:0:%s' % path
            self.startServicePlay(eServiceReference(sref))
            return (True, 'playing path started, %s' % path)

        return

    def playURL(self, url):
        return (
         False, 'Not implemented')

    def startServicePlay(self, esref):
        print '[ServiceplayerResource] playing sref', esref.toString()
        csref = self.session.nav.getCurrentlyPlayingServiceReference()
        if csref is not None:
            if csref.toString().startswith('4097') is not True:
                self.oldservice = (
                 csref.toString(), csref)
        self.session.nav.stopService()
        self.session.nav.playService(esref)
        return

    def stopServicePlay(self):
        print '[ServiceplayerResource] stopping service', self.oldservice
        self.session.nav.stopService()
        if self.oldservice is not None:
            self.session.nav.playService(self.oldservice[1])
            return (
             True, '[ServiceplayerResource] stopped, now playing old service, %s' % self.oldservice[0])
        else:
            return (
             True, '[ServiceplayerResource] stopped')
            return


return
