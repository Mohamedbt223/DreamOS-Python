# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/Stools/swap.py
# Compiled at: 2015-12-25 15:30:30
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.Button import Button
from Components.config import getConfigListEntry, config, ConfigSelection, ConfigYesNo, ConfigSubsection, ConfigText
from Components.ConfigList import ConfigListScreen
from Tools.Directories import fileExists, resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from enigma import eConsoleAppContainer, getDesktop
from os import environ, popen as os_popen, system as os_system, chmod as os_chmod, remove as os_remove, path as os_path
from tsimage import TSimagePanelImage
from Tools.TSTools import getCmdOutput
from Components.Language import language
import gettext
desktopSize = getDesktop(0).size()

def localeInit():
    lang = language.getLanguage()
    environ['LANGUAGE'] = lang[:2]
    gettext.bindtextdomain('enigma2', resolveFilename(SCOPE_LANGUAGE))
    gettext.textdomain('enigma2')
    gettext.bindtextdomain('TSSwap', '%s%s' % (resolveFilename(SCOPE_PLUGINS), 'TSimage/TSimagePanel/locale/'))
    return


def _(txt):
    t = gettext.dgettext('TSSwap', txt)
    if t == txt:
        t = gettext.gettext(txt)
    return t


localeInit()
language.addCallback(localeInit)
swapmanger_busy = '/tmp/.tsswapmanager'
version = '1.0'
about = _('With TS Swap Manager you can create and mount a real swap partition on your box. You can use all media of your box. \nTS Swap Manager plugin %s \nby colombo555@tunisia-sat.com 2012') % version
config.plugins.TSSwapmanager = ConfigSubsection()
config.plugins.TSSwapmanager.activateonboot = ConfigYesNo(default=False)
config.plugins.TSSwapmanager.mountpoint = ConfigText(default='/media/hdd')

class TSiswapScreen(Screen, ConfigListScreen):
    skin_1280 = '\n                        <screen name="TSiswapScreen" position="center,77" size="920,600" title="Swap Manager"  >\n\t\t\t<widget name="config" position="25,25" size="880,300" scrollbarMode="showOnDemand" transparent="1" zPosition="2" />\n                        <eLabel position="20,350" size="880,2" backgroundColor="white" /> \n\t                <eLabel position="20,382" size="880,2" backgroundColor="white" /> \n                        <eLabel text="Memory" position="25,353" size="130,43" font="Regular;20" backgroundColor="background" halign="center" transparent="1" />                \n\t                <widget name="usedmem" position="25,380" size="130,43" font="Regular;18" backgroundColor="background" valign="center" halign="left"  transparent="1" />\n\t                <widget name="freemem" position="25,405" size="130,43" font="Regular;18" backgroundColor="background" valign="center" halign="left" transparent="1" />\n\t                <widget name="totalmem" position="25,430" size="130,43" font="Regular;18" backgroundColor="background" valign="center" halign="left" transparent="1" />\n\t                <eLabel text="Swap" position="400,353" size="130,43" font="Regular;20" backgroundColor="background" halign="center" transparent="1" />                \n\t                <widget name="usedswap" position="400,380" size="130,43" font="Regular;18" backgroundColor="background" valign="center" halign="left" transparent="1" />\n\t                <widget name="freeswap" position="400,405" size="130,43" font="Regular;18" backgroundColor="background" valign="center" halign="left" transparent="1" />\n\t                <widget name="totalswap" position="400,430" size="130,43" font="Regular;18" backgroundColor="background" valign="center" halign="left" transparent="1" />\n\t                <eLabel text="Total" position="705,353" size="130,43" font="Regular;20" backgroundColor="background" halign="center"  transparent="1" />                \n\t                <widget name="usedtotal" position="705,380" size="130,43" font="Regular;18" backgroundColor="background" valign="center" halign="left" transparent="1" />\n\t                <widget name="freetotal" position="705,405" size="130,43" font="Regular;18" backgroundColor="background" valign="center" halign="left" transparent="1" />\n\t                <widget name="totaltotal" position="705,430" size="130,43" font="Regular;18" backgroundColor="background" valign="center" halign="left" transparent="1" />\n\t                <eLabel position="20,467" size="880,2" backgroundColor="white" />\n                        <eLabel text="Swapfile status:" position="25,135" size="160,43" font="Regular;20" backgroundColor="background" halign="left" transparent="1" />           \n                        <widget name="selstatus" position="640,135" size="230,43" font="Regular;18" backgroundColor="background" halign="right"  transparent="1" />\n                        <widget name="seloffpic" position="880,139" size="16,16" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/grey.png" zPosition="1" alphatest="blend" />\n                        <widget name="selonpic" position="880,139" size="16,16" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green.png" zPosition="1" alphatest="blend" />\n                        <eLabel text="Swap status:" position="25,470" size="160,43" font="Regular;20" backgroundColor="background" halign="left" transparent="1" />           \n                        <widget name="statustext" position="650,470" size="220,43" font="Regular;20" backgroundColor="background" halign="right" transparent="1" />\n                        <widget name="swapoffpic" position="880,477" size="16,16" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/grey.png" zPosition="1" alphatest="blend" />\n                        <widget name="swaponpic" position="880,477" size="16,16" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green.png" zPosition="1" alphatest="blend" />                         \n                        <eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\n                        <widget name="info" position="20,20" size="880,400" font="Regular;22" valign="center" halign="center" transparent="1" />\n\t                <ePixmap name="red"    position="70,545"   zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" transparent="1" alphatest="blend" />\n\t                <ePixmap name="green"  position="280,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_green.png" transparent="1" alphatest="blend" />\n\t                <ePixmap name="yellow" position="490,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_yellow.png" transparent="1" alphatest="blend" /> \n        \t        <ePixmap name="blue"   position="700,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_blue.png" transparent="1" alphatest="blend" /> \n        \t        <widget name="key_red" position="70,550" size="140,40" valign="center" halign="center" zPosition="2"  font="Regular;21" transparent="1" /> \n        \t        <widget name="key_green" position="280,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" /> \n                        <widget name="key_yellow" position="490,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;20" transparent="1" />\n        \t        <widget name="key_blue" position="700,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" />\n                </screen>'
    skin_1920 = '    <screen name="TSiswapScreen" position="center,200" size="1300,720" title="Addons Manager">\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png" position="50,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green-big.png" position="360,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/yellow-big.png" position="670,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/blue-big.png" position="980,640" size="200,40" alphatest="blend" />\n        <widget name="key_red" position="50,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#940d0d" transparent="1" />\n        <widget name="key_green" position="360,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#2d872d" transparent="1" />\n        <widget name="key_yellow" position="670,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#bba502" transparent="1" />\n        <widget name="key_blue" position="980,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#18188b" transparent="1" />\n        <ePixmap position="20,200" size="100,100" scale="1" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/dev_memory.png" transparent="1" alphatest="blend" />\n        <widget source="session.CurrentService" render="Label" position="30,305" size="380,70" foregroundColor="foreground" backgroundColor="background" valign="top" halign="left" zPosition="2" font="Regular;24" transparent="1" >\n        <convert type="TSProgressDiskSpaceInfo">MemTotal,Partial</convert>\n        </widget>\n        <widget source="session.Event_Now" render="Progress" position="140,245" size="300,12" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/memory_bar.png" borderColor="foreground" borderWidth="1" transparent="1" >\n        <convert type="TSProgressDiskSpaceInfo">MemTotal</convert>\n        </widget>\n        <widget source="session.CurrentService" render="Label" position="465,236" size="80,30" foregroundColor="foreground" backgroundColor="background" valign="center" halign="left" zPosition="2" font="Regular;23" transparent="1" >\n        <convert type="TSProgressDiskSpaceInfo">MemTotal,Percent</convert>\n        </widget>\n        <ePixmap position="20,390" size="100,100" scale="1" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/dev_swap.png" transparent="1" alphatest="blend" />\n        <widget source="session.CurrentService" render="Label" position="30,490" size="380,70" foregroundColor="foreground" backgroundColor="background" valign="top" halign="left" zPosition="2" font="Regular;24" transparent="1" >\n        <convert type="TSProgressDiskSpaceInfo">SwapTotal,Partial</convert>\n        </widget>\n        <widget source="session.Event_Now" render="Progress" position="140,430" size="300,12" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/memory_bar.png" borderColor="foreground" borderWidth="1" transparent="1" >\n        <convert type="TSProgressDiskSpaceInfo">SwapTotal</convert>\n        </widget>\n        <widget source="session.CurrentService" render="Label" position="465,421" size="80,30" foregroundColor="foreground" backgroundColor="background" valign="center" halign="left" zPosition="2" font="Regular;23" transparent="1" >\n        <convert type="TSProgressDiskSpaceInfo">SwapTotal,Percent</convert>\n        </widget>\n        <widget name="config" position="20,30" size="1260,600" zPosition="2" itemHeight="40" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background"  transparent="1" />\n        </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session, args=0):
        self.session = session
        Screen.__init__(self, session)
        self.lockswapsize = False
        self.swapexits = False
        self.swappartition = False
        self.size = 256
        self.list = []
        ConfigListScreen.__init__(self, self.list, session=self.session)
        self['key_red'] = Button(_('Close'))
        self['key_green'] = Button(_('Create'))
        self['key_yellow'] = Button(_('Enable'))
        self['key_blue'] = Button(_('Disable'))
        self['selonpic'] = Pixmap()
        self['seloffpic'] = Pixmap()
        self['selstatus'] = Label('')
        self['swaponpic'] = Pixmap()
        self['swapoffpic'] = Pixmap()
        self['statustext'] = Label('')
        self['totalswap'] = Label('')
        self['usedswap'] = Label('')
        self['freeswap'] = Label('')
        self['totalmem'] = Label('')
        self['usedmem'] = Label('')
        self['freemem'] = Label('')
        self['totaltotal'] = Label('')
        self['usedtotal'] = Label('')
        self['freetotal'] = Label('')
        self['info'] = Label(_('Swapfile is being created, please wait...'))
        self['setupActions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': (self.cancel), 'cancel': (self.cancel), 
           'green': (self.createswap), 
           'red': (self.cancel), 
           'blue': (self.disableswap), 
           'yellow': (self.enableswap)}, -1)
        self.onShown.append(self.setWindowTitle)
        self.getMountedDevices()
        self.createSetup()
        self.onLayoutFinish.append(self.updateInfos)
        if os_path.exists(swapmanger_busy):
            os_remove(swapmanger_busy)
        self.showHide()
        return

    def setWindowTitle(self):
        self.setTitle(_('Swap Manager'))
        return

    def updateInfos(self):
        self.updateSwapStatus()
        self.checkSwapfile()
        self.updateMemInfo()
        return

    def getFreeInfo(self, name):
        df = open(self.outfile)
        line = df.readline()
        sp = []
        found = False
        while line and not found:
            line = df.readline()
            if line.endswith('%s\n' % name):
                found = True
                while line.find('  ') is not -1:
                    line = line.replace('  ', ' ')

                sp = line.split(' ')

        df.close()
        return sp

    def getMountedDevices(self):
        self.outfile = '/tmp/out0'
        cmd = "grep /media/ /proc/mounts | awk '{print $2}' > %s" % self.outfile
        os_system(cmd)
        fd = open(self.outfile)
        line = fd.readline()
        location_choices = []
        while line:
            line = line.replace('\n', '')
            location_choices.append((line, line + '/'))
            line = fd.readline()

        fd.close()
        os_remove(self.outfile)
        if os_path.exists('/media/ba'):
            location_choices.append(('/media/ba', '/media/ba/'))
        if os_path.exists('/media/realroot/sbin/rambo'):
            location_choices.append(('/media/realroot/media/realroot', '/media/realroot/media/realroot/'))
        if os_path.exists('/usr/lib/enigma2/python/Plugins/Extensions/LowFAT/backup'):
            location_choices.append(('/usr/lib/enigma2/python/Plugins/Extensions/LowFAT/backup',
                                     '/usr/lib/enigma2/python/Plugins/Extensions/LowFAT/backup/'))
        if len(location_choices) == 0:
            location_choices.append(('/tmp', '/tmp/'))
        if len(location_choices) == 1:
            location_choices.append(location_choices[0])
        outline = getCmdOutput("grep 'swapfile' /proc/swaps | awk 'NR==1 {print $1}'")
        if not outline == '':
            defaultchoice = outline[:-9]
            try:
                size = os_path.getsize('%s/swapfile' % defaultchoice)
            except:
                size = 268435456

            self.size = int(size / 1048576)
        else:
            outline = getCmdOutput("grep 'partition' /proc/swaps | awk 'NR==1 {print $1}'")
            if not outline == '':
                defaultchoice = outline
                location_choices.append(('%s' % defaultchoice, '%s/' % defaultchoice))
                size = getCmdOutput("grep 'partition' /proc/swaps | awk 'NR==1 {print $3}'")
                self.size = int(int(size) / 1024)
            else:
                print 'length loc_choices= ' + str(len(location_choices))
                defaultchoice, dummy = location_choices[0]
                if defaultchoice == '/tmp':
                    self['key_green'].hide()
        self.location_list = ConfigSelection(location_choices, default=defaultchoice)
        choices = [30, 
         31, 
         32, 
         33, 
         34]
        self.newsize = False
        for i in range(len(choices)):
            if not str(self.size) == choices[i]:
                self.newsize = True

        if self.newsize:
            self.size_list = ConfigSelection([('64', '64 MB'),
             ('128', '128 MB'),
             ('196', '196 MB'),
             ('256', '256 MB'),
             ('512', '512 MB'),
             (
              str(self.size), str(self.size) + ' MB')], default=str(self.size))
        else:
            self.size_list = ConfigSelection([50, 
             51, 
             52, 
             53, 
             54], default=str(self.size))
        return

    def updateSwapStatus(self):
        outline = getCmdOutput("cat /proc/meminfo | grep SwapTotal | awk '{print $2}'")
        if outline == '0':
            self['statustext'].setText(_('Swap is not active'))
            self['swaponpic'].hide()
            self['swapoffpic'].show()
        else:
            self['statustext'].setText(_('Swap is active'))
            self['swaponpic'].show()
            self['swapoffpic'].hide()
        return

    def checkSwapfile(self):
        loc = self.location_list.value
        choices = [1, 
         2, 
         3, 
         4, 
         5]
        self.newsize = False
        if fileExists('%s/swapfile' % loc):
            self.swapexits = True
            for i in range(len(choices)):
                if not str(self.size) == choices[i]:
                    self.newsize = True

            size = os_path.getsize('%s/swapfile' % loc)
            self.size = int(size / 1048576)
            outline = getCmdOutput("cat /proc/swaps | grep %s/swapfile | awk '{print $1}'" % loc)
            if outline == '':
                if str(self.size) == self.size_list.value:
                    self.lockswapsize = False
                    self.swappartition = False
                    self['selstatus'].setText(_('Swapfile is disabled'))
                    self['selonpic'].hide()
                    self['seloffpic'].show()
                    self['key_green'].show()
                    self['key_yellow'].show()
                    self['key_blue'].hide()
                else:
                    self.lockswapsize = False
                    self.swappartition = False
                    self['selstatus'].setText(_('Swapfile does not exist'))
                    self['selonpic'].hide()
                    self['seloffpic'].show()
                    self['key_green'].show()
                    self['key_yellow'].hide()
                    self['key_blue'].hide()
            else:
                self.lockswapsize = True
                self.swappartition = False
                self['selstatus'].setText(_('Swapfile is enabled'))
                self['selonpic'].show()
                self['seloffpic'].hide()
                self['key_green'].hide()
                self['key_yellow'].hide()
                self['key_blue'].show()
        else:
            outline = getCmdOutput("grep 'partition' /proc/swaps | awk 'NR==1 {print $1}'")
            if loc == outline:
                sts, size = getCmdOutput("grep 'partition' /proc/swaps | awk 'NR==1 {print $3}'")
                self.size = int(int(size) / 1024)
                self.swappartition = True
                self.swapexits = False
                self.lockswapsize = True
                self['selstatus'].setText(_('Swap partition enabled'))
                self['selonpic'].show()
                self['seloffpic'].hide()
                self['key_green'].hide()
                self['key_yellow'].hide()
                self['key_blue'].hide()
            else:
                self.swapexits = False
                self.swappartition = False
                self.lockswapsize = False
                self['selstatus'].setText(_('Swapfile does not exist'))
                self['selonpic'].hide()
                self['seloffpic'].show()
                self['key_green'].show()
                self['key_yellow'].hide()
                self['key_blue'].hide()
        return

    def updateMemInfo(self):
        outfile = '/tmp/out'
        os_system('free -m -t > %s' % outfile)
        sp = self.getInfo(outfile, 'Mem')
        self['totalmem'].setText('Total: %d MB' % int(sp[0]))
        self['usedmem'].setText('Used: %d MB' % int(sp[1]))
        self['freemem'].setText('Free:  %d MB' % int(sp[2]))
        sp = self.getInfo(outfile, 'Swap')
        self['totalswap'].setText('Total: %d MB' % int(sp[0]))
        self['usedswap'].setText('Used: %d MB' % int(sp[1]))
        self['freeswap'].setText('Free:  %d MB' % int(sp[2]))
        sp = self.getInfo(outfile, 'Total')
        self['totaltotal'].setText('Total: %d MB' % int(sp[0]))
        self['usedtotal'].setText('Used: %d MB' % int(sp[1]))
        self['freetotal'].setText('Free:  %d MB' % int(sp[2]))
        os_remove(outfile)
        return

    def getInfo(self, outfile, name):
        fm = open(outfile)
        line = fm.readline()
        sp = []
        found = False
        while line and not found:
            line = fm.readline()
            if line.startswith('%s:' % name):
                found = True
                while line.find('  ') is not -1:
                    line = line.replace('  ', ' ')

                line = line.replace('%s: ' % name, '')
                sp = line.split(' ')

        fm.close()
        return sp

    def checkListentrys(self):
        if self['config'].getCurrent()[1] == self.location_list:
            if self.newsize:
                self.size_list.setChoices([('64', '64 MB'),
                 ('128', '128 MB'),
                 ('196', '196 MB'),
                 ('256', '256 MB'),
                 ('512', '512 MB'),
                 (
                  str(self.size), str(self.size) + ' MB')])
                self.size_list.value = str(self.size)
            if self.swapexits:
                self.size_list.setChoices([19, 
                 20, 
                 21, 
                 22, 
                 23])
                self.size_list.value = str(self.size)
            elif self.swappartition:
                self.size_list.setChoices([('64', '64 MB'),
                 ('128', '128 MB'),
                 ('196', '196 MB'),
                 ('256', '256 MB'),
                 ('512', '512 MB'),
                 (
                  str(self.size), str(self.size) + ' MB')])
                self.size_list.value = str(self.size)
            else:
                self.size_list.setChoices([29, 
                 30, 
                 31, 
                 32, 
                 33])
                self.size_list.value = '256'
        if self.lockswapsize:
            self.size_list.value = str(self.size)
        return

    def createSetup(self):
        self.list = []
        self.list.append(getConfigListEntry(_('Swap location'), self.location_list))
        self.list.append(getConfigListEntry(_('Swapsize'), self.size_list))
        self.list.append(getConfigListEntry(_('Enable autostart after reboot'), config.plugins.TSSwapmanager.activateonboot))
        self['config'].setList(self.list)
        return

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.checkSwapfile()
        self.checkListentrys()
        self.checkSwapfile()
        self.createSetup()
        return

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.checkSwapfile()
        self.checkListentrys()
        self.checkSwapfile()
        self.createSetup()
        return

    def cancel(self):
        config.plugins.TSSwapmanager.mountpoint.value = self.location_list.value
        config.plugins.TSSwapmanager.mountpoint.save()
        config.plugins.TSSwapmanager.activateonboot.save()
        self.close()
        return

    def enableswap(self):
        loc = self.location_list.value
        cmd = 'swapon %s/swapfile' % loc
        os_system(cmd)
        self.updateMemInfo()
        self.updateSwapStatus()
        self.checkSwapfile()
        self.createSetup()
        return

    def disableswap(self):
        loc = self.location_list.value
        cmd = 'swapoff %s/swapfile' % loc
        os_system(cmd)
        self.updateMemInfo()
        self.updateSwapStatus()
        self.checkSwapfile()
        self.createSetup()
        return

    def createswap(self):
        os_system('touch %s' % swapmanger_busy)
        self.showHide()
        loc = self.location_list.value
        val = int(self.size_list.value) * 1024
        cmd = 'dd if=/dev/zero of=%s/swapfile bs=1024 count=%d; ' % (loc, val)
        cmd = cmd + 'mkswap %s/swapfile; ' % loc
        cmd = cmd + 'swapon %s/swapfile; ' % loc
        self.container = eConsoleAppContainer()
        self.container_conn = self.container.appClosed.connect(self.UpdateGUI)
        self.container.execute(cmd)
        return

    def UpdateGUI(self, result):
        print result
        self.updateMemInfo()
        self.updateSwapStatus()
        self.checkSwapfile()
        self.createSetup()
        if os_path.exists(swapmanger_busy):
            os_remove(swapmanger_busy)
        self.showHide()
        return

    def showHide(self):
        if os_path.exists(swapmanger_busy):
            self['info'].show()
            self['key_green'].hide()
            self['key_yellow'].hide()
            self['key_blue'].hide()
        else:
            self['info'].hide()
        return


return
