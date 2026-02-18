# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/CamsManager/MGcamdInfo/plugin.py
# Compiled at: 2014-03-12 01:12:27
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Sources.List import List
from Tools.LoadPixmap import LoadPixmap
from Components.ScrollLabel import ScrollLabel
from enigma import eConsoleAppContainer
from os import environ, remove
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Tools.Directories import fileExists, resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS
from Components.Language import language
import gettext

def localeInit():
    lang = language.getLanguage()
    environ['LANGUAGE'] = lang[:2]
    gettext.bindtextdomain('enigma2', resolveFilename(SCOPE_LANGUAGE))
    gettext.textdomain('enigma2')
    gettext.bindtextdomain('CCcamInfo', '%s%s' % (resolveFilename(SCOPE_PLUGINS), 'TSimage/CamsManager/CCcamInfo/locale/'))
    return


def _(txt):
    t = gettext.dgettext('CCcamInfo', txt)
    if t == txt:
        t = gettext.gettext(txt)
    return t


localeInit()
language.addCallback(localeInit)
VERSION = 'v0.9b'
DATE = '10.12.2013'
CFG = '/var/keys/mg_cfg'
menu_list = [_('General'),
 _('Servers'),
 _('pid.info'),
 _('ecm.info'),
 _('About')]

class MGcamdInfoMain(Screen):
    skin = '\n\t<screen position="center,center" size="500,440" title="MGcamd Info" >\n\t\t<widget source="menu" render="Listbox" position="10,0" size="480,440" scrollbarMode="showOnDemand" transparent="1" >\n\t\t\t\t        <convert type="TemplatedMultiContent">\n\t\t\t\t\t\t{"template": [\n\t\t\t\t\t\t\t        MultiContentEntryPixmapAlphaBlend(pos = (5, 7), size = (25, 25), png = 0), # Status Icon,\n\t\t\t\t\t\t\t\tMultiContentEntryText(pos = (35, 1), size = (400, 40), font=0, flags = RT_HALIGN_LEFT| RT_VALIGN_CENTER, text = 1),\n\t\t                                        ],\n\t\t\t\t\t\t"fonts": [gFont("Regular", 23)],\n\t\t\t\t\t\t"itemHeight": 40\n\t\t\t\t\t\t}\n\t\t\t\t\t</convert>\n\t    </widget>\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        self['menu'] = List([])
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'ok': (self.okClicked), 'cancel': (self.close), 
           'red': (self.close), 
           'green': (self.okClicked)}, -2)
        self.pic = LoadPixmap(cached=True, path='%s%s' % (resolveFilename(SCOPE_PLUGINS), 'TSimage/TSimagePanel/images/info.png'))
        self.onLayoutFinish.append(self.updateMenuList)
        return

    def updateMenuList(self):
        self.menu_list = []
        for x in self.menu_list:
            del self.menu_list[0]

        list = []
        idx = 0
        for x in menu_list:
            list.append((self.pic, x, idx))
            self.menu_list.append(x)
            idx += 1

        self['menu'].setList(list)
        return

    def keyNumberGlobal(self, idx):
        if idx < len(self.menu_list):
            sel = self.menu_list[idx]
            if sel == _('General'):
                self.showInfo(self.mgstatus())
            elif sel == _('Servers'):
                self.session.open(MGcamdInfoServerScreen)
            if sel == _('pid.info'):
                self.showFile('/tmp/pid.info')
            elif sel == _('ecm.info'):
                self.showFile('/tmp/ecm.info')
            else:
                self.showInfo(_('TS MGcamd Info %s\n\nThis plugin shows you the status of your MGcamd.') % VERSION)
        return

    def okClicked(self):
        self.keyNumberGlobal(self['menu'].getIndex())
        return

    def mgstatus(self):
        mgstatus_text = ''
        if fileExists('/tmp/mgstat.info'):
            f = open('/tmp/mgstat.info', 'r')
            line = f.readline()
            if line.find('MgCamd 1.38c') == 0:
                s = line.split('  ,    ')
            else:
                s = line.split(', ')
            bin_info = '  '
            bin_date = '  '
            if len(s) > 1:
                bin_info = s[0]
                bin_date = s[1]
            mgstatus_text += bin_info + '\n' + bin_date
            line = f.readline()
            s = line.split(', ')
            for i in range(len(s)):
                mgstatus_text += '\n' + s[i]

            while line:
                line = f.readline()
                if line.find('Box:') == 0:
                    s = line.split(', ')
                    for i in range(len(s)):
                        mgstatus_text += '\n' + s[i]

                    line = f.readline()
                    s = line.split(', ')
                    for i in range(len(s)):
                        mgstatus_text += '\n' + s[i]

                    line = f.readline()
                    s = line.split(', ')
                    for i in range(len(s)):
                        mgstatus_text += '\n' + s[i]

            f.close()
        return mgstatus_text

    def showFile(self, file):
        if fileExists(file):
            f = open(file, 'r')
            content = f.read()
            f.close()
        else:
            content = _('File %s does not exist !') % file
        self.showInfo(content)
        return

    def showInfo(self, info):
        self.session.open(MGcamdInfoInfoScreen, info)
        return


class MGcamdInfoServerScreen(Screen):
    skin = '\n\t<screen position="center,center" size="500,440" title="MGcamd Info Servers" >\n\t\t<widget source="list" render="Listbox" position="10,0" size="480,300" scrollbarMode="showOnDemand" transparent="1" >\n\t\t\t\t        <convert type="TemplatedMultiContent">\n\t\t\t\t\t\t{"template": [\n\t\t\t\t\t\t\t        MultiContentEntryPixmapAlphaBlend(pos = (8, 7), size = (16, 16), png = 0), # Status Icon,\n\t\t\t\t\t\t\t\tMultiContentEntryText(pos = (35, 0), size = (455, 30), font=0, flags = RT_HALIGN_LEFT| RT_VALIGN_CENTER, text = 1),\n\t\t                                        ],\n\t\t\t\t\t\t"fonts": [gFont("Regular", 21)],\n\t\t\t\t\t\t"itemHeight": 30\n\t\t\t\t\t\t}\n\t\t\t\t\t</convert>\n\t    </widget>\n\t\t<eLabel name="line" position="0,305" size="500,1" zPosition="2"  font="Regular;18" backgroundColor="foreground" />\n\t    <widget name="recon" position="0,310" size="500,25" valign="center" halign="left" zPosition="2" font="Regular;18" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n\t    <widget name="emm_out" position="0,335" size="500,25" valign="center" halign="left" zPosition="2" font="Regular;18" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n\t    <widget name="ecm_out" position="0,360" size="500,25" valign="center" halign="left" zPosition="2" font="Regular;18" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n\t    <widget name="cw_in" position="0,385" size="500,25" valign="center" halign="left" zPosition="2" font="Regular;18" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n\t    <widget name="avg_ecmtime" position="0,410" size="500,25" valign="center" halign="left" zPosition="2" font="Regular;18" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['list'] = List([])
        self['recon'] = Label('')
        self['emm_out'] = Label('')
        self['ecm_out'] = Label('')
        self['cw_in'] = Label('')
        self['avg_ecmtime'] = Label('')
        self['actions'] = ActionMap(['OkCancelActions'], {'ok': (self.close), 'cancel': (self.close)}, -1)
        self.greenStatus = LoadPixmap(cached=True, path='%s%s' % (resolveFilename(SCOPE_PLUGINS), 'TSimage/TSimagePanel/buttons/green.png'))
        self.greyStatus = LoadPixmap(cached=True, path='%s%s' % (resolveFilename(SCOPE_PLUGINS), 'TSimage/TSimagePanel/buttons/grey.png'))
        self.container = eConsoleAppContainer()
        self.stat_list = []
        self.onLayoutFinish.append(self.getMGcamdStat)
        self['list'].onSelectionChanged.append(self.updateInfos)
        self.onShown.append(self.setWindowTitle)
        return

    def setWindowTitle(self):
        self.setTitle(_('MGcamd Servers'))
        return

    def updateInfos(self):
        idx = self['list'].getIndex()
        self['recon'].setText(_('recon.: %d') % self.stat_list[idx][0])
        self['emm_out'].setText(_('EMM out.: %d') % self.stat_list[idx][1])
        self['ecm_out'].setText(_('ECM out.: %d') % self.stat_list[idx][2])
        self['cw_in'].setText(_('CW in: %d') % self.stat_list[idx][3])
        self['avg_ecmtime'].setText(_('Avg. ECM time: %d ms') % self.stat_list[idx][4])
        return

    def getMGcamdStat(self):
        if fileExists('/tmp/mgstat.info'):
            cmd = 'cat /tmp/mgstat.info | awk \'{sub(/([^ ]+ +){3}/,"")}1\' | tr \' \' \'#\' | awk \'{print$1;print$2;print$3;print$4;print$5;print$6}\' > /tmp/.mgstat'
            self.container.appClosed.append(self.createList)
            self.container.execute(cmd)
        return

    def getInfo(self, line):
        info = 0
        try:
            info = int(line)
        except:
            print '[getMGcamdStat] Exception in convet INT16 !'

        return info

    def createList(self, result):
        self.server_list = []
        line = ''
        if fileExists('/tmp/mgshare.info'):
            f = open('/tmp/mgshare.info', 'r')
            line = 'dummy'
            while line:
                addr = ''
                port = ''
                line = f.readline()
                s = line.split(' ')
                if len(s) > 2:
                    tmp = s[2].split(':')
                    if len(tmp) > 3:
                        addr = tmp[2].strip()
                        port = tmp[3].strip()
                server = addr + ':' + port
                status = s[len(s) - 1].strip()
                if status == 'online':
                    self.server_list.append((self.greenStatus, server))
                if status == 'offline':
                    self.server_list.append((self.greyStatus, server))

            f.close()
        self.mgstat()
        self['list'].setList(self.server_list)
        self.updateInfos()
        return

    def mgstat(self):
        self.stat_list = []
        if fileExists('/tmp/.mgstat'):
            f = open('/tmp/.mgstat', 'r')
            for i in range(30):
                line = f.readline()

            while line:
                line = f.readline()
                if line.strip() == '':
                    break
                s = line.split('#')
                if len(s) > 0:
                    conn = self.getInfo(f.readline().strip())
                    emm_out = self.getInfo(f.readline().strip())
                    ecm_out = self.getInfo(f.readline().strip())
                    cw_in = self.getInfo(f.readline().strip())
                    avg_time = self.getInfo(f.readline().strip())
                    self.stat_list.append((conn,
                     emm_out,
                     ecm_out,
                     cw_in,
                     avg_time))

            f.close()
            remove('/tmp/.mgstat')
        return


class MGcamdInfoInfoScreen(Screen):
    skin = '\n\t<screen position="center,center" size="500,440" title="MGcamd Info" >\n\t\t<widget name="text" position="10,0" size="480,440" font="Regular;19" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n\t</screen>'

    def __init__(self, session, info):
        Screen.__init__(self, session)
        self['text'] = ScrollLabel(info)
        self['actions'] = ActionMap(['MGcamdInfoActions'], {'ok': (self.close), 'cancel': (self.close), 
           'up': (self['text'].pageUp), 
           'down': (self['text'].pageDown), 
           'left': (self['text'].pageUp), 
           'right': (self['text'].pageDown)}, -1)
        return


return
