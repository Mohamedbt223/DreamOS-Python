# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebComponents/Sources/SubServices.py
# Compiled at: 2025-09-18 23:33:40
from Components.Sources.Source import Source
from ServiceReference import ServiceReference

class SubServices(Source):

    def __init__(self, session, streamingScreens=None):
        Source.__init__(self)
        self.session = session
        self.streamingScreens = streamingScreens
        self.cmd = None
        return

    def handleCommand(self, cmd):
        if cmd is not None:
            print '[SubServices].handleCommand %s' % cmd
            self.cmd = cmd
        return

    def getSubservices(self):
        print '[SubServices].getSubservices called'
        list = []
        if self.streamingScreens is None:
            currentServiceRef = self.session.nav.getCurrentlyPlayingServiceReference()
            if currentServiceRef is not None:
                list.append((
                 currentServiceRef.toString(),
                 ServiceReference(currentServiceRef).getServiceName()))
                currentService = self.session.nav.getCurrentService()
                subservices = currentService and currentService.subServices()
                if subservices and subservices.getNumberOfSubservices() != 0:
                    n = subservices and subservices.getNumberOfSubservices()
                    x = 0
                    while x < n:
                        sub = subservices.getSubservice(x)
                        list.append((sub.toString(), sub.getName()))
                        x += 1

            else:
                list = (('N/A', 'N/A'), )
            print 'SubServices is returning list ', list
            return list
        else:
            if self.cmd is not None:
                print '[SubServices].getSubservices for Streaming Service'
                for screen in self.streamingScreens:
                    if screen is not None:
                        service = screen.getRecordService()
                        sref = ServiceReference(screen.getRecordServiceRef())
                        if service is not None:
                            print '[SubServices] serviceref: %s | cmd: %s' % (sref, self.cmd)
                            if sref.__str__() == self.cmd:
                                list.append((sref.__str__(), sref.getServiceName()))
                                print '[SubServices] Matching recordSerivce found!'
                                subservices = service and service.subServices()
                                if subservices and subservices.getNumberOfSubservices() != 0:
                                    n = subservices and subservices.getNumberOfSubservices()
                                    x = 0
                                    while x < n:
                                        sub = subservices.getSubservice(x)
                                        list.append((sub.toString(), sub.getName()))
                                        x += 1

                                    return list
                                print '[SubServices] no items: %s' % subservices
                        else:
                            print '[SubServices] Service is None!'

            if not list:
                return (('N/A', 'N/A'), )
            return list

    list = property(getSubservices)
    lut = {'ServiceReference': 0, 'Name': 1}


return
