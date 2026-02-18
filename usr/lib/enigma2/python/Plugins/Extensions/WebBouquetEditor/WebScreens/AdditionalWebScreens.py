# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebBouquetEditor/WebScreens/AdditionalWebScreens.py
# Compiled at: 2025-09-18 23:33:38
from Plugins.Extensions.WebInterface.WebScreens import WebScreen

class AdditionalWebScreen(WebScreen):

    def __init__(self, session, request):
        WebScreen.__init__(self, session, request)
        from Plugins.Extensions.WebBouquetEditor.WebComponents.Sources.SatellitesList import SatellitesList
        self['SatellitesList'] = SatellitesList(func=SatellitesList.FETCH)
        from Plugins.Extensions.WebBouquetEditor.WebComponents.Sources.ServiceList import ServiceList
        from Screens.ChannelSelection import service_types_tv
        from enigma import eServiceReference
        fav = eServiceReference(service_types_tv + ' FROM BOUQUET "bouquets.tv" ORDER BY bouquet')
        self['ServiceList'] = ServiceList(fav, command_func=self.getServiceList, validate_commands=False)
        from Plugins.Extensions.WebBouquetEditor.WebComponents.Sources.ProtectionSettings import ProtectionSettings
        self['ProtectionSettings'] = ProtectionSettings()
        return

    def getServiceList(self, sRef):
        self['ServiceList'].root = sRef
        return


return
