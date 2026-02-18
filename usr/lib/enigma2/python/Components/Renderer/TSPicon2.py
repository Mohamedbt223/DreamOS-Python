# -*- coding: utf-8 -*-
from Renderer import Renderer
from enigma import ePixmap, eServiceReference
from Tools.Directories import fileExists, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, resolveFilename
from Tools.PiconResolver import PiconResolver
from Components.config import config
import re

class TSPicon2(Renderer):
    GUI_WIDGET = ePixmap

    def __init__(self):
        Renderer.__init__(self)
        self.nameCache = {}
        self.pngname = ''
        self.path_attr = None
        self.fallback_paths = [
            '/data/picon/',
            '/media/ba/picon/',
            '/media/hdd/picon/',
            '/media/usb/picon/',
            '/media/cf/picon/',
            '/usr/share/enigma2/picon/'
        ]
        
        # New priority logic
        self.mypath = ''
        
        # 1. First, try to get the path from TSSkinSetup
        ts_path = self._tssetup('picon1Path', '')
        if ts_path and fileExists(ts_path):
            self.mypath = ts_path
        
        # 2. If no valid path from TSSkinSetup, try fallback_paths
        if not self.mypath:
            for fb in self.fallback_paths:
                if fileExists(fb):
                    self.mypath = fb
                    break
        
        # 3. If no valid path found anywhere, set a default path
        if not self.mypath:
            self.mypath = '/data/picon/'

        # Ensure the path ends with a slash
        if not self.mypath.endswith('/'):
            self.mypath += '/'

        self.lastpath = self.mypath
        self._sat_dir = [
            '/data/piconSat/',
            '/media/ba/piconSat/',
            '/media/hdd/piconSat/',
            '/media/usb/piconSat/',
            '/media/cf/piconSat/'
        ]

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
        for attrib, value in self.skinAttributes:
            if attrib == 'autoPicon':
                self.autoPicon = value
            else:
                attribs.append((attrib, value))
        self.skinAttributes = attribs
        return Renderer.applySkin(self, desktop, parent)

    def postWidgetCreate(self, instance):
        instance.setScale(1)
        instance.setDefaultAnimationEnabled(self.source.isAnimated)

    def changed(self, what):
        if not self.instance:
            return
        if what[0] == self.CHANGED_ANIMATED:
            self.instance.setDefaultAnimationEnabled(self.source.isAnimated)
            return

        # Use the path determined in __init__
        mypath = self.getPiconPath()
        if mypath and mypath != self.mypath:
            self.mypath = mypath if mypath.endswith('/') else mypath + '/'
            if self.lastpath != self.mypath:
                self.nameCache = {}
                self.lastpath = self.mypath

        pngname = ''
        skinpicon = 'picon_default.png'
        defaultpicon = 'ts-MetrixFHD/picon_default.png'
        cachename = 'default'
        service = self.source.service

        if what[0] != self.CHANGED_CLEAR and service is not None:
            if service.flags & eServiceReference.isMarker == eServiceReference.isMarker:
                skinpicon = 'marker.png'
                defaultpicon = 'ts-MetrixFHD/marker.png'
                cachename = 'marker'
                pngname = self.nameCache.get(cachename, '')
            elif service.flags & eServiceReference.flagDirectory == eServiceReference.flagDirectory:
                sat_png = self._satellite_picon_for(service)
                if sat_png:
                    cachename = 'sat:' + sat_png
                    pngname = self.nameCache.get(cachename, '')
                    if not pngname:
                        pngname = sat_png
                        self.nameCache[cachename] = pngname
                else:
                    skinpicon = 'bouquet.png'
                    defaultpicon = 'ts-MetrixFHD/bouquet.png'
                    cachename = 'folder'
                    pngname = self.nameCache.get(cachename, '')
            else:
                sname = service.toString()
                pngname = PiconResolver.getPngName(sname, self.nameCache, self.findPicon)

        if pngname == '':
            tmp = resolveFilename(SCOPE_CURRENT_SKIN, skinpicon)
            if fileExists(tmp):
                pngname = tmp
            else:
                pngname = resolveFilename(SCOPE_SKIN_IMAGE, defaultpicon)
            self.nameCache[cachename] = pngname

        if self.pngname != pngname:
            self.pngname = pngname
            self.instance.setPixmapFromFile(str(self.pngname))
        return

    def getPiconPath(self):
        # Return the path determined in __init__
        return self.mypath

    def findPicon(self, serviceName):
        pngname = self.mypath + serviceName + '.png'
        if fileExists(pngname):
            return pngname
        return ''

    def _satellite_picon_for(self, service):
        try:
            name = service.getName() or ''
        except Exception:
            name = ''
        if not name:
            return ''
        raw = name.replace('°', '').replace(' ', '').replace(',', '.')
        matches = re.findall('(\\d{1,3}(?:\\.\\d{1,2})?)([EeWw])', raw)
        if not matches:
            return ''

        def _to_num(m):
            try:
                return float(m[0])
            except Exception:
                return -1.0

        deg_str, hemi = max(matches, key=_to_num)
        hemi = hemi.upper()
        dec_dot = '%s%s.png' % (deg_str, hemi)
        dec_underscore = '%s_%s.png' % (deg_str.replace('.', '_'), hemi)
        dec_nodot = '%s%s.png' % (deg_str.replace('.', ''), hemi)
        try:
            deg_int = int(round(float(deg_str)))
        except Exception:
            deg_int = None

        int_variants = []
        if deg_int is not None:
            int_variants.append('%d%s.png' % (deg_int, hemi))
            if 0 < deg_int < 10:
                int_variants.insert(0, '%02d%s.png' % (deg_int, hemi))
            if deg_int < 100:
                int_variants.append('%03d%s.png' % (deg_int, hemi))
        candidates = [dec_dot, dec_underscore, dec_nodot] + int_variants
        seen, uniq = set(), []
        for c in candidates:
            if c not in seen:
                uniq.append(c)
                seen.add(c)
        for fn in uniq:
            for sat_dir in self._sat_dir:
                full = sat_dir + fn
                if fileExists(full):
                    return full
        return ''