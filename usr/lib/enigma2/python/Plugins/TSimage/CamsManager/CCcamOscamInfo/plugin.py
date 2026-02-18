# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/CamsManager/CCcamOscamInfo/plugin.py
# Compiled at: 2016-11-22 07:50:02
from __init__ import _
from enigma import *
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.Console import Console
from Components.ActionMap import ActionMap, NumberActionMap
from Components.ScrollLabel import ScrollLabel
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaBlend
from Components.Sources.StaticText import StaticText
from Plugins.Plugin import PluginDescriptor
from Tools.Directories import fileExists
from Tools.BoundFunction import boundFunction
from Components.ConfigList import ConfigListScreen
from Components.config import config
from Components.config import ConfigText
from Components.config import ConfigInteger
from Components.config import ConfigPassword
from Components.config import getConfigListEntry
from Components.config import ConfigSelection
import os
from shared.readConfig import read_Config
from shared.readWeb import read_Web
from shared.readConfigFiles import read_Config_Files
from shared.saveConfig import save_Config
from shared.saveConfig import del_Config
from shared.saveConfig import backup_Config
from cccam.parser import read_Start
from cccam.parser import read_Home
from cccam.parser import read_Clients
from cccam.parser import read_ServersGeneral
from cccam.parser import read_ServersDetail
from cccam.parser import read_Locals
from cccam.parser import read_myLocals
from cccam.parser import read_Providers
from cccam.parser import read_Shares
from cccam.parser import read_Entitlements
from cccam.ping import ping_Servers
from cccam.ping import read_Ping
from cccam.ping import ping_oneServers
from cccam.pairs import read_Mapping
from cccam.cccam_cfg import readClineFline
from cccam.cccam_cfg import writeCCcam_cfg
from cccam.cccam_cfg import changesCCcam_cfg
from cccam.cccam_cfg import backupConfig
from cccam.cccam_cfg import delConfigFile
from cccam.cccam_cfg import restoreConfigFile
from oscam.parser import read_start_oscam
from oscam.parser import parse_xml_summary
from oscam.parser import restart_shutdown_oscam
from oscam.oscam_clients import oscamClients
from oscam.oscam_clients import oscamAllClients
from oscam.oscam_readers import oscamAllReaders
from oscam.oscam_readers import oscamEnableDisable
python_ver = '2.7'
if os.path.isdir('/usr/lib/python2.6') == True:
    python_ver = '2.6'
if os.path.isdir('/usr/lib/python%s/site-packages/paramiko' % python_ver) == True:
    from ssh.get_file_ssh import ssh_list_tmp
    from ssh.get_file_ssh import ssh_grab_ecminfo
version = '0.3c'
path = '/usr/lib/enigma2/python/Plugins/TSimage/CamsManager/CCcamOscamInfo'
idx_config = 0
config = []
size_h_screen = 0
offset = 20
font_size = 18
if int(getDesktop(0).size().width()) > 720:
    used_skin = 'hd'
    scale_x = 1.5
    scale_y = 1
else:
    used_skin = 'sd'
    scale_x = 1
    scale_y = 1

def main(session, **kwargs):
    data = []
    ret, res = read_Config('/etc/enigma2/cccamoscaminfo.xml')
    if ret == 0:
        ret, res, oscamconfigpath, cccamconfigpath = read_Config_Files()
        if ret == 0:
            data = [
             'lock_error;' + _("CCcam isn't running"),
             'lock_error;' + _('Path') + ': -',
             'lock_error;' + _("Oscam isn't running"),
             'lock_error;' + _('Path') + ': -',
             'nopic;--> ' + _('Sorry! You have to make the Config with the Setup Menue')]
        else:
            if ret == 1:
                data = [
                 'lock_error;' + _("CCcam isn't running"),
                 'lock_error;' + _('Path') + ': -',
                 'lock_on;' + _('Oscam is running'),
                 'lock_on;' + _('Path') + ': %s' % oscamconfigpath,
                 'nopic;--> ' + _('Created the config file /etc/enigma2/cccamoscaminfo.xml')]
            elif ret == 2:
                data = [
                 'lock_on;' + _('CCcam is running'),
                 'lock_on;' + _('Path') + ': %s' % cccamconfigpath,
                 'lock_error;' + _("Oscam isn't running"),
                 'lock_error;' + _('Path') + ': -',
                 'nopic;--> ' + _('Created the config file /etc/enigma2/cccamoscaminfo.xml')]
            elif ret == 3:
                data = [
                 'lock_on;' + _('CCcam is running'),
                 'lock_on;' + _('Path') + ': %s' % cccamconfigpath,
                 'lock_on;' + _('Oscam is running'),
                 'lock_on;' + _('Path') + ': %s' % oscamconfigpath,
                 'nopic;--> ' + _('Created the config file /etc/enigma2/cccamoscaminfo.xml')]
            ret = save_Config(res)
            if ret == 0:
                data = [
                 'lock_error;' + _("Couldn't write the file  /etc/enigma2/config.xlm"), 'nopic;--> ' + _('Sorry! You have to make the Config with the Setup Menue')]
        ret, res = read_Config('/etc/enigma2/cccamoscaminfo.xml')
        config = res
        session.openWithCallback(check_default_cam(session, config), CCcamOScamTextList, data, '')
    else:
        config = res
        check_default_cam(session, config)
    return


def check_default_cam(session, config):
    idx_config = 0
    check = 0
    if len(config) > 0:
        count = 0
        for x in config:
            if int(x['default']) == 1:
                idx_config = count
                check = 1
            else:
                count += 1

        data = []
        if check == 0:
            for x in config:
                data.append('%s;%s;%s;%s:%s' % (x['default'],
                 x['cam'],
                 x['name'],
                 x['url'],
                 x['port']))

            if int(config[0]['default']) == 9:
                session.open(CCcamOScamSelectCam, config, idx_config, data, 'config')
            else:
                session.open(CCcamOScamSelectCam, config, idx_config, data, 'check_default_cam')
        else:
            open_start_screen(session, config, idx_config)
    else:
        open_start_screen(session, config, idx_config)
    return


def open_start_screen(session, config, idx_config):
    session.open(CCcamOScamStart, config, idx_config)
    return


class CCcamOScamSelectCam(Screen):
    raw_skin = '\n        <screen position="center,{size.pos_h}" size="{size.screen}" title="{title.screen}">\n            <widget name="header" position="{pos.header}" size="{size.header}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label1}" size="{size.label1}" font="Regular;14" backgroundColor="#ffffff" />\n            <widget name="list" position="{pos.list}" size="{size.list}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label2}" size="{size.label2}" font="Regular;14" backgroundColor="#ffffff" />\n            <ePixmap name="ButtonRed" pixmap="%s/pictures/button_red_%s.png" position="{pos.but_red}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonRedText" position="{pos.but_red}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonGreen" pixmap="%s/pictures/button_green_%s.png" position="{pos.but_green}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonGreenText" position="{pos.but_green}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonYellow" pixmap="%s/pictures/button_yellow_%s.png" position="{pos.but_yellow}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonYellowText" position="{pos.but_yellow}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonBlue" pixmap="%s/pictures/button_blue_%s.png" position="{pos.but_blue}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonBlueText" position="{pos.but_blue}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n        </screen>' % (path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)))

    def __init__(self, session, config, idx_config, data, window):
        if len(data) > 18:
            y_scale = 18 * font_size
            if y_scale < 54 * font_size:
                y_scale = 54 * font_size
        else:
            y_scale = 25 * len(data)
            if y_scale < 75:
                y_scale = 75
        size_h_screen = y_Pos_Screen(y_scale + 120)
        self.dict_text = {'size.pos_h': ('%.0f' % float(int(size_h_screen))), 'title.screen': ('CCcamOscamInfos Select-Cam Ver. %s' % version)}
        self.dict_var = {'size.screen': ('610,%s' % (y_scale + 120)), 'pos.header': '10,10', 
           'size.header': '590,25', 
           'pos.label1': '10,50', 
           'size.label1': '590,2', 
           'pos.list': '10,50', 
           'size.list': ('590,%s' % y_scale), 
           'pos.label2': ('10,%s' % (y_scale + 70)), 
           'size.label2': '590,2', 
           'size.but': '140,50', 
           'pos.but_red': ('10,%s' % (y_scale + 80)), 
           'pos.but_green': ('160,%s' % (y_scale + 80)), 
           'pos.but_yellow': ('310,%s' % (y_scale + 80)), 
           'pos.but_blue': ('460,%s' % (y_scale + 80))}
        self.skin = SkinVars(CCcamOScamSelectCam.raw_skin, self.dict_text, self.dict_var)
        self.session = session
        self.config = config
        self.idx_config = idx_config
        self.data = data
        self.window = window
        Screen.__init__(self, session)
        self['header'] = Menu([])
        self['list'] = Menu([])
        if self.window == 'check_default_cam' or self.window == 'change_cam':
            self['ButtonBlueText'] = StaticText(_('Reset default Cam'))
            self['ButtonGreenText'] = StaticText(_('Ok'))
            self['ButtonYellowText'] = StaticText(_('Set as default'))
            self['ButtonRedText'] = StaticText(_('Exit'))
        elif self.window == 'config':
            self['ButtonBlueText'] = StaticText(_('New'))
            self['ButtonGreenText'] = StaticText()
            self['ButtonYellowText'] = StaticText()
            self['ButtonRedText'] = StaticText(_('Ok'))
        else:
            self['ButtonBlueText'] = StaticText('')
            self['ButtonGreenText'] = StaticText('')
            self['ButtonYellowText'] = StaticText('')
            self['ButtonRedText'] = StaticText(_('Exit'))
        self['actions'] = ActionMap(['CCcamOscamInfoActions'], {'ok': (self.key_ok), 'cancel': (self.close), 
           'red': (self.red), 
           'green': (self.green), 
           'blue': (self.blue), 
           'yellow': (self.yellow), 
           'down': (self.down), 
           'up': (self.up)}, -1)
        self.onLayoutFinish.append(self.makeList)
        return

    def setButtonText(self):
        self['ButtonGreenText'].setText(self.text_button_green)
        self['ButtonYellowText'].setText(self.text_button_yellow)
        return

    def makeList(self):
        ret, res = read_Config('/etc/enigma2/cccamoscaminfo.xml')
        if ret == 1:
            self.config = res
        else:
            self.config = []
        list = []
        list.append(makeListCCcamOScamSelectCam('nopic', _('Cam') + ':', _('Name') + ':', _('IP') + ':'))
        self['header'].setList(list)
        self['header'].selectionEnabled(0)
        list = []
        for x in self.data:
            tmpList = x.split(';')
            list.append(makeListCCcamOScamSelectCam(tmpList[0], tmpList[1], tmpList[2], tmpList[3]))

        self['list'].setList(list)
        self['list'].selectionEnabled(1)
        self.currList = 'list'
        if self.window == 'config':
            if self.config > 0:
                self.text_button_yellow = _('Delete')
                self.text_button_green = _('Edit')
            else:
                self.text_button_yellow = ''
                self.text_button_green = ''
            self.setButtonText()
        return

    def key_ok(self):
        if self.window == 'check_default_cam' or self.window == 'change_cam':
            self.green()
        elif self.window == 'config':
            self.blue()
        return

    def blue(self):
        if self.window == 'check_default_cam' or self.window == 'change_cam':
            list = []
            count = 0
            for x in self.config:
                self.config[count].update({'default': '0'})
                count = count + 1

            del_Config()
            save_Config(self.config)
            ret, self.config = read_Config('/etc/enigma2/cccamoscaminfo.xml')
            for x in self.config:
                list.append(makeListCCcamOScamSelectCam(x['default'], x['cam'], x['name'], '%s:%s' % (x['url'], x['port'])))

            self['list'].setList(list)
        elif self.window == 'config':
            self.session.openWithCallback(self.update, CCcamOscamInfoConfigScreen, self.config, 0, 'new')
        return

    def green(self):
        if self.window == 'check_default_cam':
            self.idx_config = self['list'].getSelectedIndex()
            config = self.config
            open_start_screen(self.session, self.config, self.idx_config)
        elif self.window == 'change_cam':
            self.session.openWithCallback(self.close, CCcamOScamStart, self.config, self['list'].getSelectedIndex())
        elif self.window == 'config':
            if len(self.config) > 0:
                self.session.openWithCallback(self.update, CCcamOscamInfoConfigScreen, self.config, self['list'].getSelectedIndex(), 'edit')
        return

    def yellow(self):
        if self.window == 'check_default_cam' or self.window == 'change_cam':
            list = []
            count = 0
            self.idx_config = self['list'].getSelectedIndex()
            for x in self.config:
                if count == self.idx_config:
                    self.config[self.idx_config].update({'default': '1'})
                else:
                    self.config[count].update({'default': '0'})
                count = count + 1

            del_Config()
            save_Config(self.config)
            ret, self.config = read_Config('/etc/enigma2/cccamoscaminfo.xml')
            for x in self.config:
                list.append(makeListCCcamOScamSelectCam(x['default'], x['cam'], x['name'], '%s:%s' % (x['url'], x['port'])))

            self['list'].setList(list)
        elif self.window == 'config':
            if len(self.config) > 0:
                list = []
                del self.config[self['list'].getSelectedIndex()]
                del_Config()
                save_Config(self.config)
                ret, self.config = read_Config('/etc/enigma2/cccamoscaminfo.xml')
                for x in self.config:
                    list.append(makeListCCcamOScamSelectCam(x['default'], x['cam'], x['name'], '%s:%s' % (x['url'], x['port'])))

                self['list'].setList(list)
                if len(self.config) > 0:
                    self.text_button_yellow = _('Delete')
                    self.text_button_green = _('Edit')
                else:
                    self.text_button_yellow = ''
                    self.text_button_green = ''
                self.setButtonText()
        return

    def red(self):
        if self.window == 'check_default_cam' or self.window == 'change_cam':
            self.close()
        elif self.window == 'config':
            if len(self.config) > 0:
                self.session.openWithCallback(self.close, CCcamOScamStart, self.config, self['list'].getSelectedIndex())
            else:
                self.session.open(CCcamOscamInfoConfigScreen, self.config, 0, 'new')
        return

    def up(self):
        self[self.currList].up()
        return

    def down(self):
        self[self.currList].down()
        return

    def update(self):
        self.makeList()
        return


class CCcamOScamTextList(Screen):
    raw_skin = '\n        <screen position="center,{size.pos_h}" size="{size.screen}" title="{title.screen}">\n            <widget name="list" position="{pos.list}" size="{size.list}" itemHeight="25" scrollbarMode="showOnDemand" />\n        </screen>'

    def __init__(self, session, data, title):
        size_h_screen = y_Pos_Screen(25 * len(data) + 10)
        self.dict_text = {'size.pos_h': ('%.0f' % float(int(size_h_screen))), 'title.screen': ('CCcamOscamInfos %s Ver. %s' % (title, version))}
        self.dict_var = {'size.screen': ('655,%s' % (25 * len(data) + 10)), 'pos.list': '10,10', 
           'size.list': ('635,%s' % (25 * len(data)))}
        self.skin = SkinVars(CCcamOScamTextList.raw_skin, self.dict_text, self.dict_var)
        self.session = session
        self.data = data
        Screen.__init__(self, session)
        self['list'] = Menu([])
        self['actions'] = ActionMap(['CCcamOscamInfoActions'], {'ok': (self.close), 'cancel': (self.close)}, -1)
        self.onLayoutFinish.append(self.makeList)
        return

    def makeList(self):
        list = []
        for x in self.data:
            tmpList = x.split(';')
            list.append(makeListCCcamOscamTextList(tmpList[0], tmpList[1]))

        self['list'].setList(list)
        self['list'].selectionEnabled(0)
        return


class CCcamOScamStart(Screen):
    raw_skin = '\n        <screen position="center,{size.pos_h}" size="{size.screen}" title="{title.screen}">\n            <widget name="header" position="{pos.header}" size="{size.header}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label1}" size="{size.label1}" font="Regular;14" backgroundColor="#ffffff" />\n            <widget name="list" position="{pos.list}" size="{size.list}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label2}" size="{size.label2}" font="Regular;14" backgroundColor="#ffffff" />\n            <widget name="footer" position="{pos.footer}" size="{size.footer}" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label3}" size="{size.label3}" font="Regular;14" backgroundColor="#ffffff" />\n            <ePixmap name="ButtonRed" pixmap="%s/pictures/button_red_%s.png" position="{pos.but_red}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonRedText" position="{pos.but_red}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonGreen" pixmap="%s/pictures/button_green_%s.png" position="{pos.but_green}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonGreenText" position="{pos.but_green}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonYellow" pixmap="%s/pictures/button_yellow_%s.png" position="{pos.but_yellow}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonYellowText" position="{pos.but_yellow}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonBlue" pixmap="%s/pictures/button_blue_%s.png" position="{pos.but_blue}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonBlueText" position="{pos.but_blue}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n        </screen>' % (path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)))

    def __init__(self, session, config, idx_config):
        if (config[idx_config]['cam'] == 'CCcamLocal' or config[idx_config]['cam'] == 'CCcamRemote') and len(config) > 0:
            y_scale = 275
        elif config[idx_config]['cam'] == 'Oscam' and len(config) > 0:
            y_scale = 200
        else:
            y_scale = 25
        size_h_screen = y_Pos_Screen(y_scale + 160)
        self.dict_text = {'size.pos_h': ('%.0f' % float(int(size_h_screen))), 'title.screen': ('CCcamOscamInfos Ver. %s' % version)}
        self.dict_var = {'size.screen': ('610,%s' % (y_scale + 160)), 'pos.header': '10,10', 
           'size.header': '590,25', 
           'pos.label1': '10,50', 
           'size.label1': '590,2', 
           'pos.list': '10,50', 
           'size.list': ('590,%s' % y_scale), 
           'pos.label2': ('10,%s' % (y_scale + 50)), 
           'size.label2': '590,2', 
           'pos.footer': ('10,%s' % (y_scale + 60)), 
           'size.footer': '590,50', 
           'pos.label3': ('10,%s' % (y_scale + 110)), 
           'size.label3': '590,2', 
           'size.but': '140,50', 
           'pos.but_red': ('10,%s' % (y_scale + 120)), 
           'pos.but_green': ('160,%s' % (y_scale + 120)), 
           'pos.but_yellow': ('310,%s' % (y_scale + 120)), 
           'pos.but_blue': ('460,%s' % (y_scale + 120))}
        self.skin = SkinVars(CCcamOScamStart.raw_skin, self.dict_text, self.dict_var)
        self['header'] = Menu([])
        self['list'] = Menu([])
        self['footer'] = FooterListStart([])
        self.session = session
        self.config = config
        self.idx_config = idx_config
        self.timer = eTimer()
        self.timer_conn = self.timer.timeout.connect(self.createFooter)
        self.createFooter()
        self.timer.start(10000)
        Screen.__init__(self, session)
        if self.config[self.idx_config]['cam'] == 'CCcamLocal' or self.config[self.idx_config]['cam'] == 'CCcamRemote':
            menulist = []
            menulist.append(('Home', _('Home')))
            menulist.append(('Clients', _('Clients')))
            menulist.append(('ServersAllgemein', _('Servers general')))
            menulist.append(('ServersDetail', _('Servers details')))
            menulist.append(('Providers', _('Providers')))
            menulist.append(('Shares', _('Shares')))
            menulist.append(('Pairs', _('Pairs')))
            menulist.append(('PingServers', _('Ping servers')))
            menulist.append(('Entitlements', _('Entitlements')))
            if self.config[self.idx_config]['cam'] == 'CCcamLocal' or self.config[self.idx_config]['partnerbox'] == 'yes' and os.path.isdir('/usr/lib/python%s/site-packages/paramiko' % python_ver) == True:
                menulist.append(('ECMInfo', _('ECM info')))
            if self.config[self.idx_config]['cam'] == 'CCcamLocal' and self.config[self.idx_config]['changeconfig'] == 'yes':
                menulist.append(('EnableDisableClineFline', _('Enable/disable C-line/F-line')))
        elif self.config[self.idx_config]['cam'] == 'Oscam':
            menulist = []
            menulist.append(('Gereral', _('Gereral')))
            menulist.append(('Clients', _('Clients')))
            menulist.append(('AllClients', _('All Clients')))
            menulist.append(('Readers', _('Readers')))
            menulist.append(('Proxys', _('Proxys')))
            menulist.append(('AllReadersProxys', _('All readers/proxys')))
            menulist.append(('EnableDisableClientsReadersProxys', _('Enable/disable clients/readers/proxys')))
            menulist.append(('RestatServer', _('Restat server')))
        else:
            menulist = []
            menulist.append(('Error', _('Error')))
        self.menulist = menulist
        self['ButtonBlueText'] = StaticText(_('Config'))
        self['ButtonGreenText'] = StaticText(_('Ok'))
        self['ButtonYellowText'] = StaticText(_('Change Cam'))
        self['ButtonRedText'] = StaticText(_('Exit'))
        self['actions'] = ActionMap(['CCcamOscamInfoActions'], {'ok': (self.green), 'cancel': (self.exit), 
           'red': (self.red), 
           'green': (self.green), 
           'blue': (self.blue), 
           'yellow': (self.yellow), 
           'down': (self.down), 
           'up': (self.up), 
           'left': (self.left), 
           'right': (self.right), 
           'ch_up': (self.left), 
           'ch_down': (self.right)}, -1)
        self.onLayoutFinish.append(self.makeList)
        return

    def createFooter(self):
        self.footerlist = [_('Version') + ': NA',
         _('Uptime') + ': NA',
         _('Users') + ': NA',
         _('Servers') + ': NA']
        if self.config[self.idx_config]['cam'] == 'CCcamLocal' or self.config[self.idx_config]['cam'] == 'CCcamRemote':
            ret, res = read_Web(self.config, self.idx_config, '')
            self.footerlist = read_Start(ret, res)
        elif self.config[self.idx_config]['cam'] == 'Oscam':
            res2 = []
            ret, res1 = read_Web(self.config, self.idx_config, 'oscamapi.html?part=status')
            if ret == 1:
                ret, res2 = read_Web(self.config, self.idx_config, '')
            self.footerlist = read_start_oscam(ret, res1, res2)
        list = []
        if self.config[self.idx_config]['cam'] == 'Oscam':
            list.append(makeListFooterStart(_('Version ') + ':%s' % self.footerlist['Version'], _('Uptime') + ' :%s' % self.footerlist['Uptime'], _('Readers') + ' :%s' % self.footerlist['Readers'], _('Clients') + ' :%s' % self.footerlist['Clients'], self.config[self.idx_config]['cam']))
        else:
            list.append(makeListFooterStart(self.footerlist[0], self.footerlist[1], self.footerlist[2], self.footerlist[3], self.config[self.idx_config]['cam']))
        self['footer'].setList(list)
        return

    def makeList(self):
        list = []
        list.append(makeListCCcamOScamStart((_('Cam') + ': %s ' + _('Name') + ': %s ' + _('IP') + ': %s:%s') % (self.config[self.idx_config]['cam'],
         self.config[self.idx_config]['name'],
         self.config[self.idx_config]['url'],
         self.config[self.idx_config]['port'])))
        self['header'].setList(list)
        self['header'].selectionEnabled(0)
        list = []
        for x in self.menulist:
            list.append(makeListCCcamOScamStart(x[1]))

        self['list'].setList(list)
        self['list'].selectionEnabled(1)
        list = []
        if self.config[self.idx_config]['cam'] == 'Oscam':
            list.append(makeListFooterStart(_('Version') + ' :%s' % self.footerlist['Version'], _('Uptime') + ' :%s' % self.footerlist['Uptime'], _('Readers') + ' :%s' % self.footerlist['Readers'], _('Clients') + ' :%s' % self.footerlist['Clients'], self.config[self.idx_config]['cam']))
        else:
            list.append(makeListFooterStart(self.footerlist[0], self.footerlist[1], self.footerlist[2], self.footerlist[3], self.config[self.idx_config]['cam']))
        self['footer'].setList(list)
        self['footer'].selectionEnabled(0)
        self.currList = 'list'
        return

    def blue(self):
        self.data = []
        for x in self.config:
            self.data.append('%s;%s;%s;%s:%s' % (x['default'],
             x['cam'],
             x['name'],
             x['url'],
             x['port']))

        self.session.open(CCcamOScamSelectCam, self.config, self.idx_config, self.data, 'config')
        self.close()
        return

    def green(self):
        returnValue = self['list'].getCurrent()[0]
        if returnValue is not None:
            idx_menu = self['list'].getSelectedIndex()
            if self.config[self.idx_config]['cam'] == 'CCcamLocal' or self.config[self.idx_config]['cam'] == 'CCcamRemote':
                if self.menulist[idx_menu][0] is 'Home':
                    self.showHome()
                elif self.menulist[idx_menu][0] is 'Clients':
                    self.session.open(CCcamClientsScreen, self.idx_config, self.config)
                elif self.menulist[idx_menu][0] is 'ServersAllgemein':
                    self.session.open(CCcamServersAllgemeinScreen, self.idx_config, self.config)
                elif self.menulist[idx_menu][0] is 'ServersDetail':
                    self.session.open(CCcamServersDetailScreen, self.idx_config, self.config)
                elif self.menulist[idx_menu][0] is 'Providers':
                    self.session.open(CCcamProvidersScreen, self.idx_config, self.config)
                elif self.menulist[idx_menu][0] is 'Shares':
                    self.session.open(CCcamSharesScreen, self.idx_config, self.config)
                elif self.menulist[idx_menu][0] is 'PingServers':
                    self.session.open(CCcamPingServersScreen, self.idx_config, self.config)
                elif self.menulist[idx_menu][0] is 'Pairs':
                    self.session.open(CCcamPairsScreen, self.idx_config, self.config)
                elif self.menulist[idx_menu][0] is 'Entitlements':
                    self.session.open(CCcamEntitlementsScreen, self.idx_config, self.config)
                elif self.menulist[idx_menu][0] is 'ECMInfo':
                    self.session.open(CCcamECMInfoScreen, self.idx_config, self.config)
                elif self.menulist[idx_menu][0] is 'EnableDisableClineFline':
                    self.EnableDisableClineFline()
            elif self.config[self.idx_config]['cam'] == 'Oscam':
                if self.menulist[idx_menu][0] is 'Gereral':
                    self.session.open(OscamGeneralScreen, self.idx_config, self.config)
                elif self.menulist[idx_menu][0] is 'Clients':
                    self.session.open(OscamClientServerScreen, self.idx_config, self.config, 'Clients')
                elif self.menulist[idx_menu][0] is 'AllClients':
                    self.session.open(OscamClientServerScreen, self.idx_config, self.config, 'AllClients')
                elif self.menulist[idx_menu][0] is 'Readers':
                    self.session.open(OscamClientServerScreen, self.idx_config, self.config, 'Readers')
                elif self.menulist[idx_menu][0] is 'Proxys':
                    self.session.open(OscamClientServerScreen, self.idx_config, self.config, 'Proxys')
                elif self.menulist[idx_menu][0] is 'AllReadersProxys':
                    self.session.open(OscamClientServerScreen, self.idx_config, self.config, 'AllReadersProxys')
                elif self.menulist[idx_menu][0] is 'EnableDisableClientsReadersProxys':
                    self.session.open(EnableDisableClientsReadersProxysScreen, self.idx_config, self.config)
                elif self.menulist[idx_menu][0] is 'RestatServer':
                    self.session.open(OscamRestatServer, self.idx_config, self.config)
        return

    def exit(self):
        self.timer.stop()
        self.close()
        return

    def red(self):
        self.timer.stop()
        self.close()
        return

    def yellow(self):
        self.data = []
        for x in self.config:
            self.data.append('%s;%s;%s;%s:%s' % (x['default'],
             x['cam'],
             x['name'],
             x['url'],
             x['port']))

        self.session.open(CCcamOScamSelectCam, self.config, self.idx_config, self.data, 'change_cam')
        self.close()
        return

    def up(self):
        self[self.currList].up()
        return

    def down(self):
        self[self.currList].down()
        return

    def left(self):
        self[self.currList].pageUp()
        return

    def right(self):
        self[self.currList].pageDown()
        return

    def showHome(self):
        self.session.open(CCcamOscamInfoTextScreen, 'showCCcamHome', 'CCcam Home', self.config, self.idx_config)
        return

    def EnableDisableClineFline(self):
        if self.config[self.idx_config]['path'] == None or self.config[self.idx_config]['path'] == 'None':
            text = _('Could not find the file CCcam.cfg') + '.\n' + _('Please check the settings.')
            self.session.open(MessageBox, text, MessageBox.TYPE_INFO, timeout=20)
        else:
            text = _('WARNING!') + '\n\n' + _('The Enable/Disable C/F-Line Funktion is BETA.') + '\n' + _('The author is not responsible for data lost.') + '\n' + _('Make first a copy from the File') + ' %s/CCcam.cfg' % self.config[self.idx_config]['path']
            self.session.openWithCallback(self.callAnswer, MessageBox, text, MessageBox.TYPE_YESNO)
        return

    def callAnswer(self, answer):
        if answer:
            self.session.open(EnableDisableClineFlineScreen, self.config[self.idx_config]['path'])
        else:
            self.close
        return


class CCcamOscamInfoTextScreen(Screen):
    raw_skin = '\n        <screen position="center,{size.pos_h}" size="{size.screen}" title="{title.screen}">\n            <widget name="text" position="{pos.text}" size="{size.text}" font="Regular;%s" />\n            <eLabel text="" position="{pos.label3}" size="{size.label3}" font="Regular;14" backgroundColor="#ffffff" />\n            <ePixmap name="ButtonRed" pixmap="%s/pictures/button_red_%s.png" position="{pos.but_red}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonRedText" position="{pos.but_red}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonGreen" pixmap="%s/pictures/button_green_%s.png" position="{pos.but_green}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonGreenText" position="{pos.but_green}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonYellow" pixmap="%s/pictures/button_yellow_%s.png" position="{pos.but_yellow}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonYellowText" position="{pos.but_yellow}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonBlue" pixmap="%s/pictures/button_blue_%s.png" position="{pos.but_blue}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonBlueText" position="{pos.but_blue}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n        </screen>' % (int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)))

    def __init__(self, session, text, title, config, idx_config):
        size_h_screen = y_Pos_Screen(480)
        self.dict_text = {'size.pos_h': ('%.0f' % float(int(size_h_screen))), 'title.screen': ('CCcamOscamInfo %s Ver. %s' % (title, version))}
        self.dict_var = {'size.screen': '655,480', 'pos.text': '10,10', 
           'size.text': '635,400', 
           'pos.label3': '10,430', 
           'size.label3': '635,2', 
           'size.but': '140,50', 
           'pos.but_red': '10,440', 
           'pos.but_green': '175,440', 
           'pos.but_yellow': '340,440', 
           'pos.but_blue': '505,440'}
        self.skin = SkinVars(CCcamOscamInfoTextScreen.raw_skin, self.dict_text, self.dict_var)
        self.session = session
        self.text = text
        self.myLabel = text
        self.config = config
        self.idx_config = idx_config
        self.timer_on = 0
        Screen.__init__(self, session)
        self['text'] = ScrollLabel()
        self.onShown.append(self.setText)
        if self.myLabel == 'showCCcamHome':
            self.timer_on = 1
            self.timer_text = eTimer()
            self.timer_text_conn = self.timer_text.timeout.connect(self.createText)
            self.createText()
            self.timer_text.start(5000)
        self['ButtonBlueText'] = StaticText('')
        self['ButtonGreenText'] = StaticText('')
        self['ButtonYellowText'] = StaticText('')
        self['ButtonRedText'] = StaticText(_('Back'))
        self['actions'] = ActionMap(['CCcamOscamInfoActions'], {'ok': (self.red), 'cancel': (self.close), 
           'red': (self.red), 
           'green': (self.green), 
           'blue': (self.blue), 
           'yellow': (self.yellow), 
           'down': (self.right), 
           'up': (self.left), 
           'left': (self.left), 
           'right': (self.right), 
           'ch_up': (self.left), 
           'ch_down': (self.right)}, -1)
        return

    def setText(self):
        self['text'].setText(self.text)
        return

    def createText(self):
        if self.myLabel == 'showCCcamHome':
            ret, res = read_Web(self.config, self.idx_config, '')
            self.text = read_Home(ret, res)
            self.setText()
        return

    def left(self):
        self['text'].pageUp()
        return

    def right(self):
        self['text'].pageDown()
        return

    def blue(self):
        return

    def green(self):
        return

    def red(self):
        if self.timer_on == 1:
            self.timer_text.stop()
        self.close()
        return

    def yellow(self):
        return


class CCcamClientsScreen(Screen):
    raw_skin = '\n        <screen position="center,{size.pos_h}" size="{size.screen}" title="{title.screen}">\n            <widget name="header" position="{pos.header}" size="{size.header}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label1}" size="{size.label1}" font="Regular;14" backgroundColor="#ffffff" />\n            <widget name="clients" position="{pos.clients}" size="{size.clients}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label2}" size="{size.label2}" font="Regular;14" backgroundColor="#ffffff" />\n            <widget name="footer" position="{pos.footer}" size="{size.footer}" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label3}" size="{size.label3}" font="Regular;14" backgroundColor="#ffffff" />\n            <ePixmap name="ButtonRed" pixmap="%s/pictures/button_red_%s.png" position="{pos.but_red}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget name="ButtonRedText" position="{pos.but_red}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonGreen" pixmap="%s/pictures/button_green_%s.png" position="{pos.but_green}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget name="ButtonGreenText" position="{pos.but_green}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonYellow" pixmap="%s/pictures/button_yellow_%s.png" position="{pos.but_yellow}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget name="ButtonYellowText" position="{pos.but_yellow}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonBlue" pixmap="%s/pictures/button_blue_%s.png" position="{pos.but_blue}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget name="ButtonBlueText" position="{pos.but_blue}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n        </screen>' % (path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)))

    def __init__(self, session, idx, config):
        size_h_screen = y_Pos_Screen(480)
        self.dict_text = {'size.pos_h': ('%.0f' % float(int(size_h_screen))), 'title.screen': ('CCcamOscamInfo CCcam Clients Ver. %s' % version)}
        self.dict_var = {'size.screen': '655,480', 'pos.header': '10,10', 
           'size.header': '635,25', 
           'pos.label1': '10,30', 
           'size.label1': '635,2', 
           'pos.clients': '10,50', 
           'size.clients': '635,295', 
           'pos.label2': '10,335', 
           'size.label2': '635,2', 
           'pos.footer': '10,340', 
           'size.footer': '635,100', 
           'pos.label3': '10,430', 
           'size.label3': '635,2', 
           'size.but': '140,50', 
           'pos.but_red': '10,440', 
           'pos.but_green': '175,440', 
           'pos.but_yellow': '340,440', 
           'pos.but_blue': '505,440'}
        self.skin = SkinVars(CCcamClientsScreen.raw_skin, self.dict_text, self.dict_var)
        self['header'] = Menu([])
        self['clients'] = Menu([])
        self['footer'] = FooterListClientsCCcam([])
        self.session = session
        self.idx = idx
        self.config = config
        Screen.__init__(self, session)
        self.timer_on = 0
        self.text_button_yellow = 'Enable update'
        self.timer_client = eTimer()
        self.timer_client_conn = self.timer_client.timeout.connect(self.makeList)
        self['ButtonBlueText'] = Label(_('Shareinfo'))
        self['ButtonGreenText'] = Label(_('Info'))
        self['ButtonYellowText'] = Label()
        self['ButtonRedText'] = Label(_('Back'))
        self['actions'] = ActionMap(['CCcamOscamInfoActions'], {'ok': (self.shareInfo), 'cancel': (self.red), 
           'red': (self.red), 
           'green': (self.Info), 
           'blue': (self.showInfo), 
           'yellow': (self.yellow), 
           'down': (self.down), 
           'up': (self.up), 
           'left': (self.left), 
           'right': (self.right), 
           'ch_up': (self.left), 
           'ch_down': (self.right)}, -1)
        self['clients'].onSelectionChanged.append(self.showInfo)
        self.onShown.append(self.setButton)
        self.onLayoutFinish.append(self.makeList)
        self.currList = 'clients'
        return

    def setButton(self):
        self['ButtonYellowText'].setText(self.text_button_yellow)
        return

    def makeList(self):
        self.data = []
        self.res_clients = []
        self.res_active = []
        ret, self.res_clients = read_Web(self.config, self.idx, 'clients')
        if ret == 1:
            ret, self.res_active = read_Web(self.config, self.idx, 'activeclients')
        self.data = read_Clients(ret, self.res_clients, self.res_active, self.config, self.idx)
        list = []
        for x in self.data[1]:
            tmpList = x.split(',')
            list.append(makeListClients(tmpList[0], tmpList[2], tmpList[9]))

        self['clients'].setList(list)
        self['clients'].selectionEnabled(1)
        list = []
        tmpList = self.data[0].split(',')
        list.append(makeListClientsHeader(tmpList[0], tmpList[9]))
        self['header'].setList(list)
        self['header'].selectionEnabled(0)
        return

    def showInfo(self):
        listdetail = []
        try:
            idx = self['clients'].getSelectedIndex()
            tmp = ''
            tmp = self.data[1][idx]
            tmpList = tmp.split(',')
            listdetail.append(makeListClientsFooter(tmpList[0], tmpList[3], tmpList[4], tmpList[5], tmpList[6], tmpList[7], tmpList[8], tmpList[9]))
            self['footer'].setList(listdetail)
            self['footer'].selectionEnabled(0)
        except:
            listdetail.append(makeListClientsFooter('', '', '', '', '', '', '', ''))

        self['footer'].setList(listdetail)
        self['footer'].selectionEnabled(0)
        return

    def shareInfo(self):
        text = ''
        if 1 == 1:
            idx = self['clients'].getSelectedIndex()
            for x in self.data[2]:
                if x.split(',')[0] == self.data[1][idx].split(',')[0]:
                    x = x.split(',')
                    text = _('Username') + ': %s\n\n' % x[0] + _('Shareinfo') + ':\n'
                    del x[0]
                    for y in x:
                        text = '%s\n%s' % (text, y)

        if text == '':
            try:
                text = _('No shareinfo avriable for the client') + ' %s' % self.data[1][idx].split(',')[0]
            except:
                pass

        self.session.open(CCcamOscamInfoTextScreen, text, 'CCcam Clients ShareInfo', 0, 0)
        return

    def Info(self):
        try:
            idx = self['clients'].getSelectedIndex()
            text = ''
            text = self.data[1][idx]
            if text != '':
                text = text.split(',')
                text = _('Username') + ': %s\n' % text[0] + _('Host') + ': %s\n' % text[3] + _('Connected') + ': %s\n' % text[4] + _('Idle time') + ': %s\nECM: %s\nEMM: %s\n' % (text[5], text[6], text[7]) + _('Version') + ': %s\n' % text[8] + _('Last used share') + ': %s' % text[9]
                self.session.open(CCcamOscamInfoTextScreen, text, 'CCcam Clients Info', 0, 0)
            else:
                text = 'Shit happens'
                self.session.open(MessageBox, text, MessageBox.TYPE_INFO, timeout=20)
        except:
            text = 'Clients\n\nFische sind Freunde, kein Futter.'
            self.session.open(MessageBox, text, MessageBox.TYPE_INFO, timeout=20)

        return

    def red(self):
        if self.timer_on == 1:
            self.timer_client.stop()
        self.close()
        return

    def yellow(self):
        text = '---'
        if int(self.timer_on) == 1:
            text = _('Enable update')
            self.timer_client.stop()
            self.timer_on = 0
        else:
            text = _('Disable update')
            self.makeList()
            self.timer_client.start(10000)
            self.timer_on = 1
        self.text_button_yellow = text
        self.setButton()
        return

    def up(self):
        self[self.currList].up()
        return

    def down(self):
        self[self.currList].down()
        return

    def left(self):
        self[self.currList].pageUp()
        return

    def right(self):
        self[self.currList].pageDown()
        return


class CCcamServersAllgemeinScreen(Screen):
    raw_skin = '\n        <screen position="center,{size.pos_h}" size="{size.screen}" title="{title.screen}">\n            <widget name="header" position="{pos.header}" size="{size.header}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label1}" size="{size.label1}" font="Regular;14" backgroundColor="#ffffff" />\n            <widget name="servers" position="{pos.servers}" size="{size.servers}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label2}" size="{size.label2}" font="Regular;14" backgroundColor="#ffffff" />\n            <widget name="footer" position="{pos.footer}" size="{size.footer}" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label3}" size="{size.label3}" font="Regular;14" backgroundColor="#ffffff" />\n            <ePixmap name="ButtonRed" pixmap="%s/pictures/button_red_%s.png" position="{pos.but_red}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonRedText" position="{pos.but_red}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonGreen" pixmap="%s/pictures/button_green_%s.png" position="{pos.but_green}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonGreenText" position="{pos.but_green}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonYellow" pixmap="%s/pictures/button_yellow_%s.png" position="{pos.but_yellow}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonYellowText" position="{pos.but_yellow}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonBlue" pixmap="%s/pictures/button_blue_%s.png" position="{pos.but_blue}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonBlueText" position="{pos.but_blue}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n        </screen>' % (path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)))

    def __init__(self, session, idx, config):
        size_h_screen = y_Pos_Screen(480)
        self.dict_text = {'size.pos_h': ('%.0f' % float(int(size_h_screen))), 'title.screen': ('CCcamOscamInfo CCcam Server General Ver. %s' % version)}
        self.dict_var = {'size.screen': '655,480', 'pos.header': '10,10', 
           'size.header': '635,25', 
           'pos.label1': '10,30', 
           'size.label1': '635,2', 
           'pos.servers': '10,50', 
           'size.servers': '635,300', 
           'pos.label2': '10,345', 
           'size.label2': '635,2', 
           'pos.footer': '10,360', 
           'size.footer': '635,75', 
           'pos.label3': '10,430', 
           'size.label3': '635,2', 
           'size.but': '140,50', 
           'pos.but_red': '10,440', 
           'pos.but_green': '175,440', 
           'pos.but_yellow': '340,440', 
           'pos.but_blue': '505,440'}
        self.skin = SkinVars(CCcamServersAllgemeinScreen.raw_skin, self.dict_text, self.dict_var)
        self.session = session
        self.idx = idx
        self.config = config
        Screen.__init__(self, session)
        self.data = []
        ret, res = read_Web(self.config, self.idx, 'servers')
        self.data = read_ServersGeneral(ret, res)
        self['header'] = Menu([])
        self['servers'] = Menu([])
        self['footer'] = FooterListServerGeneralCCcam([])
        self['ButtonBlueText'] = StaticText(_('Shareinfo'))
        self['ButtonGreenText'] = StaticText(_('Info'))
        self['ButtonYellowText'] = StaticText(_('Ping Server'))
        self['ButtonRedText'] = StaticText(_('Back'))
        self['actions'] = ActionMap(['CCcamOscamInfoActions'], {'ok': (self.green), 'cancel': (self.close), 
           'red': (self.red), 
           'green': (self.green), 
           'blue': (self.blue), 
           'yellow': (self.yellow), 
           'down': (self.down), 
           'up': (self.up), 
           'left': (self.left), 
           'right': (self.right), 
           'ch_up': (self.left), 
           'ch_down': (self.right)}, -1)
        self['servers'].onSelectionChanged.append(self.showInfo)
        self.onLayoutFinish.append(self.makeList)
        self.currList = 'servers'
        return

    def makeList(self):
        list = []
        for x in self.data[1]:
            tmpList = x.split(',')
            list.append(makeListServerGeneral(tmpList[0], tmpList[1], tmpList[3], tmpList[4], tmpList[6]))

        self['servers'].setList(list)
        self['servers'].selectionEnabled(1)
        list = []
        tmpList = self.data[0].split(',')
        list.append(makeListServerGeneralHeader(tmpList[0], tmpList[2], tmpList[5]))
        self['header'].setList(list)
        self['header'].selectionEnabled(0)
        return

    def showInfo(self):
        listdetail = []
        try:
            idx = self['servers'].getSelectedIndex()
            tmp = ''
            tmp = self.data[1][idx]
            tmpList = tmp.split(',')
            listdetail.append(makeListServerGeneralFooter(tmpList[1], tmpList[2], tmpList[3], tmpList[4], tmpList[5], tmpList[6]))
        except:
            listdetail.append(makeListServerGeneralFooter('', '', '', '', '', ''))

        self['footer'].setList(listdetail)
        self['footer'].selectionEnabled(0)
        return

    def blue(self):
        text = ''
        try:
            idx = self['servers'].getSelectedIndex()
            for x in self.data[2]:
                if x.split(',')[0] == self.data[1][idx].split(',')[1]:
                    x = x.split(',')
                    text = _('Username') + ': %s\n\n' % x[0] + _('Shareinfo') + ':\n'
                    del x[0]
                    for y in x:
                        text = '%s\n%s' % (text, y)

        except:
            text = ''

        if text == '':
            try:
                text = _('No CAID/Idents avriable tor the client') + '%s' % self.data[1][idx].split(',')[1]
            except:
                pass

        self.session.open(CCcamOscamInfoTextScreen, text, 'CCcem Server General ShareInfo', 0, 0)
        return

    def green(self):
        try:
            idx = self['servers'].getSelectedIndex()
            text = ''
            text = self.data[1][idx]
            if text != '':
                text = _('Host') + ': %s\n' % text.split(',')[1] + _('Connected') + ': %s\n' % text.split(',')[2] + _('Type') + ': %s\n' % text.split(',')[3] + _('Version') + ': %s\n' % text.split(',')[4] + _('NodeID') + ': %s\n' % text.split(',')[5] + _('Cards') + ': %s' % text.split(',')[6]
            else:
                text = 'Shit happens'
        except:
            text = 'Clients\n\nFische sind Freunde, kein Futter.'

        self.session.open(MessageBox, text, MessageBox.TYPE_INFO, timeout=20)
        return

    def yellow(self):
        idx = self['servers'].getSelectedIndex()
        host = self.data[1][idx].split(',')[1].split(':')[0]
        text = ping_oneServers(host)
        self.session.open(MessageBox, text, MessageBox.TYPE_INFO, timeout=20)
        return

    def red(self):
        self.close()
        return

    def up(self):
        self[self.currList].up()
        return

    def down(self):
        self[self.currList].down()
        return

    def left(self):
        self[self.currList].pageUp()
        return

    def right(self):
        self[self.currList].pageDown()
        return


class CCcamServersDetailScreen(Screen):
    raw_skin = '\n        <screen position="center,{size.pos_h}" size="{size.screen}" title="{title.screen}">\n            <widget name="header1" position="{pos.header1}" size="{size.header1}" font="Regular;%s" />\n            <widget name="header2" position="{pos.header2}" size="{size.header2}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label1}" size="{size.label2}" font="Regular;14" backgroundColor="#ffffff" />\n            <widget name="servers" position="{pos.servers}" size="{size.servers}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label2}" size="{size.label2}" font="Regular;14" backgroundColor="#ffffff" />\n            <widget name="footer" position="{pos.footer}" size="{size.footer}" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label3}" size="{size.label3}" font="Regular;14" backgroundColor="#ffffff" />\n            <ePixmap name="ButtonRed" pixmap="%s/pictures/button_red_%s.png" position="{pos.but_red}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonRedText" position="{pos.but_red}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonGreen" pixmap="%s/pictures/button_green_%s.png" position="{pos.but_green}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonGreenText" position="{pos.but_green}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonYellow" pixmap="%s/pictures/button_yellow_%s.png" position="{pos.but_yellow}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonYellowText" position="{pos.but_yellow}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonBlue" pixmap="%s/pictures/button_blue_%s.png" position="{pos.but_blue}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonBlueText" position="{pos.but_blue}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n        </screen>' % (int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)))

    def __init__(self, session, idx, config):
        size_h_screen = y_Pos_Screen(480)
        self.dict_text = {'size.pos_h': ('%.0f' % float(int(size_h_screen))), 'title.screen': ('CCcamOscamInfo CCcam Servers Detail Ver. %s' % version)}
        self.dict_var = {'size.screen': '655,480', 'pos.header1': '10,10', 
           'size.header1': '635,25', 
           'pos.header2': '10,35', 
           'size.header2': '635,25', 
           'pos.label1': '10,60', 
           'size.label1': '635,2', 
           'pos.label2': '10,395', 
           'size.label2': '635,2', 
           'pos.header_menu': '10,10', 
           'size.header_menu': '140,25', 
           'pos.servers': '10,70', 
           'size.servers': '635,325', 
           'pos.footer': '10,400', 
           'size.footer': '635,25', 
           'pos.label3': '10,430', 
           'size.label3': '635,2', 
           'size.but': '140,50', 
           'pos.but_red': '10,440', 
           'pos.but_green': '175,440', 
           'pos.but_yellow': '340,440', 
           'pos.but_blue': '505,440'}
        self.skin = SkinVars(CCcamServersDetailScreen.raw_skin, self.dict_text, self.dict_var)
        self.session = session
        self.idx = idx
        self.config = config
        Screen.__init__(self, session)
        self.data = []
        self.res_servers = []
        self.res_shares = []
        ret, self.res_servers = read_Web(self.config, self.idx, 'servers')
        if ret == 1:
            ret, self.res_shares = read_Web(self.config, self.idx, 'shares')
        self.data = read_ServersDetail(ret, self.res_servers, self.res_shares)
        self['header1'] = Label(_('You have') + ' %s ' % self.data[0] + _('locals cards online'))
        self['header2'] = Menu([])
        self['servers'] = Menu([])
        self['footer'] = Menu([])
        self['ButtonBlueText'] = StaticText(_('Server Locals'))
        self['ButtonGreenText'] = StaticText(_('my Locals'))
        self['ButtonYellowText'] = StaticText(_('Ping Server'))
        self['ButtonRedText'] = StaticText(_('Back'))
        self['actions'] = ActionMap(['CCcamOscamInfoActions'], {'ok': (self.blue), 'cancel': (self.close), 
           'red': (self.red), 
           'green': (self.green), 
           'blue': (self.blue), 
           'yellow': (self.yellow), 
           'down': (self.down), 
           'up': (self.up), 
           'left': (self.left), 
           'right': (self.right), 
           'ch_up': (self.left), 
           'ch_down': (self.right)}, -1)
        self.onLayoutFinish.append(self.makeList)
        self.currList = 'servers'
        return

    def makeList(self):
        self.list = []
        self.list.append(makeListServersHeaderFooter(self.data[1][0], self.data[1][1], self.data[1][2], self.data[1][3], self.data[1][4], self.data[1][5]))
        self['header2'].setList(self.list)
        self['header2'].selectionEnabled(0)
        self.list = []
        self.list.append(makeListServersHeaderFooter(self.data[2][0], self.data[2][1], self.data[2][2], self.data[2][3], self.data[2][4], self.data[2][5]))
        self['footer'].setList(self.list)
        self['footer'].selectionEnabled(0)
        self.list = []
        for x in self.data[3]:
            tmpList = x.split(',')
            self.list.append(makeListServers(tmpList[0], tmpList[1], tmpList[2], tmpList[3], tmpList[4], tmpList[5], tmpList[6], tmpList[7]))

        self['servers'].setList(self.list)
        self['servers'].selectionEnabled(1)
        return

    def blue(self):
        self.res_server = []
        self.res_shares = []
        self.res_providers = []
        idx = self['servers'].getSelectedIndex()
        ret, self.res_server = read_Web(self.config, self.idx, 'servers')
        if ret == 1:
            ret, self.res_shares = read_Web(self.config, self.idx, 'shares')
            if ret == 1:
                ret, self.res_providers = read_Web(self.config, self.idx, 'providers')
        text = read_Locals(ret, self.res_server, self.res_shares, self.res_providers, idx)
        self.session.open(CCcamOscamInfoTextScreen, text, 'CCcam Server Detail Server Locals', 0, 0)
        return

    def yellow(self):
        try:
            idx = self['servers'].getSelectedIndex()
            host = self.data[3][idx].split(',')[0].split(':')[0]
            text = ping_oneServers(host)
        except:
            text = _('Error')

        self.session.open(MessageBox, text, MessageBox.TYPE_INFO, timeout=20)
        return

    def red(self):
        self.close()
        return

    def green(self):
        self.read_shares = []
        self.read_prividers = []
        ret, self.res_shares = read_Web(self.config, self.idx, 'shares')
        if ret == 1:
            ret, self.res_providers = read_Web(self.config, self.idx, 'providers')
        text = read_myLocals(ret, self.res_shares, self.res_providers)
        self.session.open(CCcamOscamInfoTextScreen, text, 'CCcam Server Detail my Locals', 0, 0)
        return

    def up(self):
        self[self.currList].up()
        return

    def down(self):
        self[self.currList].down()
        return

    def left(self):
        self[self.currList].pageUp()
        return

    def right(self):
        self[self.currList].pageDown()
        return


class CCcamPingServersScreen(Screen):
    raw_skin = '\n        <screen position="center,{size.pos_h}" size="{size.screen}" title="{title.screen}">\n            <eLabel text="" position="{pos.label1}" size="{size.label1}" font="Regular;14" backgroundColor="#ffffff" />\n            <widget name="header" position="{pos.header}" size="{size.header}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <widget name="menu" position="{pos.menu}" size="{size.menu}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label2}" size="{size.label2}" font="Regular;14" backgroundColor="#ffffff" />\n            <ePixmap name="ButtonRed" pixmap="%s/pictures/button_red_%s.png" position="{pos.but_red}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonRedText" position="{pos.but_red}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonGreen" pixmap="%s/pictures/button_green_%s.png" position="{pos.but_green}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonGreenText" position="{pos.but_green}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonYellow" pixmap="%s/pictures/button_yellow_%s.png" position="{pos.but_yellow}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonYellowText" position="{pos.but_yellow}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonBlue" pixmap="%s/pictures/button_blue_%s.png" position="{pos.but_blue}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonBlueText" position="{pos.but_blue}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n        </screen>' % (path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)))

    def __init__(self, session, idx, config):
        size_h_screen = y_Pos_Screen(480)
        self.dict_text = {'size.pos_h': ('%.0f' % float(int(size_h_screen))), 'title.screen': ('CCcamOscamInfo Ping Servers Ver. %s' % version)}
        self.dict_var = {'size.screen': '655,480', 'pos.label1': '10,30', 
           'size.label1': '635,2', 
           'pos.header': '10,10', 
           'size.header': '635,25', 
           'pos.menu': '10,50', 
           'size.menu': '635,375', 
           'pos.label2': '10,430', 
           'size.label2': '635,2', 
           'size.but': '140,50', 
           'pos.but_red': '10,440', 
           'pos.but_green': '175,440', 
           'pos.but_yellow': '340,440', 
           'pos.but_blue': '505,440'}
        self.skin = SkinVars(CCcamPingServersScreen.raw_skin, self.dict_text, self.dict_var)
        self.session = session
        self.idx = idx
        self.config = config
        Screen.__init__(self, session)
        self.data = []
        self.data = read_Ping(path)
        self['ButtonBlueText'] = StaticText(_('Ping Servers'))
        self['ButtonGreenText'] = StaticText('')
        self['ButtonYellowText'] = StaticText('')
        self['ButtonRedText'] = StaticText(_('Back'))
        self['header'] = Menu([])
        self['menu'] = Menu([])
        self['actions'] = ActionMap(['CCcamOscamInfoActions'], {'ok': (self.blue), 'cancel': (self.close), 
           'red': (self.red), 
           'green': (self.green), 
           'blue': (self.blue), 
           'yellow': (self.yellow), 
           'down': (self.down), 
           'up': (self.up), 
           'left': (self.left), 
           'right': (self.right), 
           'ch_up': (self.left), 
           'ch_down': (self.right)}, -1)
        self.onLayoutFinish.append(self.makeList)
        self.currList = 'menu'
        return

    def makeList(self):
        self.list = []
        self.list.append(makeListPingHeader(self.data[0].split(',')[0], self.data[0].split(',')[1], self.data[0].split(',')[2], self.data[0].split(',')[3]))
        self['header'].setList(self.list)
        self['header'].selectionEnabled(0)
        self.list = []
        for x in self.data[1]:
            tmpList = x.split(',')
            self.list.append(makeListPing(tmpList[0], tmpList[1], tmpList[2], tmpList[3], tmpList[4]))

        self['menu'].setList(self.list)
        self['menu'].selectionEnabled(1)
        return

    def blue(self):
        self.data = []
        ret, res = read_Web(self.config, self.idx, 'servers')
        self.data = ping_Servers(ret, res, path)
        self.list = []
        for x in self.data[1]:
            tmpList = x.split(',')
            self.list.append(makeListPing(tmpList[0], tmpList[1], tmpList[2], tmpList[3], tmpList[4]))

        self['menu'].setList(self.list)
        self['menu'].selectionEnabled(1)
        return

    def green(self):
        return

    def red(self):
        self.close()
        return

    def yellow(self):
        return

    def up(self):
        self[self.currList].up()
        return

    def down(self):
        self[self.currList].down()
        return

    def left(self):
        self[self.currList].pageUp()
        return

    def right(self):
        self[self.currList].pageDown()
        return


class CCcamProvidersScreen(Screen):
    raw_skin = '\n        <screen position="center,{size.pos_h}" size="{size.screen}" title="{title.screen}">\n            <eLabel text="" position="{pos.label1}" size="{size.label1}" font="Regular;14" backgroundColor="#ffffff" />\n            <eLabel text="" position="{pos.label2}" size="{size.label2}" font="Regular;14" backgroundColor="#ffffff" />\n            <widget name="header_menu" position="{pos.header_menu}" size="{size.header_menu}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <widget name="menu" position="{pos.menu}" size="{size.menu}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <widget name="header_info" position="{pos.header_info}" size="{size.header_info}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <widget name="info" position="{pos.info}" size="{size.info}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label3}" size="{size.label3}" font="Regular;14" backgroundColor="#ffffff" />\n            <ePixmap name="ButtonRed" pixmap="%s/pictures/button_red_%s.png" position="{pos.but_red}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonRedText" position="{pos.but_red}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonGreen" pixmap="%s/pictures/button_green_%s.png" position="{pos.but_green}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonGreenText" position="{pos.but_green}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonYellow" pixmap="%s/pictures/button_yellow_%s.png" position="{pos.but_yellow}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonYellowText" position="{pos.but_yellow}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonBlue" pixmap="%s/pictures/button_blue_%s.png" position="{pos.but_blue}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonBlueText" position="{pos.but_blue}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n        </screen>' % (path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)))

    def __init__(self, session, idx, config):
        size_h_screen = y_Pos_Screen(480)
        self.dict_text = {'size.pos_h': ('%.0f' % float(int(size_h_screen))), 'title.screen': ('CCcamOscamInfo Providers Ver. %s' % version)}
        self.dict_var = {'size.screen': '655,480', 'pos.label1': '10,30', 
           'size.label1': '635,2', 
           'pos.label2': '122,10', 
           'size.label2': '2,425', 
           'pos.header_menu': '10,10', 
           'size.header_menu': '110,25', 
           'pos.menu': '10,50', 
           'size.menu': '110,375', 
           'pos.header_info': '140,10', 
           'size.header_info': '505,25', 
           'pos.info': '140,50', 
           'size.info': '505,375', 
           'pos.label3': '10,430', 
           'size.label3': '635,2', 
           'size.but': '140,50', 
           'pos.but_red': '10,440', 
           'pos.but_green': '175,440', 
           'pos.but_yellow': '340,440', 
           'pos.but_blue': '505,440'}
        self.skin = SkinVars(CCcamProvidersScreen.raw_skin, self.dict_text, self.dict_var)
        self.session = session
        self.idx = idx
        self.config = config
        Screen.__init__(self, session)
        self.data = []
        ret, res = read_Web(self.config, self.idx, 'providers')
        self.data = read_Providers(ret, res)
        self['ButtonBlueText'] = StaticText(_('Change windows'))
        self['ButtonGreenText'] = StaticText('')
        self['ButtonYellowText'] = StaticText('')
        self['ButtonRedText'] = StaticText(_('Back'))
        self['header_menu'] = Menu([])
        self['menu'] = Menu([])
        self['header_info'] = Menu([])
        self['info'] = Menu([])
        self['actions'] = ActionMap(['CCcamOscamInfoActions'], {'ok': (self.blue), 'cancel': (self.close), 
           'red': (self.red), 
           'green': (self.green), 
           'blue': (self.blue), 
           'yellow': (self.yellow), 
           'down': (self.down), 
           'up': (self.up), 
           'left': (self.left), 
           'right': (self.right), 
           'ch_up': (self.left), 
           'ch_down': (self.right)}, -1)
        self['menu'].onSelectionChanged.append(self.showProviderList)
        self.onLayoutFinish.append(self.makeList)
        self.selectListMenu()
        return

    def selectListMenu(self):
        self.currList = 'menu'
        self['header_menu'].selectionEnabled(0)
        self['menu'].selectionEnabled(1)
        self['header_info'].selectionEnabled(0)
        self['info'].selectionEnabled(0)
        return

    def selectListInfo(self):
        self.currList = 'info'
        self['header_menu'].selectionEnabled(0)
        self['menu'].selectionEnabled(0)
        self['header_info'].selectionEnabled(0)
        self['info'].selectionEnabled(1)
        return

    def makeList(self):
        self.list = []
        self.list.append(makeMenuShort(self.data[0].split(',')[0]))
        self['header_menu'].setList(self.list)
        self['header_menu'].selectionEnabled(0)
        self.list = []
        self.list.append(makeListProviders(self.data[0].split(',')[1], self.data[0].split(',')[2], self.data[0].split(',')[3]))
        self['header_info'].setList(self.list)
        self['header_info'].selectionEnabled(0)
        self.listmenu = []
        for x in self.data[1]:
            self.listmenu.append(makeMenuShort(x))

        self['menu'].setList(self.listmenu)
        self['menu'].selectionEnabled(1)
        return

    def showProviderList(self):
        self.list = []
        idx = self['menu'].getSelectedIndex()
        for x in self.data[2]:
            if self.listmenu[idx][0] == x.split(',')[0]:
                self.list.append(makeListProviders(x.split(',')[1], x.split(',')[2], x.split(',')[3]))

        self['info'].setList(self.list)
        self['info'].selectionEnabled(0)
        return

    def blue(self):
        if self.currList == 'menu':
            self.selectListInfo()
        else:
            self.selectListMenu()
        return

    def green(self):
        return

    def red(self):
        self.close()
        return

    def yellow(self):
        return

    def up(self):
        self[self.currList].up()
        return

    def down(self):
        self[self.currList].down()
        return

    def left(self):
        self[self.currList].pageUp()
        return

    def right(self):
        self[self.currList].pageDown()
        return


class CCcamSharesScreen(Screen):
    raw_skin = '\n        <screen position="center,{size.pos_h}" size="{size.screen}" title="{title.screen}">\n            <eLabel text="" position="{pos.label1}" size="{size.label1}" font="Regular;14" backgroundColor="#ffffff" />\n            <eLabel text="" position="{pos.label2}" size="{size.label2}" font="Regular;14" backgroundColor="#ffffff" />\n            <widget name="header_menu" position="{pos.header_menu}" size="{size.header_menu}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <widget name="menu" position="{pos.menu}" size="{size.menu}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <widget name="header_info" position="{pos.header_info}" size="{size.header_info}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <widget name="info" position="{pos.info}" size="{size.info}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label3}" size="{size.label3}" font="Regular;14" backgroundColor="#ffffff" />\n            <ePixmap name="ButtonRed" pixmap="%s/pictures/button_red_%s.png" position="{pos.but_red}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonRedText" position="{pos.but_red}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonGreen" pixmap="%s/pictures/button_green_%s.png" position="{pos.but_green}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonGreenText" position="{pos.but_green}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonYellow" pixmap="%s/pictures/button_yellow_%s.png" position="{pos.but_yellow}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonYellowText" position="{pos.but_yellow}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonBlue" pixmap="%s/pictures/button_blue_%s.png" position="{pos.but_blue}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonBlueText" position="{pos.but_blue}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n        </screen>' % (path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)))

    def __init__(self, session, idx, config):
        size_h_screen = y_Pos_Screen(480)
        self.dict_text = {'size.pos_h': ('%.0f' % float(int(size_h_screen))), 'title.screen': ('CCcamOscamInfo Shares Ver. %s' % version)}
        self.dict_var = {'size.screen': '655,480', 'pos.label1': '10,30', 
           'size.label1': '635,2', 
           'pos.label2': '122,10', 
           'size.label2': '2,425', 
           'pos.header_menu': '10,10', 
           'size.header_menu': '110,25', 
           'pos.menu': '10,50', 
           'size.menu': '110,375', 
           'pos.header_info': '140,10', 
           'size.header_info': '505,25', 
           'pos.info': '140,50', 
           'size.info': '505,375', 
           'pos.label3': '10,430', 
           'size.label3': '635,2', 
           'size.but': '140,50', 
           'pos.but_red': '10,440', 
           'pos.but_green': '175,440', 
           'pos.but_yellow': '340,440', 
           'pos.but_blue': '505,440'}
        self.skin = SkinVars(CCcamSharesScreen.raw_skin, self.dict_text, self.dict_var)
        self.session = session
        self.idx = idx
        self.config = config
        Screen.__init__(self, session)
        self.data = []
        ret, res = read_Web(self.config, self.idx, 'shares')
        self.data = read_Shares(ret, res)
        menulist = [_('Local'),
         _('Hop1'),
         _('Hop2'),
         _('Hop3'),
         _('Hop4'),
         _('HopX')]
        self.menulist = menulist
        self['header_menu'] = Menu([])
        self['menu'] = Menu([])
        self['header_info'] = Menu([])
        self['info'] = Menu([])
        self['ButtonBlueText'] = StaticText(_('Change windows'))
        self['ButtonGreenText'] = StaticText('')
        self['ButtonYellowText'] = StaticText('')
        self['ButtonRedText'] = StaticText('Back')
        self['actions'] = ActionMap(['CCcamOscamInfoActions'], {'ok': (self.blue), 'cancel': (self.close), 
           'red': (self.red), 
           'green': (self.green), 
           'blue': (self.blue), 
           'yellow': (self.yellow), 
           'down': (self.down), 
           'up': (self.up), 
           'left': (self.left), 
           'right': (self.right), 
           'ch_up': (self.left), 
           'ch_down': (self.right)}, -1)
        self['menu'].onSelectionChanged.append(self.showShareList)
        self.onLayoutFinish.append(self.makeList)
        self.selectListMenu()
        return

    def selectListMenu(self):
        self.currList = 'menu'
        self['header_menu'].selectionEnabled(0)
        self['menu'].selectionEnabled(1)
        self['header_info'].selectionEnabled(0)
        self['info'].selectionEnabled(0)
        return

    def selectListInfo(self):
        self.currList = 'info'
        self['header_menu'].selectionEnabled(0)
        self['menu'].selectionEnabled(0)
        self['header_info'].selectionEnabled(0)
        self['info'].selectionEnabled(1)
        return

    def makeList(self):
        self.list = []
        self.list.append(makeMenuShort(_('Hops')))
        self['header_menu'].setList(self.list)
        self['header_menu'].selectionEnabled(0)
        self.list = []
        self.list.append(makeListShares(self.data[0].split(';;')[0], self.data[0].split(';;')[2], self.data[0].split(';;')[3], self.data[0].split(';;')[4], self.data[0].split(';;')[5], self.data[0].split(';;')[6]))
        self['header_info'].setList(self.list)
        self['header_info'].selectionEnabled(0)
        self.listmenu = []
        for x in self.menulist:
            self.listmenu.append(makeMenuShort(x))

        self['menu'].setList(self.listmenu)
        self['menu'].selectionEnabled(1)
        return

    def showShareList(self):
        self.list = []
        idx = self['menu'].getSelectedIndex()
        try:
            if idx < len(self.listmenu) - 1:
                for x in self.data[1][idx]:
                    self.list.append(makeListShares(x.split(';;')[0], x.split(';;')[2], x.split(';;')[3], x.split(';;')[4], x.split(';;')[5], x.split(';;')[6]))

            else:
                idx == 0
                while idx < len(self.listmenu) - 1:
                    for x in self.data[1][idx]:
                        self.list.append(makeListShares(x.split(';;')[0], x.split(';;')[2], x.split(';;')[3], x.split(';;')[4], x.split(';;')[5], x.split(';;')[6]))
                        idx = idx + 1

        except:
            self.list.append(makeListShares('', '', '', '', '', ''))

        self['info'].setList(self.list)
        self['info'].selectionEnabled(0)
        return

    def blue(self):
        if self.currList == 'menu':
            self.selectListInfo()
        else:
            self.selectListMenu()
        return

    def green(self):
        if self.currList == 'info':
            idx = self['info'].getSelectedIndex()
            if idx < len(self.listmenu) - 1:
                text = '%s:%s\n\n%s:%s\n\n%s:%s\n\n%s:%s\n\n%s:%s\n\n%s:%s\n\n%s:%s\n\n%s:%s' % (self.data[0].split(';;')[0],
                 self.data[idx].split(';;')[0],
                 self.data[0].split(';;')[1],
                 self.data[idx].split(';;')[1],
                 self.data[0].split(';;')[2],
                 self.data[idx].split(';;')[2],
                 self.data[0].split(';;')[3],
                 self.data[idx].split(';;')[3],
                 self.data[0].split(';;')[4],
                 self.data[idx].split(';;')[4],
                 self.data[0].split(';;')[5],
                 self.data[idx].split(';;')[5],
                 self.data[0].split(';;')[6],
                 self.data[idx].split(';;')[6],
                 self.data[0].split(';;')[7],
                 self.data[idx].split(';;')[7])
                self.session.open(CCcamOscamInfoTextScreen, text, 'Share Info', 0, 0)
        return

    def red(self):
        self.close()
        return

    def yellow(self):
        return

    def up(self):
        self[self.currList].up()
        return

    def down(self):
        self[self.currList].down()
        return

    def left(self):
        self[self.currList].pageUp()
        return

    def right(self):
        self[self.currList].pageDown()
        return


class CCcamPairsScreen(Screen):
    raw_skin = '\n        <screen position="center,{size.pos_h}" size="{size.screen}" title="{title.screen}">\n            <widget name="header" position="{pos.header}" size="{size.header}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label1}" size="{size.label1}" font="Regular;14" backgroundColor="#ffffff" />\n            <widget name="pairs" position="{pos.pairs}" size="{size.pairs}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label2}" size="{size.label2}" font="Regular;14" backgroundColor="#ffffff" />\n            <widget name="details" position="{pos.details}" size="{size.details}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label3}" size="{size.label3}" font="Regular;14" backgroundColor="#ffffff" />\n            <ePixmap name="ButtonRed" pixmap="%s/pictures/button_red_%s.png" position="{pos.but_red}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonRedText" position="{pos.but_red}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonGreen" pixmap="%s/pictures/button_green_%s.png" position="{pos.but_green}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonGreenText" position="{pos.but_green}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonYellow" pixmap="%s/pictures/button_yellow_%s.png" position="{pos.but_yellow}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonYellowText" position="{pos.but_yellow}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonBlue" pixmap="%s/pictures/button_blue_%s.png" position="{pos.but_blue}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonBlueText" position="{pos.but_blue}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n        </screen>' % (path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)))

    def __init__(self, session, idx, config):
        size_h_screen = y_Pos_Screen(480)
        self.dict_text = {'size.pos_h': ('%.0f' % float(int(size_h_screen))), 'title.screen': ('CCcamOscamInfo CCcam Pairs Detail Ver. %s' % version)}
        self.dict_var = {'size.screen': '655,480', 'pos.header': '10,10', 
           'size.header': '635,25', 
           'pos.label1': '10,30', 
           'size.label1': '635,2', 
           'pos.label2': '10,395', 
           'size.label2': '635,2', 
           'pos.pairs': '10,50', 
           'size.pairs': '635,370', 
           'pos.details': '10,400', 
           'size.details': '635,25', 
           'pos.label3': '10,430', 
           'size.label3': '635,2', 
           'size.but': '140,50', 
           'pos.but_red': '10,440', 
           'pos.but_green': '175,440', 
           'pos.but_yellow': '340,440', 
           'pos.but_blue': '505,440'}
        self.skin = SkinVars(CCcamPairsScreen.raw_skin, self.dict_text, self.dict_var)
        self.session = session
        self.idx = idx
        self.config = config
        Screen.__init__(self, session)
        self.data = []
        res_servers = []
        res_clients = []
        ret, res_servers = read_Web(self.config, self.idx, 'servers')
        if ret == 1:
            ret, res_clients = read_Web(self.config, self.idx, 'clients')
        self.data = read_Mapping(ret, res_servers, res_clients)
        self['details'] = Menu([])
        self['header'] = Menu([])
        self['pairs'] = Menu([])
        self['ButtonBlueText'] = StaticText(_('Unpaired Users'))
        self['ButtonGreenText'] = StaticText(_('Unpaired Servers'))
        self['ButtonYellowText'] = StaticText(_('Pairs'))
        self['ButtonRedText'] = StaticText(_('Back'))
        self['actions'] = ActionMap(['CCcamOscamInfoActions'], {'ok': (self.close), 'cancel': (self.close), 
           'red': (self.red), 
           'green': (self.green), 
           'blue': (self.blue), 
           'yellow': (self.yellow), 
           'down': (self.down), 
           'up': (self.up), 
           'left': (self.left), 
           'right': (self.right), 
           'ch_up': (self.left), 
           'ch_down': (self.right)}, -1)
        self.onLayoutFinish.append(self.makeList)
        self.currList = 'pairs'
        return

    def makeList(self):
        self.list = []
        self.list.append(makeListPairs(_('Server'), _('Client'), _('IP')))
        self['header'].setList(self.list)
        self['header'].selectionEnabled(0)
        self.list = []
        for x in self.data[0]:
            self.list.append(makeListPairs(x.split(',')[0], x.split(',')[1], x.split(',')[2]))

        self['pairs'].setList(self.list)
        self['pairs'].selectionEnabled(1)
        self.list = []
        self.list.append(makeListPairsDetails(_('Details') + ':   ' + _('Server total') + ': %s ' % (len(self.data[0]) + len(self.data[1])) + _('Clients total') + ': %s' % (len(self.data[0]) + len(self.data[2]))))
        self['details'].setList(self.list)
        self['details'].selectionEnabled(0)
        return

    def updateList(self, listidx):
        self.list = []
        self.listindex = listidx
        for x in self.data[self.listindex]:
            if self.listindex == 0:
                self.list.append(makeListPairs(x.split(',')[0], x.split(',')[1], x.split(',')[2]))
            else:
                self.list.append(makeListPairsUsers(x.split(',')[0], x.split(',')[1]))

        self['pairs'].setList(self.list)
        self['pairs'].selectionEnabled(1)
        self.list = []
        if self.listindex == 0:
            self.list.append(makeListPairs(_('Server'), _('Client'), _('IP')))
        elif self.listindex == 1:
            self.list.append(makeListPairsUsers(_('Server'), _('IP')))
        else:
            self.list.append(makeListPairsUsers(_('Client'), _('IP')))
        self['header'].setList(self.list)
        self['header'].selectionEnabled(0)
        return

    def blue(self):
        self.updateList(2)
        return

    def green(self):
        self.updateList(1)
        return

    def red(self):
        self.close()
        return

    def yellow(self):
        self.updateList(0)
        return

    def up(self):
        self[self.currList].up()
        return

    def down(self):
        self[self.currList].down()
        return

    def left(self):
        self[self.currList].pageUp()
        return

    def right(self):
        self[self.currList].pageDown()
        return


class CCcamEntitlementsScreen(Screen):
    raw_skin = '\n        <screen position="center,{size.pos_h}" size="{size.screen}" title="{title.screen}">\n            <eLabel text="" position="{pos.label1}" size="{size.label1}" font="Regular;14" backgroundColor="#ffffff" />\n            <eLabel text="" position="{pos.label2}" size="{size.label2}" font="Regular;14" backgroundColor="#ffffff" />\n            <widget name="header" position="{pos.header}" size="{size.header}" font="Regular;%s" />\n            <widget name="menu" position="{pos.menu}" size="{size.menu}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <widget name="info" position="{pos.info}" size="{size.info}" font="Regular;%s" />\n            <eLabel text="" position="{pos.label3}" size="{size.label3}" font="Regular;14" backgroundColor="#ffffff" />\n            <ePixmap name="ButtonRed" pixmap="%s/pictures/button_red_%s.png" position="{pos.but_red}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonRedText" position="{pos.but_red}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonGreen" pixmap="%s/pictures/button_green_%s.png" position="{pos.but_green}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonGreenText" position="{pos.but_green}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonYellow" pixmap="%s/pictures/button_yellow_%s.png" position="{pos.but_yellow}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonYellowText" position="{pos.but_yellow}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonBlue" pixmap="%s/pictures/button_blue_%s.png" position="{pos.but_blue}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonBlueText" position="{pos.but_blue}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n        </screen>' % (int('%.0f' % (font_size * scale_y)),
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)))

    def __init__(self, session, idx, config):
        size_h_screen = y_Pos_Screen(480)
        self.dict_text = {'size.pos_h': ('%.0f' % float(int(size_h_screen))), 'title.screen': ('CCcamOscam Entitlements Ver. %s' % version)}
        self.dict_var = {'size.screen': '655,480', 'pos.label1': '10,30', 
           'size.label1': '635,2', 
           'pos.label2': '122,30', 
           'size.label2': '2,400', 
           'pos.header': '10,10', 
           'size.header': '635,25', 
           'pos.menu': '10,50', 
           'size.menu': '110,375', 
           'pos.info': '140,50', 
           'size.info': '505,375', 
           'pos.label3': '10,430', 
           'size.label3': '635,2', 
           'size.but': '140,50', 
           'pos.but_red': '10,440', 
           'pos.but_green': '175,440', 
           'pos.but_yellow': '340,440', 
           'pos.but_blue': '505,440'}
        self.skin = SkinVars(CCcamEntitlementsScreen.raw_skin, self.dict_text, self.dict_var)
        self.session = session
        self.idx = idx
        self.config = config
        Screen.__init__(self, session)
        self.data = []
        ret, res = read_Web(self.config, self.idx, 'entitlements')
        self.data = read_Entitlements(ret, res)
        self.menulist = []
        for x in self.data[1]:
            self.menulist.append(x[0])

        self['menu'] = Menu([])
        self['ButtonBlueText'] = StaticText('')
        self['ButtonGreenText'] = StaticText('')
        self['ButtonYellowText'] = StaticText('')
        self['ButtonRedText'] = StaticText(_('Back'))
        self['actions'] = ActionMap(['CCcamOscamInfoActions'], {'ok': (self.close), 'cancel': (self.close), 
           'red': (self.red), 
           'green': (self.green), 
           'blue': (self.blue), 
           'yellow': (self.yellow), 
           'down': (self.down), 
           'up': (self.up), 
           'left': (self.left), 
           'right': (self.right), 
           'ch_up': (self.ch_up), 
           'ch_down': (self.ch_down)}, -1)
        self.currList = 'menu'
        self['header'] = Label(self.data[0])
        self['info'] = ScrollLabel('')
        self['menu'].onSelectionChanged.append(self.showInfo)
        self.onLayoutFinish.append(self.makeList)
        return

    def makeList(self):
        list = []
        for x in self.menulist:
            list.append(makeMenuShort(x))

        self['menu'].setList(list)
        self['menu'].selectionEnabled(1)
        return

    def showInfo(self):
        idx = self['menu'].getSelectedIndex()
        self['info'].setText(self.data[1][idx][1])
        return

    def blue(self):
        return

    def green(self):
        return

    def red(self):
        self.close()
        return

    def yellow(self):
        return

    def up(self):
        self[self.currList].up()
        return

    def down(self):
        self[self.currList].down()
        return

    def left(self):
        self[self.currList].pageUp()
        return

    def right(self):
        self[self.currList].pageDown()
        return

    def ch_up(self):
        self['info'].pageUp()
        return

    def ch_down(self):
        self['info'].pageDown()
        return


class CCcamECMInfoScreen(Screen):
    raw_skin = '\n        <screen position="center,{size.pos_h}" size="{size.screen}" title="{title.screen}">\n            <eLabel text="" position="{pos.label}" size="{size.label}" font="Regular;14" backgroundColor="#ffffff" />\n            <widget name="menu" position="{pos.menu}" size="{size.menu}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <widget name="info" position="{pos.info}" size="{size.info}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label2}" size="{size.label2}" font="Regular;14" backgroundColor="#ffffff" />\n            <ePixmap name="ButtonRed" pixmap="%s/pictures/button_red_%s.png" position="{pos.but_red}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonRedText" position="{pos.but_red}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonGreen" pixmap="%s/pictures/button_green_%s.png" position="{pos.but_green}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonGreenText" position="{pos.but_green}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonYellow" pixmap="%s/pictures/button_yellow_%s.png" position="{pos.but_yellow}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonYellowText" position="{pos.but_yellow}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonBlue" pixmap="%s/pictures/button_blue_%s.png" position="{pos.but_blue}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonBlueText" position="{pos.but_blue}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n        </screen>' % (path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)))

    def __init__(self, session, idx_config, config):
        size_h_screen = y_Pos_Screen(480)
        self.dict_text = {'size.pos_h': ('%.0f' % float(int(size_h_screen))), 'title.screen': ('CCcamOscamInfo ECM Info Ver. %s' % version)}
        self.dict_var = {'size.screen': '655,480', 'pos.label': '122,10', 
           'size.label': '2,425', 
           'pos.menu': '10,10', 
           'size.menu': '110,400', 
           'pos.info': '140,10', 
           'size.info': '505,400', 
           'pos.label2': '10,430', 
           'size.label2': '635,2', 
           'size.but': '140,50', 
           'pos.but_red': '10,440', 
           'pos.but_green': '175,440', 
           'pos.but_yellow': '340,440', 
           'pos.but_blue': '505,440'}
        self.skin = SkinVars(CCcamECMInfoScreen.raw_skin, self.dict_text, self.dict_var)
        self.session = session
        self.idx_config = idx_config
        self.config = config
        Screen.__init__(self, session)
        self['menu'] = Menu([])
        self['info'] = Menu([])
        self.timer_on = 1
        self.timer_time = 5000
        self.timer_ecm = eTimer()
        self.timer_ecm_conn = self.timer_ecm.timeout.connect(self.makeList)
        self.makeList()
        if self.config[self.idx_config]['cam'] == 'CCcamRemote':
            self.timer_time = 15000
        self.timer_ecm.start(self.timer_time)
        self['ButtonBlueText'] = StaticText('')
        self['ButtonGreenText'] = StaticText('')
        self['ButtonYellowText'] = StaticText('')
        self['ButtonRedText'] = StaticText(_('Back'))
        self['actions'] = ActionMap(['CCcamOscamInfoActions'], {'ok': (self.red), 'cancel': (self.close), 
           'red': (self.red), 
           'green': (self.green), 
           'blue': (self.blue), 
           'yellow': (self.yellow), 
           'down': (self.down), 
           'up': (self.up), 
           'left': (self.left), 
           'right': (self.right), 
           'ch_up': (self.left), 
           'ch_down': (self.right)}, -1)
        self.currList = 'menu'
        self['menu'].onSelectionChanged.append(self.showECMInfo)
        self.onLayoutFinish.append(self.makeList)
        return

    def makeList(self):
        if self.config[self.idx_config]['cam'] == 'CCcamLocal':
            menulist = []
            for t in os.walk('/tmp'):
                menulist.append(t)

            self.menulist = menulist[0][2]
            self.menulist.sort()
            self.listmenu = []
            for x in self.menulist:
                if x.startswith('ecm') and x.endswith('.info'):
                    self.listmenu.append(makeMenuShort(x))

        elif self.config[self.idx_config]['cam'] == 'CCcamRemote':
            self.menulist = []
            self.menulist = ssh_list_tmp(self.config[self.idx_config]['url'], self.config[self.idx_config]['partnerboxsshport'], self.config[self.idx_config]['partnerboxpassword'], 'root')
            self.menulist.sort()
            self.listmenu = []
            for x in self.menulist:
                self.listmenu.append(makeMenuShort(x))

        self['menu'].setList(self.listmenu)
        self['menu'].selectionEnabled(1)
        return

    def showECMInfo(self):
        list = []
        idx = self['menu'].getSelectedIndex()
        try:
            if self.config[self.idx_config]['cam'] == 'CCcamLocal':
                data = open('/tmp/%s' % self.listmenu[idx][0], 'r').read().split('\n')
                del data[-1]
            elif self.config[self.idx_config]['cam'] == 'CCcamRemote':
                data = ssh_grab_ecminfo(self.config[self.idx_config]['url'], self.config[self.idx_config]['partnerboxsshport'], self.config[self.idx_config]['partnerboxpassword'], 'root', self.listmenu[idx][0])
            for x in data:
                list.append(makeECMList(x.split(':')[0].strip(), x.split(':')[1].strip()))

        except:
            pass

        self['info'].setList(list)
        self['info'].selectionEnabled(0)
        return

    def blue(self):
        return

    def green(self):
        return

    def red(self):
        if self.timer_on == 1:
            self.timer_ecm.stop()
        self.close()
        return

    def yellow(self):
        return

    def up(self):
        self[self.currList].up()
        return

    def down(self):
        self[self.currList].down()
        return

    def left(self):
        self[self.currList].pageUp()
        return

    def right(self):
        self[self.currList].pageDown()
        return


class EnableDisableClineFlineScreen(Screen):
    raw_skin = '\n        <screen position="center,{size.pos_h}" size="{size.screen}" title="{title.screen}">\n            <eLabel text="" position="{pos.label1}" size="{size.label1}" font="Regular;14" backgroundColor="#ffffff" />\n            <widget name="header" position="{pos.header}" size="{size.header}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <widget name="menu" position="{pos.menu}" size="{size.menu}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label2}" size="{size.label2}" font="Regular;14" backgroundColor="#ffffff" />\n            <ePixmap name="ButtonRed" pixmap="%s/pictures/button_red_%s.png" position="{pos.but_red}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget name="ButtonRedText" position="{pos.but_red}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonGreen" pixmap="%s/pictures/button_green_%s.png" position="{pos.but_green}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget name="ButtonGreenText" position="{pos.but_green}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonYellow" pixmap="%s/pictures/button_yellow_%s.png" position="{pos.but_yellow}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget name="ButtonYellowText" position="{pos.but_yellow}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonBlue" pixmap="%s/pictures/button_blue_%s.png" position="{pos.but_blue}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget name="ButtonBlueText" position="{pos.but_blue}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="IconMenu" pixmap="%s/pictures/key_menu_%s.png" position="{pos.icon_menu}" size="{size.icon_menu}" zPosition="4" transparent="1" alphatest="on"/>\n        </screen>' % (path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin)

    def __init__(self, session, cfg_path):
        size_h_screen = y_Pos_Screen(480)
        self.dict_text = {'size.pos_h': ('%.0f' % float(int(size_h_screen))), 'title.screen': ('CCcamOscamInfo Enable Disable C/F-Line Ver. %s' % version)}
        self.dict_var = {'size.screen': '655,480', 'pos.label1': '10,30', 
           'size.label1': '635,2', 
           'pos.header': '10,10', 
           'size.header': '635,25', 
           'pos.menu': '10,50', 
           'size.menu': '635,375', 
           'pos.label2': '10,430', 
           'size.label2': '635,2', 
           'size.but': '140,50', 
           'pos.but_red': '10,440', 
           'pos.but_green': '155,440', 
           'pos.but_yellow': '300,440', 
           'pos.but_blue': '445, 440', 
           'size.icon_menu': '55,50', 
           'pos.icon_menu': '590, 440'}
        self.skin = SkinVars(EnableDisableClineFlineScreen.raw_skin, self.dict_text, self.dict_var)
        self.session = session
        self.cfg_path = cfg_path
        self.myGreen = 'C'
        self.text_button_yellow = _('C-Lines')
        self.changes = {}
        Screen.__init__(self, session)
        self.data_fline = []
        self.data_cline = []
        ret, self.data_fline, self.data_cline = readClineFline(self.cfg_path)
        self['ButtonBlueText'] = Label()
        self['ButtonGreenText'] = Label(_('Save changes'))
        self['ButtonYellowText'] = Label()
        self['ButtonRedText'] = Label(_('Back'))
        self['header'] = Menu([])
        self['menu'] = Menu([])
        self['actions'] = ActionMap(['CCcamOscamInfoActions'], {'ok': (self.blue), 'cancel': (self.close), 
           'red': (self.red), 
           'green': (self.green), 
           'blue': (self.blue), 
           'yellow': (self.yellow), 
           'down': (self.down), 
           'up': (self.up), 
           'left': (self.left), 
           'right': (self.right), 
           'ch_up': (self.left), 
           'ch_down': (self.right), 
           'key_menu': (self.key_menu)}, -1)
        self['menu'].onSelectionChanged.append(self.setButtonText)
        self.onShown.append(self.setButton)
        self.onLayoutFinish.append(self.makeListFline)
        self.currList = 'menu'
        return

    def setButton(self):
        self['ButtonYellowText'].setText(self.text_button_yellow)
        self['ButtonBlueText'].setText(self.text_button_blue)
        return

    def setButtonText(self):
        text = '---'
        idx = self['menu'].getSelectedIndex()
        if self.myGreen == 'F':
            if idx < len(self.data_cline):
                if self.data_cline[idx].startswith('C'):
                    text = _('Disable')
                elif self.data_cline[idx].startswith('#C'):
                    text = _('Enable')
        elif self.myGreen == 'C':
            if idx < len(self.data_fline):
                if self.data_fline[idx].startswith('F'):
                    text = _('Disable')
                elif self.data_fline[idx].startswith('#F'):
                    text = _('Enable')
        self.text_button_blue = text
        self.setButton()
        return

    def makeListFline(self):
        self.list = []
        self.list.append(makeListEnableDisableClineFlineHeader(_('Enable/Disable F-Lines')))
        self['header'].setList(self.list)
        self['header'].selectionEnabled(0)
        self.list = []
        for x in self.data_fline:
            tmpList = x.split(' ')
            self.list.append(makeListEnableDisableClineFline(tmpList[0], tmpList[1]))

        self['menu'].setList(self.list)
        self['menu'].selectionEnabled(1)
        self.text_button_yellow = 'C-Lines'
        self.setButtonText()
        return

    def makeListCline(self):
        self.list = []
        self.list.append(makeListEnableDisableClineFlineHeader(_('Enable/Disable C-Lines')))
        self['header'].setList(self.list)
        self['header'].selectionEnabled(0)
        self.list = []
        for x in self.data_cline:
            tmpList = x.split(' ')
            self.list.append(makeListEnableDisableClineFline(tmpList[0], '%s:%s' % (tmpList[1], tmpList[2])))

        self['menu'].setList(self.list)
        self['menu'].selectionEnabled(1)
        self.text_button_yellow = _('F-Lines')
        self.setButtonText()
        return

    def blue(self):
        idx = self['menu'].getSelectedIndex()
        self.retchanges, self.changes, self.data_fline, self.data_cline = changesCCcam_cfg(self.changes, self.myGreen, idx, self.data_fline, self.data_cline)
        if self.myGreen == 'F':
            self.makeListCline()
        if self.myGreen == 'C':
            self.makeListFline()
        return

    def yellow(self):
        if self.myGreen == 'F':
            self.myGreen = 'C'
            self.makeListFline()
        elif self.myGreen == 'C':
            self.myGreen = 'F'
            self.makeListCline()
        return

    def red(self):
        try:
            if self.retchanges == 0:
                self.close()
            else:
                text = _('WARNING!') + '\n\n' + _('Are you sure that you want leave without save?')
                self.session.openWithCallback(self.callAnswer, MessageBox, text, MessageBox.TYPE_YESNO)
        except:
            self.close()

        return

    def callAnswer(self, answer):
        if answer:
            self.close()
        return

    def green(self):
        ret = writeCCcam_cfg(self.cfg_path, self.changes)
        if ret == 1:
            text = _('File') + ': %s/CCcam.cfg ' % self.cfg_path + _('saved')
            self.retchanges = 0
            self.changes = {}
        else:
            text = _('WARNING') + '!\n\n ' + _('File') + ' %s/CCcam.cfg ' % self.cfg_path + _('not saved')
        self.session.open(MessageBox, text, MessageBox.TYPE_INFO, timeout=20)
        return

    def up(self):
        self[self.currList].up()
        return

    def down(self):
        self[self.currList].down()
        return

    def left(self):
        self[self.currList].pageUp()
        return

    def right(self):
        self[self.currList].pageDown()
        return

    def key_menu(self):
        self.session.openWithCallback(self.key_menu_update, EnableDisableClineFlineBackupScreen, self.cfg_path)
        return

    def key_menu_update(self):
        self.data_fline = []
        self.data_cline = []
        ret, self.data_fline, self.data_cline = readClineFline(self.cfg_path)
        self.myGreen = 'C'
        self.text_button_yellow = _('C-Lines')
        self.makeListFline()
        return


class EnableDisableClineFlineBackupScreen(Screen):
    raw_skin = '\n        <screen position="center,{size.pos_h}" size="{size.screen}" title="{title.screen}">\n            <widget name="menu" position="{pos.menu}" size="{size.menu}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label1}" size="{size.label1}" font="Regular;14" backgroundColor="#ffffff" />\n            <ePixmap name="ButtonRed" pixmap="%s/pictures/button_red_%s.png" position="{pos.but_red}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget name="ButtonRedText" position="{pos.but_red}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonYellow" pixmap="%s/pictures/button_yellow_%s.png" position="{pos.but_yellow}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget name="ButtonYellowText" position="{pos.but_yellow}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonBlue" pixmap="%s/pictures/button_blue_%s.png" position="{pos.but_blue}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget name="ButtonBlueText" position="{pos.but_blue}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n        </screen>' % (path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)))

    def __init__(self, session, cfg_path):
        size_h_screen = y_Pos_Screen(210)
        self.dict_text = {'size.pos_h': ('%.0f' % float(int(size_h_screen))), 'title.screen': ('CCcamOscamInfo Backup CCcam.cfg Ver. %s' % version)}
        self.dict_var = {'size.screen': '455,210', 'pos.menu': '10,10', 
           'size.menu': '435,140', 
           'pos.label1': '10,160', 
           'size.label1': '435,2', 
           'size.but': '140,50', 
           'pos.but_red': '10,170', 
           'pos.but_yellow': '155, 170', 
           'pos.but_blue': '300, 170'}
        self.skin = SkinVars(EnableDisableClineFlineBackupScreen.raw_skin, self.dict_text, self.dict_var)
        self.session = session
        self.cfg_path = cfg_path
        self.text_button_blue = _('Backup cfg-File')
        Screen.__init__(self, session)
        self['ButtonBlueText'] = Label()
        self['ButtonYellowText'] = Label()
        self['ButtonRedText'] = Label(_('Back'))
        self['menu'] = Menu([])
        self['actions'] = ActionMap(['CCcamOscamInfoActions'], {'ok': (self.blue), 'cancel': (self.red), 
           'red': (self.red), 
           'yellow': (self.yellow), 
           'blue': (self.blue), 
           'down': (self.down), 
           'up': (self.up), 
           'left': (self.left), 
           'right': (self.right), 
           'ch_up': (self.left), 
           'ch_down': (self.right)}, -1)
        self['menu'].onSelectionChanged.append(self.setButtonText)
        self.onShown.append(self.setButton)
        self.onLayoutFinish.append(self.makeList)
        self.currList = 'menu'
        return

    def setButton(self):
        self['ButtonBlueText'].setText(self.text_button_blue)
        self['ButtonYellowText'].setText(self.text_button_yellow)
        return

    def setButtonText(self):
        text_blue = '---'
        text_yellow = '---'
        idx = self['menu'].getSelectedIndex()
        if self.menulist[idx] == 'CCcam.cfg':
            text_blue = _('Backup cfg-File')
            text_yellow = ''
        else:
            text_blue = _('Restore file')
            text_yellow = _('Delete file')
        self.text_button_blue = text_blue
        self.text_button_yellow = text_yellow
        self.setButton()
        return

    def makeList(self):
        self.tmp = []
        self.menulist = []
        self.list = []
        for t in os.walk(self.cfg_path):
            self.tmp.append(t)

        self.tmp = self.tmp[0][2]
        for t in self.tmp:
            if t.startswith('CCcam.cfg'):
                self.menulist.append(t)

        self.menulist.sort()
        for x in self.menulist:
            self.list.append(makeListEnableDisableClineFlineBackup(x))

        self['menu'].setList(self.list)
        self['menu'].selectionEnabled(1)
        self.setButtonText()
        return

    def blue(self):
        idx = self['menu'].getSelectedIndex()
        text = ''
        if self.menulist[idx] == 'CCcam.cfg':
            ret = backupConfig(self.cfg_path)
            if ret == 1:
                text = _('Backup success.')
            else:
                text = _('Backup fail.')
            self.makeList()
            self.session.open(MessageBox, text, MessageBox.TYPE_INFO, timeout=20)
        else:
            text = _('Restore the File') + ' %s/%s?' % (self.cfg_path, self.menulist[idx])
            self.session.openWithCallback(boundFunction(self.callAnswerRestore, self.menulist[idx]), MessageBox, text, MessageBox.TYPE_YESNO)
        return

    def yellow(self):
        idx = self['menu'].getSelectedIndex()
        text = ''
        if self.menulist[idx] == 'CCcam.cfg':
            pass
        else:
            text = _('Delete the File') + ' %s/%s?' % (self.cfg_path, self.menulist[idx])
            self.session.openWithCallback(boundFunction(self.callAnswerDelete, self.menulist[idx]), MessageBox, text, MessageBox.TYPE_YESNO)
        return

    def red(self):
        self.close()
        return

    def up(self):
        self[self.currList].up()
        return

    def down(self):
        self[self.currList].down()
        return

    def left(self):
        self[self.currList].pageUp()
        return

    def right(self):
        self[self.currList].pageDown()
        return

    def callAnswerDelete(self, delfile, answer):
        if answer:
            text = ''
            ret = delConfigFile(self.cfg_path, delfile)
            if ret == 1:
                text = _('File') + ' %s/%s ' + _('deleted') + '.' % (self.cfg_path, delfile)
            else:
                text = _('File') + ' %s/%s ' + _('not deleted') + '.' % (self.cfg_path, delfile)
            self.session.open(MessageBox, text, MessageBox.TYPE_INFO, timeout=20)
            self.makeList()
        return

    def callAnswerRestore(self, restorefile, answer):
        if answer:
            text = ''
            ret = restoreConfigFile(self.cfg_path, restorefile)
            if ret == 1:
                text = _('File') + ' %s/%s ' + _('restored') + '.' % (self.cfg_path, restorefile)
            else:
                text = _('File') + ' %s/%s ' + _('not restored') + '.' % (self.cfg_path, restorefile)
            self.session.open(MessageBox, text, MessageBox.TYPE_INFO, timeout=20)
            self.makeList()
        return


class OscamGeneralScreen(Screen):
    raw_skin = '\n        <screen position="center,{size.pos_h}" size="{size.screen}" title="{title.screen}">\n            <widget name="text_oscam" position="{pos.text_oscam}" size="{size.text_oscam}" font="Regular;%s" />\n            <widget name="menu_oscam" position="{pos.list_oscam}" size="{size.list_oscam}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label1}" size="{size.label1}" font="Regular;14" backgroundColor="#ffffff" />\n            <widget name="text_cw" position="{pos.text_cw}" size="{size.text_cw}" font="Regular;%s" />\n            <widget name="menu_cw" position="{pos.list_cw}" size="{size.list_cw}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label2}" size="{size.label2}" font="Regular;14" backgroundColor="#ffffff" />\n            <widget name="text_user" position="{pos.text_user}" size="{size.text_user}" font="Regular;%s" />\n            <widget name="menu_user" position="{pos.list_user}" size="{size.list_user}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label3}" size="{size.label3}" font="Regular;14" backgroundColor="#ffffff" />\n            <ePixmap name="ButtonRed" pixmap="%s/pictures/button_red_%s.png" position="{pos.but_red}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonRedText" position="{pos.but_red}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonGreen" pixmap="%s/pictures/button_green_%s.png" position="{pos.but_green}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonGreenText" position="{pos.but_green}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonYellow" pixmap="%s/pictures/button_yellow_%s.png" position="{pos.but_yellow}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonYellowText" position="{pos.but_yellow}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonBlue" pixmap="%s/pictures/button_blue_%s.png" position="{pos.but_blue}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonBlueText" position="{pos.but_blue}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n        </screen>' % (int('%.0f' % (font_size * scale_y)),
     int('%.0f' % (font_size * scale_y)),
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)))

    def __init__(self, session, idx, config):
        size_h_screen = y_Pos_Screen(480)
        self.dict_text = {'size.pos_h': ('%.0f' % float(int(size_h_screen))), 'title.screen': ('CCcamOscamInfo Oscam General Ver. %s' % version)}
        self.dict_var = {'size.screen': '655,480', 'pos.text_oscam': '10,10', 
           'size.text_oscam': '635,25', 
           'pos.list_oscam': '10,50', 
           'size.list_oscam': '635,60', 
           'pos.label1': '10,120', 
           'size.label1': '635,2', 
           'pos.text_cw': '10,140', 
           'size.text_cw': '635,25', 
           'pos.list_cw': '10,170', 
           'size.list_cw': '635,60', 
           'pos.label2': '10,250', 
           'size.label2': '635,2', 
           'pos.text_user': '10,270', 
           'size.text_user': '635,25', 
           'pos.list_user': '10,300', 
           'size.list_user': '635,60', 
           'pos.label3': '10,430', 
           'size.label3': '635,2', 
           'size.but': '140,50', 
           'pos.but_red': '10,440', 
           'pos.but_green': '175,440', 
           'pos.but_yellow': '340,440', 
           'pos.but_blue': '505,440'}
        self.skin = SkinVars(OscamGeneralScreen.raw_skin, self.dict_text, self.dict_var)
        self['text_oscam'] = Label()
        self['text_cw'] = Label()
        self['text_user'] = Label()
        self['menu_oscam'] = OscamGeneralList([])
        self['menu_cw'] = OscamGeneralList([])
        self['menu_user'] = OscamGeneralList([])
        self['ButtonBlueText'] = StaticText('')
        self['ButtonGreenText'] = StaticText('')
        self['ButtonYellowText'] = StaticText('')
        self['ButtonRedText'] = StaticText(_('Back'))
        self['actions'] = ActionMap(['CCcamOscamInfoActions'], {'ok': (self.red), 'cancel': (self.close), 
           'red': (self.red), 
           'green': (self.green), 
           'blue': (self.blue), 
           'yellow': (self.yellow)}, -1)
        self.session = session
        self.idx_config = idx
        self.config = config
        self.oscam_version = 0
        self.oscam = []
        self.totals = []
        self.users = []
        Screen.__init__(self, session)
        self.timer_on = 1
        self.timer_general = eTimer()
        self.timer_general_conn = self.timer_general.timeout.connect(self.makeList)
        self.makeList()
        self.timer_general.start(5000)
        self.onLayoutFinish.append(self.makeList)
        return

    def makeList(self):
        self['text_oscam'].setText(_('Oscam info') + ':')
        self['text_cw'].setText(_('CW info') + ':')
        self['text_user'].setText(_('User info') + ':')
        ret, res = read_Web(self.config, self.idx_config, 'oscamapi.html?part=userstats')
        self.oscam, self.total = parse_xml_summary(ret, res)
        if int(self.oscam['Revision']) < 6214:
            self['text_user'].setText(_('User info') + ': ' + _('You need Ver. 6214 or higher. Your version is') + ': %s' % self.oscam['Revision'])
        self.list = []
        self.list.append(makeListOscamGeneralMenuOscam(_('Version') + ': ', self.oscam['Version'], _('Revision') + ': ', self.oscam['Revision'], _('Starttime') + ': ', self.oscam['Starttime'], _('Uptime') + ': ', self.oscam['Uptime'], _('Readonly') + ': ', self.oscam['Readonly']))
        self['menu_oscam'].setList(self.list)
        self['menu_oscam'].selectionEnabled(0)
        self.list = []
        self.list.append(makeListOscamGeneral(_('OK') + ': ', self.total['CWOK'], _('NOK') + ': ', self.total['CWNOK'], _('Ignore') + ': ', self.total['CWIgnore'], _('Timeout') + ': ', self.total['CWTtimeout'], _('Cache') + ': ', self.total['CWCache'], _('Tun') + ': ', self.total['CWTun']))
        self['menu_cw'].setList(self.list)
        self['menu_cw'].selectionEnabled(0)
        self.list = []
        self.list.append(makeListOscamGeneral(_('Connected') + ': ', self.total['UserConnected'], _('Online') + ': ', self.total['UserOnline'], _('Active') + ': ', self.total['UserActive'], _('Total') + ': ', self.total['UserTotal'], _('Disabled') + ': ', self.total['UserDisabled'], _('Expired') + ': ', self.total['UserExpired']))
        self['menu_user'].setList(self.list)
        self['menu_user'].selectionEnabled(0)
        return

    def blue(self):
        return

    def green(self):
        return

    def red(self):
        if self.timer_on == 1:
            self.timer_general.stop()
        self.close()
        return

    def yellow(self):
        return


class OscamClientServerScreen(Screen):
    raw_skin = '\n        <screen position="center,{size.pos_h}" size="{size.screen}" title="{title.screen}">\n            <widget name="header" position="{pos.header}" size="{size.header}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label1}" size="{size.label1}" font="Regular;14" backgroundColor="#ffffff" />\n            <widget name="servers" position="{pos.servers}" size="{size.servers}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label2}" size="{size.label2}" font="Regular;14" backgroundColor="#ffffff" />\n            <widget name="footer" position="{pos.footer}" size="{size.footer}" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label3}" size="{size.label3}" font="Regular;14" backgroundColor="#ffffff" />\n            <ePixmap name="ButtonRed" pixmap="%s/pictures/button_red_%s.png" position="{pos.but_red}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget name="ButtonRedText" position="{pos.but_red}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonGreen" pixmap="%s/pictures/button_green_%s.png" position="{pos.but_green}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget name="ButtonGreenText" position="{pos.but_green}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonYellow" pixmap="%s/pictures/button_yellow_%s.png" position="{pos.but_yellow}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget name="ButtonYellowText" position="{pos.but_yellow}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonBlue" pixmap="%s/pictures/button_blue_%s.png" position="{pos.but_blue}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget name="ButtonBlueText" position="{pos.but_blue}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n        </screen>' % (path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)))

    def __init__(self, session, idx_config, config, windows):
        size_h_screen = y_Pos_Screen(480)
        title = ''
        if windows == 'AllClients':
            title = _('all Clients')
        elif windows == 'Clients':
            title = _('Clients')
        elif windows == 'Readers':
            title = _('Readers')
        elif windows == 'Proxys':
            title = _('Proxys')
        elif windows == 'AllReadersProxys':
            title = _('all Readers/Proxys')
        self.dict_text = {'size.pos_h': ('%.0f' % float(int(size_h_screen))), 'title.screen': ('CCcamOscamInfo Oscam %s Ver. %s' % (title, version))}
        self.dict_var = {'size.screen': '655,480', 'pos.header': '10,10', 
           'size.header': '635,25', 
           'pos.label1': '10,30', 
           'size.label1': '635,2', 
           'pos.servers': '10,50', 
           'size.servers': '635,300', 
           'pos.label2': '10,345', 
           'size.label2': '635,2', 
           'pos.footer': '10,360', 
           'size.footer': '635,75', 
           'pos.label3': '10,430', 
           'size.label3': '635,2', 
           'size.but': '140,50', 
           'pos.but_red': '10,440', 
           'pos.but_green': '175,440', 
           'pos.but_yellow': '340,440', 
           'pos.but_blue': '505,440'}
        self.skin = SkinVars(OscamClientServerScreen.raw_skin, self.dict_text, self.dict_var)
        self['header'] = Menu([])
        self['servers'] = Menu([])
        self['footer'] = FooterListClientsOscam([])
        self.session = session
        self.idx_config = idx_config
        self.config = config
        self.windows = windows
        Screen.__init__(self, session)
        self.timer_on = 0
        self.text_button_yellow = _('Enable update')
        if self.windows == 'Clients' or self.windows == 'Readers' or self.windows == 'Proxys':
            self.text_button_red = _('Request')
        else:
            self.text_button_red = ''
        self.idx_readerlist = 0
        if self.windows == 'AllReadersProxys':
            self.text_button_green = _('Proxys')
        else:
            self.text_button_green = ''
        self.timer_client = eTimer()
        self.timer_client_conn = self.timer_client.timeout.connect(self.makeListTimer)
        self['ButtonBlueText'] = Label()
        self['ButtonGreenText'] = Label()
        self['ButtonYellowText'] = Label()
        self['ButtonRedText'] = Label(_('Back'))
        self['actions'] = ActionMap(['CCcamOscamInfoActions'], {'ok': (self.blue), 'cancel': (self.red), 
           'red': (self.red), 
           'green': (self.green), 
           'blue': (self.blue), 
           'yellow': (self.yellow), 
           'down': (self.down), 
           'up': (self.up), 
           'left': (self.left), 
           'right': (self.right), 
           'ch_up': (self.left), 
           'ch_down': (self.right)}, -1)
        self['servers'].onSelectionChanged.append(self.showInfo)
        self.onShown.append(self.setButton)
        self.onLayoutFinish.append(self.makeList)
        self.currList = 'servers'
        return

    def makeListTimer(self):
        self.makeList()
        self.showInfo()
        return

    def setButton(self):
        self['ButtonYellowText'].setText(self.text_button_yellow)
        self['ButtonBlueText'].setText(self.text_button_red)
        self['ButtonGreenText'].setText(self.text_button_green)
        return

    def makeList(self):
        self.data = []
        self.status = []
        self.userstatus = []
        self.readers = []
        if self.windows == 'Clients' or self.windows == 'Readers' or self.windows == 'Proxys':
            ret, self.status = read_Web(self.config, self.idx_config, 'oscamapi.html?part=status')
            self.data = oscamClients(ret, self.status, self.windows)
            list = []
            if self.windows == 'Clients':
                list.append(makeListClientsOscamHeader(_('Username'), _('AU'), _('CurrentChannel'), _('Answered')))
            elif self.windows == 'Readers':
                list.append(makeListClientsOscamHeader(_('Label'), _('AU'), _('CurrentChannel'), _('Answered')))
            elif self.windows == 'Proxys':
                list.append(makeListClientsOscamHeader(_('Proxyname'), _('AU'), _('CurrentChannel'), _('Answered')))
            self['header'].setList(list)
            self['header'].selectionEnabled(0)
            list = []
            for x in self.data:
                self.color_au = ''
                if x['AU'] == '-1':
                    self.color_au = 'blue'
                elif x['AU'] == '1':
                    self.color_au = 'green'
                elif x['AU'] == '0':
                    self.color_au = 'red'
                list.append(makeListClientsOscam(x['Name'], self.color_au, x['CurrentChannel'], x['Answered']))

            self['servers'].setList(list)
            self['servers'].selectionEnabled(1)
        elif self.windows == 'AllClients':
            ret, self.userstatus = read_Web(self.config, self.idx_config, 'oscamapi.html?part=userstats')
            self.data = oscamAllClients(ret, self.userstatus)
            list = []
            list.append(makeListAllClientsOscamHeader(_('Name'), _('IP-Address'), _('Protocol')))
            self['header'].setList(list)
            self['header'].selectionEnabled(0)
            list = []
            for x in self.data:
                self.color_status = ''
                if x['Status'].startswith('online'):
                    self.color_status = 'green'
                elif x['Status'].startswith('connected'):
                    self.color_status = 'blue'
                elif x['Status'].startswith('offline'):
                    self.color_status = 'red'
                list.append(makeListAllClientsOscam(self.color_status, x['Name'], x['IP'], x['Protocol']))

            self['servers'].setList(list)
            self['servers'].selectionEnabled(1)
        elif self.windows == 'AllReadersProxys':
            ret, self.readers = read_Web(self.config, self.idx_config, 'oscamapi.html?part=readerlist')
            self.data = oscamAllReaders(ret, self.readers)
            list = []
            list.append(makeListAllReadersOscamHeader(_('Label'), _('Protocol'), _('Type')))
            self['header'].setList(list)
            self['header'].selectionEnabled(0)
            list = []
            for x in self.data[self.idx_readerlist]:
                self.color_enabled = ''
                if x['Enabled'] == '0':
                    self.color_enabled = 'red'
                elif x['Enabled'] == '1':
                    self.color_enabled = 'green'
                list.append(makeListAllReadersOscam(self.color_enabled, x['Label'], x['Protocol'], x['Type']))

            self['servers'].setList(list)
            self['servers'].selectionEnabled(1)
        return

    def showInfo(self):
        listdetail = []
        idx = self['servers'].getSelectedIndex()
        if self.windows == 'AllClients':
            listdetail.append(makeListClientsOscamFooterCWEMM(self.data[idx]['CWOK'], self.data[idx]['CWNOK'], self.data[idx]['CWIgnore'], self.data[idx]['CWTtimeout'], self.data[idx]['CWCache'], self.data[idx]['CWTun'], self.data[idx]['CWLlastresptime'], self.data[idx]['CWRate'], self.data[idx]['EMMOK'], self.data[idx]['EMMNOK']))
        elif self.windows == 'Clients' or self.windows == 'Readers' or self.windows == 'Proxys':
            if self.text_button_red == _('Request'):
                listdetail.append(makeListClientsOscamFooterTime(self.data[idx]['Login'], self.data[idx]['Protocol'], self.data[idx]['Online'], self.data[idx]['IP'], self.data[idx]['Idle'], self.data[idx]['Port']))
            elif self.text_button_red == _('Time/Con'):
                listdetail.append(makeListClientsOscamFooterRequest(self.data[idx]['CurrentChannel'], self.data[idx]['Answered'], self.data[idx]['CaID'], self.data[idx]['SrvID'], self.data[idx]['ECMTime'], self.data[idx]['ECMHistory']))
        self['footer'].setList(listdetail)
        self['footer'].selectionEnabled(0)
        return

    def blue(self):
        if self.windows == 'Clients' or self.windows == 'Readers' or self.windows == 'Proxys':
            if self.text_button_red == _('Request'):
                self.text_button_red = _('Time/Con')
            elif self.text_button_red == _('Time/Con'):
                self.text_button_red = _('Request')
            self.setButton()
            self.showInfo()
        else:
            self.text_button_red = ''
            self.setButton()
        return

    def green(self):
        if self.windows == 'AllReadersProxys':
            if self.text_button_green == _('Proxys'):
                self.text_button_green = _('Readers')
                self.idx_readerlist = 1
            elif self.text_button_green == _('Readers'):
                self.text_button_green = _('Proxys')
                self.idx_readerlist = 0
            self.setButton()
            self.makeList()
            self.showInfo()
        else:
            self.text_button_green = ''
            self.setButton()
        return

    def red(self):
        if self.timer_on == 1:
            self.timer_client.stop()
        self.close()
        return

    def yellow(self):
        text = '---'
        if int(self.timer_on) == 1:
            text = _('Enable update')
            self.timer_client.stop()
            self.timer_on = 0
        else:
            text = _('Disable update')
            self.makeList()
            self.timer_client.start(10000)
            self.timer_on = 1
        self.text_button_yellow = text
        self.setButton()
        return

    def up(self):
        self[self.currList].up()
        return

    def down(self):
        self[self.currList].down()
        return

    def left(self):
        self[self.currList].pageUp()
        return

    def right(self):
        self[self.currList].pageDown()
        return


class OScamTextList(Screen):
    raw_skin = '\n        <screen position="center,{size.pos_h}" size="{size.screen}" title="{title.screen}">\n            <widget name="list" position="{pos.list}" size="{size.list}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label1}" size="{size.label1}" font="Regular;14" backgroundColor="#ffffff" />\n            <ePixmap name="ButtonRed" pixmap="%s/pictures/button_red_%s.png" position="{pos.but_red}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonRedText" position="{pos.but_red}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonGreen" pixmap="%s/pictures/button_green_%s.png" position="{pos.but_green}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonGreenText" position="{pos.but_green}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonYellow" pixmap="%s/pictures/button_yellow_%s.png" position="{pos.but_yellow}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonYellowText" position="{pos.but_yellow}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonBlue" pixmap="%s/pictures/button_blue_%s.png" position="{pos.but_blue}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonBlueText" position="{pos.but_blue}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n        </screen>' % (path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)))

    def __init__(self, session, data):
        size_h_screen = y_Pos_Screen(480)
        self.dict_text = {'size.pos_h': ('%.0f' % float(int(size_h_screen))), 'title.screen': ('CCcamOscamInfo Oscam Clients Info Ver. %s' % version)}
        self.dict_var = {'size.screen': '655,480', 'pos.list': '10,10', 
           'size.list': '635,400', 
           'pos.label1': '10,430', 
           'size.label1': '635,2', 
           'size.but': '140,50', 
           'pos.but_red': '10,440', 
           'pos.but_green': '175,440', 
           'pos.but_yellow': '340,440', 
           'pos.but_blue': '505,440'}
        self.skin = SkinVars(OScamTextList.raw_skin, self.dict_text, self.dict_var)
        self.session = session
        self.data = data
        Screen.__init__(self, session)
        self['list'] = Menu([])
        self['ButtonBlueText'] = StaticText('')
        self['ButtonGreenText'] = StaticText('')
        self['ButtonYellowText'] = StaticText('')
        self['ButtonRedText'] = StaticText(_('Back'))
        self['actions'] = ActionMap(['CCcamOscamInfoActions'], {'ok': (self.close), 'cancel': (self.close), 
           'red': (self.red), 
           'green': (self.green), 
           'blue': (self.blue), 
           'yellow': (self.yellow), 
           'down': (self.right), 
           'up': (self.left), 
           'left': (self.left), 
           'right': (self.right), 
           'ch_up': (self.left), 
           'ch_down': (self.right)}, -1)
        self.onLayoutFinish.append(self.makeList)
        return

    def makeList(self):
        list = []
        for x in self.data:
            list.append(makeListOscamTextList(x[0], x[1]))

        self['list'].setList(list)
        self['list'].selectionEnabled(1)
        return

    def left(self):
        self['list'].pageUp()
        return

    def right(self):
        self['list'].pageDown()
        return

    def blue(self):
        return

    def green(self):
        return

    def red(self):
        self.close()
        return

    def yellow(self):
        return


class EnableDisableClientsReadersProxysScreen(Screen):
    raw_skin = '\n        <screen position="center,{size.pos_h}" size="{size.screen}" title="{title.screen}">\n            <eLabel text="" position="{pos.label1}" size="{size.label1}" font="Regular;14" backgroundColor="#ffffff" />\n            <widget name="header" position="{pos.header}" size="{size.header}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <widget name="menu" position="{pos.menu}" size="{size.menu}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label2}" size="{size.label2}" font="Regular;14" backgroundColor="#ffffff" />\n            <ePixmap name="ButtonRed" pixmap="%s/pictures/button_red_%s.png" position="{pos.but_red}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget name="ButtonRedText" position="{pos.but_red}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonGreen" pixmap="%s/pictures/button_green_%s.png" position="{pos.but_green}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget name="ButtonGreenText" position="{pos.but_green}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonYellow" pixmap="%s/pictures/button_yellow_%s.png" position="{pos.but_yellow}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget name="ButtonYellowText" position="{pos.but_yellow}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonBlue" pixmap="%s/pictures/button_blue_%s.png" position="{pos.but_blue}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget name="ButtonBlueText" position="{pos.but_blue}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n        </screen>' % (path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)))

    def __init__(self, session, idx, config):
        size_h_screen = y_Pos_Screen(480)
        self.dict_text = {'size.pos_h': ('%.0f' % float(int(size_h_screen))), 'title.screen': ('CCcamOscamInfo Enable Disable Clients Readers Proxys Ver. %s' % version)}
        self.dict_var = {'size.screen': '655,480', 'pos.label1': '10,30', 
           'size.label1': '635,2', 
           'pos.header': '10,10', 
           'size.header': '635,25', 
           'pos.menu': '10,50', 
           'size.menu': '635,375', 
           'pos.label2': '10,430', 
           'size.label2': '635,2', 
           'size.but': '140,50', 
           'pos.but_red': '10,440', 
           'pos.but_green': '175,440', 
           'pos.but_yellow': '340,440', 
           'pos.but_blue': '505,440'}
        self.skin = SkinVars(EnableDisableClientsReadersProxysScreen.raw_skin, self.dict_text, self.dict_var)
        self.session = session
        self.idx_config = idx
        self.config = config
        self.text_button_green = _('Readers')
        self.button_green_status = 'R'
        Screen.__init__(self, session)
        self['ButtonBlueText'] = Label()
        self['ButtonGreenText'] = Label()
        self['ButtonYellowText'] = Label('')
        self['ButtonRedText'] = Label('Back')
        self['header'] = Menu([])
        self['menu'] = Menu([])
        self['actions'] = ActionMap(['CCcamOscamInfoActions'], {'ok': (self.blue), 'cancel': (self.close), 
           'red': (self.red), 
           'green': (self.green), 
           'blue': (self.blue), 
           'yellow': (self.yellow), 
           'down': (self.down), 
           'up': (self.up), 
           'left': (self.left), 
           'right': (self.right), 
           'ch_up': (self.left), 
           'ch_down': (self.right)}, -1)
        self['menu'].onSelectionChanged.append(self.setButtonText)
        self.onShown.append(self.setButton)
        self.onLayoutFinish.append(self.makeList)
        self.currList = 'menu'
        return

    def setButton(self):
        self['ButtonGreenText'].setText(self.text_button_green)
        self['ButtonBlueText'].setText(self.text_button_red)
        return

    def setButtonText(self):
        text = ''
        self.idx = self['menu'].getSelectedIndex()
        if self.button_green_status == 'R':
            try:
                if self.reader[self.idx]['Enabled'] == '1':
                    text = _('Disable')
                elif self.reader[self.idx]['Enabled'] == '0':
                    text = _('Enable')
            except:
                pass

        elif self.button_green_status == 'P':
            try:
                if self.proxy[self.idx]['Enabled'] == '1':
                    text = _('Disable')
                elif self.proxy[self.idx]['Enabled'] == '0':
                    text = _('Enable')
            except:
                pass

        elif self.button_green_status == 'C':
            try:
                if self.client[self.idx]['Status'] == '1':
                    text = _('Disable')
                elif self.client[self.idx]['Status'] == '0':
                    text = _('Enable')
            except:
                pass

        self.text_button_red = text
        self.setButton()
        return

    def makeList(self):
        self.readers = []
        self.clients = []
        self.reader = []
        self.proxy = []
        self.client = []
        self.listheader = []
        self.list = []
        ret, self.readers = read_Web(self.config, self.idx_config, 'oscamapi.html?part=readerlist')
        if ret == 1:
            ret, self.clients = read_Web(self.config, self.idx_config, 'oscamapi.html?part=userstats')
        self.reader, self.proxy, self.client = oscamEnableDisable(ret, self.readers, self.clients)
        if self.text_button_green == _('Readers'):
            self.listheader.append(EnableDisableClientsReadersProxysHeader(_('Label'), _('Protocol')))
            for x in self.reader:
                self.list.append(EnableDisableClientsReadersProxys(x['Enabled'], x['Label'], x['Protocol']))

            self.button_green_status = 'R'
            self.text_button_green = _('Proxys')
        elif self.text_button_green == _('Proxys'):
            self.listheader.append(EnableDisableClientsReadersProxysHeader(_('Name'), _('Protocol')))
            for x in self.proxy:
                self.list.append(EnableDisableClientsReadersProxys(x['Enabled'], x['Label'], x['Protocol']))

            self.button_green_status = 'P'
            self.text_button_green = _('Clients')
        elif self.text_button_green == _('Clients'):
            self.listheader.append(EnableDisableClientsReadersProxysHeader(_('Client'), _('Protocol')))
            for x in self.client:
                self.list.append(EnableDisableClientsReadersProxys(x['Status'], x['Name'], x['Protocol']))

            self.button_green_status = 'C'
            self.text_button_green = _('Readers')
        self['header'].setList(self.listheader)
        self['header'].selectionEnabled(0)
        self['menu'].setList(self.list)
        self['menu'].selectionEnabled(1)
        self.setButtonText()
        return

    def blue(self):
        res = []
        if self.text_button_red == '':
            pass
        elif self.button_green_status == 'R':
            self.text_button_green = _('Readers')
            if self.reader[self.idx]['Enabled'] == '1':
                ret, res = read_Web(self.config, self.idx_config, 'oscamapi.html?part=readerlist&action=disable&label=%s' % self.reader[self.idx]['Label'])
            elif self.reader[self.idx]['Enabled'] == '0':
                ret, res = read_Web(self.config, self.idx_config, 'oscamapi.html?part=readerlist&action=enable&label=%s' % self.reader[self.idx]['Label'])
        elif self.button_green_status == 'P':
            self.text_button_green = _('Proxys')
            if self.proxy[self.idx]['Enabled'] == '1':
                ret, res = read_Web(self.config, self.idx_config, 'oscamapi.html?part=readerlist&action=disable&label=%s' % self.proxy[self.idx]['Label'])
            elif self.proxy[self.idx]['Enabled'] == '0':
                ret, res = read_Web(self.config, self.idx_config, 'oscamapi.html?part=readerlist&action=enable&label=%s' % self.proxy[self.idx]['Label'])
        elif self.button_green_status == 'C':
            self.text_button_green = _('Clients')
            if self.client[self.idx]['Status'] == '1':
                ret, res = read_Web(self.config, self.idx_config, 'oscamapi.html?part=userconfig&user=%s&disabled=1&action=Save' % self.client[self.idx]['Name'])
            elif self.client[self.idx]['Status'] == '0':
                ret, res = read_Web(self.config, self.idx_config, 'oscamapi.html?part=userconfig&user=%s&disabled=0&action=Save' % self.client[self.idx]['Name'])
        self.makeList()
        return

    def green(self):
        self.makeList()
        return

    def red(self):
        self.close()
        return

    def yellow(self):
        return

    def up(self):
        self[self.currList].up()
        return

    def down(self):
        self[self.currList].down()
        return

    def left(self):
        self[self.currList].pageUp()
        return

    def right(self):
        self[self.currList].pageDown()
        return


class OscamRestatServer(Screen):
    raw_skin = '\n        <screen position="center,{size.pos_h}" size="{size.screen}" title="{title.screen}">\n            <widget name="menu" position="{pos.menu}" size="{size.menu}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label1}" size="{size.label1}" font="Regular;14" backgroundColor="#ffffff" />\n            <ePixmap name="ButtonRed" pixmap="%s/pictures/button_red_%s.png" position="{pos.but_red}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget name="ButtonRedText" position="{pos.but_red}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonGreen" pixmap="%s/pictures/button_green_%s.png" position="{pos.but_green}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget name="ButtonGreenText" position="{pos.but_green}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonBlue" pixmap="%s/pictures/button_blue_%s.png" position="{pos.but_blue}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget name="ButtonBlueText" position="{pos.but_blue}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n        </screen>' % (path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)))

    def __init__(self, session, idx_config, config):
        size_h_screen = y_Pos_Screen(170)
        self.dict_text = {'size.pos_h': ('%.0f' % float(int(size_h_screen))), 'title.screen': ('CCcamOscamInfo Oscam Restart/Shutdown Server Info Ver. %s' % version)}
        self.dict_var = {'size.screen': '455,170', 'pos.menu': '10,10', 
           'size.menu': '435,100', 
           'pos.label1': '10,120', 
           'size.label1': '435,2', 
           'size.but': '140,50', 
           'pos.but_red': '10,130', 
           'pos.but_green': '155, 130', 
           'pos.but_blue': '300, 130'}
        self.skin = SkinVars(OscamRestatServer.raw_skin, self.dict_text, self.dict_var)
        self['ButtonBlueText'] = Label(_('Restart'))
        self['ButtonGreenText'] = Label(_('Shutdown'))
        self['ButtonRedText'] = Label(_('Back'))
        self['menu'] = Menu([])
        self['actions'] = ActionMap(['CCcamOscamInfoActions'], {'cancel': (self.red), 'red': (self.red), 
           'green': (self.green), 
           'blue': (self.blue)}, -1)
        self.session = session
        self.idx_config = idx_config
        self.config = config
        self.timer_restart = eTimer()
        self.timer_restart_conn = self.timer_restart.timeout.connect(self.makeList)
        self.makeList()
        self.timer_restart.start(10000)
        Screen.__init__(self, session)
        return

    def makeList(self):
        self.data = {'Version': 'NA', 'Revision': 'NA', 
           'Starttime': 'NA', 
           'Uptime': 'NA', 
           'Readonly': 'NA'}
        ret, res = read_Web(self.config, self.idx_config, 'oscamapi.html?part=status')
        if ret == 1:
            self.data = restart_shutdown_oscam(ret, res)
        list = []
        list.append(makeListShutdownRestart(_('Version') + ':', self.data['Version']))
        list.append(makeListShutdownRestart(_('Revision') + ':', self.data['Revision']))
        list.append(makeListShutdownRestart(_('Starttime') + ':', self.data['Starttime']))
        list.append(makeListShutdownRestart(_('Uptime') + ':', self.data['Uptime']))
        list.append(makeListShutdownRestart(_('Readonly') + ':', self.data['Readonly']))
        self['menu'].selectionEnabled(0)
        self['menu'].setList(list)
        return

    def blue(self):
        text = _('Restart Oscam Server?')
        self.session.openWithCallback(self.callAnswerRestart, MessageBox, text, MessageBox.TYPE_YESNO)
        return

    def green(self):
        text = _('Shutdown Oscam Server?')
        self.session.openWithCallback(self.callAnswerShutdown, MessageBox, text, MessageBox.TYPE_YESNO)
        return

    def red(self):
        self.timer_restart.stop()
        self.close()
        return

    def callAnswerRestart(self, answer):
        if answer:
            ret, res = read_Web(self.config, self.idx_config, 'oscamapi.html?part=shutdown&action=restart')
        else:
            self.close()
        return

    def callAnswerShutdown(self, answer):
        if answer:
            ret, res = read_Web(self.config, self.idx_config, 'oscamapi.html?part=shutdown&action=shutdown')
        else:
            self.close()
        return


class CCcamOscamInfoConfigScreen(Screen, ConfigListScreen):
    raw_skin = '\n        <screen position="center,80" size="{size.screen}" title="{title.screen}">\n            <widget name="config" position="{pos.config}" size="{size.config}" itemHeight="25" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label1}" size="{size.label1}" font="Regular;14" backgroundColor="#ffffff" />\n            <ePixmap name="ButtonRed" pixmap="%s/pictures/button_red_%s.png" position="{pos.but_red}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonRedText" position="{pos.but_red}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonGreen" pixmap="%s/pictures/button_green_%s.png" position="{pos.but_green}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonGreenText" position="{pos.but_green}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonYellow" pixmap="%s/pictures/button_yellow_%s.png" position="{pos.but_yellow}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonYellowText" position="{pos.but_yellow}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonBlue" pixmap="%s/pictures/button_blue_%s.png" position="{pos.but_blue}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonBlueText" position="{pos.but_blue}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n        </screen>' % (path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)),
     path,
     used_skin,
     int('%.0f' % (font_size * scale_y)))

    def __init__(self, session, config, idx_config, edit_mode):
        self.dict_text = {'title.screen': ('CCcamOscamInfos Config Screen %s' % version)}
        self.dict_var = {'size.screen': '595,300', 'pos.config': '10,10', 
           'size.config': '575,230', 
           'pos.label1': '10,250', 
           'size.label1': '575,2', 
           'size.but': '140,50', 
           'pos.but_red': '10,260', 
           'pos.but_green': '160,260', 
           'pos.but_yellow': '310,260', 
           'pos.but_blue': '460,260'}
        self.session = session
        self.config = config
        self.idx_config = idx_config
        self.edit_mode = edit_mode
        self.config_vars = {}
        self.skin = SkinVars(CCcamOscamInfoConfigScreen.raw_skin, self.dict_text, self.dict_var)
        self.config_vars = self.set_variables(self.edit_mode)
        if self.edit_mode == 'edit':
            self.cam = ConfigSelection(default=self.config_vars['cam'], choices=[(self.config_vars['cam'], self.config_vars['cam'])])
        else:
            self.cam = ConfigSelection(default=self.config_vars['cam'], choices=[('CCcamLocal', 'CCcam local'), ('CCcamRemote', 'CCcam remote'), ('Oscam', 'Oscam')])
        self.http = ConfigSelection(default=self.config_vars['http'], choices=['http', 'https'])
        self.serverName = ConfigText(default=self.config_vars['name'], fixed_size=False, visible_width=40)
        self.serverIP = ConfigText(default=self.config_vars['url'], fixed_size=False, visible_width=40)
        self.serverPort = ConfigInteger(default=int(self.config_vars['port']), limits=(0,
                                                                                       65536))
        self.username = ConfigText(default=self.config_vars['user'], fixed_size=False, visible_width=40)
        self.password = ConfigPassword(default=self.config_vars['password'], fixed_size=False)
        self.changeconfig = ConfigSelection(default=self.config_vars['changeconfig'], choices=[('yes', _('Yes')), ('no', _('No'))])
        self.configPath = ConfigText(default=self.config_vars['path'], fixed_size=False, visible_width=40)
        self.partnerbox = ConfigSelection(default=self.config_vars['partnerbox'], choices=[('yes', _('Yes')), ('no', _('No'))])
        self.partnerboxpassword = ConfigPassword(default=self.config_vars['partnerboxpassword'], fixed_size=False)
        self.partnerboxsshport = ConfigInteger(default=int(self.config_vars['partnerboxsshport']), limits=(0,
                                                                                                           65536))
        Screen.__init__(self, session)
        ConfigListScreen.__init__(self, [], session=session)
        self['ButtonBlueText'] = StaticText('')
        self['ButtonGreenText'] = StaticText(_('Save config'))
        self['ButtonYellowText'] = StaticText('')
        self['ButtonRedText'] = StaticText(_('Back'))
        self['actions'] = ActionMap(['CCcamOscamInfoActions'], {'cancel': (self.close), 'red': (self.red), 
           'green': (self.green), 
           'blue': (self.blue), 
           'yellow': (self.yellow)}, -1)
        self.onLayoutFinish.append(self.makeList)
        return

    def makeList(self):
        self.list = []
        self.list.append(getConfigListEntry(_('Cam (CCcam or Oscam)'), self.cam))
        self.list.append(getConfigListEntry(_('Webinterface (http or https)'), self.http))
        self.list.append(getConfigListEntry(_('Server name'), self.serverName))
        if self.cam.value == 'CCcamRemote' or self.cam.value == 'Oscam':
            self.list.append(getConfigListEntry(_('Server IP/URL'), self.serverIP))
        self.list.append(getConfigListEntry(_('Server port'), self.serverPort))
        self.list.append(getConfigListEntry(_('Username'), self.username))
        self.list.append(getConfigListEntry(_('Password'), self.password))
        if self.cam.value == 'CCcamLocal' and self.edit_mode == 'new':
            self.configPath = ConfigText(default='/etc', fixed_size=False, visible_width=40)
        if self.cam.value == 'CCcamLocal':
            self.list.append(getConfigListEntry(_('Do you want Change the CCcam.cfg over the plugin?'), self.changeconfig))
            if self.changeconfig.value == 'yes':
                self.list.append(getConfigListEntry(_('Configfile path (optional)'), self.configPath))
        if self.cam.value == 'CCcamRemote':
            self.list.append(getConfigListEntry(_('Do you want ECM info from the Partnerbox?'), self.partnerbox))
            if self.partnerbox.value == 'yes':
                self.list.append(getConfigListEntry(_('SSH Password from the Partnerbox'), self.partnerboxpassword))
                self.list.append(getConfigListEntry(_('SSH Port from the Partnerbox'), self.partnerboxsshport))
        self['config'].setList(self.list)
        return

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.makeList()
        return

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.makeList()
        return

    def green(self):
        if self.cam.value == '':
            self.cam.value = 'None'
        if self.http.value == '':
            self.http.value = 'None'
        if self.serverName.value == '':
            self.serverName.value = 'None'
        if self.serverIP.value == '':
            self.serverIP.value = 'None'
        if self.serverPort.value == '':
            self.serverPort.value = 'None'
        if self.username.value == '':
            self.username.value = 'None'
        if self.password.value == '':
            self.password.value = 'None'
        if self.cam.value == 'CCcamLocal':
            if self.changeconfig.value == '':
                self.changeconfig.value = 'None'
            if self.configPath.value == '':
                self.configPath.value = 'None'
        elif self.cam.value == 'CCcamRemote':
            if self.partnerbox.value == '':
                self.partnerbox.value = 'None'
            if self.partnerboxpassword.value == '':
                self.partnerboxpassword.value = 'None'
                partnerboxsshport
            if self.partnerboxsshport.value == '':
                self.partnerboxsshport.value = 22
        if self.edit_mode == 'new':
            self.config_vars = {'cam': (self.cam.value), 'default': '0', 'http': (self.http.value), 
               'name': (self.serverName.value), 
               'url': (self.serverIP.value), 
               'port': (self.serverPort.value), 
               'user': (self.username.value), 
               'password': (self.password.value)}
            if self.cam.value == 'CCcamLocal':
                self.config_vars.update({'changeconfig': (self.changeconfig.value)})
                if self.changeconfig.value == 'yes':
                    self.config_vars.update({'path': (self.configPath.value)})
            elif self.cam.value == 'CCcamRemote':
                self.config_vars.update({'partnerbox': (self.partnerbox.value)})
                if self.partnerbox.value == 'yes':
                    self.config_vars.update({'partnerboxpassword': (self.partnerboxpassword.value), 'partnerboxsshport': (self.partnerboxsshport.value)})
            self.config.append(self.config_vars)
            self.idx_config = 0
        elif self.edit_mode == 'edit':
            self.config_vars = {'cam': (self.cam.value), 'default': (self.config[self.idx_config]['default']), 'http': (self.http.value), 
               'name': (self.serverName.value), 
               'url': (self.serverIP.value), 
               'port': (self.serverPort.value), 
               'user': (self.username.value), 
               'password': (self.password.value)}
            if self.cam.value == 'CCcamLocal':
                self.config_vars.update({'changeconfig': (self.changeconfig.value)})
                if self.changeconfig.value == 'yes':
                    self.config_vars.update({'path': (self.configPath.value)})
            elif self.cam.value == 'CCcamRemote':
                self.config_vars.update({'partnerbox': (self.partnerbox.value)})
                if self.partnerbox.value == 'yes':
                    self.config_vars.update({'partnerboxpassword': (self.partnerboxpassword.value), 'partnerboxsshport': (self.partnerboxsshport.value)})
            ret = del_Config()
            self.config[self.idx_config] = self.config_vars
        ret = save_Config(self.config)
        self.close()
        return

    def blue(self):
        return

    def yellow(self):
        return

    def red(self):
        self.close()
        return

    def set_variables(self, edit_mode):
        self.edit_mode = edit_mode
        self.config_vars = {'cam': '', 'default': '', 
           'http': '', 
           'name': '', 
           'url': '', 
           'port': '', 
           'user': '', 
           'password': '', 
           'path': '', 
           'partnerbox': '', 
           'partnerboxpassword': '', 
           'partnerboxsshport': '', 
           'changeconfig': ''}
        if self.edit_mode == 'edit':
            self.config_vars.update(self.config[self.idx_config])
        elif self.edit_mode == 'new':
            self.config_vars = {'cam': 'CCcamLocal', 'default': '0', 'http': 'http', 
               'name': 'localhost', 
               'url': '127.0.0.1', 
               'port': '16001', 
               'user': 'None', 
               'password': 'None', 
               'path': '/etc', 
               'partnerbox': 'no', 
               'partnerboxpassword': 'None', 
               'partnerboxsshport': '22', 
               'changeconfig': 'no'}
        return self.config_vars


def makeMenuShort(tmp):
    res = [
     tmp]
    res.append(MultiContentEntryText(pos=(0, 0), size=(110 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp))
    return res


def makeListCCcamOscamTextList(tmp0, tmp1):
    res = [
     tmp1]
    png = '%s/pictures/%s_%s.png' % (path, str(tmp0), used_skin)
    if fileExists(png):
        res.append(MultiContentEntryPixmapAlphaBlend(pos=(0, 4), size=(18 * scale_x, 18 * scale_y), png=loadPNG(png)))
    res.append(MultiContentEntryText(pos=(30 * scale_x, 0), size=(605 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp1))
    return res


def makeListCCcamOScamSelectCam(tmp0, tmp1, tmp2, tmp3):
    res = [
     (
      tmp1, tmp2, tmp3)]
    png = ''
    if tmp0 == 'nopic':
        png = 'nopic'
    elif int(tmp0) == 1:
        png = '%s/pictures/lock_on_%s.png' % (path, used_skin)
    else:
        png = '%s/pictures/lock_off_%s.png' % (path, used_skin)
    if fileExists(png):
        res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 2), size=(20 * scale_x, 20 * scale_y), png=loadPNG(png)))
    res.append(MultiContentEntryText(pos=(25 * scale_x, 0), size=(90 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp1))
    res.append(MultiContentEntryText(pos=(120 * scale_x, 0), size=(270 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp2))
    res.append(MultiContentEntryText(pos=(400 * scale_x, 0), size=(200 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp3))
    return res


def makeListCCcamOScamStart(tmp0):
    res = [
     tmp0]
    res.append(MultiContentEntryText(pos=(5, 0), size=(590 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp0))
    return res


def makeListFooterStart(tmp0, tmp1, tmp2, tmp3, cam):
    res = [
     (
      tmp0,
      tmp1,
      tmp2,
      tmp3)]
    if cam == 'CCcam':
        res.append(MultiContentEntryText(pos=(5, 0), size=(290 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp0))
        res.append(MultiContentEntryText(pos=(300 * scale_x, 0), size=(290 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp1))
        res.append(MultiContentEntryText(pos=(5, 20 * scale_y), size=(290 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp2))
        res.append(MultiContentEntryText(pos=(300 * scale_x, 20 * scale_y), size=(290 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp3))
    elif cam == 'Oscam':
        res.append(MultiContentEntryText(pos=(5, 0), size=(380 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp0))
        res.append(MultiContentEntryText(pos=(390 * scale_x, 0), size=(200 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp1))
        res.append(MultiContentEntryText(pos=(5, 20 * scale_y), size=(380 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp3))
        res.append(MultiContentEntryText(pos=(390 * scale_x, 20 * scale_y), size=(200 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp2))
    else:
        res.append(MultiContentEntryText(pos=(5, 0), size=(290 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp0))
        res.append(MultiContentEntryText(pos=(300 * scale_x, 0), size=(290 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp1))
        res.append(MultiContentEntryText(pos=(5, 20 * scale_y), size=(290 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp2))
        res.append(MultiContentEntryText(pos=(300 * scale_x, 20 * scale_y), size=(290 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp3))
    return res


def makeListClients(tmp0, tmp1, tmp2):
    res = [
     (
      tmp0, tmp2)]
    png = '%s/pictures/%s_%s.png' % (path, str(tmp1), used_skin)
    if fileExists(png):
        res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 4), size=(18 * scale_x, 18 * scale_y), png=loadPNG(png)))
    res.append(MultiContentEntryText(pos=(25 * scale_x, 0), size=(140 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp0))
    res.append(MultiContentEntryText(pos=(170 * scale_x, 0), size=(465 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp2))
    return res


def makeListClientsHeader(tmp0, tmp1):
    res = [
     (
      tmp0, tmp1)]
    res.append(MultiContentEntryText(pos=(5, 0), size=(160 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp0))
    res.append(MultiContentEntryText(pos=(175 * scale_x, 0), size=(465 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp1))
    return res


def makeListClientsFooter(tmp0, tmp1, tmp2, tmp3, tmp4, tmp5, tmp6, tmp7):
    res = [
     (
      tmp0,
      tmp1,
      tmp2,
      tmp3,
      tmp4,
      tmp5,
      tmp6,
      tmp7)]
    res.append(MultiContentEntryText(pos=(0, 0), size=(100 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('Username') + ':'))
    res.append(MultiContentEntryText(pos=(250 * scale_x, 0), size=(110 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('Host') + ':'))
    res.append(MultiContentEntryText(pos=(0, 20 * scale_y), size=(100 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('Connected') + ':'))
    res.append(MultiContentEntryText(pos=(250 * scale_x, 20 * scale_y), size=(110 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('Idle time') + ':'))
    res.append(MultiContentEntryText(pos=(0, 40 * scale_y), size=(100 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('ECM') + ':'))
    res.append(MultiContentEntryText(pos=(250 * scale_x, 40 * scale_y), size=(110 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('EMM') + ':'))
    res.append(MultiContentEntryText(pos=(0, 60 * scale_y), size=(100 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('Version') + ':'))
    res.append(MultiContentEntryText(pos=(250 * scale_x, 60 * scale_y), size=(125 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('Last used share') + ':'))
    res.append(MultiContentEntryText(pos=(110 * scale_x, 0), size=(130 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp0))
    res.append(MultiContentEntryText(pos=(380 * scale_x, 0), size=(255 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp1))
    res.append(MultiContentEntryText(pos=(110 * scale_x, 20 * scale_y), size=(130 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp2))
    res.append(MultiContentEntryText(pos=(380 * scale_x, 20 * scale_y), size=(255 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp3))
    res.append(MultiContentEntryText(pos=(110 * scale_x, 40 * scale_y), size=(130 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp4))
    res.append(MultiContentEntryText(pos=(380 * scale_x, 40 * scale_y), size=(255 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp5))
    res.append(MultiContentEntryText(pos=(110 * scale_x, 60 * scale_y), size=(130 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp6))
    res.append(MultiContentEntryText(pos=(380 * scale_x, 60 * scale_y), size=(255 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp7))
    return res


def makeListServerGeneral(tmp0, tmp1, tmp2, tmp3, tmp4):
    res = [
     (
      tmp1,
      tmp2,
      tmp3,
      tmp4)]
    png = '%s/pictures/%s_%s.png' % (path, str(tmp0), used_skin)
    if fileExists(png):
        res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 4), size=(18 * scale_x, 18 * scale_y), png=loadPNG(png)))
    res.append(MultiContentEntryText(pos=(25 * scale_x, 0), size=(330 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp1))
    res.append(MultiContentEntryText(pos=(360 * scale_x, 0), size=(160 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text='%s  %s' % (tmp2, tmp3)))
    res.append(MultiContentEntryText(pos=(530 * scale_x, 0), size=(75 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp4))
    return res


def makeListServerGeneralHeader(tmp0, tmp1, tmp2):
    res = [
     (
      tmp0, tmp1, tmp2)]
    res.append(MultiContentEntryText(pos=(0, 0), size=(350 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp0))
    res.append(MultiContentEntryText(pos=(360 * scale_x, 0), size=(160 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp1))
    res.append(MultiContentEntryText(pos=(530 * scale_x, 0), size=(75 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp2))
    return res


def makeListServerGeneralFooter(tmp0, tmp1, tmp2, tmp3, tmp4, tmp5):
    res = [
     (
      tmp0,
      tmp1,
      tmp2,
      tmp3,
      tmp4,
      tmp5)]
    res.append(MultiContentEntryText(pos=(0, 0), size=(90 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('Host') + ':'))
    res.append(MultiContentEntryText(pos=(315 * scale_x, 0), size=(90 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('Connected') + ':'))
    res.append(MultiContentEntryText(pos=(0, 20 * scale_y), size=(90 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('Type') + ':'))
    res.append(MultiContentEntryText(pos=(315 * scale_x, 20 * scale_y), size=(90 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('NodeID') + ':'))
    res.append(MultiContentEntryText(pos=(0, 40 * scale_y), size=(90 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('Version') + ':'))
    res.append(MultiContentEntryText(pos=(315 * scale_x, 40 * scale_y), size=(90 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('Cards') + ':'))
    res.append(MultiContentEntryText(pos=(100 * scale_x, 0), size=(205 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp0))
    res.append(MultiContentEntryText(pos=(415 * scale_x, 0), size=(205 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp1))
    res.append(MultiContentEntryText(pos=(100 * scale_x, 20 * scale_y), size=(205 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp2))
    res.append(MultiContentEntryText(pos=(415 * scale_x, 20 * scale_y), size=(205 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp4))
    res.append(MultiContentEntryText(pos=(100 * scale_x, 40 * scale_y), size=(205 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp3))
    res.append(MultiContentEntryText(pos=(415 * scale_x, 40 * scale_y), size=(205 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp5))
    return res


def makeListServersHeaderFooter(tmp0, tmp1, tmp2, tmp3, tmp4, tmp5):
    res = [
     (
      tmp0,
      tmp1,
      tmp2,
      tmp3,
      tmp4,
      tmp5)]
    res.append(MultiContentEntryText(pos=(0, 0), size=(300 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp0))
    res.append(MultiContentEntryText(pos=(330 * scale_x, 0), size=(48 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp1))
    res.append(MultiContentEntryText(pos=(385 * scale_x, 0), size=(48 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp2))
    res.append(MultiContentEntryText(pos=(440 * scale_x, 0), size=(48 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp3))
    res.append(MultiContentEntryText(pos=(495 * scale_x, 0), size=(48 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp4))
    res.append(MultiContentEntryText(pos=(550 * scale_x, 0), size=(48 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp5))
    return res


def makeListServers(tmp0, tmp1, tmp2, tmp3, tmp4, tmp5, tmp6, tmp7):
    res = [
     (
      tmp0,
      tmp3,
      tmp4,
      tmp5,
      tmp6,
      tmp7)]
    png1 = '%s/pictures/%s_%s.png' % (path, str(tmp1), used_skin)
    png2 = '%s/pictures/%s_%s.png' % (path, str(tmp2), used_skin)
    if fileExists(png1):
        res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 4), size=(18 * scale_x, 18 * scale_y), png=loadPNG(png1)))
    if fileExists(png2):
        res.append(MultiContentEntryPixmapAlphaBlend(pos=(25 * scale_x, 4), size=(18 * scale_x, 18 * scale_y), png=loadPNG(png2)))
    res.append(MultiContentEntryText(pos=(40 * scale_x, 0), size=(300 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp0))
    res.append(MultiContentEntryText(pos=(330 * scale_x, 0), size=(48 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp3))
    res.append(MultiContentEntryText(pos=(385 * scale_x, 0), size=(48 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp4))
    res.append(MultiContentEntryText(pos=(440 * scale_x, 0), size=(48 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp5))
    res.append(MultiContentEntryText(pos=(495 * scale_x, 0), size=(48 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp6))
    res.append(MultiContentEntryText(pos=(550 * scale_x, 0), size=(48 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp7))
    return res


def makeListPingHeader(tmp0, tmp1, tmp2, tmp3):
    res = [
     (
      tmp0,
      tmp1,
      tmp2,
      tmp3)]
    res.append(MultiContentEntryText(pos=(0, 0), size=(290 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp0))
    res.append(MultiContentEntryText(pos=(375 * scale_x, 0), size=(75 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp1))
    res.append(MultiContentEntryText(pos=(460 * scale_x, 0), size=(75 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp2))
    res.append(MultiContentEntryText(pos=(545 * scale_x, 0), size=(75 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp3))
    return res


def makeListPing(tmp0, tmp1, tmp2, tmp3, tmp4):
    res = [
     (
      tmp0,
      tmp2,
      tmp3,
      tmp4)]
    png = '%s/pictures/%s_%s.png' % (path, str(tmp1), used_skin)
    if fileExists(png):
        res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 4), size=(18 * scale_x, 18 * scale_y), png=loadPNG(png)))
    res.append(MultiContentEntryText(pos=(25 * scale_x, 0), size=(355 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp0))
    res.append(MultiContentEntryText(pos=(375 * scale_x, 0), size=(75 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp2))
    res.append(MultiContentEntryText(pos=(460 * scale_x, 0), size=(75 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp3))
    res.append(MultiContentEntryText(pos=(545 * scale_x, 0), size=(75 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp4))
    return res


def makeListProviders(tmp0, tmp1, tmp2):
    res = [
     (
      tmp0, tmp1, tmp2)]
    res.append(MultiContentEntryText(pos=(0, 0), size=(80 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp0))
    res.append(MultiContentEntryText(pos=(90 * scale_x, 0), size=(305 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp1))
    res.append(MultiContentEntryText(pos=(405 * scale_x, 0), size=(100 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp2))
    return res


def makeListShares(tmp0, tmp1, tmp2, tmp3, tmp4, tmp5):
    res = [
     (
      tmp0,
      tmp1,
      tmp2,
      tmp3,
      tmp4,
      tmp5)]
    res.append(MultiContentEntryText(pos=(0, 0), size=(200 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp0))
    res.append(MultiContentEntryText(pos=(205 * scale_x, 0), size=(50 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp1))
    res.append(MultiContentEntryText(pos=(260 * scale_x, 0), size=(70 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp2))
    res.append(MultiContentEntryText(pos=(335 * scale_x, 0), size=(95 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp3))
    res.append(MultiContentEntryText(pos=(435 * scale_x, 0), size=(20 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp4))
    res.append(MultiContentEntryText(pos=(460 * scale_x, 0), size=(20 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp5))
    return res


def makeListPairs(tmp0, tmp1, tmp2):
    res = [
     (
      tmp0, tmp1, tmp2)]
    res.append(MultiContentEntryText(pos=(0, 0), size=(250 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp0))
    res.append(MultiContentEntryText(pos=(260 * scale_x, 0), size=(200 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp1))
    res.append(MultiContentEntryText(pos=(470 * scale_x, 0), size=(165 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp2))
    return res


def makeListPairsUsers(tmp0, tmp1):
    res = [
     (
      tmp0, tmp1)]
    res.append(MultiContentEntryText(pos=(0, 0), size=(460 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp0))
    res.append(MultiContentEntryText(pos=(470 * scale_x, 0), size=(165 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp1))
    return res


def makeListPairsDetails(tmp0):
    res = [
     tmp0]
    res.append(MultiContentEntryText(pos=(0, 0), size=(590 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp0))
    return res


def makeECMList(tmp0, tmp1):
    res = [
     (
      tmp0, tmp1)]
    res.append(MultiContentEntryText(pos=(0, 0), size=(120 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp0))
    res.append(MultiContentEntryText(pos=(130 * scale_x, 0), size=(505 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp1))
    return res


def makeListEnableDisableClineFlineHeader(tmp0):
    res = [
     tmp0]
    res.append(MultiContentEntryText(pos=(0, 0), size=(635 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp0))
    return res


def makeListEnableDisableClineFline(tmp0, tmp1):
    res = [
     (
      tmp0, tmp1)]
    png1 = '%s/pictures/lock_off_%s.png' % (path, used_skin)
    if tmp0 == 'C:' or tmp0 == 'F:':
        png1 = '%s/pictures/lock_on_%s.png' % (path, used_skin)
    elif tmp0 == '#C:' or tmp0 == '#F:':
        png1 = '%s/pictures/lock_off_%s.png' % (path, used_skin)
    if fileExists(png1):
        res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 2), size=(20 * scale_x, 20 * scale_y), png=loadPNG(png1)))
    res.append(MultiContentEntryText(pos=(25 * scale_x, 0), size=(615 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp1))
    return res


def makeListEnableDisableClineFlineBackup(tmp0):
    res = [
     tmp0]
    res.append(MultiContentEntryText(pos=(0, 0), size=(435 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp0))
    return res


def makeListOscamGeneralMenuOscam(tmp0, tmp1, tmp2, tmp3, tmp4, tmp5, tmp6, tmp7, tmp8, tmp9):
    res = [
     (
      tmp0,
      tmp1,
      tmp2,
      tmp3,
      tmp4,
      tmp5,
      tmp6,
      tmp7,
      tmp8,
      tmp9)]
    res.append(MultiContentEntryText(pos=(0, 0), size=(90 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text='%s:' % tmp0))
    res.append(MultiContentEntryText(pos=(100 * scale_x, 0), size=(235 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp1))
    res.append(MultiContentEntryText(pos=(340 * scale_x, 0), size=(90 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text='%s:' % tmp2))
    res.append(MultiContentEntryText(pos=(440 * scale_x, 0), size=(195 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp3))
    res.append(MultiContentEntryText(pos=(0, 20 * scale_y), size=(90 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text='%s:' % tmp4))
    res.append(MultiContentEntryText(pos=(100 * scale_x, 20 * scale_y), size=(235 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp5))
    res.append(MultiContentEntryText(pos=(340 * scale_x, 20 * scale_y), size=(90 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text='%s:' % tmp6))
    res.append(MultiContentEntryText(pos=(440 * scale_x, 20 * scale_y), size=(195 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp7))
    res.append(MultiContentEntryText(pos=(0, 40 * scale_y), size=(90 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text='%s:' % tmp8))
    res.append(MultiContentEntryText(pos=(100 * scale_x, 40 * scale_y), size=(235 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp9))
    return res


def makeListOscamGeneral(tmp0, tmp1, tmp2, tmp3, tmp4, tmp5, tmp6, tmp7, tmp8, tmp9, tmp10, tmp11):
    res = [
     (
      tmp0,
      tmp1,
      tmp2,
      tmp3,
      tmp4,
      tmp5,
      tmp6,
      tmp7,
      tmp8,
      tmp9,
      tmp10,
      tmp11)]
    res.append(MultiContentEntryText(pos=(0, 0), size=(90 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text='%s:' % tmp0))
    res.append(MultiContentEntryText(pos=(100 * scale_x, 0), size=(70 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp1))
    res.append(MultiContentEntryText(pos=(320 * scale_x, 0), size=(90 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text='%s:' % tmp2))
    res.append(MultiContentEntryText(pos=(420 * scale_x, 0), size=(70 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp3))
    res.append(MultiContentEntryText(pos=(0, 20 * scale_y), size=(90 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text='%s:' % tmp4))
    res.append(MultiContentEntryText(pos=(100 * scale_x, 20 * scale_y), size=(70 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp5))
    res.append(MultiContentEntryText(pos=(320 * scale_x, 20 * scale_y), size=(90 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text='%s:' % tmp6))
    res.append(MultiContentEntryText(pos=(420 * scale_x, 20 * scale_y), size=(70 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp7))
    res.append(MultiContentEntryText(pos=(0, 40 * scale_y), size=(90 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text='%s:' % tmp8))
    res.append(MultiContentEntryText(pos=(100 * scale_x, 40 * scale_y), size=(70 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp9))
    res.append(MultiContentEntryText(pos=(320 * scale_x, 40 * scale_y), size=(90 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text='%s:' % tmp10))
    res.append(MultiContentEntryText(pos=(420 * scale_x, 40 * scale_y), size=(70 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp11))
    return res


def makeListClientsOscamHeader(tmp0, tmp1, tmp2, tmp3):
    res = [
     (
      tmp0,
      tmp1,
      tmp2,
      tmp3)]
    res.append(MultiContentEntryText(pos=(0, 0), size=(130 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp0))
    res.append(MultiContentEntryText(pos=(140 * scale_x, 0), size=(30 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_CENTER, text=tmp1))
    res.append(MultiContentEntryText(pos=(170 * scale_x, 0), size=(345 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp2))
    res.append(MultiContentEntryText(pos=(525 * scale_x, 0), size=(110 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp3))
    return res


def makeListClientsOscam(tmp0, tmp1, tmp2, tmp3):
    res = [
     (
      tmp0, tmp2, tmp3)]
    png = '%s/pictures/%s_%s.png' % (path, str(tmp1), used_skin)
    res.append(MultiContentEntryText(pos=(0, 0), size=(130 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp0))
    if fileExists(png):
        res.append(MultiContentEntryPixmapAlphaBlend(pos=(145, 2), size=(16 * scale_x, 16 * scale_y), png=loadPNG(png)))
    res.append(MultiContentEntryText(pos=(170 * scale_x, 0), size=(345 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp2))
    res.append(MultiContentEntryText(pos=(525 * scale_x, 0), size=(110 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp3))
    return res


def makeListAllClientsOscamHeader(tmp0, tmp1, tmp2):
    res = [
     (
      tmp0, tmp1, tmp2)]
    res.append(MultiContentEntryText(pos=(0, 0), size=(200 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp0))
    res.append(MultiContentEntryText(pos=(210 * scale_x, 0), size=(100 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_CENTER, text=tmp1))
    res.append(MultiContentEntryText(pos=(320 * scale_x, 0), size=(315 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp2))
    return res


def makeListAllClientsOscam(tmp0, tmp1, tmp2, tmp3):
    res = [
     (
      tmp1, tmp2, tmp3)]
    png = '%s/pictures/%s_%s.png' % (path, str(tmp0), used_skin)
    if fileExists(png):
        res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 4), size=(18 * scale_x, 18 * scale_y), png=loadPNG(png)))
    res.append(MultiContentEntryText(pos=(25 * scale_x, 0), size=(180 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp1))
    res.append(MultiContentEntryText(pos=(210 * scale_x, 0), size=(100 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp2))
    res.append(MultiContentEntryText(pos=(320 * scale_x, 0), size=(315 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp3))
    return res


def makeListAllReadersOscamHeader(tmp0, tmp1, tmp2):
    res = [
     (
      tmp0, tmp1, tmp2)]
    res.append(MultiContentEntryText(pos=(0, 0), size=(250 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp0))
    res.append(MultiContentEntryText(pos=(260 * scale_x, 0), size=(330 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp1))
    res.append(MultiContentEntryText(pos=(600 * scale_x, 0), size=(35 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp2))
    return res


def makeListAllReadersOscam(tmp0, tmp1, tmp2, tmp3):
    res = [
     (
      tmp1, tmp2, tmp3)]
    png = '%s/pictures/%s_%s.png' % (path, str(tmp0), used_skin)
    if fileExists(png):
        res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 4), size=(18 * scale_x, 18 * scale_y), png=loadPNG(png)))
    res.append(MultiContentEntryText(pos=(25 * scale_x, 0), size=(230 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp1))
    res.append(MultiContentEntryText(pos=(260 * scale_x, 0), size=(330 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp2))
    res.append(MultiContentEntryText(pos=(600 * scale_x, 0), size=(35 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_CENTER, text=tmp3))
    return res


def makeListClientsOscamFooterTime(tmp0, tmp1, tmp2, tmp3, tmp4, tmp5):
    res = [
     (
      tmp0,
      tmp1,
      tmp2,
      tmp3,
      tmp4,
      tmp5)]
    res.append(MultiContentEntryText(pos=(0, 0), size=(75 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text='Login:'))
    res.append(MultiContentEntryText(pos=(85 * scale_x, 0), size=(220 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp0))
    res.append(MultiContentEntryText(pos=(315 * scale_x, 0), size=(90 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('Protocol') + ':'))
    res.append(MultiContentEntryText(pos=(415 * scale_x, 0), size=(220 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp1))
    res.append(MultiContentEntryText(pos=(0, 20 * scale_y), size=(75 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('Online') + ':'))
    res.append(MultiContentEntryText(pos=(85 * scale_x, 20 * scale_y), size=(205 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp2))
    res.append(MultiContentEntryText(pos=(315 * scale_x, 20 * scale_y), size=(90 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('IP-Adress') + ':'))
    res.append(MultiContentEntryText(pos=(415 * scale_x, 20 * scale_y), size=(205 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp3))
    res.append(MultiContentEntryText(pos=(0, 40 * scale_y), size=(75 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('Idle') + ':'))
    res.append(MultiContentEntryText(pos=(85 * scale_x, 40 * scale_y), size=(220 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp4))
    res.append(MultiContentEntryText(pos=(315 * scale_x, 40 * scale_y), size=(90 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('Con. Port') + ':'))
    res.append(MultiContentEntryText(pos=(415 * scale_x, 40 * scale_y), size=(205 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp5))
    return res


def makeListClientsOscamFooterCWEMM(tmp0, tmp1, tmp2, tmp3, tmp4, tmp5, tmp6, tmp7, tmp8, tmp9):
    res = [
     (
      tmp0,
      tmp1,
      tmp2,
      tmp3,
      tmp4,
      tmp5,
      tmp6,
      tmp7,
      tmp8,
      tmp9)]
    res.append(MultiContentEntryText(pos=(0, 0), size=(35 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('CW') + ':'))
    res.append(MultiContentEntryText(pos=(40 * scale_x, 0), size=(61 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('OK') + ':'))
    res.append(MultiContentEntryText(pos=(101 * scale_x, 0), size=(72 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp0))
    res.append(MultiContentEntryText(pos=(183 * scale_x, 0), size=(72 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('NOK') + ':'))
    res.append(MultiContentEntryText(pos=(255 * scale_x, 0), size=(72 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp1))
    res.append(MultiContentEntryText(pos=(337 * scale_x, 0), size=(72 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('Ignore') + ':'))
    res.append(MultiContentEntryText(pos=(409 * scale_x, 0), size=(72 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp2))
    res.append(MultiContentEntryText(pos=(491 * scale_x, 0), size=(72 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('Timeout') + ':'))
    res.append(MultiContentEntryText(pos=(563 * scale_x, 0), size=(72 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp3))
    res.append(MultiContentEntryText(pos=(40 * scale_x, 20 * scale_y), size=(61 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('Cache') + ':'))
    res.append(MultiContentEntryText(pos=(101 * scale_x, 20 * scale_y), size=(72 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp4))
    res.append(MultiContentEntryText(pos=(183 * scale_x, 20 * scale_y), size=(72 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('Tun') + ':'))
    res.append(MultiContentEntryText(pos=(255 * scale_x, 20 * scale_y), size=(72 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp5))
    res.append(MultiContentEntryText(pos=(337 * scale_x, 20 * scale_y), size=(72 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('RespTime') + ':'))
    res.append(MultiContentEntryText(pos=(409 * scale_x, 20 * scale_y), size=(72 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp6))
    res.append(MultiContentEntryText(pos=(491 * scale_x, 20 * scale_y), size=(72 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('Rate') + ':'))
    res.append(MultiContentEntryText(pos=(563 * scale_x, 20 * scale_y), size=(72 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp7))
    res.append(MultiContentEntryText(pos=(0, 40 * scale_y), size=(35 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('EMM') + ':'))
    res.append(MultiContentEntryText(pos=(40 * scale_x, 40 * scale_y), size=(61 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('OK') + ':'))
    res.append(MultiContentEntryText(pos=(101 * scale_x, 40 * scale_y), size=(72 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp8))
    res.append(MultiContentEntryText(pos=(183 * scale_x, 40 * scale_y), size=(72 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('NOK') + ':'))
    res.append(MultiContentEntryText(pos=(255 * scale_x, 40 * scale_y), size=(72 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_RIGHT, text=tmp9))
    return res


def makeListClientsOscamFooterRequest(tmp0, tmp1, tmp2, tmp3, tmp4, tmp5):
    res = [
     (
      tmp0,
      tmp1,
      tmp2,
      tmp3,
      tmp4,
      tmp5)]
    res.append(MultiContentEntryText(pos=(0, 0), size=(90 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('Current Channel') + ':'))
    res.append(MultiContentEntryText(pos=(100 * scale_x, 0), size=(210 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp0))
    res.append(MultiContentEntryText(pos=(315 * scale_x, 0), size=(90 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('Protocol') + ':'))
    res.append(MultiContentEntryText(pos=(415 * scale_x, 0), size=(220 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp1))
    res.append(MultiContentEntryText(pos=(0, 20 * scale_y), size=(205 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('CaID') + ': % s' % tmp2))
    res.append(MultiContentEntryText(pos=(215, 20 * scale_y), size=(205 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('SrvID') + ': % s' % tmp3))
    res.append(MultiContentEntryText(pos=(430, 20 * scale_y), size=(205 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('ECM Time') + ': % s' % tmp4))
    res.append(MultiContentEntryText(pos=(0, 40 * scale_y), size=(635 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=_('ECM History') + ': % s' % tmp5))
    return res


def makeListOscamTextList(tmp0, tmp1):
    res = [
     (
      tmp0, tmp1)]
    res.append(MultiContentEntryText(pos=(0, 0), size=(100 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp0))
    res.append(MultiContentEntryText(pos=(110 * scale_x, 0), size=(525 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp1))
    return res


def EnableDisableClientsReadersProxysHeader(tmp0, tmp1):
    res = [
     (
      tmp0, tmp1)]
    res.append(MultiContentEntryText(pos=(0, 0), size=(475 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp0))
    res.append(MultiContentEntryText(pos=(445 * scale_x, 0), size=(190 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp1))
    return res


def EnableDisableClientsReadersProxys(tmp0, tmp1, tmp2):
    res = [
     (
      tmp1, tmp2)]
    if tmp0 == '1':
        png1 = '%s/pictures/lock_on_%s.png' % (path, used_skin)
    elif tmp0 == '0':
        png1 = '%s/pictures/lock_off_%s.png' % (path, used_skin)
    if fileExists(png1):
        res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 2), size=(20 * scale_x, 20 * scale_y), png=loadPNG(png1)))
    res.append(MultiContentEntryText(pos=(25 * scale_x, 0), size=(455 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp1))
    res.append(MultiContentEntryText(pos=(445 * scale_x, 0), size=(190 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp2))
    return res


def makeListShutdownRestart(tmp0, tmp1):
    res = [
     (
      tmp0, tmp1)]
    res.append(MultiContentEntryText(pos=(0, 0), size=(100 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp0))
    res.append(MultiContentEntryText(pos=(110 * scale_x, 0), size=(525 * scale_x, int('%.0f' % (font_size * scale_y)) + 5), font=0, flags=RT_HALIGN_LEFT, text=tmp1))
    return res


class Menu(MenuList):

    def __init__(self, items, enableWrapAround=False):
        MenuList.__init__(self, items, enableWrapAround, eListboxPythonMultiContent)
        self.l.setFont(0, gFont('Regular', int('%.0f' % (font_size * scale_y))))
        self.l.setFont(1, gFont('Regular', int('%.0f' % ((font_size - 2) * scale_y))))
        self.l.setFont(2, gFont('Regular', int('%.0f' % ((font_size - 4) * scale_y))))
        self.l.setItemHeight(int('%.0f' % (font_size * scale_y)))
        return


class FooterListStart(MenuList):

    def __init__(self, items, enableWrapAround=False):
        MenuList.__init__(self, items, enableWrapAround, eListboxPythonMultiContent)
        self.l.setFont(0, gFont('Regular', int('%.0f' % (font_size * scale_y))))
        self.l.setItemHeight(2 * int('%.0f' % ((font_size + 2) * scale_y)))
        return


class FooterListClientsCCcam(MenuList):

    def __init__(self, items, enableWrapAround=False):
        MenuList.__init__(self, items, enableWrapAround, eListboxPythonMultiContent)
        self.l.setFont(0, gFont('Regular', int('%.0f' % (font_size * scale_y))))
        self.l.setItemHeight(4 * int('%.0f' % ((font_size + 2) * scale_y)))
        return


class FooterListServerGeneralCCcam(MenuList):

    def __init__(self, items, enableWrapAround=False):
        MenuList.__init__(self, items, enableWrapAround, eListboxPythonMultiContent)
        self.l.setFont(0, gFont('Regular', int('%.0f' % (font_size * scale_y))))
        self.l.setItemHeight(3 * int('%.0f' % ((font_size + 2) * scale_y)))
        return


class OscamGeneralList(MenuList):

    def __init__(self, items, enableWrapAround=False):
        MenuList.__init__(self, items, enableWrapAround, eListboxPythonMultiContent)
        self.l.setFont(0, gFont('Regular', int('%.0f' % (font_size * scale_y))))
        self.l.setItemHeight(3 * int('%.0f' % ((font_size + 2) * scale_y)))
        return


class FooterListClientsOscam(MenuList):

    def __init__(self, items, enableWrapAround=False):
        MenuList.__init__(self, items, enableWrapAround, eListboxPythonMultiContent)
        self.l.setFont(0, gFont('Regular', int('%.0f' % (font_size * scale_y))))
        self.l.setItemHeight(3 * int('%.0f' % ((font_size + 2) * scale_y)))
        return


def SkinVars(skin, dict_text, dict_var):
    for key in dict_text.keys():
        skin = skin.replace('{' + key + '}', dict_text[key])

    for key in dict_var.keys():
        if used_skin == 'hd':
            skin = skin.replace('{' + key + '}', '%.0f,%.0f' % (float(dict_var[key].split(',')[0]) * scale_x, float(dict_var[key].split(',')[1]) * scale_y))
        else:
            skin = skin.replace('{' + key + '}', dict_var[key])

    return skin


def y_Pos_Screen(y_size_screen):
    size_h = int(getDesktop(0).size().height())
    size_h_screen = (size_h - scale_y * int(y_size_screen)) / 2 + int(offset)
    return size_h_screen


def debug(debug):
    f = open('/media/hdd/debug.txt', 'a')
    f.write('%s\n' % debug)
    f.close()
    return


return
