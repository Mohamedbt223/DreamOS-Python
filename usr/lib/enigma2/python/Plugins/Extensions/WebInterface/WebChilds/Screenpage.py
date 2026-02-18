# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebChilds/Screenpage.py
# Compiled at: 2025-09-18 23:33:39
from twisted.web import resource, http, server, static
from Plugins.Extensions.WebInterface import webif
from os import path as os_path
AppTextHeaderFiles = frozenset(('stream.m3u.xml', 'ts.m3u.xml', 'streamcurrent.m3u.xml',
                                'movielist.m3u.xml', 'services.m3u.xml'))
TextHtmlHeaderFiles = frozenset(('wapremote.xml', 'stream.xml'))
NoExplicitHeaderFiles = frozenset(('getpid.xml', 'tvbrowser.xml'))
TextJavascriptHeaderFiles = frozenset(('strings.js.xml', ))
resource.ErrorPage.template = '<!doctype html>\n<html lang="en">\n<head>\n    <meta charset="utf-8">\n    <title>%(code)s - %(brief)s</title>\n    <meta name="viewport" content="width=device-width, initial-scale=1">\n    <style>\n\n        * {\n            line-height: 1.2;\n            margin: 0;\n        }\n\n        html {\n            color: #888;\n            display: table;\n            font-family: sans-serif;\n            height: 100%%;\n            text-align: center;\n            width: 100%%;\n        }\n\n        body {\n            display: table-cell;\n            vertical-align: middle;\n            margin: 2em auto;\n        }\n\n        h1 {\n            color: #555;\n            font-size: 2em;\n            font-weight: 400;\n        }\n\n        p {\n            margin: 0 auto;\n            width: 280px;\n        }\n\n        @media only screen and (max-width: 280px) {\n\n            body, p {\n                width: 95%%;\n            }\n\n            h1 {\n                font-size: 1.5em;\n                margin: 0 0 0.3em;\n            }\n\n        }\n\n    </style>\n</head>\n<body>\n    <h1>%(code)s - %(brief)s</h1>\n    <p>%(detail)s</p>\n</body>\n</html>\n<!-- IE needs 512+ bytes: https://blogs.msdn.microsoft.com/ieinternals/2010/08/18/friendly-http-error-pages/ -->\n'

class ScreenPage(resource.Resource):

    def __init__(self, session, path, addSlash=False):
        resource.Resource.__init__(self)
        self.session = session
        self.path = path
        self.addSlash = addSlash
        return

    def render(self, request):
        path = self.path
        if os_path.isfile(path):
            lastComponent = path.split('/')[-1]
            if lastComponent in AppTextHeaderFiles:
                request.setHeader('Content-Type', 'application/text')
            elif lastComponent in TextHtmlHeaderFiles or path.endswith('.html.xml') and lastComponent != 'updates.html.xml':
                request.setHeader('Content-Type', 'text/html; charset=UTF-8')
            elif lastComponent in TextJavascriptHeaderFiles:
                request.setHeader('Content-Type', 'text/javascript; charset=UTF-8')
            elif lastComponent not in NoExplicitHeaderFiles:
                request.setHeader('Content-Type', 'application/xhtml+xml; charset=UTF-8')
            webif.renderPage(request, path, self.session)
            request.setResponseCode(http.OK)
        else:
            if os_path.isdir(path) and self.addSlash is True:
                uri = '%s/' % request.path
                request.redirect(uri)
                return ''
            else:
                return resource.ErrorPage(http.NOT_FOUND, 'Page Not Found', 'Sorry, but the page you were trying to view does not exist.').render(request)

        return server.NOT_DONE_YET

    def getChild(self, path, request):
        path = '%s/%s' % (self.path, path)
        if path[-1] == '/':
            path += 'index.html'
        path += '.xml'
        return ScreenPage(self.session, path)


return
