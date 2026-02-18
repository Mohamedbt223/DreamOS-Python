# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Components/Renderer/TSLCDPicon.py
# Compiled at: 2016-05-20 19:47:43
from Renderer import Renderer
from enigma import ePixmap
from Tools.Directories import fileExists, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, resolveFilename
from Tools.PiconResolver import PiconResolver
from Components.config import config

class TSLCDPicon(Renderer):

    def __init__(self):
        Renderer.__init__(self)
        self.path = 'picon_oled'
        self.nameCache = {}
        self.pngname = ''
        self.lastpath = self.mypath = config.plugins.TSSkinSetup.piconOledPath.value
        self.chSel = 'off'
        return

    def applySkin(self, desktop, parent):
        attribs = []
        for attrib, value in self.skinAttributes:
            if attrib == 'chSel':
                self.chSel = value
            else:
                attribs.append((attrib, value))

        self.skinAttributes = attribs
        return Renderer.applySkin(self, desktop, parent)

    GUI_WIDGET = ePixmap

    def postWidgetCreate(self, instance):
        instance.setScale(1)
        instance.setDefaultAnimationEnabled(self.source.isAnimated)
        return

    def changed(self, what):
        if self.instance:
            if what[0] == self.CHANGED_ANIMATED:
                self.instance.setDefaultAnimationEnabled(self.source.isAnimated)
                return
            oled_disabled = not config.plugins.TSSkinSetup.piconOledEnabled.value
            switch_time = int(config.plugins.TSSkinSetup.piconOledSwitchTime.value)
            pngname = ''
            self.checkpath()
            if oled_disabled:
                if pngname == '':
                    pngname = self.nameCache.get('default', '')
                    if pngname == '':
                        pngname = self.findPicon('lcdpicon_default')
                        if pngname == '':
                            tmp = resolveFilename(SCOPE_CURRENT_SKIN, 'lcdpicon_default.png')
                            if fileExists(tmp):
                                pngname = tmp
                            else:
                                pngname = resolveFilename(SCOPE_SKIN_IMAGE, 'skin_default/lcdpicon_default.png')
                        self.nameCache['default'] = pngname
            elif what[0] != self.CHANGED_CLEAR:
                sname = self.source.text
                pngname = PiconResolver.getPngName(sname, self.nameCache, self.findPicon)
                self.nameCache[sname] = pngname
            if switch_time != 0:
                if pngname == '':
                    pngname = self.nameCache.get('default', '')
                    if pngname == '':
                        pngname = self.findPicon('lcdpicon_default')
                        if pngname == '':
                            tmp = resolveFilename(SCOPE_CURRENT_SKIN, 'lcdpicon_default.png')
                        if fileExists(tmp):
                            pngname = tmp
                        else:
                            pngname = resolveFilename(SCOPE_SKIN_IMAGE, 'skin_default/lcdpicon_default.png')
                    self.nameCache['default'] = pngname
            elif self.chSel == 'on':
                if pngname == '':
                    pngname = self.nameCache.get('default', '')
                    if pngname == '':
                        pngname = self.findPicon('lcdpicon_default')
                        if pngname == '':
                            tmp = resolveFilename(SCOPE_CURRENT_SKIN, 'lcdpicon_default.png')
                        if fileExists(tmp):
                            pngname = tmp
                        else:
                            pngname = resolveFilename(SCOPE_SKIN_IMAGE, 'skin_default/lcdpicon_default.png')
                    self.nameCache['default'] = pngname
            if self.pngname != pngname:
                self.instance.setPixmapFromFile(pngname)
                self.pngname = pngname
        return

    def checkpath(self):
        pos = config.plugins.TSSkinSetup.piconOledPath.value.rfind('/')
        if pos != -1:
            self.mypath = config.plugins.TSSkinSetup.piconOledPath.value + '/'
        else:
            self.mypath = config.plugins.TSSkinSetup.piconOledPath.value
        if self.lastpath != self.mypath:
            self.nameCache = {}
            self.lastpath = self.mypath
        return

    def findPicon(self, serviceName):
        pngname = self.mypath + serviceName + '.png'
        if fileExists(pngname):
            return pngname
        return ''


return
