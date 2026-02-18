# -*- coding: utf-8 -*-
from __future__ import print_function

from os import statvfs as os_statvfs, popen as os_popen, path as os_path
from glob import glob
import platform

# -------------------------------------------------
# Shell helpers / disk info
# -------------------------------------------------

def getCmdOutput(cmd):
    """
    Run a shell command and return stdout+stderr as a single string (no trailing newline).
    """
    pipe = os_popen('{ ' + cmd + '; } 2>&1', 're')
    text = pipe.read()
    rc = pipe.close()
    if text[-1:] == '\n':
        text = text[:-1]
    return text


def getFreeSpace():
    spacestr = ''
    diskSpace = os_statvfs('/')
    capacity = float(diskSpace.f_bsize * diskSpace.f_blocks)
    available = float(diskSpace.f_bsize * diskSpace.f_bavail)
    fspace = round(float(available / 1048576.0), 2)
    tspace = round(float(capacity / 1048576.0), 1)
    spacestr = 'Free space(' + str(fspace) + 'MB) Total space(' + str(tspace) + 'MB)'
    return spacestr


# -------------------------------------------------
# Hostname / arch detection
# -------------------------------------------------

def getHostname():
    """
    Map /etc/hostname to a normalized Dreambox token used by some feeds.

    Returns one of:
      'dmone', 'dmtwo', 'dm7080', 'dm820', 'dm520', 'dm900', 'dm920',
      'dm7020hd', 'dm800sev2', 'dm500hdv2', or the raw hostname / 'None'.
    """
    path = '/etc/hostname'
    if os_path.exists(path):
        try:
            f = open(path, 'r')
            raw = (f.read() or '').strip()
            f.close()
        except:
            raw = ''
        s = (raw or '').lower()

        # Newer boxes (explicit)
        if ('dmone' in s) or ('dreamone' in s) or ('dreambox-one' in s):
            return 'dmone'
        if ('dmtwo' in s) or ('dreamtwo' in s) or ('dreambox-two' in s):
            return 'dmtwo'

        # Classic mappings
        if 'dm7080' in s:     return 'dm7080'
        if 'dm820'  in s:     return 'dm820'
        if 'dm520'  in s:     return 'dm520'
        if 'dm900'  in s:     return 'dm900'
        if 'dm920'  in s:     return 'dm920'
        if 'dm7020' in s:     return 'dm7020hd'
        if 'dm800sev2' in s:  return 'dm800sev2'
        if 'dm500v2' in s:    return 'dm500hdv2'

        return raw or 'None'
    return 'None'


def _read_model_string():
    """
    Read model string from DreamOS.
    """
    path = '/proc/stb/info/model'
    try:
        if os_path.exists(path):
            f = open(path, 'r')
            model = (f.read() or '').strip().lower()
            f.close()
            return model
    except:
        pass
    return ''


def getArch():
    """
    Returns one of: 'mipsel', 'armhf', 'aarch64'

    Rules:
      - dmone / dmtwo => aarch64
      - dm900 / dm920 / dm7080 / dm820 => armhf
      - else: detect via platform.machine() / uname -m; fallback by /proc/stb/info/model
      - default => mipsel
    """
    # Honor dmone/dmtwo explicitly via hostname
    try:
        hn = getHostname().lower()
        if hn in ('dmone', 'dmtwo'):
            return 'aarch64'
    except:
        pass

    # Try platform / uname first
    try:
        mach = (platform.machine() or '').lower()
    except:
        mach = (getCmdOutput('uname -m') or '').lower()

    if ('aarch64' in mach) or ('arm64' in mach):
        return 'aarch64'
    if mach.startswith('arm') or ('armv7' in mach) or ('armv6' in mach):
        return 'armhf'
    if 'mips' in mach:
        return 'mipsel'

    # Fallback via model hints
    model = _read_model_string()
    if ('dm900' in model) or ('dm920' in model) or ('dm7080' in model) or ('dm820' in model):
        return 'armhf'
    if ('one' in model) or ('two' in model):
        return 'aarch64'

    # Old boxes default
    return 'mipsel'


# -------------------------------------------------
# APT sources parsing / feed selection
# -------------------------------------------------

def _iter_apt_source_lines():
    """
    Yield 'deb ...' lines from /etc/apt/sources.list and *.list.
    Supports lines like:
      deb http://host/path DIST comp
      deb [trusted=yes] http://host/path ./          (DreamArabia style)
    """
    files = ['/etc/apt/sources.list']
    files.extend(sorted(glob('/etc/apt/sources.list.d/*.list')))
    for p in files:
        if not os_path.exists(p):
            continue
        try:
            f = open(p, 'r')
            for raw in f:
                line = (raw or '').strip()
                if not line or line.startswith('#'):
                    continue
                if line.startswith('deb '):
                    yield line
            f.close()
        except:
            pass


def getDistroFeed(hostname):
    """
    Returns (base_url, debarchname)

    Behavior:
      - Prefer DreamArabia feeds (no '/deb/<arch>'):
          'deb [trusted=yes] http://.../dreamarabia/.../DreamArabia-Addons/ ./'
        Priority: Addons (0) > Cams (1) > Settings (2)
        Returns: ( 'http://.../DreamArabia-Addons/', '' )
      - Fall back to classic '/deb/<arch>' feeds:
        Returns: ( 'http://.../deb/', '<arch-from-line>' )
      - Skip lines containing the current 'hostname' token (compat with older behavior).
    """
    candidates = []  # (priority, base_url, debarchname)

    def _consider(line):
        parts = line.split()
        if len(parts) < 2 or parts[0] != 'deb':
            return

        # URL token position (with or without [options])
        url_idx = 2 if (len(parts) > 2 and parts[1].startswith('[')) else 1
        if url_idx >= len(parts):
            return

        url = parts[url_idx].rstrip('/')

        # Skip model-specific lines that include hostname token
        if hostname and (hostname in url):
            return

        # DreamArabia style: direct folder, no '/deb/<arch>'
        if '/dreamarabia/' in url:
            base = url + '/'
            prio = 10
            if 'DreamArabia-Addons' in url:
                prio = 0
            elif 'DreamArabia-Cams' in url:
                prio = 1
            elif 'DreamArabia-Settings' in url:
                prio = 2
            candidates.append((prio, base, ''))
            return

        # Classic '/deb/<arch>' layout
        if '/deb/' in url:
            try:
                base, after = url.split('/deb/', 1)
                base = base + '/deb/'
                debarchname = after  # e.g. mipsel | armhf | aarch64 | all
                # prefer arch-specific over "all"
                prio = 50 if debarchname == 'all' else 40
                candidates.append((prio, base, debarchname))
            except:
                pass

    for line in _iter_apt_source_lines():
        _consider(line)

    if candidates:
        candidates.sort(key=lambda x: x[0])
        _, base, debarchname = candidates[0]
        return (base, debarchname)

    return ('', '')


def build_repo_url(distro_feed, debarchname, arch=None):
    """
    Build the effective base URL to fetch packages.

    - DreamArabia (debarchname == '') => return distro_feed + '/'
    - Classic '/deb/<arch>' => return distro_feed + '<debarchname>/'
      (If 'arch' is passed, we don't rewrite; we trust debarchname from the list.)
    """
    if not distro_feed:
        return ''
    if not debarchname:
        return distro_feed.rstrip('/') + '/'
    return distro_feed.rstrip('/') + '/' + debarchname.strip('/') + '/'


# -------------------------------------------------
# Misc utils (compat)
# -------------------------------------------------

def getDigitVersion(ipkversionstr):
    """
    Convert a version like '1.0+git1234-r2' -> digits only,
    roughly preserving '-rN' via concatenation.
    """
    tstr = ''
    s = ipkversionstr.split('+')
    if len(s) == 3:
        sr = ipkversionstr.split('-r')
        rev = ''
        if len(sr) == 2:
            rev = '-r' + sr[1]
        ipkversionstr = s[0] + s[1] + rev
    e = list(ipkversionstr)
    for j in e:
        if j.isdigit():
            tstr = tstr + str(j)
    return tstr


def getText(nodelist):
    """
    Extract text from a minidom node list.
    """
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ('').join(rc)
