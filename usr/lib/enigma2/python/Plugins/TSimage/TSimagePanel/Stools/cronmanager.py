# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/Stools/cronmanager.py
# Compiled at: 2016-02-01 09:02:24
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from Components.Pixmap import Pixmap
from Components.Button import Button
from Screens.MessageBox import MessageBox
from Components.Sources.List import List
from Components.Label import Label
from os import environ, popen as os_popen, system as os_system, listdir as os_listdir, chmod as os_chmod, remove as os_remove, path as os_path
from Tools.LoadPixmap import LoadPixmap
from Tools.TSTools import getCmdOutput
from Plugins.TSimage.TSimagePanel.multInstaller import TSConsole
from Tools.Directories import fileExists, SCOPE_CURRENT_PLUGIN, SCOPE_PLUGINS, SCOPE_LANGUAGE, resolveFilename
from Components.config import getConfigListEntry, ConfigSelection, ConfigClock
from Components.ConfigList import ConfigListScreen
from Components.Language import language
from enigma import getDesktop
from datetime import datetime
import gettext
desktopSize = getDesktop(0).size()

def localeInit():
    lang = language.getLanguage()
    environ['LANGUAGE'] = lang[:2]
    gettext.bindtextdomain('enigma2', resolveFilename(SCOPE_LANGUAGE))
    gettext.textdomain('enigma2')
    gettext.bindtextdomain('TSCronManager', '%s%s' % (resolveFilename(SCOPE_PLUGINS), 'TSimage/TSimagePanel/locale/'))
    return


def _(txt):
    t = gettext.dgettext('TSCronManager', txt)
    if t == txt:
        t = gettext.gettext(txt)
    return t


localeInit()
language.addCallback(localeInit)
crontab_path = '/etc/cron/crontabs/root'
crontab_backup_path = '/etc/cron/crontabs/root.bak'
cronmanager_path = '/etc/cron'
cronmanager_script = '/etc/cron/cronmanager.sh'

class TSiCronScreen(Screen):
    skin_1280 = '\n\t\t<screen name="TSiCronScreen" position="center,77" size="920,600" title="Cron Manager" >\n                          <widget source="CronList" render="Listbox" position="20,20" size="880,450" scrollbarMode="showOnDemand" transparent="1" >\n\t\t\t\t<convert type="TemplatedMultiContent">\n\t\t\t\t   {"template": [\n\t\t\t\t\tMultiContentEntryText(pos = (10, 0), size = (750, 30), font=0, flags = RT_HALIGN_LEFT, text = 0), # Description\n\t\t\t\t\tMultiContentEntryText(pos = (530, 25), size = (210, 30), font=0, flags = RT_HALIGN_RIGHT, text = 1), # Status\n\t\t\t\t\tMultiContentEntryText(pos = (10, 25), size = (550, 22), font=1, flags = RT_HALIGN_LEFT, text = 2), # Scriptname\n\t\t\t\t\tMultiContentEntryText(pos = (10, 45), size = (550, 22), font=1, flags = RT_HALIGN_LEFT, text = 3), # time\n\t\t\t\t   ],\n\t\t\t\t   "fonts": [gFont("Regular", 22),gFont("Regular", 18)],\n\t\t\t\t   "itemHeight": 75\n\t\t\t\t   }\n\t\t                </convert> \n                          </widget>\n                          <eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\t\n                          <ePixmap name="red"    position="70,545"   zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" transparent="1" alphatest="on" />\n\t                  <ePixmap name="green"  position="280,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_green.png" transparent="1" alphatest="on" />\n\t                  <ePixmap name="yellow" position="490,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_yellow.png" transparent="1" alphatest="on" /> \n                          <ePixmap name="blue" position="700,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_blue.png" transparent="1" alphatest="on" /> \n        \t          <widget name="key_red" position="70,550" size="140,40" valign="center" halign="center" zPosition="2"  font="Regular;20" transparent="1" /> \n        \t          <widget name="key_green" position="280,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;20" transparent="1" /> \n        \t          <widget name="key_yellow" position="490,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;20" transparent="1" /> \n        \t          <widget name="key_blue" position="700,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;20" transparent="1" /> \n        \t</screen>\n\t\t'
    skin_1920 = '    <screen name="TSiCronScreen" position="center,200" size="1300,720" title="">\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png" position="50,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green-big.png" position="360,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/yellow-big.png" position="670,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/blue-big.png" position="980,640" size="200,40" alphatest="blend" />\n        <widget name="key_red" position="50,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#940d0d" transparent="1" />\n        <widget name="key_green" position="360,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#2d872d" transparent="1" />\n        <widget name="key_yellow" position="670,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#bba502" transparent="1" />\n        <widget name="key_blue" position="980,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#18188b" transparent="1" />\n        <widget source="CronList" render="Listbox" position="20,20" size="1260,480" zPosition="2" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background"  transparent="1" >\n        <convert type="TemplatedMultiContent">\n        {"template": [\n        MultiContentEntryText(pos = (15, 0), size = (1000, 40), font=0, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 0) ,\n        MultiContentEntryText(pos = (15, 0), size = (1260, 100), font=0, flags = RT_HALIGN_RIGHT | RT_VALIGN_CENTER, text = 1) ,\n        MultiContentEntryText(pos = (15, 35), size = (1000, 30), font=1, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 2) ,\n        MultiContentEntryText(pos = (15, 65), size = (1000, 30), font=1, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 3) ,\n        ],\n        "fonts": [gFont("Regular", 30),gFont("Regular", 23)],\n        "itemHeight": 100\n        }\n        </convert>\n        </widget>\n        </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session):
        Screen.__init__(self, session)
        self.path = '/etc/cron/scripts/'
        self.enabled_crond = False
        list = []
        self['red'] = Pixmap()
        self['green'] = Pixmap()
        self['yellow'] = Pixmap()
        self['blue'] = Pixmap()
        self['key_red'] = Label('')
        self['key_green'] = Label(_('Add'))
        self['key_yellow'] = Label(_('Stop Crond'))
        self['key_blue'] = Label(_('List script'))
        self['info'] = Label()
        self['actions'] = ActionMap(['OkCancelActions', 'ShortcutActions', 'TimerEditActions'], {'red': (self.removeCronQuestion), 'green': (self.AddCron), 
           'yellow': (self.StopStartCronQuestion), 
           'blue': (self.excScript), 
           'ok': (self.close), 
           'cancel': (self.close)}, -2)
        self.onShown.append(self.setWindowTitle)
        self.cronlist = []
        self.getCrontabList()
        self['CronList'] = List(self.cronlist)
        return

    def setWindowTitle(self):
        self.setTitle('Cron Manager')
        cmd = cronmanager_script + ' info | grep crontab'
        status = getCmdOutput(cmd)
        print 'status=' + status
        if status == '':
            self.enabled_crond = False
            print 'Crond is not running'
            self['key_yellow'].setText(_('Start Crond'))
            self['key_green'].setText('')
        else:
            self.enabled_crond = True
            print 'Crond is running'
            self['key_yellow'].setText(_('Stop Crond'))
            self['key_green'].setText(_('Add'))
        return

    def StopStartCronQuestion(self):
        text = 'crond'
        if self.enabled_crond:
            self.session.openWithCallback(self.StopStartCron, MessageBox, _('Do you really want to stop %s?') % text)
        else:
            self.StopStartCron(True)
        return

    def StopStartCron(self, result):
        if not result:
            return
        if self.enabled_crond:
            cmd = cronmanager_script + ' stop'
            os_system(cmd)
            os_system('mv ' + crontab_path + ' ' + crontab_backup_path)
            label_green = ''
            label_red = ''
            label_yellow = _('Start Crond')
            if os_path.exists('/etc/rc3.d/S99busybox-cron'):
                os_system('rm -f /etc/rc3.d/S99busybox-cron')
            self.enabled_crond = False
        else:
            os_system('mv ' + crontab_backup_path + ' ' + crontab_path)
            cmd = cronmanager_script + ' start'
            os_system(cmd)
            label_green = _('Add')
            label_red = ''
            label_yellow = _('Stop Crond')
            if not os_path.exists('/etc/rc3.d/S99busybox-cron'):
                os_system('ln -sfn /etc/init.d/busybox-cron /etc/rc3.d/S99busybox-cron')
            self.enabled_crond = True
        self['key_red'].setText(label_red)
        self['key_green'].setText(label_green)
        self['key_yellow'].setText(label_yellow)
        self.getCrontabList()
        self['CronList'].setList(self.cronlist)
        return

    def removeCronQuestion(self):
        cur = self['CronList'].getCurrent()
        if not cur:
            return
        self.session.openWithCallback(self.RemoveCron, MessageBox, _('Do you really want to delete %s?') % cur[0])
        return

    def RemoveCron(self, result):
        if not result:
            return
        self.cronlist_new = []
        cur = self['CronList'].getCurrent()
        if not len(self.cronlist) == 1:
            cronlist = self.readCronList()
            crontab_tmp_path = '/tmp/.newcronlist'
            for x in range(len(self.cronlist)):
                if not self.cronlist[x] == cur:
                    cmd = 'echo "' + cronlist[x].replace('\n', '') + '" >> ' + crontab_tmp_path
                    print 'cmd = ' + cmd
                    print 'cronlist = ' + cronlist[x].replace('\n', '')
                    os_system(cmd)
                    self.cronlist_new.append(self.cronlist[x])

            self.cronlist = self.cronlist_new
            self['CronList'].setList(self.cronlist)
            cmd = '/usr/bin/crontab ' + crontab_tmp_path
            os_system(cmd)
            if fileExists(crontab_tmp_path):
                os_remove(crontab_tmp_path)
            else:
                self.cronlist = self.cronlist_new
                self['CronList'].setList(self.cronlist)
                self['key_red'].setText('')
                os_remove(crontab_path)
                os_system('touch ' + crontab_path)
        else:
            self.cronlist = self.cronlist_new
            self['CronList'].setList(self.cronlist)
            self['key_red'].setText('')
            os_remove(crontab_path)
            os_system('touch ' + crontab_path)
        return

    def AddCron(self):
        if self.enabled_crond:
            self.session.openWithCallback(self.updateCronList, TSiAddCronScript, 'add')
        return

    def EditCron(self):
        if self.enabled_crond:
            cur = self['CronList'].getCurrent()
            self.session.openWithCallback(self.updateCronList, TSiAddCronScript, ('edit', cur))
        return

    def excScript(self):
        self.session.open(TSiListScript)
        return

    def readCronList(self):
        fm = open(crontab_path)
        cronlist = []
        line = '  '
        while line:
            line = fm.readline()
            cronlist.append(line)

        fm.close()
        return cronlist

    def getCrontabList(self):
        self.cronlist = []
        if fileExists(crontab_path):
            fm = open(crontab_path)
            line = '  '
            while line and not line == '':
                line = fm.readline()
                if not len(line) == 0:
                    sp = line.split(' ')
                    script_name = sp[5]
                    cron_description = script_name[18:-4].replace('_', ' ')
                    crontab_infos = self.getCrontabInfos(sp)
                    status = ''
                    self.cronlist.append((cron_description,
                     status,
                     'script: ' + script_name,
                     crontab_infos))

            fm.close()
            if not self.cronlist == []:
                self['key_red'].setText(_('Delete'))
        return

    def getCrontabInfos(self, sp):
        repeat_modus = _('user defined')
        weekday = ''
        day = ''
        month = ''
        time = sp[1] + ':' + sp[0] + ' '
        if not sp[2] == '*' and sp[3] == '*':
            if sp[2] == '1':
                day = sp[2] + _('st') + ' '
            elif sp[2] == '2':
                day = sp[2] + _('nd') + ' '
            elif sp[2] == '3':
                day = sp[2] + _('rd') + ' '
            else:
                day = sp[2] + _('th') + ' '
            repeat_modus = _('monthly')
        if not sp[2] == '*' and not sp[3] == '*' and sp[4] == '*':
            day = sp[2] + ' '
            month = self.nr2Month(sp[3]) + ', '
            repeat_modus = _('once')
        if not sp[2] == '*' and not sp[3] == '*' and not sp[4] == '*':
            day = sp[2] + ' '
            weekday = self.nr2Weekday(sp[4]) + ' '
            month = self.nr2Month(sp[3]) + ', '
            repeat_modus = _('once')
        if sp[2] == '*' and sp[3] == '*' and sp[4] == '*':
            repeat_modus = _('daily')
        if sp[2] == '*' and sp[3] == '*' and not sp[4] == '*':
            weekday = self.nr2Weekday(sp[4]) + ' '
            repeat_modus = _('weekly')
        mn = sp[0].replace('*/', '')
        if not mn == sp[0]:
            time = ''
            repeat_modus = _('Every ') + mn + _(' min(s)')
        hh = sp[1].replace('*/', '')
        if not hh == sp[1]:
            time = ''
            repeat_modus = _('Every ') + hh + _(' hour(s)')
        crontab_infos = weekday + day + month + time + repeat_modus
        return crontab_infos

    def updateCronList(self, answer):
        if not answer == None:
            self.getCrontabList()
            self['CronList'].setList(self.cronlist)
        return

    def nr2Weekday(self, nr):
        weekday_name = ''
        if nr == '0':
            weekday_name = _('Sun')
        elif nr == '1':
            weekday_name = _('Mon')
        elif nr == '2':
            weekday_name = _('Tue')
        elif nr == '3':
            weekday_name = _('Wed')
        elif nr == '4':
            weekday_name = _('Thu')
        elif nr == '5':
            weekday_name = _('Fri')
        elif nr == '6':
            weekday_name = _('Sat')
        return weekday_name

    def nr2Month(self, nr):
        month_name = ''
        if nr == '01':
            month_name = _('Jan')
        elif nr == '02':
            month_name = _('Feb')
        elif nr == '03':
            month_name = _('Mar')
        elif nr == '04':
            month_name = _('Apr')
        elif nr == '05':
            month_name = _('May')
        elif nr == '06':
            month_name = _('Jun')
        elif nr == '07':
            month_name = _('Jul')
        elif nr == '08':
            month_name = _('Aug')
        elif nr == '09':
            month_name = _('Sep')
        elif nr == '10':
            month_name = _('Oct')
        elif nr == '11':
            month_name = _('Nov')
        elif nr == '12':
            month_name = _('Dec')
        return month_name


class TSiListScript(Screen):
    skin_1280 = '\n                <screen  name="TSiListScript" position="center,77" size="920,600" title=""  >\n\t\t<widget source="menu" render="Listbox" position="20,15" size="880,416" scrollbarMode="showOnDemand" transparent="1" zPosition="1" >\n\t\t                <convert type="TemplatedMultiContent">\n\t\t\t\t\t{"template": [\n\t\t\t\t\t                MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (22, 22), png = 1), # Status Icon,\n\t\t\t\t\t\t\tMultiContentEntryText(pos = (40, 0), size = (650, 32), font=0, flags = RT_HALIGN_LEFT| RT_VALIGN_CENTER, text = 0),\n\t\t\t\t\t\t],\n\t\t\t\t\t"fonts": [gFont("Regular", 22)],\n\t\t\t\t\t"itemHeight": 32\n\t\t\t\t\t}\n\t\t\t\t</convert>\n                </widget>                \t                   \n\t        <eLabel position="20,470" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\n\t\t<widget name="info" position="20,460" zPosition="4" size="880,80" font="Regular;24" foregroundColor="yellow" transparent="1" halign="center" valign="center" />\n\t\t<eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\n                <widget name="red"    position="70,545"   zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" transparent="1" alphatest="blend" />\n\t        <widget name="green"  position="280,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_green.png" transparent="1" alphatest="blend" />\n        \t<widget name="key_red" position="70,550" size="140,40" valign="center" halign="center" zPosition="2"  font="Regular;21" transparent="1" /> \n        \t<widget name="key_green" position="280,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" /> \n        \t</screen>\n\t\t'
    skin_1920 = '    <screen name="TSiListScript" position="center,200" size="1300,720" title="">\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png" position="375,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green-big.png" position="725,640" size="200,40" alphatest="blend" />\n        <widget name="key_red" position="375,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#940d0d" transparent="1" />\n        <widget name="key_green" position="725,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#2d872d" transparent="1" />\n        <widget name="info" position="20,530" size="1260,40" foregroundColor="foreground" backgroundColor="background" font="Regular;28" valign="center" halign="center" transparent="1" zPosition="1" />\n        <widget source="menu" render="Listbox" position="20,20" size="1260,480" zPosition="2" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background"  transparent="1" >\n        <convert type="TemplatedMultiContent">\n        {"template": [\n        MultiContentEntryText(pos = (45, 0), size = (1000, 40), flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 0) ,\n        MultiContentEntryPixmapAlphaBlend(pos = (2, 7), size = (28, 28), png = 1),\n        ],\n        "fonts": [gFont("Regular", 32)],\n        "itemHeight": 40\n        }\n        </convert>\n        </widget>\n        </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session):
        Screen.__init__(self, session)
        self.path = '/etc/cron/scripts/'
        self.scriptIcon = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, 'TSimage/TSimagePanel/buttons/script.png'))
        self.script_list = []
        self['menu'] = List(self.script_list)
        self['red'] = Pixmap()
        self['green'] = Pixmap()
        self['yellow'] = Pixmap()
        self['key_red'] = Label(_('Close'))
        self['key_green'] = Label(_('Execute'))
        self['info'] = Label('FTP your script to /etc/cron/scripts')
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'red': (self.close), 'green': (self.doCommand), 
           'ok': (self.doCommand), 
           'cancel': (self.close)}, -2)
        self.listScripts()
        self.onShown.append(self.setWindowTitle)
        return

    def setWindowTitle(self):
        self.setTitle('Select Script to execute...')
        return

    def listScripts(self):
        self.script_list = []
        if fileExists(self.path):
            for x in os_listdir(self.path):
                x = x.replace('.sh', '')
                if x == 'cam' or x == 'script':
                    pass
                else:
                    self.script_list.append((x, self.scriptIcon))

            self.script_list.sort()
            self['menu'].setList(self.script_list)
        return

    def doCommand(self):
        if not len(self.script_list) == 0:
            selectedfolder = self['menu'].getCurrent()[0]
            script = self.path + selectedfolder + '.sh'
            os_chmod(script, 755)
            title = _('Executing script %s...') % selectedfolder
            cmd = 'sh ' + script + ' ; echo ; echo Done.'
            self.session.open(TSConsole, cmd, title)
        return


class TSiAddCronScript(Screen, ConfigListScreen):
    skin_1280 = '\n\t\t<screen name="TSiAddCronScript" position="center,77" size="920,600" title="Select CronScript to add... " >\n                          <widget name="config" position="20,20" size="880,450" scrollbarMode="showOnDemand" />\t\n                          <eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\t        \t\n\t                  <ePixmap name="cancel"    position="70,545"   zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" transparent="1" alphatest="blend" />\n\t                  <ePixmap name="ok"  position="280,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_green.png" transparent="1" alphatest="blend" />\n        \t          <widget name="canceltext" position="70,550" size="140,40" valign="center" halign="center" zPosition="2"  font="Regular;21" transparent="1" /> \n        \t          <widget name="oktext" position="280,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" /> \n                          <widget name="info" position="20,510" zPosition="4" size="780,45" font="Regular;20" foregroundColor="yellow" transparent="1" halign="center" valign="center" />                  \n        \t</screen>\n\t\t'
    skin_1920 = '    <screen name="TSiAddCronScript" position="center,200" size="1300,720" title="Addons Manager Setup">\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png" position="375,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green-big.png" position="725,640" size="200,40" alphatest="blend" />\n        <widget name="canceltext" position="375,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#940d0d" transparent="1" />\n        <widget name="oktext" position="725,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#2d872d" transparent="1" />\n        <widget name="config" position="20,30" size="1260,600" zPosition="2" itemHeight="40" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background"  transparent="1" />\n        <widget name="info" position="20,530" size="1260,40" foregroundColor="foreground" backgroundColor="background" font="Regular;28" valign="center" halign="center" transparent="1" zPosition="1" />\n        </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session, mode):
        self.session = session
        Screen.__init__(self, session)
        self.list = []
        ConfigListScreen.__init__(self, self.list, session=self.session)
        self.onShown.append(self.setWindowTitle)
        self.path = '/etc/cron/scripts/'
        self['cancel'] = Pixmap()
        self['ok'] = Pixmap()
        self['canceltext'] = Label(_('Cancel'))
        self['oktext'] = Label(_('OK'))
        self['info'] = Label('')
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'red': (self.keyCancel), 'green': (self.keyAdd), 
           'ok': (self.keyAdd), 
           'cancel': (self.keyCancel)}, -2)
        self.initScripList()
        self.mode_list = ConfigSelection([('timecron', _('Time')), ('delaycron', _('Delay'))], default='timecron')
        defchoice_script, dummy = self.script_choices[0]
        self.script_list = ConfigSelection(self.script_choices, default=defchoice_script)
        self.simple_time = ConfigClock(default=81000)
        self.delay_time = ConfigClock(default=-1800)
        dayname, month, day, time, zone, year = self.getCurrentDate()
        self.simple_day = ConfigSelection(default=day, choices=[26, 
         27, 
         28, 
         29, 
         30, 
         31, 
         32, 
         33, 
         34, 
         35, 
         36, 
         37, 
         38, 
         39, 
         40, 
         41, 
         42, 
         43, 
         44, 
         45, 
         46, 
         47, 
         48, 
         49, 
         50, 
         51, 
         52, 
         53, 
         54, 
         55, 
         56])
        self.delay_mins = ConfigSelection(default='5', choices=[26, 
         27, 
         28, 
         29, 
         30, 
         31, 
         32, 
         33, 
         34, 
         35, 
         36, 
         37, 
         38, 
         39, 
         40, 
         41, 
         42, 
         43, 
         44, 
         45, 
         46, 
         47, 
         48, 
         49, 
         50, 
         51, 
         52, 
         53, 
         54, 
         55, 
         56, 
         57, 
         58, 
         59, 
         60, 
         61, 
         62, 
         63, 
         64, 
         65, 
         66, 
         67, 
         68, 
         69, 
         70, 
         71, 
         72, 
         73, 
         74, 
         75, 
         76, 
         77, 
         78, 
         79, 
         80, 
         81, 
         82, 
         83, 
         84])
        self.delay_hours = ConfigSelection(default='1', choices=[26, 
         27, 
         28, 
         29, 
         30, 
         31, 
         32, 
         33, 
         34, 
         35, 
         36, 
         37, 
         38, 
         39, 
         40, 
         41, 
         42, 
         43, 
         44, 
         45, 
         46, 
         47, 
         48])
        self.simple_weekday = ConfigSelection(default=_('Mon'), choices=[_('Mon'),
         _('Tue'),
         _('Wed'),
         _('Thu'),
         _('Fri'),
         _('Sat'),
         _('Sun')])
        self.simple_month = ConfigSelection(default=month, choices=[_('Jan'),
         _('Feb'),
         _('Mar'),
         _('Apr'),
         _('May'),
         _('Jun'),
         _('Jul'),
         _('Aug'),
         _('Sep'),
         _('Oct'),
         _('Nov'),
         _('Dec')])
        self.repeat_time = ConfigSelection([('once', _('once')),
         (
          'daily', _('daily')),
         (
          'weekly', _('weekly')),
         (
          'monthly', _('monthly'))], default='once')
        self.repeat_delay = ConfigSelection([('once', _('once')), ('everymin', _('every n minutes')), ('everyhour', _('every n hours'))], default='once')
        if mode[0] == 'edit':
            sp = self.getCurrentCrontabInfo(mode[1])
        self.createSetup()
        return

    def getCurrentCrontabInfo(self, cur):
        sp = []
        fm = open(crontab_path)
        line = '  '
        count = -1
        found = False
        current = cur
        while line and not found:
            line = fm.readline()
            count = count + 1
            if line == current:
                sp = line.split(' ')
                found = True

        print 'count = ' + str(count)
        print 'current = ' + str(current)
        fm.close()
        return sp

    def setWindowTitle(self):
        title = _('Timer entry')
        title = title.replace(_('Timer'), 'Crontab')
        self.setTitle(title)
        return

    def getCurrentDate(self):
        sp = []
        line = getCmdOutput('date')
        found = False
        while line.find('  ') is not -1:
            line = line.replace('  ', ' ')

        sp = line.split(' ')
        dayname = sp[0]
        month = sp[1]
        day = sp[2]
        time = sp[3]
        zone = sp[4]
        year = sp[5]
        return (dayname,
         month,
         day,
         time,
         zone,
         year)

    def getTimestamp(self, date, mytime):
        d = localtime(date)
        dt = datetime(d.tm_year, d.tm_mon, d.tm_mday, mytime[0], mytime[1])
        return int(mktime(dt.timetuple()))

    def parseTime(self, time_value):
        hh = time_value[0]
        mn = time_value[1]
        return (hh, mn)

    def weekday2Nr(self, day):
        day_nr = '-1'
        if day == _('Sun'):
            day_nr = '0'
        elif day == _('Mon'):
            day_nr = '1'
        elif day == _('Tue'):
            day_nr = '2'
        elif day == _('Wed'):
            day_nr = '3'
        elif day == _('Thu'):
            day_nr = '4'
        elif day == _('Fri'):
            day_nr = '5'
        elif day == _('Sat'):
            day_nr = '6'
        return day_nr

    def month2Nr(self, month):
        month_nr = '-1'
        if month == _('Jan'):
            month_nr = '01'
        elif month == _('Feb'):
            month_nr = '02'
        elif month == _('Mar'):
            month_nr = '03'
        elif month == _('Apr'):
            month_nr = '04'
        elif month == _('May'):
            month_nr = '05'
        elif month == _('Jun'):
            month_nr = '05'
        elif month == _('Jul'):
            month_nr = '07'
        elif month == _('Aug'):
            month_nr = '08'
        elif month == _('Sep'):
            month_nr = '09'
        elif month == _('Oct'):
            month_nr = '10'
        elif month == _('Nov'):
            month_nr = '11'
        elif month == _('Dec'):
            month_nr = '12'
        return month_nr

    def initScripList(self):
        self.script_choices = []
        try:
            for x in os_listdir(self.path):
                x = x.replace('.sh', '')
                if x == 'cam' or x == 'script':
                    pass
                else:
                    self.script_choices.append((str(x), str(x)))

            self.script_choices.sort()
        except:
            pass

        return

    def createSetup(self):
        self.config_list = []
        self.mn = '-1'
        self.hh = '-1'
        self.day = '-1'
        self.month = '-1'
        self.weekday = '-1'
        self.script = '-1'
        syntaxtext = ''
        self.config_list.append(getConfigListEntry(_('Script for adding to crontab'), self.script_list))
        self.script = self.script_list.value
        self.config_list.append(getConfigListEntry(_('Cron setup Mode'), self.mode_list))
        if self.mode_list.value == 'timecron':
            self.config_list.append(getConfigListEntry(_('Repeat Type'), self.repeat_time))
            if self.repeat_time.value == 'once':
                self.config_list.append(getConfigListEntry(_('day'), self.simple_day))
                self.day = self.simple_day.value
                self.config_list.append(getConfigListEntry(_('month'), self.simple_month))
                self.month = self.month2Nr(self.simple_month.value)
            elif self.repeat_time.value == 'weekly':
                self.config_list.append(getConfigListEntry(_('Weekday'), self.simple_weekday))
                self.weekday = self.weekday2Nr(self.simple_weekday.value)
            elif self.repeat_time.value == 'monthly':
                self.config_list.append(getConfigListEntry(_('day'), self.simple_day))
                self.day = self.simple_day.value
            self.config_list.append(getConfigListEntry(_('StartTime'), self.simple_time))
            self.hh, self.mn = self.parseTime(self.simple_time.value)
            if int(self.hh) < 10:
                self.hh = '0' + str(self.hh)
            if int(self.mn) < 10:
                self.mn = '0' + str(self.mn)
            syntaxtext = ''
        elif self.mode_list.value == 'delaycron':
            self.config_list.append(getConfigListEntry(_('Repeat Type'), self.repeat_delay))
            if self.repeat_delay.value == 'once':
                self.config_list.append(getConfigListEntry(_('Delay'), self.delay_time))
                self.hh, self.mn = self.parseTime(self.delay_time.value)
                if int(self.hh) == 0:
                    self.hh = '-1'
                elif int(self.hh) < 10:
                    self.hh = '0' + str(self.hh)
                if int(self.mn) == 0:
                    self.mn = '-1'
                elif int(self.mn) < 10:
                    self.mn = '0' + str(self.mn)
            elif self.repeat_delay.value == 'everymin':
                self.config_list.append(getConfigListEntry(_('Step [min]'), self.delay_mins))
                self.mn = self.delay_mins.value
                if int(self.mn) < 10:
                    self.mn = '0' + str(self.mn)
                self.mn = '*/' + self.mn
            elif self.repeat_delay.value == 'everyhour':
                self.config_list.append(getConfigListEntry(_('Step [h]'), self.delay_hours))
                self.hh = self.delay_hours.value
                if int(self.hh) < 10:
                    self.hh = '0' + str(self.hh)
                self.hh = '*/' + self.hh
            crontab_syntax = str(self.mn) + ' ' + str(self.hh) + ' ' + str(self.day) + ' ' + str(self.month) + ' ' + str(self.weekday) + ' ' + str(self.script)
            syntaxtext = ''
        self['config'].setList(self.config_list)
        self['info'].setText(syntaxtext)
        return

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.createSetup()
        return

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.createSetup()
        return

    def keyAdd(self):
        answer = True
        if self.mode_list.value == 'delaycron' and self.repeat_delay.value == 'once':
            self.hh, self.mn = self.parseTime(self.delay_time.value)
            if int(self.hh) == 0:
                self.hh = '-1'
            elif int(self.hh) < 10:
                self.hh = '0' + str(self.hh)
            if int(self.mn) == 0:
                self.mn = '-1'
            elif int(self.mn) < 10:
                self.mn = '0' + str(self.mn)
            self.addcron_syntax = self.path + str(self.script) + '.sh' + ' ' + str(self.mn) + ' ' + str(self.hh) + ' ' + str(self.day) + ' ' + str(self.month) + ' ' + str(self.weekday)
            cmd = cronmanager_script + ' delay ' + self.addcron_syntax
            print 'cmd_delay= ' + cmd
            os_system(cmd)
        elif self.mode_list.value == 'timecron':
            self.hh, self.mn = self.parseTime(self.simple_time.value)
            if int(self.hh) < 10:
                self.hh = '0' + str(self.hh)
            if int(self.mn) < 10:
                self.mn = '0' + str(self.mn)
        self.addcron_syntax = self.path + str(self.script) + '.sh' + ' ' + str(self.mn) + ' ' + str(self.hh) + ' ' + str(self.day) + ' ' + str(self.month) + ' ' + str(self.weekday)
        cmd = cronmanager_script + ' add ' + self.addcron_syntax
        print 'cmd= ' + cmd
        os_system(cmd)
        self.close(answer)
        return

    def keyCancel(self):
        answer = None
        self.close(answer)
        return


return
