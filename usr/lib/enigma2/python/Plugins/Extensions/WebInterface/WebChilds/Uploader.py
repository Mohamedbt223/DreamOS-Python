# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebChilds/Uploader.py
# Compiled at: 2025-09-18 23:33:39
from os import statvfs, path as os_path, chmod as os_chmod, write as os_write, close as os_close, unlink as os_unlink, open as os_open, O_WRONLY, O_CREAT
from twisted.web import resource, http
from tempfile import mkstemp
from re import search

class UploadResource(resource.Resource):
    default_uploaddir = '/tmp/'
    restricted_paths = frozenset(('/bin/', '/boot/', '/dev/', '/etc/', '/lib/', '/proc/',
                                  '/sbin/', '/sys/', '/usr/', '/var/'))

    def out_POST(self, req, state, statetext, isXml):
        req.setResponseCode(http.OK)
        if isXml:
            req.setHeader('Content-type', 'application/xhtml+xml;')
            req.setHeader('charset', 'UTF-8')
            return '<?xml version="1.0" encoding="UTF-8" ?>\n<e2simplexmlresult>\n\t<e2state>%s</e2state>\n\t<e2statetext>%s</e2statetext>\n</e2simplexmlresult>' % ('True' if state else 'False', statetext)
        else:
            req.setResponseCode(http.OK)
            req.setHeader('Content-type', 'text/html')
            return statetext

        return

    def render_POST(self, req):
        isXml = 'xml' in req.args and req.args['xml'][0] == 'True'
        uploaddir = self.default_uploaddir
        if req.args['path'][0]:
            if os_path.isdir(req.args['path'][0]):
                uploaddir = req.args['path'][0]
                if uploaddir[-1] != '/':
                    uploaddir += '/'
            else:
                return self.out_POST(req, False, "path '%s' to upload not existing!" % req.args['path'][0], isXml)
        data = req.args['file'][0]
        if not data:
            return self.out_POST(req, False, 'filesize was 0, not uploaded', isXml)
        else:
            overwrite = 'overwrite' in req.args and req.args['overwrite'][0] == 'True'
            if overwrite and uploaddir in self.restricted_paths:
                overwrite = False
            try:
                matches = search('.*?filename="(.*?)"\r\n.*?', req.content.getvalue())
                fn = os_path.join(uploaddir, matches.group(1))
            except Exception as e:
                fn = None

            if fn and (overwrite or not os_path.exists(fn)):
                fd = os_open(fn, O_WRONLY | O_CREAT)
            else:
                fd, fn = mkstemp(dir=uploaddir)
            cnt = os_write(fd, data)
            os_close(fd)
            os_chmod(fn, 493)
            if cnt <= 0:
                try:
                    os_unlink(fn)
                except OSError as oe:
                    pass

                return self.out_POST(req, False, 'error writing to disk, not uploaded', isXml)
            statetext = fn if isXml else 'uploaded to %s' % fn
            return self.out_POST(req, True, statetext, isXml)
            return

    def render_GET(self, req):
        try:
            stat = statvfs('/tmp/')
        except OSError:
            return -1

        freespace = stat.f_bfree / 1000 * stat.f_bsize / 1000
        req.setResponseCode(http.OK)
        req.setHeader('Content-type', 'text/html')
        return '\n\t\t\t\t<form method="POST" enctype="multipart/form-data">\n\t\t\t\t<table>\n\t\t\t\t<tr><td>Path to save (default is \'%s\')</td><td><input name="path"></td></tr>\n\t\t\t\t<tr><td>File to upload</td><td><input name="file" type="file"></td></tr>\n\t\t\t\t<tr><td colspan="2">Filesize must not be greather than %dMB! /tmp/ has not more free space!</td></tr>\n\t\t\t\t<tr><td colspan="2"><input type="submit"></td><tr>\n\t\t\t\t</table>\n\t\t\t\t</form>\n\t\t' % (self.default_uploaddir, freespace)


return
