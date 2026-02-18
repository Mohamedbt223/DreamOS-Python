# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebChilds/External/EPGRefresh.py
# Compiled at: 2025-09-18 23:33:21
from Plugins.Extensions.WebInterface.WebChilds.Toplevel import addExternalChild
from Plugins.Extensions.EPGRefresh.EPGRefreshResource import EPGRefreshStartRefreshResource, EPGRefreshAddRemoveServiceResource, EPGRefreshListServicesResource, EPGRefreshChangeSettingsResource, EPGRefreshSettingsResource, EPGRefreshPreviewServicesResource, API_VERSION
root = EPGRefreshListServicesResource()
root.putChild('refresh', EPGRefreshStartRefreshResource())
root.putChild('add', EPGRefreshAddRemoveServiceResource(EPGRefreshAddRemoveServiceResource.TYPE_ADD))
root.putChild('del', EPGRefreshAddRemoveServiceResource(EPGRefreshAddRemoveServiceResource.TYPE_DEL))
root.putChild('set', EPGRefreshChangeSettingsResource())
root.putChild('get', EPGRefreshSettingsResource())
root.putChild('preview', EPGRefreshPreviewServicesResource())
addExternalChild(('epgrefresh', root, 'EPGRefresh-Plugin', API_VERSION))
return
