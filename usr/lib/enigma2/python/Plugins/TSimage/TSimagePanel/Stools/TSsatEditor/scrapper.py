# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/Stools/TSsatEditor/scrapper.py
# Compiled at: 2025-09-17 10:00:00
"""
scrapper.py  —  Python 2.7 satellites scraper (robust)
- No external deps (stdlib only)
- Importable function: scrape_satellites(...)
- CLI usage preserved

Examples (import):
    from scrapper import scrape_satellites
    scrape_satellites(url="https://satellites-xml.org",
                      out_path="/tmp/satellites.xml",
                      min_pos=None, max_pos=None,
                      timeout=45, retries=5,
                      enigma2_format=True)

Examples (CLI):
    python scrapper.py --url "https://example.com/page" -o /tmp/sat.xml --timeout 45 --retries 5
    python scrapper.py --file page.html -o /tmp/sat.xml --min -30 --max 60 --enigma2
"""
import sys, re, time, socket, argparse, xml.etree.ElementTree as ET
try:
    import urllib2
except ImportError:
    urllib2 = None

try:
    import ssl
except:
    ssl = None

try:
    from HTMLParser import HTMLParser
except ImportError:
    HTMLParser = None

try:
    import cgi
except:
    cgi = None

LON_RE = re.compile('\\b(\\d{1,3}(?:\\.\\d+)?)([EW])\\b', re.IGNORECASE)

class _TextExtractor(HTMLParser):
    """HTML -> visible text, skipping <script>/<style>/<noscript>."""

    def __init__(self):
        HTMLParser.__init__(self)
        self._buf = []
        self._skip = 0
        return

    def handle_starttag(self, tag, attrs):
        t = tag.lower()
        if t in ('script', 'style', 'noscript'):
            self._skip += 1
        return

    def handle_endtag(self, tag):
        t = tag.lower()
        if t in ('script', 'style', 'noscript') and self._skip > 0:
            self._skip -= 1
        return

    def handle_data(self, data):
        if self._skip == 0:
            self._buf.append(data)
        return

    def get_text(self):
        txt = (u' ').join(self._buf)
        txt = re.sub(u'\s+', u' ', txt, flags=re.UNICODE).strip()
        return txt


def _html_unescape(s):
    try:
        return HTMLParser().unescape(s)
    except:
        if cgi and hasattr(cgi, 'escape'):
            s = s.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
            s = s.replace('&quot;', '"').replace('&#39;', "'")
            return s
        return s

    return


def extract_text_from_html(html_content):
    if not isinstance(html_content, unicode):
        try:
            html_content = html_content.decode('utf-8')
        except:
            html_content = html_content.decode('latin-1', 'ignore')

    if HTMLParser is None:
        text = re.sub(u'<[^>]+>', u' ', html_content)
        text = re.sub(u'\s+', u' ', text).strip()
        return _html_unescape(text)
    else:
        parser = _TextExtractor()
        try:
            parser.feed(html_content)
            parser.close()
        except:
            text = re.sub(u'<[^>]+>', u' ', html_content)
            text = re.sub(u'\s+', u' ', text).strip()
            return _html_unescape(text)

        txt = parser.get_text()
        return _html_unescape(txt)


def fetch_url(url, timeout=30, retries=4, backoff=2.0, allow_insecure_ssl=True):
    """
    Fetch URL with retries, exponential backoff, HTTPS->HTTP fallback,
    and optional insecure SSL context (helpful on old boxes w/o CA bundle).
    """
    if urllib2 is None:
        raise RuntimeError('urllib2 not available in this Python.')
    try:
        socket.setdefaulttimeout(timeout)
    except:
        pass

    last_err = None
    test_urls = [
     url]
    if url.lower().startswith('https://'):
        http_fallback = 'http://' + url.split('://', 1)[1]
        test_urls.append(http_fallback)
    handler_list = []
    if url.lower().startswith('https') and ssl and allow_insecure_ssl:
        try:
            ctx = ssl._create_unverified_context()
            handler_list.append(urllib2.HTTPSHandler(context=ctx))
        except:
            pass

    opener = urllib2.build_opener(*handler_list)
    opener.addheaders = [('User-Agent', 'sat-scraper/1.0 (py2)')]
    attempt = 0
    while attempt < retries:
        for u in test_urls:
            try:
                resp = opener.open(u, timeout=timeout)
                raw = resp.read()
                try:
                    return raw.decode('utf-8')
                except:
                    return raw.decode('latin-1', 'ignore')

            except Exception as e:
                last_err = e

        attempt += 1
        try:
            time.sleep(backoff ** attempt)
        except:
            pass

    raise RuntimeError('urlopen failed after retries: %s' % (last_err,))
    return


def read_file(path, encoding=None):
    f = open(path, 'rb')
    raw = f.read()
    f.close()
    if encoding:
        return raw.decode(encoding, 'ignore')
    try:
        return raw.decode('utf-8')
    except:
        return raw.decode('latin-1', 'ignore')

    return


def detect_captcha(text):
    t = text.lower()
    for k in [1, 2, 
     3, 4, 5]:
        if k in t:
            return True

    return False


def parse_satellites_from_text(text):
    if not isinstance(text, unicode):
        try:
            text = text.decode('utf-8')
        except:
            text = text.decode('latin-1', 'ignore')

    matches = list(LON_RE.finditer(text))
    sats = []
    if not matches:
        return sats
    for i, m in enumerate(matches):
        try:
            lon_val = float(m.group(1))
        except:
            continue

        lon_dir = m.group(2).upper()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        name = text[start:end].strip()
        name = re.sub(u'\s{2,}', u' ', name)
        name = re.sub(u'(^[:;,\.\-\s]+)|([:;,\.\-\s]+$)', u'', name)
        name = name.replace(u'\u', u'').strip()
        name = re.split(u'\s+\d{1,3}(?:\.\d+)?[EW]\b', name)[0].strip()
        if not name:
            pre = text[max(0, m.start() - 80):m.start()].strip()
            parts = pre.split()
            name = (u' ').join(parts[-6:]).strip()
            if not name:
                name = u'UNKNOWN'
        pos = lon_val if lon_dir == 'E' else -lon_val
        pos = float('%.1f' % pos)
        sats.append({'name': name, 
           'orbital_position': pos, 
           'position': pos, 
           'raw_long': (u'%.1f%s' % (lon_val, lon_dir))})

    return sats


def _write_scraper_schema(satellites, out_path):
    """
    Default writer: <satellites><satellite name=... position=.. orbital_position=.. raw_long=.. /></satellites>
    (position/orbital_position are floats signed; Enigma2 conversion can be done later.)
    """
    root = ET.Element('satellites')
    for s in satellites:
        el = ET.SubElement(root, 'satellite')
        name = s['name']
        if isinstance(name, unicode):
            name = name.encode('utf-8')
        el.set('name', name)
        el.set('orbital_position', '%.1f' % s['orbital_position'])
        el.set('position', '%.1f' % s['position'])
        el.set('raw_long', s.get('raw_long', '') if isinstance(s.get('raw_long', ''), str) else s.get('raw_long', '').encode('utf-8'))

    tree = ET.ElementTree(root)
    tree.write(out_path, encoding='utf-8', xml_declaration=True)
    return


def _enigma2_int_pos_from_signed_float(pos):
    """
    Convert signed degrees float to Enigma2 integer:
      East:  deg * 10
      West:  3600 - deg * 10
    """
    tenths = int(round(abs(pos) * 10.0))
    if pos >= 0:
        return tenths
    else:
        return 3600 - tenths

    return


def _write_enigma2_schema(satellites, out_path):
    """
    Enigma2 writer: <satellites><sat name="..." position="INT"/></satellites>
    """
    root = ET.Element('satellites')
    for s in satellites:
        pos_int = _enigma2_int_pos_from_signed_float(s['position'])
        el = ET.SubElement(root, 'sat')
        name = s['name']
        if isinstance(name, unicode):
            name = name.encode('utf-8')
        el.set('name', name)
        el.set('position', str(pos_int))

    tree = ET.ElementTree(root)
    tree.write(out_path, encoding='utf-8', xml_declaration=True)
    return


def scrape_satellites(url=None, file_path=None, out_path=None, min_pos=None, max_pos=None, timeout=30, retries=4, backoff=2.0, enigma2_format=True, allow_insecure_ssl=True):
    """
    Scrape satellites list and write XML.

    Args:
        url (str): fetch from URL
        file_path (str): or read from local HTML file
        out_path (str): output XML path (default: 'satellites.xml')
        min_pos (float): min orbital position (signed degrees, W negative)
        max_pos (float): max orbital position
        timeout (int): per-attempt timeout seconds
        retries (int): number of retry rounds
        backoff (float): exponential backoff base
        enigma2_format (bool): if True, write <sat> with int positions; else write <satellite> schema
        allow_insecure_ssl (bool): allow unverified ssl context (handy on old boxes)

    Returns:
        out_path (str) on success

    Raises:
        Exception on error
    """
    if not out_path:
        out_path = 'satellites.xml'
    if url:
        raw = fetch_url(url, timeout=timeout, retries=retries, backoff=backoff, allow_insecure_ssl=allow_insecure_ssl)
    elif file_path:
        raw = read_file(file_path, encoding=None)
    else:
        raise ValueError('Provide url or file_path')
    text = extract_text_from_html(raw)
    satellites = parse_satellites_from_text(text)
    if not satellites:
        raise RuntimeError('No satellites found (page may differ or need JS).')
    if min_pos is not None or max_pos is not None:
        minv = min_pos if min_pos is not None else -360.0
        maxv = max_pos if max_pos is not None else 360.0
        satellites = [s for s in satellites if s['position'] >= minv and s['position'] <= maxv]
    if enigma2_format:
        _write_enigma2_schema(satellites, out_path)
    else:
        _write_scraper_schema(satellites, out_path)
    return out_path


def main():
    p = argparse.ArgumentParser(description='Scrape satellites list -> satellites.xml (Python 2.7, robust)')
    grp = p.add_mutually_exclusive_group(required=True)
    grp.add_argument('--url', help='URL to fetch')
    grp.add_argument('--file', help='Local HTML file to read')
    p.add_argument('--out', '-o', default='satellites.xml', help='Output XML file')
    p.add_argument('--min', type=float, default=None, help='Minimum orbital position (deg, negative=west)')
    p.add_argument('--max', type=float, default=None, help='Maximum orbital position (deg, negative=west)')
    p.add_argument('--timeout', type=int, default=30, help='Per-attempt timeout seconds')
    p.add_argument('--retries', type=int, default=4, help='Retry rounds')
    p.add_argument('--backoff', type=float, default=2.0, help='Exponential backoff base (2.0 -> 2,4,8..)')
    p.add_argument('--no-insecure-ssl', action='store_true', help='Disable unverified SSL context')
    p.add_argument('--enigma2', action='store_true', help='Write Enigma2 <sat> format instead of <satellite>')
    args = p.parse_args()
    try:
        scrape_satellites(url=args.url, file_path=args.file, out_path=args.out, min_pos=args.min, max_pos=args.max, timeout=args.timeout, retries=args.retries, backoff=args.backoff, enigma2_format=bool(args.enigma2), allow_insecure_ssl=not args.no_insecure_ssl)
        sys.stdout.write('Saved: %s\n' % args.out)
    except Exception as e:
        sys.stderr.write('Error: %s\n' % e)
        sys.exit(2)

    return


if __name__ == '__main__':
    main()
return
