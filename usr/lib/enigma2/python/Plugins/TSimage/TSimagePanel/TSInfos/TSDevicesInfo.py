# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/TSDevicesInfo.py
# Compiled at: 2017-02-19 18:39:04
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.Pixmap import Pixmap
from Components.Label import Label
from Components.ProgressBar import ProgressBar
from Components.ScrollLabel import ScrollLabel
from enigma import getDesktop
import os
desktopSize = getDesktop(0).size()

class TSDevicesInfo(Screen):
    skin_1280 = '\n             <screen name="TSDevicesInfo" position="center,77" size="920,600"  title="Devices Info" >              \n                <ePixmap position="35,25" size="64,64" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/dev_cf.png" transparent="1" alphatest="blend" />                                              \n                <widget name="sd" position="35,90" size="280,45" backgroundColor="background" valign="top" halign="left" zPosition="-2" font="Regular;19" transparent="1"/>                                             \n                <widget name="sdbar" position="145,50" size="150,12" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/memory_bar.png" borderWidth="1" transparent="1"/>\n                <widget name="sdused" position="310,44" size="60,24" backgroundColor="background" valign="center" halign="left" zPosition="-2"  foregroundColor="#00ffffff" font="Regular;20" transparent="1"/>                                              \n                \n                <ePixmap position="35,165" size="64,64" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/dev_usb.png" transparent="1" alphatest="blend" />                                              \n                <widget name="usb" position="35,230" size="280,45" backgroundColor="background" valign="top" halign="left" zPosition="-2" font="Regular;19" transparent="1"/>\n                <widget name="usbbar" position="145,190" size="150,12" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/memory_bar.png" borderWidth="1" transparent="1"/>\n                <widget name="usbused" position="310,184" size="60,24" backgroundColor="background" valign="center" halign="left" zPosition="-2" font="Regular;20" transparent="1"/>                                              \n\n                <ePixmap position="35,305" size="64,64" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/dev_hdd.png" transparent="1" alphatest="blend" /> \n                <widget name="sleep" position="90,308" size="32,32" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/zzz-sleeping.png" zPosition="1" alphatest="blend" />                                                                                         \n                <widget name="hdd" position="35,370" size="350,45" backgroundColor="background" valign="top" halign="left" zPosition="-2" font="Regular;19" transparent="1"/>\n                <widget name="hddbar" position="145,330" size="150,12" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/memory_bar.png" borderWidth="1" transparent="1"/>\n                <widget name="hddused" position="310,324" size="60,24" backgroundColor="background" valign="center" halign="left" zPosition="-2" font="Regular;20" transparent="1"/>                                              \n                \n                <ePixmap position="35,445" size="64,64" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/dev_storage.png" transparent="1" alphatest="blend" />\n                <widget name="storage" position="35,515" size="350,45" backgroundColor="background" valign="top" halign="left" zPosition="-2"  foregroundColor="yellow" font="Regular;19" transparent="1"/>\n                <widget name="storagebar" position="145,475" size="150,12" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/memory_bar.png" borderWidth="1" transparent="1"/>\n                <widget name="storageused" position="310,469" size="60,24" backgroundColor="background" valign="center" halign="left" zPosition="-2" font="Regular;20" transparent="1"/>                                              \n                            \n                <ePixmap position="560,25" size="64,64" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/dev_flash.png" transparent="1" alphatest="blend" />                                              \n                <widget name="flash" position="560,90" size="280,45" backgroundColor="background" valign="top" halign="left" zPosition="-2" font="Regular;19" transparent="1"/>\n                <widget name="flashbar" position="670,50" size="150,12" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/memory_bar.png" borderWidth="1" transparent="1"/>\n                <widget name="flashused" position="835,44" size="60,24" backgroundColor="background" valign="center" halign="left" zPosition="-2" font="Regular;20" transparent="1"/>                                              \n                \n                <ePixmap position="560,165" size="64,64" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/dev_memory.png" transparent="1" alphatest="blend" />                                              \n                <widget name="ram" position="560,230" size="280,45" backgroundColor="background" valign="top" halign="left" zPosition="-2" font="Regular;19" transparent="1"/>\n                <widget name="rambar" position="670,190" size="150,12" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/memory_bar.png" borderWidth="1" transparent="1"/>\n                <widget name="ramused" position="835,184" size="60,24" backgroundColor="background" valign="center" halign="left" zPosition="-2" font="Regular;20" transparent="1"/>                                              \n\n                <ePixmap position="560,305" size="64,64" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/dev_swap.png" transparent="1" alphatest="blend" />\n                <widget name="swapoff" position="605,348" size="12,12" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/swapoff.png" zPosition="1" alphatest="blend" />\n                <widget name="swapon" position="605,348" size="12,12" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/swapon.png" zPosition="1" alphatest="blend" />                                            \n                <widget name="swap" position="560,370" size="280,45" backgroundColor="background" valign="top" halign="left" zPosition="-2" font="Regular;19" transparent="1"/>\n                <widget name="swapbar" position="670,330" size="150,12" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/memory_bar.png" borderWidth="1" transparent="1"/>\n                <widget name="swapused" position="835,324" size="60,24" backgroundColor="background" valign="center" halign="left" zPosition="-2" font="Regular;20" transparent="1"/>                                              \n                \n                <ePixmap position="560,445" size="64,64" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/dev_mem.png" transparent="1" alphatest="blend" />                                              \n                <widget name="total" position="560,515" size="280,45" backgroundColor="background" valign="top" halign="left" zPosition="-2"  foregroundColor="yellow" font="Regular;19" transparent="1"/>\n                <widget name="totalbar" position="670,475" size="150,12" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/memory_bar.png" borderWidth="1" transparent="1"/>\n                <widget name="totalused" position="835,469" size="60,24" backgroundColor="background" valign="center" halign="left" zPosition="-2" font="Regular;20" transparent="1"/>                                              \n              </screen>'
    skin_1920 = '  <screen name="TSDevicesInfo" position="center,200" size="1300,720" title="Devices Info">\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/images/tsimagelogo2.png" position="945,160" size="250,243" zPosition="-1" alphatest="blend" />\n        <ePixmap position="40,40" size="72,72" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/dev_cf.png" transparent="1" alphatest="blend" />\n        <widget name="sd" position="50,106" size="360,50" backgroundColor="background" valign="top" halign="left" zPosition="2"  foregroundColor="foreground" font="Regular;21" transparent="1"/>\n        <widget name="sdbar" position="115,66" size="150,12" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/memory_bar.png" borderColor="foreground" borderWidth="1" transparent="1"/>\n        <widget name="sdused" position="280,60" size="60,24" backgroundColor="background" valign="center" halign="left" zPosition="2"  foregroundColor="foreground" font="Regular;22" transparent="1"/>\n        <ePixmap position="40,185" size="72,72" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/dev_usb.png" transparent="1" alphatest="blend" />\n        <widget name="usb" position="50,259" size="360,50" backgroundColor="background" valign="top" halign="left" zPosition="2"  foregroundColor="foreground" font="Regular;21" transparent="1"/>\n        <widget name="usbbar" position="115,214" size="150,12" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/memory_bar.png" borderColor="foreground" borderWidth="1" transparent="1"/>\n        <widget name="usbused" position="280,208" size="60,24" backgroundColor="background" valign="center" halign="left" zPosition="2"  foregroundColor="foreground" font="Regular;22" transparent="1"/>\n        <ePixmap position="40,332" size="72,72" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/dev_hdd.png" transparent="1" alphatest="blend" />\n        <widget name="sleep" position="107,332" size="32,32" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/zzz-sleeping.png" zPosition="1" alphatest="blend" />\n        <widget name="hdd" position="50,407" size="360,50" backgroundColor="background" valign="top" halign="left" zPosition="2"  foregroundColor="foreground" font="Regular;21" transparent="1"/>\n        <widget name="hddbar" position="115,357" size="150,12" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/memory_bar.png" borderColor="foreground" borderWidth="1" transparent="1"/>\n        <widget name="hddused" position="280,351" size="60,24" backgroundColor="background" valign="center" halign="left" zPosition="2"  foregroundColor="foreground" font="Regular;22" transparent="1"/>\n        <ePixmap position="40,480" size="72,72" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/dev_storage.png" transparent="1" alphatest="blend" />\n        <widget name="storage" position="50,555" size="360,50" backgroundColor="background" valign="top" halign="left" zPosition="2"  foregroundColor="yellow" font="Regular;21" transparent="1"/>\n        <widget name="storagebar" position="115,505" size="150,12" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/memory_bar.png" borderColor="foreground" borderWidth="1" transparent="1"/>\n        <widget name="storageused" position="280,499" size="60,24" backgroundColor="background" valign="center" halign="left" zPosition="2"  foregroundColor="foreground" font="Regular;22" transparent="1"/>\n        <ePixmap position="540,40" size="72,72" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/dev_flash.png" transparent="1" alphatest="blend" />\n        <widget name="flash" position="550,106" size="360,50" backgroundColor="background" valign="top" halign="left" zPosition="2"  foregroundColor="foreground" font="Regular;21" transparent="1"/>\n        <widget name="flashbar" position="620,66" size="150,12" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/memory_bar.png" borderColor="foreground" borderWidth="1" transparent="1"/>\n        <widget name="flashused" position="785,60" size="60,24" backgroundColor="background" valign="center" halign="left" zPosition="2"  foregroundColor="foreground" font="Regular;22" transparent="1"/>\n        <ePixmap position="540,185" size="72,72" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/dev_memory.png" transparent="1" alphatest="blend" />\n        <widget name="ram" position="550,259" size="360,50" backgroundColor="background" valign="top" halign="left" zPosition="2"  foregroundColor="foreground" font="Regular;21" transparent="1"/>\n        <widget name="rambar" position="620,214" size="150,12" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/memory_bar.png" borderColor="foreground" borderWidth="1" transparent="1"/>\n        <widget name="ramused" position="785,208" size="60,24" backgroundColor="background" valign="center" halign="left" zPosition="2"  foregroundColor="foreground" font="Regular;22" transparent="1"/>\n        <ePixmap position="540,332" size="72,72" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/dev_swap.png" transparent="1" alphatest="blend" />\n        <widget name="swapoff" position="595,385" size="12,12" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/swapoff.png" zPosition="1" alphatest="blend" />\n        <widget name="swapon" position="595,385" size="12,12" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/swapon.png" zPosition="1" alphatest="blend" />\n        <widget name="swap" position="550,407" size="360,50" backgroundColor="background" valign="top" halign="left" zPosition="2"  foregroundColor="foreground" font="Regular;21" transparent="1"/>\n        <widget name="swapbar" position="620,357" size="150,12" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/memory_bar.png" borderColor="foreground" borderWidth="1" transparent="1"/>\n        <widget name="swapused" position="785,351" size="60,24" backgroundColor="background" valign="center" halign="left" zPosition="2"  foregroundColor="foreground" font="Regular;22" transparent="1"/>\n        <ePixmap position="540,480" size="72,72" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/dev_mem.png" transparent="1" alphatest="blend" />\n        <widget name="total" position="550,555" size="360,50" backgroundColor="background" valign="top" halign="left" zPosition="2"  foregroundColor="yellow" font="Regular;21" transparent="1"/>\n        <widget name="totalbar" position="620,505" size="150,12" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/pictures/memory_bar.png" borderColor="foreground" borderWidth="1" transparent="1"/>\n        <widget name="totalused" position="785,499" size="60,24" backgroundColor="background" valign="center" halign="left" zPosition="2"  foregroundColor="foreground" font="Regular;22" transparent="1"/>\n        <widget source="global.CurrentTime" render="Label" position="840,50" size="460,70" font="Regular;65" halign="center" foregroundColor="foreground" backgroundColor="background" transparent="1">\n        <convert type="ClockToText">Default</convert>\n        </widget>\n        <widget source="session.CurrentService" render="Label" position="850,480" size="440,100" font="Regular;38" halign="center" foregroundColor="foreground" backgroundColor="background" transparent="1">\n        <convert type="ServiceName">Name</convert>\n        </widget>\n        </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session):
        Screen.__init__(self, session)
        self['swapoff'] = Pixmap()
        self['swapon'] = Pixmap()
        self['sleep'] = Pixmap()
        self.outfile = '/tmp/out'
        os.system('free -t > %s' % self.outfile)
        sp1 = self.getMemInfo('Mem')
        sp2 = self.getMemInfo('Swap')
        sp3 = self.getMemInfo('Total')
        os.system('df -m > %s' % self.outfile)
        sp_flash = self.getFreeInfo('/')
        sp_hdd = self.getFreeInfo('/media/hdd')
        sp_usb = self.getFreeInfo('/media/usb')
        sp_sd = self.getFreeInfo('/media/sd')
        os.remove(self.outfile)
        storage_total = int(sp_hdd[1]) + int(sp_usb[1]) + int(sp_sd[1]) + int(sp_flash[1])
        storage_used = int(sp_hdd[2]) + int(sp_usb[2]) + int(sp_sd[2]) + int(sp_flash[2])
        storage_free = int(sp_hdd[3]) + int(sp_usb[3]) + int(sp_sd[3]) + int(sp_flash[3])
        sp_storage = (storage_total, storage_used, storage_free)
        if int(sp_hdd[1]) >= 102400:
            total_hdd_label = str(int(float(sp_hdd[1]) / 1024)) + ' GB'
        else:
            total_hdd_label = str(int(sp_hdd[1])) + ' MB'
        if int(sp_hdd[2]) >= 102400:
            used_hdd_label = str(int(float(sp_hdd[2]) / 1024)) + ' GB'
        else:
            used_hdd_label = str(int(sp_hdd[2])) + ' MB'
        if int(sp_hdd[3]) >= 102400:
            free_hdd_label = str(int(float(sp_hdd[3]) / 1024)) + ' GB'
        else:
            free_hdd_label = str(int(sp_hdd[3])) + ' MB'
        if int(sp_storage[0]) >= 102400:
            total_storage_label = str(int(float(sp_storage[0]) / 1024)) + ' GB'
        else:
            total_storage_label = str(int(sp_storage[0])) + ' MB'
        if int(sp_storage[1]) >= 102400:
            used_storage_label = str(int(float(sp_storage[1]) / 1024)) + ' GB'
        else:
            used_storage_label = str(int(sp_storage[1])) + ' MB'
        if int(sp_storage[2]) >= 102400:
            free_storage_label = str(int(float(sp_storage[2]) / 1024)) + ' GB'
        else:
            free_storage_label = str(int(sp_storage[2])) + ' MB'
        self.flash_percent = sp_flash[4].replace('%', '')
        self.flashused_label = '%s %%' % str(self.flash_percent)
        self.hdd_percent = sp_hdd[4].replace('%', '')
        self.hddused_label = '%s %%' % str(self.hdd_percent)
        self.usb_percent = sp_usb[4].replace('%', '')
        self.usbused_label = '%s %%' % str(self.usb_percent)
        self.sd_percent = sp_sd[4].replace('%', '')
        self.sdused_label = '%s %%' % str(self.sd_percent)
        self.storage_percent = float(sp_storage[1]) / float(sp_storage[0]) * 100
        self.storageused_label = '%i %%' % int(self.storage_percent)
        if int(sp_hdd[1]) == 0:
            self.hdd_string = _('HDD: %s  \n') % 'Not Found'
            self.hddused_label = ''
        else:
            self.hdd_string = _('HDD: %s  \nUsed: %s   Free: %s') % (total_hdd_label, used_hdd_label, free_hdd_label)
            state = os.popen("hdparm -C /dev/sda1 | grep 'drive state' | awk '{print$4}'").readline()
            if state[:7] == 'standby':
                self['sleep'].show()
            else:
                self['sleep'].hide()
        if int(sp_usb[1]) == 0:
            self.usb_string = _('USB: %s  \n') % 'Not Found'
            self.usbused_label = ''
        else:
            self.usb_string = _('USB: %i MB  \nUsed: %i MB   Free: %i MB') % (int(sp_usb[1]), int(sp_usb[2]), int(sp_usb[3]))
        if int(sp_sd[1]) == 0:
            self.sd_string = _('SD: %s  \n') % 'Not Found'
            self.sdused_label = ''
        else:
            self.sd_string = _('SD: %i MB  \nUsed: %i MB   Free: %i MB') % (int(sp_sd[1]), int(sp_sd[2]), int(sp_sd[3]))
        self.flash_string = _('Flash: %i MB  \nUsed: %i MB   Free: %i MB') % (int(sp_flash[1]), int(sp_flash[2]), int(sp_flash[3]))
        self.storage_string = _('Total Storage: %s  \nUsed: %s   Free: %s') % (total_storage_label, used_storage_label, free_storage_label)
        self.ram_percent = (float(sp1[0]) - float(sp1[2])) / float(sp1[0]) * 100
        if not int(sp2[0]) == 0:
            self['swapoff'].hide()
            self['swapon'].show()
            self.swap_percent = float(sp2[1]) / float(sp2[0]) * 100
        else:
            self.swap_percent = 0
            self['swapoff'].show()
            self['swapon'].hide()
        self.total_percent = (float(sp3[0]) - float(sp3[2])) / float(sp3[0]) * 100
        self.ramused_label = '%i %%' % int(self.ram_percent)
        self.swapused_label = '%i %%' % int(self.swap_percent)
        self.totalused_label = '%i %%' % int(self.total_percent)
        self.ram_string = _('Ram: %i MB  \nUsed: %i MB   Free: %i MB') % (int(sp1[0]) / 1024, int(float(sp1[0]) - float(sp1[2]) + 0.5) / 1024, int(sp1[2]) / 1024)
        self.swap_string = _('Swap: %i MB  \nUsed: %i MB   Free: %i MB') % (int(sp2[0]) / 1024, int(sp2[1]) / 1024, int(sp2[2]) / 1024)
        self.total_string = _('Total Memory: %i MB  \nUsed: %i MB   Free: %i MB') % (int(sp3[0]) / 1024, int(float(sp3[0]) - float(sp3[2]) + 0.5) / 1024, int(sp3[2]) / 1024)
        self['key_red'] = Button(_('Close'))
        self['ram'] = Label(self.ram_string)
        self['ramused'] = Label(self.ramused_label)
        self['swap'] = Label(self.swap_string)
        self['swapused'] = Label(self.swapused_label)
        self['total'] = Label(self.total_string)
        self['totalused'] = Label(self.totalused_label)
        self['flash'] = Label(self.flash_string)
        self['flashused'] = Label(self.flashused_label)
        self['sd'] = Label(self.sd_string)
        self['sdused'] = Label(self.sdused_label)
        self['cf'] = Label(self.sd_string)
        self['cfused'] = Label(self.sdused_label)
        self['usb'] = Label(self.usb_string)
        self['usbused'] = Label(self.usbused_label)
        self['hdd'] = Label(self.hdd_string)
        self['hddused'] = Label(self.hddused_label)
        self['storage'] = Label(self.storage_string)
        self['storageused'] = Label(self.storageused_label)
        self['rambar'] = ProgressBar()
        self['swapbar'] = ProgressBar()
        self['totalbar'] = ProgressBar()
        self['flashbar'] = ProgressBar()
        self['sdbar'] = ProgressBar()
        self['cfbar'] = ProgressBar()
        self['usbbar'] = ProgressBar()
        self['hddbar'] = ProgressBar()
        self['storagebar'] = ProgressBar()
        self['setupActions'] = ActionMap(['SetupActions'], {'ok': (self.cancel), 'cancel': (self.cancel), 
           'red': (self.cancel)})
        self.onShown.append(self.setWindowTitle)
        self.onLayoutFinish.append(self.SetProgressbarInfo)
        return

    def setWindowTitle(self):
        self.setTitle(_('Devices Info'))
        return

    def SetProgressbarInfo(self):
        self['rambar'].setValue(int(self.ram_percent))
        self['swapbar'].setValue(int(self.swap_percent))
        self['totalbar'].setValue(int(self.total_percent))
        self['flashbar'].setValue(int(self.flash_percent))
        self['sdbar'].setValue(int(self.sd_percent))
        self['cfbar'].setValue(int(self.sd_percent))
        self['usbbar'].setValue(int(self.usb_percent))
        self['hddbar'].setValue(int(self.hdd_percent))
        self['storagebar'].setValue(int(self.storage_percent))
        return

    def getMemInfo(self, name):
        fm = open(self.outfile)
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
        if sp == []:
            sp = (
             str('1'),
             str('0'),
             str('0'),
             str('0'),
             str('0'))
        return sp

    def cancel(self):
        self.close()
        return


return
