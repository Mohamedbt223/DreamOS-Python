# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/TSInfos/TSMounts.py
# Compiled at: 2015-12-25 09:37:09
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.Label import Label
from Components.Sources.List import List
from Components.MenuList import MenuList
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import resolveFilename, SCOPE_CURRENT_PLUGIN
from Tools.TSTools import getCmdOutput
from enigma import getDesktop
desktopSize = getDesktop(0).size()

class TSMounts(Screen):
    skin_1280 = '\n                       <screen name="TSMounts" position="center,77" size="920,600"  title="General Info" >\n                       <widget source="mountslist" render="Listbox" position="40,35" size="850,525" scrollbarMode="showOnDemand" transparent="1" zPosition="2" >\n\t\t\t\t<convert type="TemplatedMultiContent">\n\t\t\t\t\t{"template": [\n\t\t\t\t\t\tMultiContentEntryText(pos = (80, 2), size = (750, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # Device\n\t\t\t\t\t\tMultiContentEntryText(pos = (80, 25), size = (750, 22), font=1, flags = RT_HALIGN_LEFT, text = 1), # Mountpoint\n\t\t\t\t\t\tMultiContentEntryText(pos = (80, 45), size = (750, 22), font=1, flags = RT_HALIGN_LEFT, text = 2), # filesystem+parameter\n\t\t\t\t\t\tMultiContentEntryPixmapAlphaTest(pos = (3, 7), size = (64, 64), png = 3), # Icon\n\t\t\t\t\t],\n\t\t\t\t\t"fonts": [gFont("Regular", 22),gFont("Regular", 18)],\n\t\t\t\t\t"itemHeight": 75\n\t\t\t\t\t}\n\t\t\t\t</convert>\n\t\t\t</widget>\n                       </screen>'
    skin_1920 = '    <screen name="TSMounts" position="center,200" size="1300,720" title="Mounts">\n        <widget source="mountslist" render="Listbox" position="20,15" size="1260,700" zPosition="2" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background"  transparent="1" >\n        <convert type="TemplatedMultiContent">\n        {"template": [\n        MultiContentEntryText(pos = (80, 0), size = (1000, 40), font=0, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 0) ,\n        MultiContentEntryText(pos = (80, 35), size = (1000, 30), font=1, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 1) ,\n        MultiContentEntryText(pos = (80, 65), size = (1000, 30), font=1, flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 2) ,\n        MultiContentEntryPixmapAlphaBlend(pos = (2, 7), size = (64, 64), png = 3),\n        ],\n        "fonts": [gFont("Regular", 30),gFont("Regular", 23)],\n        "itemHeight": 100\n        }\n        </convert>\n        </widget>\n        </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session):
        Screen.__init__(self, session)
        self.mountslist = []
        self.flashIcon = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, 'TSimage/TSimagePanel/TSInfos/pictures/dev_flash.png'))
        self.hddIcon = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, 'TSimage/TSimagePanel/TSInfos/pictures/dev_hdd.png'))
        self.usbIcon = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, 'TSimage/TSimagePanel/TSInfos/pictures/dev_usb.png'))
        mmcIcon = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, 'TSimage/TSimagePanel/icons/media-flash-sd-mmc.png'))
        self.usbhddIcon = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, 'TSimage/TSimagePanel/icons/drive-removable-media-usb.png'))
        self.cfIcon = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_PLUGIN, 'TSimage/TSimagePanel/TSInfos/pictures/dev_cf.png'))
        self.icons = {'hdd': (self.hddIcon), 'pendrive': (self.usbIcon), 
           'mmc': mmcIcon, 
           'usbhdd': (self.usbhddIcon), 
           'cf': (self.cfIcon)}
        self.getMounts()
        self['mountslist'] = List(self.mountslist)
        self['key_red'] = Button(_('Close'))
        self['setupActions'] = ActionMap(['SetupActions'], {'ok': (self.cancel), 'cancel': (self.cancel), 
           'red': (self.cancel)})
        self.onShown.append(self.setWindowTitle)
        return

    def setWindowTitle(self):
        self.setTitle(_('Mounts Info'))
        return

    def getMounts(self):
        self.mountslist = []
        tmp = getCmdOutput("mount | awk '{print $1}'")
        devices = tmp.split('\n')
        tmp = getCmdOutput("mount | awk '{print $2}'")
        status = tmp.split('\n')
        tmp = getCmdOutput("mount | awk '{print $3}'")
        mountpoints = tmp.split('\n')
        tmp = getCmdOutput("mount | awk '{print $5}'")
        filesystems = tmp.split('\n')
        tmp = getCmdOutput("mount | awk '{print $6}'")
        parameters = tmp.split('\n')
        for i in range(len(devices)):
            dev = devices[i]
            mnt = mountpoints[i]
            if dev[:7] == '/dev/sd' or mnt[:7] == '/media/':
                icon = self.usbIcon
                if mountpoints[i] == '/media/hdd':
                    icon = self.hddIcon
                if mountpoints[i] == '/media/usb':
                    icon = self.usbIcon
                if mountpoints[i] == '/media/cf':
                    icon = self.cfIcon
            else:
                icon = self.flashIcon
            self.mountslist.append(('' + devices[i],
             'mountpoint: ' + mountpoints[i],
             'filesystem: %s %s ' % (filesystems[i], parameters[i]),
             icon))

        return

    def cancel(self):
        self.close()
        return


return
