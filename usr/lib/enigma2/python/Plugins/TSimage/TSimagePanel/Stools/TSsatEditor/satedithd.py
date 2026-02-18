# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/Stools/TSsatEditor/satedithd.py
# Compiled at: 2025-09-13 23:09:01
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.config import config, ConfigFloat, ConfigInteger, ConfigSelection, ConfigText, ConfigYesNo, getConfigListEntry
from Components.ConfigList import ConfigListScreen
from Components.GUIComponent import GUIComponent
from Components.HTMLComponent import HTMLComponent
from Components.Label import Label
from Components.MenuList import MenuList
from Components.Sources.List import List
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.NimManager import nimmanager, getConfigSatlist
from enigma import eListbox, gFont, eListboxPythonMultiContent, RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, RT_VALIGN_CENTER, RT_VALIGN_TOP, RT_WRAP, eRect, eTimer
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
import hashlib, urllib2, re, requests, os, time, thread, urllib2, xml.etree.cElementTree, satellite, xml.etree.cElementTree as etree
from Plugins.TSimage.TSimagePanel.Stools.setloader import TSiServersScreen
import ServiceEditor.plugin
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.GUIComponent import GUIComponent
from Components.MultiContent import MultiContentEntryText
from enigma import eRect, eTimer, gFont, eListbox, eListboxPythonMultiContent
import hashlib, urllib2, re, os, time, thread
try:
    from bs4 import BeautifulSoup
except ImportError:
    raise ImportError("BeautifulSoup4 is required. Install 'python-beautifulsoup4'.")

def _clean_spaces(s):
    return re.sub(u'\s+', u' ', (s or u'').replace(u'\u', u' ')).strip()


def _u(x):
    """Coerce any input to unicode text (Python 2 safe)."""
    try:
        basestring
    except NameError:
        basestring = (
         str,)

    try:
        unicode
    except NameError:
        return str(x)

    if isinstance(x, unicode):
        return x
    if isinstance(x, basestring):
        try:
            return x.decode('utf-8', 'ignore')
        except Exception:
            try:
                return unicode(x, 'utf-8', 'ignore')
            except Exception:
                return unicode(str(x), errors='ignore')

    return unicode('%s' % (x,), errors='ignore')


def format_position(p):
    try:
        n = int(str(p))
        hemi = 'E' if n >= 0 else 'W'
        n = abs(n)
        return u'\u1f0xb0%s' % (n / 10.0, hemi)
    except Exception:
        return u''

    return


from Components.MenuList import MenuList
from Components.GUIComponent import GUIComponent
from Components.HTMLComponent import HTMLComponent
from enigma import eListbox, eListboxPythonMultiContent, gFont, eRect
from Tools.Directories import resolveFilename
LIST_ROW_H = 44
LIST_FONT_SZ = 28
HEAD_ROW_H = 36
HEAD_FONT_SZ = 26

class SatelliteListlyngsat(MenuList):

    def __init__(self):
        MenuList.__init__(self, list=[], content=eListboxPythonMultiContent)
        self.l.setItemHeight(LIST_ROW_H)
        self.l.setFont(0, gFont('Regular', LIST_FONT_SZ))
        return

    def setEntries(self, satelliteslist):
        print 'setEntries', len(satelliteslist)
        res = []
        for x in satelliteslist:
            satparameter = x[0]
            satentry = []
            pos = int(satparameter.get('position'))
            if pos < 0:
                pos += 3600
            satentry.append(pos)
            color = None
            color_sel = None
            if satparameter.get('selected', False):
                color = 0
                color_sel = 65344
            backcolor = None
            backcolor_sel = None
            if len(x) == 1:
                backcolor = 1644912
                backcolor_sel = 9466996
            satentry.append(MultiContentEntryText(pos=(0, 0), size=(930, LIST_ROW_H), font=0, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER, text=satparameter.get('name'), color=color, color_sel=color_sel, backcolor=backcolor, backcolor_sel=backcolor_sel, border_width=1, border_color=15792383))
            pos = int(satparameter.get('position'))
            posStr = str(abs(pos) / 10) + '.' + str(abs(pos) % 10)
            if pos < 0:
                posStr += ' ' + _('West')
            if pos > 0:
                posStr += ' ' + _('East')
            satentry.append(MultiContentEntryText(pos=(930, 0), size=(170, LIST_ROW_H), font=0, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER, text=posStr, color=color, color_sel=color_sel, backcolor=backcolor, backcolor_sel=backcolor_sel, border_width=1, border_color=15792383))
            res.append(satentry)

        self.l.setList(res)
        return


class Headlyngsat(HTMLComponent, GUIComponent):

    def __init__(self):
        GUIComponent.__init__(self)
        self.l = eListboxPythonMultiContent()
        self.l.setSelectionClip(eRect(0, 0, 0, 0))
        self.l.setItemHeight(HEAD_ROW_H)
        self.l.setFont(0, gFont('Regular', HEAD_FONT_SZ))
        return

    GUI_WIDGET = eListbox

    def postWidgetCreate(self, instance):
        instance.setContent(self.l)
        return

    def setEntries(self, data=None):
        res = [None]
        if data is not None:
            for x in data:
                res.append(MultiContentEntryText(pos=(
                 x[0], 0), size=(x[1], HEAD_ROW_H), font=0, flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER, text=x[2], color=12632256, backcolor=4671288, color_sel=16777215, backcolor_sel=6316032, border_width=1, border_color=15792383))

        self.l.setList([res])
        return


class SatelliteImport(Screen):
    modeToggle = 0
    modeSelect = 1
    modeUnSelect = 2
    skin = '<screen name="SatelliteImportTS" position="center,center" size="1700,900" title="LyngSat satellites"><widget name="head" position="40,20" size="1620,40" scrollbarMode="showNever"/><widget name="list" position="40,70" size="1620,760" scrollbarMode="showOnDemand" transparent="1" zPosition="2"/><eLabel position="40,845" size="1620,2" backgroundColor="#ffffff"/><widget name="fspace" position="40,855" size="1620,32" font="Regular;24" foregroundColor="yellow" transparent="1" halign="center" valign="center"/></screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.skinName = ['SatelliteImportTS', 'SatelliteImport']
        self['actions'] = ActionMap([
         'SatellitesEditorActions', 'DirectionActions', 'OkCancelActions'], {'nextPage': (self.nextPage), 
           'prevPage': (self.prevPage), 'select': (self.editTransponders), 
           'ok': (self.editTransponders), 'cancel': (self.exitSatelliteImport), 
           'exit': (self.exitSatelliteImport), 'left': (self.left), 
           'right': (self.right), 'upUp': (self.upUp), 
           'up': (self.up), 'upRepeated': (self.upRepeated), 'down': (self.down), 
           'downUp': (self.downUp), 'downRepeated': (self.downRepeated)}, -1)
        self['head'] = Headlyngsat()
        self['list'] = SatelliteListlyngsat()
        self['fspace'] = Label('connecting..please wait')
        self.onLayoutFinish.append(self.layoutFinished)
        self.currentSelectedColumn = 0
        self.row = [['name', _('Satellites'), False], ['position', _('Pos'), False]]
        self.satelliteslist = []
        self.getSatellites_state = self.thread_is_off
        self.satTimer = eTimer()
        try:
            self.satTimer.timeout.connect(self.pollSatellites)
        except Exception:
            self.satTimer.callback.append(self.pollSatellites)

        self.getTransponders_state = self.thread_is_off
        self.tpTimer = eTimer()
        try:
            self.tpTimer.timeout.connect(self.pollTransponders)
        except Exception:
            self.tpTimer.callback.append(self.pollTransponders)

        self.requestSatelliteslistRefresh = False
        self.lastSelectedIndex = 0
        self._pending_tp_open_idx = None
        self._pending_tp_open_once = False
        return

    def editTransponders(self):
        if not self.satelliteslist:
            return
        cur_idx = self['list'].getSelectedIndex()
        if len(self.satelliteslist[cur_idx]) == 1:
            self.satelliteslist[cur_idx][0]['selected'] = True
            self._pending_tp_open_idx = cur_idx
            self._pending_tp_open_once = True
            self.pollTransponders()
        else:
            self.session.openWithCallback(self.finishedTranspondersEdit, TranspondersEditor, self.satelliteslist[cur_idx])
        self['list'].setEntries(self.satelliteslist)
        return

    def exitSatelliteImport(self):
        return

    def left(self):
        return

    def right(self):
        return

    def nextPage(self):
        self['list'].pageUp()
        self.lastSelectedIndex = self['list'].getSelectedIndex()
        return

    def prevPage(self):
        self['list'].pageDown()
        self.lastSelectedIndex = self['list'].getSelectedIndex()
        return

    def up(self):
        self['list'].up()
        self.lastSelectedIndex = self['list'].getSelectedIndex()
        return

    def down(self):
        self['list'].down()
        self.lastSelectedIndex = self['list'].getSelectedIndex()
        return

    def upUp(self):
        cur = self['list'].getSelectedIndex()
        if self.lastSelectedIndex != cur:
            self.lastSelectedIndex = cur
        return

    def downUp(self):
        cur = self['list'].getSelectedIndex()
        if self.lastSelectedIndex != cur:
            self.lastSelectedIndex = cur
        return

    def upRepeated(self):
        self['list'].up()
        return

    def downRepeated(self):
        self['list'].down()
        return

    def updateSelection(self):
        return

    def finishedTranspondersEdit(self, result):
        if result is None:
            return
        else:
            cur_idx = self['list'].getSelectedIndex()
            self.satelliteslist[cur_idx][1] = result
            return

    def importTransponders(self):
        self.pollTransponders()
        self.exitSatelliteImport()
        return

    def pollSatellites(self):
        if self.getSatellites_state:
            if self.getSatellites_state == self.thread_is_running:
                if self.requestSatelliteslistRefresh:
                    self.requestSatelliteslistRefresh = False
                    self['list'].setEntries(self.satelliteslist)
            elif self.getSatellites_state == self.thread_is_done:
                try:
                    self.satTimer.stop()
                except Exception:
                    pass

                self.getSatellites_state = self.thread_is_off
                self.requestSatelliteslistRefresh = False
                self['list'].setEntries(self.satelliteslist)
                try:
                    if self.satelliteslist:
                        self['list'].instance.setCurrentIndex(0)
                except Exception:
                    pass

        else:
            self.getSatellites_state = self.thread_is_running
            thread.start_new_thread(self.getSatellites, (None, ))
        return

    def getTransponders(self, dummy=None):
        return

    def pollTransponders(self):
        if self.getTransponders_state:
            if self.getTransponders_state == self.thread_is_running:
                if self.requestSatelliteslistRefresh:
                    self.requestSatelliteslistRefresh = False
                    self['list'].setEntries(self.satelliteslist)
            elif self.getTransponders_state == self.thread_is_done:
                try:
                    self.tpTimer.stop()
                except Exception:
                    pass

                self.getTransponders_state = self.thread_is_off
                self['list'].setEntries(self.satelliteslist)
        elif self.getTransponders_state == self.thread_is_done:
            try:
                self.tpTimer.stop()
            except Exception:
                pass

            self.getTransponders_state = self.thread_is_off
            self['list'].setEntries(self.satelliteslist)
            if self._pending_tp_open_once and self._pending_tp_open_idx is not None:
                idx = self._pending_tp_open_idx
                self._pending_tp_open_once = False
                self._pending_tp_open_idx = None
                try:
                    if idx < len(self.satelliteslist) and len(self.satelliteslist[idx]) > 1:
                        self.session.openWithCallback(self.finishedTranspondersEdit, TranspondersEditor, self.satelliteslist[idx])
                except Exception:
                    pass

        else:
            self.getTransponders_state = self.thread_is_running
            thread.start_new_thread(self.getTransponders, (None, ))
            try:
                self.tpTimer.start(1000)
            except Exception:
                self.tpTimer.start(1000)

        return

    def compareFrequency(self, a):
        return int(a.get('frequency'))

    def layoutFinished(self):
        try:
            if hasattr(self['list'], 'applyMetrics'):
                self['list'].applyMetrics(self['list'].instance.size())
            self['list']._enforce_fullrow_selection_clip()
        except Exception:
            pass

        try:
            if hasattr(self['head'], 'applyMetrics'):
                self['head'].applyMetrics(self['head'].instance.size())
        except Exception:
            pass

        self.pollSatellites()
        try:
            self.satTimer.start(1000)
        except Exception:
            self.satTimer.start(1000)

        return

    def selectSatellite(self):
        self.satelliteSelection(mode=self.modeSelect)
        return

    def unSelectSatellite(self):
        self.satelliteSelection(mode=self.modeUnSelect)
        return

    def selectSatelliteRepeated(self):
        self.down()
        self.satelliteSelection(mode=self.modeSelect, update=False)
        return

    def unSelectSatelliteRepeated(self):
        self.down()
        self.satelliteSelection(mode=self.modeUnSelect, update=False)
        return

    def selectSatelliteFinish(self):
        self['list'].down()
        self['list'].setEntries(self.satelliteslist)
        return

    def satelliteSelection(self, mode=modeToggle, update=True):
        if not self.satelliteslist:
            return
        cur_idx = self['list'].getSelectedIndex()
        if mode == self.modeToggle:
            selected = not self.satelliteslist[cur_idx][0].get('selected', False)
        elif mode == self.modeSelect:
            selected = True
        else:
            selected = False
        self.satelliteslist[cur_idx][0].update({'selected': selected})
        if update:
            self['list'].setEntries(self.satelliteslist)
        return

    def getSatellites(self, dummy):
        return


class LyngSat(SatelliteImport):
    skin = '<screen name="LyngSatTS" position="center,center" size="1700,900" title="LyngSat satellites"><widget name="head" position="40,20" size="1620,40" scrollbarMode="showNever"/><widget name="list" position="40,70" size="1620,760" scrollbarMode="showOnDemand" transparent="1" zPosition="2"/><eLabel position="40,845" size="1620,2" backgroundColor="#ffffff"/><widget name="fspace" position="40,855" size="1620,32" font="Regular;24" foregroundColor="yellow" transparent="1" halign="center" valign="center"/></screen>'
    thread_is_off = 0
    thread_is_running = 1
    thread_is_done = 2
    transFec = {'1/2': '1', '2/3': '2', '3/4': '3', '5/6': '4', '7/8': '5', '8/9': '6', '3/5': '7', '4/5': '8', '9/10': '9'}

    def __init__(self, session, selectedregion=None):
        SatelliteImport.__init__(self, session)
        self.skinName = ['LyngSatTS', 'LyngSat', 'SatelliteImportTS', 'SatelliteImport']
        self.baseurl = 'http://lyngsat.com'
        self.urlRegions = ('asia.html', 'europe.html', 'atlantic.html', 'america.html')
        self['fspace'].setText('connecting ... please wait')
        self.selectedregion = selectedregion
        self.no_cache = False
        return

    def robust_urlopen(self, url, max_retries=3):
        for i in range(max_retries):
            try:
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36')
                return urllib2.urlopen(req, timeout=30)
            except Exception as e:
                print 'Attempt %d failed: %s' % (i + 1, str(e))
                if i < max_retries - 1:
                    time.sleep(2)
                else:
                    raise e

        return

    def get_cached_content(self, url, cache_dir='/tmp/lyngsat_cache', max_age=86400):
        if self.no_cache:
            return self.robust_urlopen(url).read()
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        key = url.encode('utf-8') if isinstance(url, unicode) else url
        h = hashlib.md5(key).hexdigest()
        path = os.path.join(cache_dir, h)
        if os.path.exists(path) and time.time() - os.path.getmtime(path) < max_age:
            with open(path, 'r') as f:
                return f.read()
        data = self.robust_urlopen(url).read()
        with open(path, 'w') as f:
            f.write(data)
        return data

    def parse_lyngsat_table(self, html_content):
        try:
            html = html_content.decode('utf-8', 'ignore')
        except Exception:
            html = html_content

        soup = BeautifulSoup(html, 'html.parser')
        pos_re = re.compile(u'\ud+(?:\s*\.\s*\d+)?)\s*(?:0xb0|&deg;|&#176;)?\s*([EW])', re.I | re.U)
        satellites, seen = [], set()
        current_pos = None

        def is_satellite_page(href):
            h = href.lower()
            if not h.endswith('.html'):
                return False
            if '/tvchannels/' in h or '/stream/' in h or '/packages/' in h or '/tracker/' in h:
                return False
            path = href if href.startswith('/') else '/' + href
            if '/' in path[1:]:
                return False
            banned = ('index.html', 'headlines.html', 'launches.html')
            return not any(path.endswith(b) for b in banned)

        for tr in soup.find_all('tr'):
            tds = tr.find_all('td', recursive=False)
            if not tds:
                continue
            pos_td = next((td for td in tds if (td.get('width') or '').strip() == '70'), None)
            if pos_td:
                mp = pos_re.search(_clean_spaces(pos_td.get_text(' ', strip=True)))
                if mp:
                    try:
                        pos_val = float(re.sub(u'\s+', u'', mp.group(1)))
                        pos_dir = mp.group(2).upper()
                        current_pos = int(pos_val * 10)
                        if pos_dir == 'W':
                            current_pos = -current_pos
                    except Exception:
                        current_pos = None

            else:
                row_text = _clean_spaces(tr.get_text(' ', strip=True))
                mp = pos_re.search(row_text)
                if mp:
                    try:
                        pos_val = float(re.sub(u'\s+', u'', mp.group(1)))
                        pos_dir = mp.group(2).upper()
                        current_pos = int(pos_val * 10)
                        if pos_dir == 'W':
                            current_pos = -current_pos
                    except Exception:
                        pass

            name_td = next((td for td in tds if (td.get('width') or '').strip() == '180'), None)
            candidates = [name_td] if name_td else [td for td in tds if (td.get('width') or '').strip() != '70']
            sat_href, sat_name = (None, None)
            for td in filter(None, candidates):
                for a in td.find_all('a', href=True):
                    href = a['href']
                    label = _u(_clean_spaces(a.get_text(' ', strip=True)))
                    if not label or not is_satellite_page(href):
                        continue
                    sat_href, sat_name = href, label
                    break

                if sat_href:
                    break

            if not sat_href or current_pos is None:
                continue
            if not sat_href.startswith('http'):
                sat_href = self.baseurl + (sat_href if sat_href.startswith('/') else '/' + sat_href)
            if sat_href in seen:
                continue
            seen.add(sat_href)
            satellites.append({'name': (_u(sat_name)), 'position': (_u(str(current_pos))), 'url': sat_href})

        return satellites

    def getSatellites(self, dummy):
        print 'getSatellites'
        sats = []
        self.satelliteslist = sats
        regions = self.urlRegions if self.selectedregion in (None, 'All') else [self.selectedregion]
        for region in regions:
            try:
                url = self.baseurl + '/' + region
                print 'Fetching: ' + url
                html = self.robust_urlopen(url).read() if self.no_cache else self.get_cached_content(url)
                try:
                    print 'Fetched bytes: %d for %s' % (len(html), region)
                except Exception:
                    pass

                parsed = self.parse_lyngsat_table(html)
                print 'Parsed %d satellites from %s' % (len(parsed), region)
                for sat in parsed:
                    sat['name'] = str(sat['name'])
                    sat['position'] = _u(sat['position'])
                    sats.append([sat])
                    try:
                        print 'Added: %s @ %s' % (sat['name'], sat['position'])
                    except Exception:
                        pass

            except Exception as e:
                print 'Error processing %s: %s' % (region, str(e))
                try:
                    self['fspace'].setText('Error: ' + str(e))
                except Exception:
                    pass

                time.sleep(1)

        self.getSatellites_state = self.thread_is_done
        self.requestSatelliteslistRefresh = True
        try:
            self['list'].setEntries(self.satelliteslist)
            if self.satelliteslist:
                self['list'].instance.setCurrentIndex(0)
            self['fspace'].setText('Press OK to include satellites in satellites.xml' if sats else 'No satellites found')
            self['list']._enforce_fullrow_selection_clip()
        except Exception:
            pass

        return

    def getTransponders(self, dummy=None):
        transSystem = {'dvb-s': '0', 'dvb-s2': '1'}
        transPolarisation = {'h': '0', 'v': '1', 'l': '2', 'r': '3'}
        transModulation = {'dvb-s': '1', 'dvb-s2': '2', 'qpsk': '1', '8psk': '2', 'qam16': '3'}
        num = lambda s: re.sub('[^0-9]', '', s or '')
        text = lambda n: (n or '').strip().lower()
        idle = False
        while not idle:
            idle = True
            for sat in self.satelliteslist:
                if sat[0].get('selected', False):
                    idle = False
                    if len(sat) == 1:
                        url = sat[0].get('url', '')
                        try:
                            raw = self.get_cached_content(url)
                            try:
                                html = raw.decode('utf-8', 'ignore')
                            except Exception:
                                html = raw

                        except Exception:
                            try:
                                self['fspace'].setText(_('Failed to get %s') % url)
                            except Exception:
                                pass

                            return

                        soup = BeautifulSoup(html, 'html.parser')
                        tps = {}
                        for tr in soup.find_all('tr'):
                            tds = tr.find_all(['td', 'th'])
                            if len(tds) < 4:
                                continue
                            cells = [_clean_spaces(td.get_text(' ', strip=True)) for td in tds]
                            freq = next((c for c in cells if re.search('\\d{4,5}(\\.\\d+)?\\s*(mhz)?', c, re.I)), None)
                            pol = next((c for c in cells if re.match('^[HVLR]$', c, re.I)), None)
                            sr = next((c for c in cells if re.search('\\d{2,5}\\s*(ks|ksym|sym)', c, re.I) or re.match('^\\d{4,5}$', c)), None)
                            fec = next((c for c in cells if re.search('^(auto|none|[1-9]/\\d{1,2})$', c, re.I)), None)
                            if not (freq and pol and sr and fec):
                                continue
                            try:
                                freq_hz = num(freq)
                                if len(freq_hz) <= 5:
                                    freq_hz = str(int(freq_hz) * 1000)
                                sr_sym = num(sr)
                                if len(sr_sym) <= 5:
                                    sr_sym = str(int(sr_sym) * 1000)
                                pol_l = text(pol)[:1]
                                row_txt = (' ').join(cells).lower()
                                prefer_s2 = 'dvb-s2' in row_txt or '8psk' in row_txt
                                sys = 'dvb-s2' if prefer_s2 else 'dvb-s'
                                mod = '8psk' if prefer_s2 else 'qpsk'
                                key = freq_hz + transPolarisation.get(pol_l, '0')
                                tps[key] = {'frequency': freq_hz, 
                                   'system': (transSystem.get(sys, '0')), 
                                   'polarization': (transPolarisation.get(pol_l, '0')), 
                                   'symbol_rate': sr_sym, 
                                   'modulation': (transModulation.get(mod, '0')), 
                                   'fec_inner': (self.transFec.get(_clean_spaces(fec), '0')), 
                                   'import': 13749320}
                            except Exception:
                                continue

                        lst = tps.values()
                        lst.sort(key=self.compareFrequency)
                        sat.append(list(lst))
                    sat[0]['selected'] = False
                    self.requestSatelliteslistRefresh = True

        self.getTransponders_state = self.thread_is_done
        return

    def exitSatelliteImport(self):
        posList = {}
        for sat in self.satelliteslist:
            if len(sat) > 1:
                pos = sat[0].get('position')
                if pos in posList:
                    posList.get(pos)[1].extend(sat[1])
                else:
                    posList.update({pos: sat})

        cleanList = []
        for pos in posList:
            a = posList.get(pos)
            if 'selected' in a[0]:
                del a[0]['selected']
            newName = a[0]['name'].replace('C-Band:', '').split('-')
            newPos = newName[-1].split()
            newPos = newPos[-1].replace(')', '').replace('(', '').strip()
            newName = newName[0].strip() + ' (' + newPos + ')'
            a[0].update({'name': (_u(newName))})
            cleanList.append(a)

        self.close(cleanList)
        return


class Lamedb():

    def __init__(self):
        self.satellitesList = self.translateTransponders(self.getTransponders(self.readLamedb()))
        return

    def readLamedb(self):
        f = file('/etc/enigma2/lamedb', 'r')
        lamedb = f.readlines()
        f.close()
        if lamedb[0].find('/3/') != -1:
            self.version = 3
        elif lamedb[0].find('/4/') != -1:
            self.version = 4
        else:
            print 'unknown version: ', lamedb[0]
            return
        print 'import version %d' % self.version
        return lamedb

    def getTransponders(self, lamedb):
        if lamedb is None:
            return
        else:
            collect = False
            state = 0
            transponders = []
            tp = []
            for x in lamedb:
                if x == 'transponders\n':
                    collect = True
                    continue
                if x == 'end\n':
                    break
                y = x.strip().split(':')
                if collect:
                    if y[0] == '/':
                        transponders.append(tp)
                        tp = []
                    else:
                        tp.append(y)

            return transponders
            return

    def translateTransponders(self, transponders):
        t1 = [
         'namespace', 'tsid', 'onid']
        t2_sv3 = [4, 
         5, 
         6, 
         7, 
         8, 
         9, 
         10, 
         11, 
         12, 
         13]
        t2_sv4 = [4, 
         5, 
         6, 
         7, 
         8, 
         9, 
         14, 
         10, 
         11, 
         12, 
         13]
        if transponders is None:
            return
        else:
            tplist = []
            for x in transponders:
                tp = {}
                if len(x[0]) > len(t1):
                    print 'zu viele Parameter (t1) in ', x[0]
                    continue
                freq = x[1][0].split()
                if len(freq) != 2:
                    print 'zwei Parameter erwartet in ', freq
                    continue
                x[1][0] = freq[1]
                if freq[0] == 's' or freq[0] == 'S':
                    if self.version == 3 and len(x[1]) > len(t2_sv3) or self.version == 4 and len(x[1]) > len(t2_sv4):
                        print 'zu viele Parameter (t2) in ', x[1]
                        continue
                    for y in range(0, len(x[0])):
                        tp.update({(t1[y]): (x[0][y])})

                    for y in range(0, len(x[1])):
                        if self.version == 3:
                            tp.update({(t2_sv3[y]): (x[1][y])})
                        elif self.version == 4:
                            tp.update({(t2_sv4[y]): (x[1][y])})

                    tp.update({'import': 13468991})
                    if int(tp.get('namespace'), 16) / 65536 != int(tp.get('position')):
                        print 'Namespace %s und Position %s sind  nicht identisch' % (tp.get('namespace'), tp.get('position'))
                        continue
                elif freq[0] == 'c' or freq[0] == 'C':
                    print 'DVB-C'
                    continue
                elif freq[0] == 't' or freq[0] == 'T':
                    print 'DVB-T'
                    continue
                tplist.append(tp)

            satlist = {}
            for x in tplist:
                tmp = satlist.get(x.get('position'), [])
                tmp.append(x)
                satlist.update({(x.get('position')): tmp})

            del tplist
            print 'Anzahl der Satelliten: ', len(satlist)
            for x in satlist:
                print 'Position: ', x
                print 'Transponder: ', len(satlist.get(x))

            return satlist
            return


class Transponder():
    essential = [
     'frequency', 'polarization', 'symbol_rate']
    niceToHave = ['system',
     'fec_inner',
     'tsid',
     'onid']
    transSystem = {'0': 'DVB-S', '1': 'DVB-S2', 'dvb-s': 'DVB-S', 
       'dvb-s2': 'DVB-S2'}
    reTransSystem = {'DVB-S': '0', 'DVB-S2': '1'}
    transPolarisation = {'0': 'H', 'h': 'H', '1': 'V', 
       'v': 'V', 
       '2': 'L', 
       'cl': 'L', 
       'l': 'L', 
       '3': 'R', 
       'cr': 'R', 
       'r': 'R', 
       'i': 'i'}
    reTransPolarisation = {'H': '0', 'V': '1', 'L': '2', 
       'R': '3'}
    transModulation = {'0': 'AUTO', '1': 'QPSK', '2': '8PSK', 
       '3': 'QAM16'}
    reTransModulation = {'AUTO': '0', 'QPSK': '1', '8PSK': '2', 
       'QAM16': '3'}
    transRolloff = {'0': '0_35', '1': '0_25', '2': '0_20'}
    reTransRolloff = {'0_35': '0', '0_25': '1', '0_20': '2'}
    transOnOff = {'0': 'OFF', '1': 'ON', '2': 'AUTO'}
    reTransOnOff = {'OFF': '0', 'ON': '1', 'AUTO': '2'}
    transFec = {'0': 'FEC_AUTO', '1': 'FEC_1_2', '2': 'FEC_2_3', 
       '3': 'FEC_3_4', 
       '4': 'FEC_5_6', 
       '5': 'FEC_7_8', 
       '6': 'FEC_8_9', 
       '7': 'FEC_3_5', 
       '8': 'FEC_4_5', 
       '9': 'FEC_9_10', 
       '15': 'FEC_NONE', 
       'auto': 'FEC_AUTO', 
       '1/2': 'FEC_1_2', 
       '2/3': 'FEC_2_3', 
       '3/4': 'FEC_3_4', 
       '5/6': 'FEC_5_6', 
       '7/8': 'FEC_7_8', 
       '8/9': 'FEC_8_9', 
       '3/5': 'FEC_3_5', 
       '4/5': 'FEC_4_5', 
       '9/10': 'FEC_9_10', 
       'none': 'FEC_NONE'}
    reTransFec = {'FEC_AUTO': '0', 'FEC_1_2': '1', 'FEC_2_3': '2', 
       'FEC_3_4': '3', 
       'FEC_5_6': '4', 
       'FEC_7_8': '5', 
       'FEC_8_9': '6', 
       'FEC_3_5': '7', 
       'FEC_4_5': '8', 
       'FEC_9_10': '9', 
       'FEC_NONE': '15'}
    onlyDVBS2Fec = ['FEC_8_9',
     'FEC_3_5',
     'FEC_4_5',
     'FEC_9_10']
    transBand = {'KU': ('10700000', '12750000'), 'C': ('3400000', '4200000')}

    def __init__(self, transponder):
        self.rawData = transponder
        self.system = 'DVB-S'
        self.__frequency = '10700000'
        self.__symbolrate = '27500000'
        self.polarisation = 'H'
        self.modulation = 'QPSK'
        self.pilot = 'OFF'
        self.rolloff = '0_35'
        self.fec = 'FEC_AUTO'
        self.inversion = 'AUTO'
        self.__tsid = '0'
        self.useTsid = False
        self.__onid = '0'
        self.useOnid = False
        self.band = 'KU'
        self.__importColor = None
        self.transponderDoctor(self.rawData)
        return

    def transponderDoctor(self, transponder):
        if not isinstance(transponder, dict):
            print 'transponderDoctor: Transponderdaten muessen vom Type DICT sein'
            print transponder
            return
        else:
            param = transponder.keys()
            transParam = {}
            for x in param:
                transParam[x] = x.lower()

            if 'polarisation' in transParam:
                transParam.update({'polarization': (transParam.get('polarisation').lower())})
                del transParam['polarisation']
            missing = []
            for x in self.essential:
                if x not in transParam:
                    missing.append(x)

            if len(missing):
                print 'transponderDoctor: Folgende Parameter fehlen:', missing
                return
            self.polarisation = self.transPolarisation.get(transponder.get(transParam.get('polarization'), 'i').lower())
            if self.polarisation == 'i':
                print 'transponderDoctor: unbekannter Wert fuer Polarisation (%s)' % transParam.get('polarization')
                return
            self.__frequency = transponder.get(transParam.get('frequency'), 'i').lower()
            self.__symbolrate = transponder.get(transParam.get('symbol_rate'), 'i').lower()
            dvb_s_cnt = 0
            dvb_s2_cnt = 0
            self.__importColor = transponder.get('import', None)
            if 'system' in transParam:
                self.system = self.transSystem.get(transponder.get(transParam.get('system'), 'i').lower())
                if self.system == 'DVB-S':
                    dvb_s_cnt += 1
                if self.system == 'DVB-S2':
                    dvb_s2_cnt += 1
            if 'modulation' in transParam:
                self.modulation = self.transModulation.get(transponder.get(transParam.get('modulation'), 'i').lower())
                if self.modulation == '8PSK' or self.modulation == 'QAM16':
                    dvb_s2_cnt += 1
            if 'pilot' in transParam:
                self.pilot = self.transOnOff.get(transponder.get(transParam.get('pilot'), 'i').lower())
                if self.pilot == 'ON' or self.pilot == 'AUTO':
                    dvb_s2_cnt += 1
            if 'rolloff' in transParam:
                self.rolloff = self.transRolloff.get(transponder.get(transParam.get('rolloff'), 'i').lower())
                if self.rolloff == '0_25':
                    dvb_s2_cnt += 1
            if 'fec_inner' in transParam:
                self.fec = self.transFec.get(transponder.get(transParam.get('fec_inner'), 'i').lower())
                if self.fec in self.onlyDVBS2Fec:
                    dvb_s2_cnt += 1
            if dvb_s2_cnt:
                self.system = 'DVB-S2'
            else:
                self.system = 'DVB-S'
            if 'inversion' in transParam:
                self.inversion = self.transOnOff.get(transponder.get(transParam.get('inversion'), 'i').lower())
            if 'tsid' in transParam:
                self.__tsid = transponder.get(transParam.get('tsid'), 'i').lower()
                self.useTsid = True
            if 'onid' in transParam:
                self.__onid = transponder.get(transParam.get('onid'), 'i').lower()
                self.useOnid = True
            return
            return

    def getFrequency(self):
        return self.__frequency

    def setFrequency(self, frequency):
        if isinstance(frequency, list):
            if len(frequency) == 2:
                if isinstance(frequency[0], int) and isinstance(frequency[1], int):
                    self.__frequency = str(frequency[0] * 1000 + frequency[1])
                    return
        else:
            self.__frequency = str(frequency)
        return

    frequency = property(getFrequency, setFrequency)
    importColor = property((lambda self: self.__importColor))

    def getSymbolrate(self):
        return self.__symbolrate

    def setSymbolrate(self, symbolrate):
        self.__symbolrate = str(symbolrate)
        return

    symbolrate = property(getSymbolrate, setSymbolrate)

    def setTsid(self, newTsid):
        self.__tsid = str(newTsid)
        return

    tsid = property((lambda self: self.__tsid), setTsid)

    def getOnid(self):
        return self.__onid

    def setOnid(self, newOnid):
        self.__onid = str(newOnid)
        return

    onid = property((lambda self: self.__onid), setOnid)

    def exportImportColor(self):
        return {'import': (self.__importColor)}

    def exportSystem(self):
        return {'system': (self.reTransSystem.get(self.system))}

    def exportFec(self):
        return {'fec_inner': (self.reTransFec.get(self.fec))}

    def exportFrequency(self):
        return {'frequency': (self.__frequency)}

    def exportPolarisation(self):
        return {'polarization': (self.reTransPolarisation.get(self.polarisation))}

    def exportSymbolrate(self):
        return {'symbol_rate': (self.__symbolrate)}

    def exportModulation(self):
        return {'modulation': (self.reTransModulation.get(self.modulation))}

    def exportOnid(self):
        return {'onid': (self.__onid)}

    def exportTsid(self):
        return {'tsid': (self.__tsid)}

    def exportInversion(self):
        return {'inversion': (self.reTransOnOff.get(self.inversion))}

    def exportPilot(self):
        return {'pilot': (self.reTransOnOff.get(self.pilot))}

    def exportRolloff(self):
        return {'rolloff': (self.reTransRolloff.get(self.rolloff))}

    def exportClean(self):
        res = {}
        res.update(self.exportSystem())
        res.update(self.exportFec())
        res.update(self.exportFrequency())
        res.update(self.exportPolarisation())
        res.update(self.exportSymbolrate())
        res.update(self.exportModulation())
        if self.useOnid:
            res.update(self.exportOnid())
        if self.useTsid:
            res.update(self.exportTsid())
        if self.inversion != 'AUTO':
            res.update(self.exportInversion())
        if self.system == 'DVB-S2':
            if self.pilot != 'OFF':
                res.update(self.exportPilot())
        if self.rolloff != '0_35':
            res.update(self.exportRolloff())
        return res

    def exportAll(self):
        res = self.exportClean()
        res.update(self.exportImportColor())
        return res


class TransponderList(MenuList):

    def __init__(self):
        MenuList.__init__(self, list=[], content=eListboxPythonMultiContent)
        self.rowHight = 24
        self.l.setItemHeight(24)
        self.l.setFont(0, gFont('Regular', 20))
        return

    def setEntries(self, transponderlist):
        transRolloff = {'0_35': '0.35', '0_25': '0.25', '0_20': '0.20'}
        transFec = {'FEC_AUTO': 'auto', 'FEC_1_2': '1/2', 'FEC_2_3': '2/3', 
           'FEC_3_4': '3/4', 
           'FEC_5_6': '5/6', 
           'FEC_7_8': '7/8', 
           'FEC_8_9': '8/9', 
           'FEC_3_5': '3/5', 
           'FEC_4_5': '4/5', 
           'FEC_9_10': '9/10', 
           'FEC_NONE': 'none'}
        res = []
        z = 0
        for x in transponderlist:
            transponder = Transponder(x)
            tp = []
            tp.append(z)
            z += 1
            calc_xpos = lambda a: a[len(a) - 1][1] + a[len(a) - 1][3]
            color = transponder.importColor
            tp.append(MultiContentEntryText(pos=(0, 0), size=(110, self.rowHight), font=0, flags=RT_HALIGN_LEFT | RT_VALIGN_TOP, text=transponder.system, color=color, border_width=1, border_color=12092939))
            tp.append(MultiContentEntryText(pos=(calc_xpos(tp), 0), size=(100, self.rowHight), font=0, flags=RT_HALIGN_RIGHT | RT_VALIGN_TOP, text=str(int(transponder.frequency) / 1000), color=color, border_width=1, border_color=12092939))
            tp.append(MultiContentEntryText(pos=(calc_xpos(tp), 0), size=(45, self.rowHight), font=0, flags=RT_HALIGN_CENTER | RT_VALIGN_TOP, text=transponder.polarisation, color=color, border_width=1, border_color=12092939))
            tp.append(MultiContentEntryText(pos=(calc_xpos(tp), 0), size=(100, self.rowHight), font=0, flags=RT_HALIGN_RIGHT | RT_VALIGN_TOP, text=str(int(transponder.symbolrate) / 1000), color=color, border_width=1, border_color=12092939))
            tp.append(MultiContentEntryText(pos=(calc_xpos(tp), 0), size=(75, self.rowHight), font=0, flags=RT_HALIGN_CENTER | RT_VALIGN_TOP, text=transFec.get(transponder.fec), color=color, border_width=1, border_color=12092939))
            tp.append(MultiContentEntryText(pos=(calc_xpos(tp), 0), size=(85, self.rowHight), font=0, flags=RT_HALIGN_CENTER | RT_VALIGN_TOP, text=transponder.modulation, color=color, border_width=1, border_color=12092939))
            tp.append(MultiContentEntryText(pos=(calc_xpos(tp), 0), size=(70, self.rowHight), font=0, flags=RT_HALIGN_CENTER | RT_VALIGN_TOP, text=transRolloff.get(transponder.rolloff), color=color, border_width=1, border_color=12092939))
            tp.append(MultiContentEntryText(pos=(calc_xpos(tp), 0), size=(60, self.rowHight), font=0, flags=RT_HALIGN_CENTER | RT_VALIGN_TOP, text=transponder.inversion, color=color, border_width=1, border_color=12092939))
            tp.append(MultiContentEntryText(pos=(calc_xpos(tp), 0), size=(60, self.rowHight), font=0, flags=RT_HALIGN_CENTER | RT_VALIGN_TOP, text=transponder.pilot, color=color, border_width=1, border_color=12092939))
            tp.append(MultiContentEntryText(pos=(calc_xpos(tp), 0), size=(90, self.rowHight), font=0, flags=RT_HALIGN_CENTER | RT_VALIGN_TOP, text=transponder.tsid, color=color, border_width=1, border_color=12092939))
            tp.append(MultiContentEntryText(pos=(calc_xpos(tp), 0), size=(90, self.rowHight), font=0, flags=RT_HALIGN_CENTER | RT_VALIGN_TOP, text=transponder.onid, color=color, border_width=1, border_color=12092939))
            res.append(tp)

        self.l.setList(res)
        return


class TransponderEditor(Screen, ConfigListScreen, Transponder):
    skin = '\n                <screen name="TransponderEditor" position="center,center" size="920,600" title="Edit transponder" >\n                <eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\n\t        <ePixmap name="red"    position="70,545"   zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" transparent="1" alphatest="blend" />\n\t        <ePixmap name="green"  position="280,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_green.png" transparent="1" alphatest="blend" />\n\t        <ePixmap name="yellow" position="490,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_yellow.png" transparent="1" alphatest="blend" /> \n        \t<ePixmap name="blue"   position="700,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_blue.png" transparent="1" alphatest="blend" /> \n        \t<widget name="key_red" position="70,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" /> \n        \t<widget name="key_green" position="280,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" /> \n\t\t<widget name="config" position="25,25" size="880,340" scrollbarMode="showOnDemand" transparent="1" zPosition="2" />\n\t\t</screen>'

    def __init__(self, session, transponderData=None):
        self.skin = TransponderEditor.skin
        Screen.__init__(self, session)
        Transponder.__init__(self, transponderData)
        self.createConfig()
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'cancel': (self.cancel), 'ok': (self.okExit), 'red': (self.cancel), 
           'green': (self.okExit)}, -1)
        self['key_red'] = Button(_('Cancel'))
        self['key_green'] = Button(_('OK'))
        self.list = []
        ConfigListScreen.__init__(self, self.list)
        self.createSetup()
        self.onShown.append(self.setWindowTitle)
        return

    def setWindowTitle(self):
        self.setTitle('Edit transponder')
        return

    def createConfig(self):
        self.configTransponderSystem = ConfigSelection([('DVB-S', _('DVB-S')), ('DVB-S2', _('DVB-S2'))], self.system)
        self.configTransponderFrequency = ConfigFloat(default=[int(self.frequency) / 1000, int(self.frequency) % 1000], limits=[(0, 99999), (0, 999)])
        self.configTransponderPolarisation = ConfigSelection([('H', _('horizontal')),
         (
          'V', _('vertical')),
         (
          'L', _('circular left')),
         (
          'R', _('circular right'))], self.polarisation)
        self.configTransponderSymbolrate = ConfigInteger(default=int(self.symbolrate) / 1000, limits=(0,
                                                                                                      99999))
        self.configTransponderFec = ConfigSelection([('FEC_AUTO', _('auto')),
         (
          'FEC_1_2', _('1/2')),
         (
          'FEC_2_3', _('2/3')),
         (
          'FEC_3_4', _('3/4')),
         (
          'FEC_5_6', _('5/6')),
         (
          'FEC_7_8', _('7/8'))], self.fec)
        self.configTransponderFec2 = ConfigSelection([('FEC_AUTO', _('auto')),
         (
          'FEC_1_2', _('1/2')),
         (
          'FEC_2_3', _('2/3')),
         (
          'FEC_3_4', _('3/4')),
         (
          'FEC_5_6', _('5/6')),
         (
          'FEC_7_8', _('7/8')),
         (
          'FEC_8_9', _('8/9')),
         (
          'FEC_3_5', _('3/5')),
         (
          'FEC_4_5', _('4/5')),
         (
          'FEC_9_10', _('9/10'))], self.fec)
        self.configTransponderInversion = ConfigSelection([('OFF', _('off')), ('ON', _('on')), ('AUTO', _('auto'))], self.inversion)
        self.configTransponderModulation = ConfigSelection([('AUTO', _('auto')),
         (
          'QPSK', _('QPSK')),
         (
          '8PSK', _('8PSK')),
         (
          'QAM16', _('QAM16'))], self.modulation)
        self.configTransponderRollOff = ConfigSelection([('0_35', _('0.35')), ('0_25', _('0.25')), ('0_20', _('0.20'))], self.rolloff)
        self.configTransponderPilot = ConfigSelection([('OFF', _('off')), ('ON', _('on')), ('AUTO', _('auto'))], self.pilot)
        self.configTransponderUseTsid = ConfigYesNo(default=self.useTsid)
        self.configTransponderUseOnid = ConfigYesNo(default=self.useOnid)
        self.configTransponderTsid = ConfigInteger(default=int(self.tsid), limits=(0,
                                                                                   65535))
        self.configTransponderOnid = ConfigInteger(default=int(self.onid), limits=(0,
                                                                                   65535))
        return

    def createSetup(self):
        self.list = []
        self.list.append(getConfigListEntry(_('System'), self.configTransponderSystem))
        if self.system == 'DVB-S' or self.system == 'DVB-S2':
            self.list.append(getConfigListEntry(_('Freqency'), self.configTransponderFrequency))
            self.list.append(getConfigListEntry(_('Polarisation'), self.configTransponderPolarisation))
            self.list.append(getConfigListEntry(_('Symbolrate'), self.configTransponderSymbolrate))
        if self.system == 'DVB-S':
            self.list.append(getConfigListEntry(_('FEC'), self.configTransponderFec))
        elif self.system == 'DVB-S2':
            self.list.append(getConfigListEntry(_('FEC'), self.configTransponderFec2))
        if self.system == 'DVB-S' or self.system == 'DVB-S2':
            self.list.append(getConfigListEntry(_('Inversion'), self.configTransponderInversion))
            self.list.append(getConfigListEntry(_('use tsid'), self.configTransponderUseTsid))
            self.list.append(getConfigListEntry(_('use onid'), self.configTransponderUseOnid))
        if self.system == 'DVB-S2':
            self.list.append(getConfigListEntry(_('Modulation'), self.configTransponderModulation))
            self.list.append(getConfigListEntry(_('RollOff'), self.configTransponderRollOff))
            self.list.append(getConfigListEntry(_('Pilot'), self.configTransponderPilot))
        if self.system == 'DVB-S' or self.system == 'DVB-S2':
            if self.useTsid:
                self.list.append(getConfigListEntry(_('TSID'), self.configTransponderTsid))
            if self.useOnid:
                self.list.append(getConfigListEntry(_('ONID'), self.configTransponderOnid))
        self['config'].list = self.list
        self['config'].l.setList(self.list)
        return

    def cancel(self):
        self.close(None)
        return

    def okExit(self):
        self.system = self.configTransponderSystem.value
        self.frequency = self.configTransponderFrequency.value
        self.polarisation = self.configTransponderPolarisation.value
        self.symbolrate = self.configTransponderSymbolrate.value * 1000
        if self.system == 'DVB-S':
            self.fec = self.configTransponderFec.value
        else:
            self.fec = self.configTransponderFec2.value
        self.inversion = self.configTransponderInversion.value
        self.modulation = self.configTransponderModulation.value
        self.rolloff = self.configTransponderRollOff.value
        self.pilot = self.configTransponderPilot.value
        self.tsid = self.configTransponderTsid.value
        self.onid = self.configTransponderOnid.value
        self.close(self.exportAll())
        return

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.newConfig()
        return

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.newConfig()
        return

    def newConfig(self):
        print 'newConfig'
        checkList = (self.configTransponderSystem, self.configTransponderUseTsid, self.configTransponderUseOnid)
        for x in checkList:
            if self['config'].getCurrent()[1] == x:
                if x == self.configTransponderSystem:
                    self.system = self.configTransponderSystem.value
                elif x == self.configTransponderUseTsid:
                    self.useTsid = self.configTransponderUseTsid.value
                elif x == self.configTransponderUseOnid:
                    self.useOnid = self.configTransponderUseOnid.value
            self.createSetup()

        return


class TranspondersEditor(Screen):
    skin = '\n                <screen name="SatellitesEditor" position="center,center" size="920,600" title=""  >\n                <eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\n\t        <ePixmap name="red"    position="70,545"   zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" transparent="1" alphatest="blend" />\n\t        <ePixmap name="green"  position="280,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_green.png" transparent="1" alphatest="blend" />\n\t        <ePixmap name="yellow" position="490,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_yellow.png" transparent="1" alphatest="blend" /> \n        \t<ePixmap name="blue"   position="700,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_blue.png" transparent="1" alphatest="blend" /> \n        \t<widget name="key_red" position="70,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" /> \n        \t<widget name="key_green" position="280,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" /> \n                <widget name="key_yellow" position="490,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;20" transparent="1" />\n        \t<widget name="key_blue" position="700,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" />\n\t\t<widget name="list" position="20,49" size="880,436" scrollbarMode="showOnDemand" transparent="1" zPosition="2" />\n\t\t<widget name="head" position="20,25" size="880,24" scrollbarMode="showNever" transparent="1" zPosition="2" />\n\t\t</screen>'

    def __init__(self, session, satellite=None):
        self.skin = TranspondersEditor.skin
        Screen.__init__(self, session)
        self['actions'] = ActionMap(['SatellitesEditorActions'], {'nextPage': (self.nextPage), 'prevPage': (self.prevPage), 'select': (self.editTransponder), 
           'exit': (self.cancel), 
           'left': (self.left), 
           'leftUp': (self.doNothing), 
           'leftRepeated': (self.doNothing), 
           'right': (self.right), 
           'rightUp': (self.doNothing), 
           'rightRepeated': (self.doNothing), 
           'up': (self.up), 
           'upUp': (self.upUp), 
           'upRepeated': (self.upRepeated), 
           'down': (self.down), 
           'downUp': (self.downUp), 
           'downRepeated': (self.downRepeated), 
           'red': (self.removeTransponder), 
           'green': (self.editTransponder), 
           'yellow': (self.addTransponder), 
           'blue': (self.sortColumn)}, -1)
        self.transponderslist = satellite[1]
        self.satelliteName = satellite[0].get('name')
        self['key_red'] = Button(_('remove'))
        self['key_green'] = Button(_('edit'))
        self['key_yellow'] = Button(_('add'))
        self['key_blue'] = Button(_('sort'))
        self['head'] = Head()
        self.currentSelectedColumn = 0
        self['list'] = TransponderList()
        self['list'].setEntries(self.transponderslist)
        self.row = [['system', _('1'), False],
         [
          'freq', _('2'), False],
         [
          'pol', _('3'), False],
         [
          'sr', _('4'), False],
         [
          'fec', _('5'), False],
         [
          'modul', _('6'), False],
         [
          'rolloff', _('7'), False],
         [
          'invers', _('8'), False],
         [
          'pilot', _('9'), False],
         [
          'tsid', _('10'), False],
         [
          'onid', _('11'), False]]
        self.onLayoutFinish.append(self.layoutFinished)
        return

    def layoutFinished(self):
        self.setTitle('Transponders Editor (%s)' % self.satelliteName)
        row = self['list'].getCurrent()
        if row is None:
            return
        else:
            head = []
            for x in range(1, len(row)):
                head.append((row[x][1], row[x][3], self.row[x - 1][0]))

            self['head'].setEntries(head)
            data = self['head'].l.getCurrentSelection()
            data = data[self.currentSelectedColumn + 1]
            self['head'].l.setSelectionClip(eRect(data[1], data[0], data[3], data[4]), True)
            self.updateSelection()
            return
            return

    def updateSelection(self):
        row = self['list'].l.getCurrentSelection()
        if row is None:
            return
        else:
            firstColumn = row[1]
            lastColumn = row[len(row) - 1]
            self['list'].l.setSelectionClip(eRect(firstColumn[1], firstColumn[0], lastColumn[1] + lastColumn[3], lastColumn[4]), True)
            return
            return

    def doNothing(self):
        return

    def left(self):
        print 'left'
        if self.currentSelectedColumn:
            self.currentSelectedColumn -= 1
            data = self['head'].l.getCurrentSelection()
            data = data[self.currentSelectedColumn + 1]
            self['head'].l.setSelectionClip(eRect(data[1], data[0], data[3], data[4]), True)
        return

    def right(self):
        print 'right'
        if self.currentSelectedColumn < len(self.row) - 1:
            self.currentSelectedColumn += 1
            data = self['head'].l.getCurrentSelection()
            data = data[self.currentSelectedColumn + 1]
            self['head'].l.setSelectionClip(eRect(data[1], data[0], data[3], data[4]), True)
        return

    def upRepeated(self):
        self['list'].up()
        self.updateSelection()
        return

    def downRepeated(self):
        self['list'].down()
        self.updateSelection()
        return

    def nextPage(self):
        self['list'].pageUp()
        self.lastSelectedIndex = self['list'].getSelectedIndex()
        self.updateSelection()
        return

    def prevPage(self):
        self['list'].pageDown()
        self.lastSelectedIndex = self['list'].getSelectedIndex()
        self.updateSelection()
        return

    def up(self):
        self['list'].up()
        self.lastSelectedIndex = self['list'].getSelectedIndex()
        self.updateSelection()
        return

    def down(self):
        self['list'].down()
        self.lastSelectedIndex = self['list'].getSelectedIndex()
        self.updateSelection()
        return

    def upUp(self):
        cur_idx = self['list'].getSelectedIndex()
        if self.lastSelectedIndex != cur_idx:
            self.lastSelectedIndex = cur_idx
        return

    def downUp(self):
        cur_idx = self['list'].getSelectedIndex()
        if self.lastSelectedIndex != cur_idx:
            self.lastSelectedIndex = cur_idx
        return

    def addTransponder(self):
        print 'addTransponder'
        self.session.openWithCallback(self.finishedTransponderAdd, TransponderEditor)
        return

    def editTransponder(self):
        print 'editTransponder'
        if not len(self.transponderslist):
            return
        cur_idx = self['list'].getSelectedIndex()
        self.session.openWithCallback(self.finishedTransponderEdit, TransponderEditor, self.transponderslist[cur_idx])
        return

    def finishedTransponderEdit(self, result):
        print 'finishedTransponderEdit'
        if result is None:
            return
        else:
            cur_idx = self['list'].getSelectedIndex()
            self.transponderslist[cur_idx] = result
            self['list'].setEntries(self.transponderslist)
            return
            return

    def finishedTransponderAdd(self, result):
        print 'finishedTransponderAdd'
        if result is None:
            return
        else:
            self.transponderslist.append(result)
            self['list'].setEntries(self.transponderslist)
            return
            return

    def removeTransponder(self):
        print 'removeTransponder'
        if len(self.transponderslist):
            cb_func = lambda ret: not ret or self.deleteTransponder()
            self.session.openWithCallback(cb_func, MessageBox, _('Remove Transponder?'), MessageBox.TYPE_YESNO)
        return

    def deleteTransponder(self):
        if len(self.transponderslist):
            self.transponderslist.pop(self['list'].getSelectedIndex())
            self['list'].setEntries(self.transponderslist)
        return

    def cancel(self):
        self.close(None)
        return

    def compareColumn(self, a):
        return int(a.get(self.row[self.currentSelectedColumn][0], '-1'))

    def sortColumn(self):
        rev = self.row[self.currentSelectedColumn][2]
        self.transponderslist.sort(key=self.compareColumn, reverse=rev)
        if rev:
            self.row[self.currentSelectedColumn][2] = False
        else:
            self.row[self.currentSelectedColumn][2] = True
        self['list'].setEntries(self.transponderslist)
        self.update = True
        return


class SatelliteList(MenuList):

    def __init__(self):
        MenuList.__init__(self, list=[], content=eListboxPythonMultiContent)
        self.l.setItemHeight(24)
        self.l.setFont(0, gFont('Regular', 20))
        return

    def setEntries(self, satelliteslist):
        print 'setEntries', len(satelliteslist)
        res = []
        for x in satelliteslist:
            satparameter = x[0]
            satentry = []
            pos = int(satparameter.get('position'))
            if pos < 0:
                pos += 3600
            satentry.append(pos)
            color = None
            color_sel = None
            if satparameter.get('selected', False):
                color = 0
                color_sel = 65344
            backcolor = None
            backcolor_sel = None
            if len(x) == 1:
                backcolor = 1644912
                backcolor_sel = 9466996
            satentry.append(MultiContentEntryText(pos=(0, 0), size=(530, 24), font=0, flags=RT_HALIGN_LEFT | RT_VALIGN_TOP, text=satparameter.get('name'), color=color, color_sel=color_sel, backcolor=backcolor, backcolor_sel=backcolor_sel, border_width=1, border_color=15792383))
            pos = int(satparameter.get('position'))
            posStr = str(abs(pos) / 10) + '.' + str(abs(pos) % 10)
            if pos < 0:
                posStr = posStr + ' ' + _('West')
            if pos > 0:
                posStr = posStr + ' ' + _('East')
            satentry.append(MultiContentEntryText(pos=(530, 0), size=(170, 24), font=0, flags=RT_HALIGN_LEFT | RT_VALIGN_TOP, text=posStr, color=color, color_sel=color_sel, backcolor=backcolor, backcolor_sel=backcolor_sel, border_width=1, border_color=15792383))
            res.append(satentry)

        self.l.setList(res)
        return


class Head(HTMLComponent, GUIComponent):

    def __init__(self):
        GUIComponent.__init__(self)
        self.l = eListboxPythonMultiContent()
        self.l.setSelectionClip(eRect(0, 0, 0, 0))
        self.l.setItemHeight(20)
        self.l.setFont(0, gFont('Regular', 20))
        return

    GUI_WIDGET = eListbox

    def postWidgetCreate(self, instance):
        instance.setContent(self.l)
        return

    def setEntries(self, data=None):
        res = [None]
        if data is not None:
            for x in data:
                res.append(MultiContentEntryText(pos=(x[0], 0), size=(x[1], 20), font=0, flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER, text=x[2], color=12632256, backcolor=4671288, color_sel=16777215, backcolor_sel=6316032, border_width=1, border_color=15792383))

        self.l.setList([res])
        return


class SatEditor(Screen, ConfigListScreen):
    flagNetworkScan = 1
    flagUseBAT = 2
    flagUseONIT = 4
    skin = '\n                <screen name="SatEditor" position="center,center" size="920,600" title="Edit Sat"   >\n                <eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\n\t        <ePixmap name="red"    position="70,545"   zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" transparent="1" alphatest="blend" />\n\t        <ePixmap name="green"  position="280,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_green.png" transparent="1" alphatest="blend" />\n\t        <ePixmap name="yellow" position="490,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_yellow.png" transparent="1" alphatest="blend" /> \n        \t<ePixmap name="blue"   position="700,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_blue.png" transparent="1" alphatest="blend" /> \n        \t<widget name="key_red" position="70,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" /> \n        \t<widget name="key_green" position="280,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" /> \n\t\t<widget name="config" position="25,25" size="880,276" scrollbarMode="showOnDemand"  transparent="1" zPosition="2" />\n\t\t</screen>'

    def __init__(self, session, satelliteData=None):
        self.skin = SatEditor.skin
        Screen.__init__(self, session)
        self.satelliteData = satelliteData
        self.satelliteOrientation = 'east'
        if self.satelliteData is not None:
            self.satelliteName = self.satelliteData.get('name', 'new satellite')
            satellitePosition = int(self.satelliteData.get('position', '0'))
            if satellitePosition < 0:
                self.satelliteOrientation = 'west'
            satellitePosition = abs(satellitePosition)
            self.satellitePosition = [satellitePosition / 10, satellitePosition % 10]
            self.satelliteFlags = int(self.satelliteData.get('flags', '1'))
        else:
            self.satelliteName = 'new satellite'
            self.satellitePosition = [0, 0]
            self.satelliteFlags = 1
        self.createConfig()
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'cancel': (self.cancel), 'ok': (self.okExit), 'red': (self.cancel), 
           'green': (self.okExit)}, -1)
        self['key_red'] = Button(_('Cancel'))
        self['key_green'] = Button(_('OK'))
        self.list = []
        ConfigListScreen.__init__(self, self.list)
        self.onShown.append(self.setWindowTitle)
        self.createSetup()
        return

    def setWindowTitle(self):
        self.setTitle('Edit satellite')
        return

    def createConfig(self):
        self.configSatelliteName = ConfigText(default=self.satelliteName, visible_width=50, fixed_size=False)
        self.configSatellitePosition = ConfigFloat(default=self.satellitePosition, limits=[(0, 179), (0, 9)])
        self.configSatelliteOrientation = ConfigSelection([('east', _('East')), ('west', _('West'))], self.satelliteOrientation)
        self.configSatelliteFlagNetworkScan = ConfigYesNo(default=self.satelliteFlags & self.flagNetworkScan and True)
        self.configSatelliteFlagUseBAT = ConfigYesNo(default=self.satelliteFlags & self.flagUseBAT and True)
        self.configSatelliteFlagUseONIT = ConfigYesNo(default=self.satelliteFlags & self.flagUseONIT and True)
        return

    def createSetup(self):
        self.list = []
        self.list.append(getConfigListEntry(_('Name'), self.configSatelliteName))
        self.list.append(getConfigListEntry(_('Position'), self.configSatellitePosition))
        self.list.append(getConfigListEntry(_('Orientation'), self.configSatelliteOrientation))
        self.list.append(getConfigListEntry(_('Network scan'), self.configSatelliteFlagNetworkScan))
        self.list.append(getConfigListEntry(_('BAT'), self.configSatelliteFlagUseBAT))
        self.list.append(getConfigListEntry(_('ONIT'), self.configSatelliteFlagUseONIT))
        self['config'].list = self.list
        self['config'].l.setList(self.list)
        return

    def cancel(self):
        self.close(None)
        return

    def okExit(self):
        satelliteFlags = (self.configSatelliteFlagNetworkScan.value and self.flagNetworkScan) + (self.configSatelliteFlagUseBAT.value and self.flagUseBAT) + (self.configSatelliteFlagUseONIT.value and self.flagUseONIT)
        satellitePosition = self.configSatellitePosition.value[0] * 10 + self.configSatellitePosition.value[1]
        if self.configSatelliteOrientation.value == 'west':
            satellitePosition = -satellitePosition
        satelliteData = {'name': (self.configSatelliteName.value), 'flags': (str(satelliteFlags)), 'position': (str(satellitePosition))}
        self.close(satelliteData)
        return


class TSipanelMenuSelection(Screen):
    skin = '\n                <screen name="TSipanelMenuSelection" position="center,center" size="920,600" title="updates satellites" >\n                <widget source="menulist" render="Listbox" position="200,15" size="520,252" scrollbarMode="showOnDemand" transparent="1" zPosition="2" >\n\t\t                <convert type="TemplatedMultiContent">\n\t\t\t\t\t{"template": [\n\t\t\t\t\t\t\tMultiContentEntryText(pos = (0, 0), size = (520, 36), font=0, flags = RT_HALIGN_CENTER| RT_VALIGN_CENTER, text = 0),\n\t\t\t\t\t\t],\n\t\t\t\t\t"fonts": [gFont("Regular", 26)],\n\t\t\t\t\t"itemHeight": 36\n\t\t\t\t\t}\n\t\t\t\t</convert>\n                </widget>                \t\n\t\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.actionList = []
        self.actionList.append((_('Default source-recommonded'), ''))
        self.actionList.append((_('Internet Settings loader'), ''))
        self.actionList.append((_('LyngSat-All satellites'), ''))
        self.actionList.append((_('LyngSat-Europe satellites'), ''))
        self.actionList.append((_('LyngSat-Asia satellites'), ''))
        self.actionList.append((_('LyngSat-Atlantic satellites'), ''))
        self.actionList.append((_('LyngSat-America satellites'), ''))
        self['menulist'] = List(self.actionList)
        self['key_red'] = Button(_('Close'))
        self['setupActions'] = ActionMap(['SetupActions'], {'ok': (self.okbuttonClick), 'cancel': (self.cancel), 'red': (self.cancel)})
        self.onShown.append(self.setWindowTitle)
        return

    def setWindowTitle(self):
        self.setTitle('Updates satellites')
        return

    def okbuttonClick(self):
        print 'okbuttonClick'
        self.close(self['menulist'].getCurrent()[0])
        print '[menulist Current]'
        print self['menulist'].getCurrent()[0]
        return

    def cancel(self):
        self.close(None)
        return


class SatellitesEditor(Screen):
    skin = '\n                <screen name="SatellitesEditor" position="center,center" size="920,600" title=""  >\n                <eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\n                <ePixmap name="red"    position="44,545"   zPosition="2" size="150,30" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" transparent="1" alphatest="blend" />\n                <ePixmap name="green"  position="200,545" zPosition="2" size="150,30" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_green.png" transparent="1" alphatest="blend" />\n                <ePixmap name="yellow" position="356,545" zPosition="2" size="150,30" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_yellow.png" transparent="1" alphatest="blend" /> \n                <ePixmap name="blue"   position="512,545" zPosition="2" size="150,30" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_blue.png" transparent="1" alphatest="blend" /> \n                <widget name="key_red" position="44,550" size="150,30" valign="center" halign="center" zPosition="4" font="Regular;20" transparent="1" /> \n                <widget name="key_green" position="200,550" size="150,30" valign="center" halign="center" zPosition="4" font="Regular;20" transparent="1" /> \n                <widget name="key_yellow" position="356,550" size="150,30" valign="center" halign="center" zPosition="4" font="Regular;20" transparent="1" />\n                <widget name="key_blue" position="512,550" size="150,30" valign="center" halign="center" zPosition="4" font="Regular;20" transparent="1" />\n\t\t<ePixmap alphatest="blend" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_menu.png" position="680,545" size="35,25" zPosition="5"/>\n\t\t<widget name="menu" font="Regular;18" halign="left" position="725,547" size="140,25" transparent="1" valign="center" zPosition="6"/>\n\t\t<widget name="list" position="90,49" size="720,340" scrollbarMode="showOnDemand" transparent="1" zPosition="2" />\n\t\t<widget name="head" position="90,25" size="720,24" scrollbarMode="showNever" transparent="1" zPosition="2" />\n\t\t<widget name="polhead" position="140,395" size="660,24" transparent="1" zPosition="2" />\n\t\t<widget name="bandlist" position="80,419" size="60,72" transparent="1" zPosition="2" />\n\t\t<widget name="infolist" position="140,419" size="720,72" transparent="1" zPosition="2" />\n\t\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['actions'] = ActionMap(['SatellitesEditorActions'], {'nextPage': (self.nextPage), 'prevPage': (self.prevPage), 'displayHelp': (self.showHelp), 
           'displayMenu': (self.openMenu), 
           'select': (self.editTransponders), 
           'exit': (self.Exit), 
           'left': (self.left), 
           'leftUp': (self.doNothing), 
           'leftRepeated': (self.doNothing), 
           'right': (self.right), 
           'rightUp': (self.doNothing), 
           'rightRepeated': (self.doNothing), 
           'upUp': (self.upUp), 
           'up': (self.up), 
           'upRepeated': (self.upRepeated), 
           'upUp': (self.upUp), 
           'down': (self.down), 
           'downUp': (self.downUp), 
           'downRepeated': (self.downRepeated), 
           'red': (self.removeSatellite), 
           'green': (self.editSatellite), 
           'yellow': (self.sortColumn), 
           'blue': (self.serviceeditor)}, -1)
        self.satelliteslist = self.readSatellites('/etc/tuxbox/satellites.xml')
        self['key_red'] = Button(_('Remove'))
        self['key_green'] = Button(_('Edit'))
        self['key_yellow'] = Button(_('Sort'))
        self['key_blue'] = Button(_('Service editor'))
        self['menu'] = Button(_('Add-update'))
        self['infolist'] = MenuList([])
        self['infolist'].l = eListboxPythonMultiContent()
        self['infolist'].l.setSelectionClip(eRect(0, 0, 0, 0))
        self['infolist'].l.setItemHeight(24)
        self['infolist'].l.setFont(0, gFont('Regular', 20))
        self['polhead'] = MenuList([])
        self['polhead'].l = eListboxPythonMultiContent()
        self['polhead'].l.setItemHeight(24)
        self['polhead'].l.setFont(0, gFont('Regular', 20))
        self['bandlist'] = MenuList([])
        self['bandlist'].l = eListboxPythonMultiContent()
        self['bandlist'].l.setItemHeight(24)
        self['bandlist'].l.setFont(0, gFont('Regular', 20))
        self['head'] = Head()
        self['list'] = SatelliteList()
        self['list'].setEntries(self.satelliteslist)
        self.onLayoutFinish.append(self.layoutFinished)
        self.currentSelectedColumn = 0
        self.row = [['name', _('Satellites'), False], ['position', _('Pos'), False]]
        self.update = False
        self.onShown.append(self.setWindowTitle)
        return

    def setWindowTitle(self):
        self.setTitle('Satellites manager')
        return

    def serviceeditor(self):
        self.session.open(ServiceEditor.plugin.TSiServicesEditor)
        return

    def layoutFinished(self):
        row = self['list'].getCurrent()
        head = []
        for x in range(1, len(row)):
            head.append([row[x][1], row[x][3], ''])

        head[0][2] = self.row[0][1]
        head[1][2] = self.row[1][1]
        self['head'].setEntries(head)
        data = self['head'].l.getCurrentSelection()
        data = data[self.currentSelectedColumn + 1]
        self['head'].l.setSelectionClip(eRect(data[1], data[0], data[3], data[4]), True)
        self.updateSelection()
        return

    def updateSelection(self):
        row = self['list'].l.getCurrentSelection()
        if row is None:
            return
        else:
            firstColumn = row[1]
            lastColumn = row[len(row) - 1]
            self['list'].l.setSelectionClip(eRect(firstColumn[1], firstColumn[0], lastColumn[1] + lastColumn[3], lastColumn[4]), True)
            self.getInfo()
            return
            return

    def doNothing(self):
        return

    def left(self):
        print 'left'
        if self.currentSelectedColumn:
            self.currentSelectedColumn -= 1
            data = self['head'].l.getCurrentSelection()
            data = data[self.currentSelectedColumn + 1]
            self['head'].l.setSelectionClip(eRect(data[1], data[0], data[3], data[4]), True)
        return

    def right(self):
        print 'right'
        if self.currentSelectedColumn < len(self.row) - 1:
            self.currentSelectedColumn += 1
            data = self['head'].l.getCurrentSelection()
            data = data[self.currentSelectedColumn + 1]
            self['head'].l.setSelectionClip(eRect(data[1], data[0], data[3], data[4]), True)
        return

    def nextPage(self):
        self['list'].pageUp()
        self.lastSelectedIndex = self['list'].getSelectedIndex()
        self.updateSelection()
        return

    def prevPage(self):
        self['list'].pageDown()
        self.lastSelectedIndex = self['list'].getSelectedIndex()
        self.updateSelection()
        return

    def up(self):
        self['list'].up()
        self.lastSelectedIndex = self['list'].getSelectedIndex()
        self.updateSelection()
        return

    def down(self):
        self['list'].down()
        self.lastSelectedIndex = self['list'].getSelectedIndex()
        self.updateSelection()
        return

    def upUp(self):
        cur_idx = self['list'].getSelectedIndex()
        if self.lastSelectedIndex != cur_idx:
            self.lastSelectedIndex = cur_idx
        return

    def downUp(self):
        cur_idx = self['list'].getSelectedIndex()
        if self.lastSelectedIndex != cur_idx:
            self.lastSelectedIndex = cur_idx
        return

    def upRepeated(self):
        self['list'].up()
        self.updateSelection()
        return

    def downRepeated(self):
        self['list'].down()
        self.updateSelection()
        return

    def getInfo(self):
        print 'getInfo'
        cur_idx = self['list'].getSelectedIndex()
        satellite = self.satelliteslist[cur_idx]
        self.name = satellite[0].get('name')
        self.position = satellite[0].get('position')
        self.tp_all = len(satellite[1])
        self.tp_ku = 0
        self.tp_c = 0
        self.tp_other = 0
        self.tp_ku_v = 0
        self.tp_ku_h = 0
        self.tp_ku_l = 0
        self.tp_ku_r = 0
        self.tp_ku_v2 = 0
        self.tp_ku_h2 = 0
        self.tp_ku_l2 = 0
        self.tp_ku_r2 = 0
        self.tp_c_v = 0
        self.tp_c_h = 0
        self.tp_c_l = 0
        self.tp_c_r = 0
        self.tp_c_v2 = 0
        self.tp_c_h2 = 0
        self.tp_c_l2 = 0
        self.tp_c_r2 = 0
        self.tp_ku_dvb_s = 0
        self.tp_ku_dvb_s2 = 0
        self.tp_c_dvb_s = 0
        self.tp_c_dvb_s2 = 0
        for tp in satellite[1]:
            freq = int(tp.get('frequency'))
            pol = tp.get('polarization')
            system = tp.get('system')
            if freq >= 10700000 and freq <= 12750000:
                if system == '0':
                    if pol == '0':
                        self.tp_ku_h += 1
                    elif pol == '1':
                        self.tp_ku_v += 1
                    elif pol == '2':
                        self.tp_ku_l += 1
                    elif pol == '3':
                        self.tp_ku_r += 1
                elif system == '1':
                    if pol == '0':
                        self.tp_ku_h2 += 1
                    elif pol == '1':
                        self.tp_ku_v2 += 1
                    elif pol == '2':
                        self.tp_ku_l2 += 1
                    elif pol == '3':
                        self.tp_ku_r2 += 1
            elif freq >= 3400000 and freq <= 4200000:
                if system == '0':
                    if pol == '0':
                        self.tp_c_h += 1
                    elif pol == '1':
                        self.tp_c_v += 1
                    elif pol == '2':
                        self.tp_c_l += 1
                    elif pol == '3':
                        self.tp_c_r += 1
                elif system == '1':
                    if pol == '0':
                        self.tp_c_h2 += 1
                    elif pol == '1':
                        self.tp_c_v2 += 1
                    elif pol == '2':
                        self.tp_c_l2 += 1
                    elif pol == '3':
                        self.tp_c_r2 += 1

        entryList = (
         _('Band'), _('Ku'), _('C'))
        l = []
        for entry in entryList:
            bandList = [None]
            bandList.append(MultiContentEntryText(pos=(0, 0), size=(75, 24), font=0, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER, text=entry, border_width=1, border_color=15792383))
            l.append(bandList)

        self['bandlist'].l.setList(l)
        calc_xpos = lambda a: a[len(a) - 1][1] + a[len(a) - 1][3]
        entryList = (_('horizontal'),
         _('vertical'),
         _('left'),
         _('right'))
        xpos = 0
        polarisationList = [None]
        for entry in entryList:
            polarisationList.append(MultiContentEntryText(pos=(xpos, 0), size=(165,
                                                                               24), font=0, flags=RT_HALIGN_CENTER | RT_VALIGN_TOP, text=entry, border_width=1, border_color=15792383))
            xpos = calc_xpos(polarisationList)

        self['polhead'].l.setList([polarisationList])
        l = []
        infolist = [None]
        entryList = (('dvb-s', 80),
         ('dvb-s2', 85),
         ('dvb-s', 80),
         ('dvb-s2', 85),
         ('dvb-s', 80),
         ('dvb-s2', 85),
         ('dvb-s', 80),
         ('dvb-s2', 85))
        xpos = 0
        for entry in entryList:
            infolist.append(MultiContentEntryText(pos=(xpos, 0), size=(entry[1], 24), font=0, flags=RT_HALIGN_CENTER | RT_VALIGN_TOP, text=entry[0], border_width=1, border_color=15792383))
            xpos = calc_xpos(infolist)

        l.append(infolist)
        infolist = [None]
        entryList = ((self.tp_ku_h, 80),
         (
          self.tp_ku_h2, 85),
         (
          self.tp_ku_v, 80),
         (
          self.tp_ku_v2, 85),
         (
          self.tp_ku_l, 80),
         (
          self.tp_ku_l2, 85),
         (
          self.tp_ku_r, 80),
         (
          self.tp_ku_r2, 85))
        xpos = 0
        for entry in entryList:
            infolist.append(MultiContentEntryText(pos=(xpos, 0), size=(entry[1], 24), font=0, flags=RT_HALIGN_CENTER | RT_VALIGN_TOP, text=str(entry[0]).lstrip('0'), border_width=1, border_color=15792383))
            xpos = calc_xpos(infolist)

        l.append(infolist)
        infolist = [None]
        entryList = ((self.tp_c_h, 80),
         (
          self.tp_c_h2, 85),
         (
          self.tp_c_v, 80),
         (
          self.tp_c_v2, 85),
         (
          self.tp_c_l, 80),
         (
          self.tp_c_l2, 85),
         (
          self.tp_c_r, 80),
         (
          self.tp_c_r2, 85))
        xpos = 0
        for entry in entryList:
            infolist.append(MultiContentEntryText(pos=(xpos, 0), size=(entry[1], 24), font=0, flags=RT_HALIGN_CENTER | RT_VALIGN_TOP, text=str(entry[0]).lstrip('0'), border_width=1, border_color=15792383))
            xpos = calc_xpos(infolist)

        l.append(infolist)
        self['infolist'].l.setList(l)
        return

    def readSatellites(self, file):
        satellitesXML = xml.etree.cElementTree.parse(file)
        satDict = satellitesXML.getroot()
        satelliteslist = []
        for sat in satDict.getiterator('sat'):
            transponderslist = []
            for transponder in sat.getiterator('transponder'):
                transponderslist.append(transponder.attrib)

            sat.attrib.update({'name': (sat.attrib.get('name', 'new Satellite').encode('latin-1'))})
            satelliteslist.append([sat.attrib, transponderslist])

        return satelliteslist

    def importLamedb(self):
        print 'importLamedb'
        lamedb = Lamedb()
        for x in lamedb.satellitesList:
            found = False
            for y in self.satelliteslist:
                if x == y[0].get('position'):
                    found = True
                    break

            if found:
                freq = []
                for tp in y[1]:
                    freq.append(int(tp.get('frequency')) + 100000000 * int(tp.get('polarization')) + 300000000 * int(tp.get('fec_inner')))

                for tp in lamedb.satellitesList.get(x):
                    print int(tp.get('frequency')) + 100000000 * int(tp.get('polarization')) + 300000000 * int(tp.get('fec_inner')) in freq and 'Transponder in Liste', tp
                    continue
                    print 'neuer Transponder', tp
                    newTp = Transponder(tp).exportAll()
                    y[1].append(newTp)

            else:
                posString = str(abs(int(x) / 10)) + '.' + str(abs(int(x) % 10))
                if int(x) < 0:
                    posString += 'W'
                elif int(x) > 0:
                    posString += 'E'
                newName = 'new Satellite (%s)' % posString
                newSat = [
                 {'name': newName, 'flags': '0', 'position': x}, []]
                for tp in lamedb.satellitesList.get(x):
                    tsid = tp.get('tsid', '-1')
                    if tsid != '-1':
                        tp.update({'tsid': (str(int(tsid, 16)))})
                    onid = tp.get('onid', '-1')
                    if onid != '-1':
                        tp.update({'onid': (str(int(onid, 16)))})
                    newTp = Transponder(tp).exportAll()
                    newSat[1].append(newTp)

                newSat[0].update({'flags': (newTp.get('flags', '1'))})
                self.satelliteslist.append(newSat)

        self['list'].setEntries(self.satelliteslist)
        return

    def writeSatellites(self):
        root = etree.Element('satellites')
        root.text = '\n\t'
        transponder = None
        satellite = None
        for x in self.satelliteslist:
            satellite = xml.etree.cElementTree.SubElement(root, 'sat', x[0])
            satellite.text = '\n\t\t'
            satellite.tail = '\n\t'
            for y in x[1]:
                y = Transponder(y).exportClean()
                transponder = xml.etree.cElementTree.SubElement(satellite, 'transponder', y)
                transponder.tail = '\n\t\t'

            if transponder is not None:
                transponder.tail = '\n\t'

        if transponder is not None:
            transponder.tail = '\n\t'
        if satellite is not None:
            satellite.tail = '\n'
        os.rename('/etc/tuxbox/satellites.xml', '/etc/tuxbox/satellites.xml.' + str(int(time.time())))
        newFile = open('/etc/tuxbox/satellites.xml', 'w')
        xmlString = etree.tostring(root)
        newFile.writelines(xmlString)
        newFile.close()
        nimmanager.satList = []
        nimmanager.cablesList = []
        nimmanager.terrestrialsList = []
        nimmanager.readTransponders()
        return

    def finishedSatAdd2(self):
        print 'finishedSatAdd'
        self.satelliteslist = self.readSatellites('/etc/tuxbox/satellites.xml')
        self['list'].setEntries(self.satelliteslist)
        return

    def addSatelliteloader(self):
        print 'addSatellite'
        if self.update == True:
            self.session.openWithCallback(self.updatesatsloader, MessageBox, _('By updating or adding satellites all changes made to satellites.xml will be lost,continue?'), MessageBox.TYPE_YESNO)
        else:
            self.session.openWithCallback(self.finishedSatAdd2, TSiServersScreen)
        return

    def updatesatsloader(self, result):
        if result:
            self.session.openWithCallback(self.finishedSatAdd2, TSiServersScreen)
        return

    def addSatellite(self):
        print 'addSatellite'
        if self.update == True:
            self.session.openWithCallback(self.updatesats, MessageBox, _('By updating or adding satellites all changes made to satellites.xml will be lost,continue?'), MessageBox.TYPE_YESNO)
        else:
            self.session.openWithCallback(self.finishedSatAdd2, satellite.NewTSisatEditor)
        return

    def updatesats(self, result):
        if result:
            self.session.openWithCallback(self.finishedSatAdd2, satellite.NewTSisatEditor)
        return

    def editTransponders(self):
        print 'editTransponders'
        if not len(self.satelliteslist):
            return
        cur_idx = self['list'].getSelectedIndex()
        self.update = True
        self.session.openWithCallback(self.finishedTranspondersEdit, TranspondersEditor, self.satelliteslist[cur_idx])
        return

    def finishedTranspondersEdit(self, result):
        print 'finishedTranspondersEdit'
        if result is None:
            return
        else:
            cur_idx = self['list'].getSelectedIndex()
            self.satelliteslist[cur_idx][1] = result
            self.update = True
            return
            return

    def editSatellite(self):
        print 'editSatellite'
        if not len(self.satelliteslist):
            return
        cur_idx = self['list'].getSelectedIndex()
        self.update = True
        self.session.openWithCallback(self.finishedSatEdit, SatEditor, self.satelliteslist[cur_idx][0])
        return

    def finishedSatEdit(self, result):
        print 'finishedSatEdit'
        if result is None:
            return
        else:
            cur_idx = self['list'].getSelectedIndex()
            self.satelliteslist[cur_idx][0] = result
            self['list'].setEntries(self.satelliteslist)
            self.update = True
            return
            return

    def finishedSatAdd(self, result):
        print 'finishedSatAdd'
        if result is None:
            return
        else:
            self.satelliteslist.append([result])
            self['list'].setEntries(self.satelliteslist)
            self.update = True
            return
            return

    def deleteSatellite(self):
        if len(self.satelliteslist):
            self.satelliteslist.pop(self['list'].getSelectedIndex())
            self['list'].setEntries(self.satelliteslist)
            self.update = True
        return

    def removeSatellite(self):
        print 'removeSatellite'
        self.update = True
        if len(self.satelliteslist):
            cur_idx = self['list'].getSelectedIndex()
            satellite = self.satelliteslist[cur_idx][0].get('name')
            cb_func = lambda ret: not ret or self.deleteSatellite()
            self.session.openWithCallback(cb_func, MessageBox, _('Remove Satellite %s?' % satellite), MessageBox.TYPE_YESNO)
        return

    def compareColumn(self, a):
        if self.row[self.currentSelectedColumn][0] == 'name':
            return a[0].get('name')
        if self.row[self.currentSelectedColumn][0] == 'position':
            return int(a[0].get('position'))
        return

    def sortColumn(self):
        rev = self.row[self.currentSelectedColumn][2]
        self.satelliteslist.sort(key=self.compareColumn, reverse=rev)
        if rev:
            self.row[self.currentSelectedColumn][2] = False
        else:
            self.row[self.currentSelectedColumn][2] = True
        self['list'].setEntries(self.satelliteslist)
        self.updateSelection()
        self.update = True
        return

    def openMenu(self):
        self.session.openWithCallback(self.menu, TSipanelMenuSelection)
        return

    def menu(self, result):
        print result
        if result is None:
            return
        else:
            print 'menu', result
            if result == 'Default source-recommonded':
                self.addSatellite()
            elif result == 'Internet Settings loader':
                self.addSatelliteloader()
            elif result == 'LyngSat-All satellites':
                self.update = True
                self.session.openWithCallback(self.finishedSatImport, LyngSat, 'All')
            elif result == 'LyngSat-Europe satellites':
                self.update = True
                self.session.openWithCallback(self.finishedSatImport, LyngSat, 'europe.html')
            elif result == 'LyngSat-Asia satellites':
                self.update = True
                self.session.openWithCallback(self.finishedSatImport, LyngSat, 'asia.html')
            elif result == 'LyngSat-Atlantic satellites':
                self.update = True
                self.session.openWithCallback(self.finishedSatImport, LyngSat, 'atlantic.html')
            elif result == 'LyngSat-America satellites':
                self.update = True
                self.session.openWithCallback(self.finishedSatImport, LyngSat, 'america.html')
            return
            return

    def finishedSatImport(self, result):
        print 'finishedSatImport'
        self.update = True
        if result is None:
            return
        else:
            if result is not None and len(result):
                for satelliteSrc in result:
                    posSrc = satelliteSrc[0].get('position', None)
                    print 'posSrc'
                    if posSrc is not None:
                        for satelliteDst in self.satelliteslist:
                            print satelliteDst[0].get('position', None)
                            if satelliteDst[0].get('position', None) == posSrc:
                                satelliteDst[1].extend(satelliteSrc[1])
                                if satelliteDst[0].get('name', 'new Satellite').find('new Satellite') != -1 and satelliteSrc[0].get('name', None) is not None:
                                    satelliteDst[0].update({'name': (satelliteSrc[0].get('name'))})
                                print 'extended:', posSrc
                                break
                            else:
                                continue
                        else:
                            self.satelliteslist.append(satelliteSrc)
                            print 'appended:', posSrc

                self['list'].setEntries(self.satelliteslist)
            return
            return

    def Exit(self):
        if self.update == False:
            pass
        else:
            cb_func = lambda ret: not ret or self.writeSatellites()
            self.session.openWithCallback(cb_func, MessageBox, _('Save satellites.xml? \n(This take some seconds.)'), MessageBox.TYPE_YESNO)
        self.close()
        self.cleansatellitesxml()
        return

    def cleansatellitesxml(self):
        top = '/etc/tuxbox/'
        for root, dirs, files in os.walk(top, topdown=False):
            for name in files:
                if 'satellites.xml.' in name:
                    os.remove(os.path.join(root, name))

        return

    def showHelp(self):
        print 'showHelp'
        return


def SatellitesEditorMain(session, **kwargs):
    session.open(SatellitesEditor)
    return


def SatellitesEditorStart(menuid, **kwargs):
    if menuid == 'scan':
        return [
         (
          _('TS-Satellites Editor'),
          SatellitesEditorMain,
          'TS-Satellites Editor',
          None)]
    else:
        return []
        return


def Plugins(**kwargs):
    if nimmanager.hasNimType('DVB-S'):
        return PluginDescriptor(name=_('TS-Satellites Editor'), description='Lets you edit satellites in your Dreambox', where=PluginDescriptor.WHERE_MENU, fnc=SatellitesEditorStart)
    else:
        return []

    return


return
