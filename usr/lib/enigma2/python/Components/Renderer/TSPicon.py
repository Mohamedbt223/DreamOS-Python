# -*- coding: utf-8 -*-
from Renderer import Renderer
from enigma import ePixmap
from Tools.Directories import fileExists, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, resolveFilename
from Tools.PiconResolver import PiconResolver
from Components.config import config

class TSPicon(Renderer):
    GUI_WIDGET = ePixmap

    def __init__(self):
        Renderer.__init__(self)
        self.nameCache = {}
        self.pngname = ''
        self.path_attr = None
        
        # قائمة المسارات الاحتياطية للبحث عن مجلد picon
        self.fallback_paths = [
            '/data/picon/',
            '/media/ba/picon/',
            '/media/hdd/picon/',
            '/media/usb/picon/',
            '/media/cf/picon/',
            '/usr/share/enigma2/picon/'
        ]
        
        # نبدأ بالتحقق من المسار المحدد في TSSkinSetup
        # هذا يضمن أن اختيار المستخدم من الواجهة الرسومية له الأولوية
        self.mypath = self._tssetup('picon1Path', '')
        
        # إذا كان المسار المحدد غير موجود أو فارغ
        if not self.mypath or not fileExists(self.mypath):
            # نبحث في المسارات الاحتياطية
            found_path = False
            for fb in self.fallback_paths:
                if fileExists(fb):
                    self.mypath = fb
                    found_path = True
                    break
            
            # إذا لم يتم العثور على أي مسار صالح، نعود إلى الافتراضي
            if not found_path:
                self.mypath = '/data/picon/'
                if not self.mypath.endswith('/'):
                    self.mypath += '/'
        else:
            # إذا كان المسار المحدد صالحًا، نتأكد من أنه ينتهي بـ '/'
            if not self.mypath.endswith('/'):
                self.mypath += '/'

        self.lastpath = self.mypath

    def _tssetup(self, key, default):
        try:
            return getattr(config.plugins.TSSkinSetup, key).value
        except Exception:
            return default

    def _default_path(self):
        return self.fallback_paths

    def _get_base_path(self):
        if self.path_attr and self.path_attr.startswith('/'):
            base = self.path_attr
        else:
            base = self.mypath
        return base if base.endswith('/') else base + '/'

    def applySkin(self, desktop, parent):
        attribs = []
        if self.skinAttributes:
            for attrib, value in self.skinAttributes:
                if attrib == 'path':
                    self.path_attr = value.strip() or None
                else:
                    attribs.append((attrib, value))
        self.skinAttributes = attribs
        return Renderer.applySkin(self, desktop, parent)

    def postWidgetCreate(self, instance):
        instance.setScale(1)

    def changed(self, what):
        if not self.instance:
            return

        self.mypath = self._get_base_path()
        if self.lastpath != self.mypath:
            self.nameCache = {}
            self.lastpath = self.mypath

        pngname = ''
        if what[0] != self.CHANGED_CLEAR:
            try:
                sname = self.source.text
            except Exception:
                sname = ''
            if sname:
                pngname = PiconResolver.getPngName(sname, self.nameCache, self.findPicon)
        
        # Fallback to skin/default icon if no picon found
        if not pngname:
            tmp = resolveFilename(SCOPE_CURRENT_SKIN, 'picon_default.png')
            if fileExists(tmp):
                pngname = tmp
            else:
                pngname = resolveFilename(SCOPE_SKIN_IMAGE, 'ts-MetrixFHD/picon_default.png')
            self.nameCache['default'] = pngname
        
        if self.pngname != pngname:
            self.pngname = pngname
            if fileExists(self.pngname):
                self.instance.setPixmapFromFile(self.pngname)

    def findPicon(self, serviceName):
        candidate = self.mypath + serviceName + '.png'
        if fileExists(candidate):
            return candidate
        return ''