# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebBouquetEditor/WebChilds/WebUploadResource.py
# Compiled at: 2025-09-18 23:33:38
from os import write as os_write, close as os_close, O_WRONLY as os_O_WRONLY, O_CREAT as os_O_CREAT, open as os_open, remove as os_remove
from twisted.web import resource, http

class WebUploadResource(resource.Resource):
    FILENAME = '/tmp/webbouqueteditor_backup.tar'

    def __init__(self, session):
        self.session = session
        resource.Resource.__init__(self)
        return

    def render_POST(self, req):
        req.setResponseCode(http.OK)
        req.setHeader('Content-type', 'application/xhtml+xml;')
        req.setHeader('charset', 'UTF-8')
        data = req.args['file'][0]
        if not data:
            result = '<?xml version="1.0" encoding="UTF-8" ?>\n\n\t\t\t\t<e2simplexmlresult>\n\n\t\t\t\t\t<e2state>False</e2state>\n\t\t\t\t\t<e2statetext>Filesize was 0, not uploaded</e2statetext>\n\t\t\t\t</e2simplexmlresult>\n'
            return result
        fd = os_open(self.FILENAME, os_O_WRONLY | os_O_CREAT)
        if fd:
            cnt = os_write(fd, data)
            os_close(fd)
        if cnt <= 0:
            try:
                os_remove(FILENAME)
            except OSError as oe:
                pass

            result = '<?xml version="1.0" encoding="UTF-8" ?>\n\n\t\t\t\t<e2simplexmlresult>\n\n\t\t\t\t\t<e2state>False</e2state>\n\t\t\t\t\t<e2statetext>Error writing to disk, not uploaded</e2statetext>\n\t\t\t\t</e2simplexmlresult>\n'
        else:
            result = '<?xml version="1.0" encoding="UTF-8" ?>\n\n\t\t\t\t<e2simplexmlresult>\n\n\t\t\t\t\t<e2state>True</e2state>\n\t\t\t\t\t<e2statetext>%s</e2statetext>\n\t\t\t\t</e2simplexmlresult>\n' % self.FILENAME
        return result


return
