# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Components/Renderer/TSPiconProv.py
# Compiled at: 2015-04-12 02:26:41
from Renderer import Renderer
from enigma import ePixmap
from Tools.Directories import fileExists, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, resolveFilename

class TSPiconProv(Renderer):
    __module__ = __name__
    searchPaths = ('/usr/share/enigma2/%s/', '/media/hdd/%s/', '/media/sda1/%s/', '/media/usb/%s/',
                   '/media/sd/%s/')

    def __init__(self):
        Renderer.__init__(self)
        self.path = 'piconProv'
        self.nameCache = {}
        self.pngname = ''
        return

    def applySkin(self, desktop, parent):
        attribs = []
        for attrib, value in self.skinAttributes:
            if attrib == 'path':
                self.path = value
            else:
                attribs.append((attrib, value))

        self.skinAttributes = attribs
        return Renderer.applySkin(self, desktop, parent)

    GUI_WIDGET = ePixmap

    def changed(self, what):
        if self.instance:
            pngname = ''
            if what[0] != self.CHANGED_CLEAR:
                sname = self.source.text
                sname = sname.upper()
                pngname = self.nameCache.get(sname, '')
                if pngname == '':
                    pngname = self.findPicon(sname)
                    if pngname != '':
                        self.nameCache[sname] = pngname
            if pngname == '':
                pngname = self.nameCache.get('default', '')
                if pngname == '':
                    pngname = self.findPicon('picon_default')
                    if pngname == '':
                        tmp = resolveFilename(SCOPE_CURRENT_SKIN, 'picon_default.png')
                        if fileExists(tmp):
                            pngname = tmp
                        else:
                            pngname = resolveFilename(SCOPE_SKIN_IMAGE, 'skin_default/picon_default.png')
                    self.nameCache['default'] = pngname
            if self.pngname != pngname:
                if pngname:
                    self.instance.setScale(1)
                    self.instance.setPixmapFromFile(pngname)
                    self.instance.show()
        return

    def findPicon(self, serviceName):
        for path in self.searchPaths:
            pngname = path % self.path + serviceName + '.png'
            if fileExists(pngname):
                return pngname

        return ''


return
