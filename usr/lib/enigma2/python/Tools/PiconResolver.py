# -*- coding: utf-8 -*-
import re, unicodedata
from enigma import eServiceReference, eServiceCenter
from Tools.Log import Log

try:
    unicode
except NameError:
    unicode = str

def _u(s):
    if s is None:
        return u""
    if isinstance(s, unicode):
        return s
    try:
        return s.decode('utf-8', 'ignore')
    except Exception:
        try:
            return unicode(s, 'utf-8', 'ignore')
        except Exception:
            return unicode(s, 'latin-1', 'ignore')

def getServiceName(ref_str):
    try:
        ref = eServiceReference(ref_str)
        info = eServiceCenter.getInstance().info(ref)
        name = (info and info.getName(ref)) or ""
        Log.i("PiconResolver: Retrieved service name for %s: %s" % (ref_str, _u(name)))
        return _u(name)
    except Exception as e:
        Log.i("PiconResolver: Failed to get service name for %s: %s" % (ref_str, str(e)))
        return u""

def _normalize_snp(name):
    s = _u(name)
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')
    s = s.lower()
    s = re.sub(r'\b(?:uhd|fhd|hd|sd|4k|hevc|hdr)\b', '', s).strip()
    s = s.replace('&', ' and ').replace('+', ' plus ').replace('@', ' at ')
    s = s.replace('/', ' ').replace('\\', ' ').replace('.', ' ')
    s = s.replace("'", '')
    s = re.sub(r'[\(\)\[\]\{\}]', ' ', s)
    s = re.sub(r'[^a-z0-9]+', ' ', s).strip()
    s = ''.join(s.split())
    return s or 'unknown'

def _normalize_snp_raw(name):
    s = _u(name)
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')
    s = s.lower()
    # لا نحذف hd أو fhd هنا — نريدها للبيكونات التي تتضمنها في الاسم
    s = s.replace('&', ' and ').replace('+', ' plus ').replace('@', ' at ')
    s = s.replace('/', ' ').replace('\\', ' ').replace('.', ' ')
    s = s.replace("'", '')
    s = re.sub(r'[\(\)\[\]\{\}]', ' ', s)
    s = re.sub(r'[^a-z0-9]+', ' ', s).strip()
    s = ''.join(s.split())
    return s or 'unknown'

class PiconResolver(object):

    @staticmethod
    def _try_snp(findPicon, nameCandidates):
        tried = set()
        for n in nameCandidates:
            if not n:
                continue
            base_clean = _normalize_snp(n)      # ← مثل: "mbc" أو "adnatgeo"
            base_raw = _normalize_snp_raw(n)    # ← مثل: "mbchd" أو "adnatgeohd"

            # جرب أولاً النسخة النظيفة (بدون hd) — لأن mbc.png أكثر شيوعاً
            # ثم جرب النسخة الخام (مع hd) — لدعم adnatgeohd.png
            for cand in (
                base_clean,
                base_clean.replace('__', '_').strip('_'),
                re.sub(r'_(?:uhd|fhd|hd|sd|4k|hevc|hdr)(?:_\d+)?$', '', base_clean),
                re.sub(r'(?:uhd|fhd|hd|sd|4k|hevc|hdr)$', '', base_clean),
                base_raw,
                base_raw.replace('__', '_').strip('_'),
                re.sub(r'_(?:uhd|fhd|hd|sd|4k|hevc|hdr)(?:_\d+)?$', '', base_raw),
                re.sub(r'(?:uhd|fhd|hd|sd|4k|hevc|hdr)$', '', base_raw),
            ):
                if cand and cand not in tried:
                    tried.add(cand)
                    png = findPicon(cand)
                    if png:
                        Log.i("PiconResolver: Found SNP picon for candidate: %s" % cand)
                        return png
        Log.i("PiconResolver: No SNP picon found for candidates: %s" % str(nameCandidates))
        return ""

    @staticmethod
    def getPngName(ref_or_name, nameCache, findPicon):
        s = ref_or_name or ""
        Log.i("PiconResolver: Processing ref_or_name: %s" % s)
        if ':' not in s:
            png = PiconResolver._try_snp(findPicon, [s])
            if not png:
                png = nameCache.get("default", "") or findPicon("picon_default")
                if png and not nameCache.get("default"):
                    nameCache["default"] = png
            return png or ""
        x = s.split(':')
        if len(x) < 10:
            Log.i("PiconResolver: Invalid SRP format, length < 10: %s" % s)
            return ""
        if len(x) >= 12:
            x = x[:11]
        elif len(x) == 11:
            x = x[:11] if x[10] else x[:10]
        else:
            x = x[:10]
        x[1] = '0'
        x[6] = x[6].upper()
        srp_full = '_'.join(x).strip('_')
        srp_10   = '_'.join(x[:10])
        pngname = nameCache.get(srp_full, "")
        if pngname:
            Log.i("PiconResolver: Found cached SRP picon: %s" % pngname)
            return pngname
        pngname = findPicon(srp_full)
        if not pngname:
            pngname = findPicon(srp_10)
        if not pngname and x[0] in ('4097', '4098', '5001', '5002', '8193', '8739'):
            pngname = findPicon('1_' + '_'.join(x[1:10]))
        if not pngname:
            try:
                if int(x[0]) == 1:
                    ns = int(x[6], 16)
                    if (ns & 0xFFFF0000) == 0xEEEE0000:
                        x_t = list(x)
                        x_t[6] = "EEEE0000"
                        pngname = findPicon('1_' + '_'.join(x_t[1:10]))
            except Exception as e:
                Log.i("PiconResolver: DVB-T/T2 fallback failed: %s" % str(e))
        if not pngname:
            svcname = getServiceName(s)
            if svcname:
                Log.i("PiconResolver: Trying SNP fallback with service name: %s" % svcname)
                pngname = PiconResolver._try_snp(findPicon, [svcname, svcname.replace(u'.', u' '), svcname.replace(u'-', u' ')])
        if not pngname:
            pngname = nameCache.get("default", "") or findPicon("picon_default")
            if pngname and not nameCache.get("default"):
                nameCache["default"] = pngname
        if pngname:
            nameCache[srp_full] = pngname
            Log.i("PiconResolver: Cached picon name: %s" % pngname)
        else:
            Log.i("PiconResolver: No picon found for: %s" % s)
        return pngname or ""