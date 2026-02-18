# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/Stools/SetBackupRestore.py
# Compiled at: 2016-05-20 21:00:55
from Screens.ChoiceBox import ChoiceBox
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from Components.Harddisk import harddiskmanager
from Components.config import config
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.Label import Label
from enigma import RT_HALIGN_LEFT, RT_VALIGN_CENTER, eListboxPythonMultiContent, eListbox, gFont, getDesktop
from os import path, makedirs, access, remove, W_OK, R_OK, F_OK
from tsimage import TSimagePanelImage
from Plugins.SystemPlugins.SoftwareManager.BackupRestore import BackupScreen, BackupSelection, RestoreMenu, RestoreScreen, getBackupFilename, getBackupPath
desktopSize = getDesktop(0).size()

class TSBackupSettings(Screen):
    skin_1280 = '\n                <screen name="TSBackupSettings"  position="center,77"  title=" "  size="920,600"  >\n                <widget name="list" position="20,20" size="880,450" scrollbarMode="showOnDemand" transparent="1" zPosition="2" />\n                <eLabel position="20,440" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\n                <eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\n\t\t<widget name="info" position="20,430" zPosition="4" size="880,80" font="Regular;24" foregroundColor="yellow" transparent="1" halign="center" valign="center" />\n\t\t<ePixmap name="red"    position="50,545"   zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" transparent="1" alphatest="blend" />\n\t\t<eLabel name="key_red" text="Close" position="50,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" />\n        </screen>'
    skin_1920 = '    <screen name="TSBackupSettings" position="center,200" size="1300,720" title="">\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png" position="50,640" size="200,40" alphatest="blend" />\n        <eLabel name="key_red" text="Close" position="50,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#940d0d" transparent="1" />\n        <widget name="info" position="20,500" size="1260,100" foregroundColor="foreground" backgroundColor="background" font="Regular;28" valign="center" halign="center" transparent="1" zPosition="1" />\n        <widget name="list" position="20,20" size="1260,520" zPosition="2" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background"  transparent="1" />\n        </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session, args=0):
        Screen.__init__(self, session)
        self.list = []
        self.oktext = _('\nPress OK on your remote control to continue.')
        self['info'] = Label(_('\nBackup your Dreambox settings.') + self.oktext)
        self['list'] = MenuList([], True, eListboxPythonMultiContent)
        self['list'].onSelectionChanged.append(self.selectionChanged)
        self.text = ''
        self.backupdirs = (' ').join(config.plugins.configurationbackup.backupdirs.value)
        self.list.append(_('Backup system settings'))
        self.list.append(_('Restore system settings'))
        self.list.append(_('Advanced restore'))
        self.list.append(_('Choose backup location'))
        self.list.append(_('Choose backup files'))
        self['actions'] = ActionMap(['SetupActions'], {'ok': (self.go), 'cancel': (self.close)}, -1)
        self.onLayoutFinish.append(self.layoutFinished)
        self.backuppath = getBackupPath()
        self.backupfile = getBackupFilename()
        self.fullbackupfilename = self.backuppath + '/' + self.backupfile
        self.ListToMulticontent()
        self.onShown.append(self.setWindowTitle)
        return

    def setWindowTitle(self):
        self.setTitle(_('Settings backup&restore'))
        return

    def ListToMulticontent(self):
        res = []
        theevents = []
        self.events = []
        self.events = self.list
        if desktopSize.width() == 1920:
            self['list'].l.setItemHeight(60)
            self['list'].l.setFont(0, gFont('Regular', 32))
            for i in range(0, len(self.events)):
                res.append(MultiContentEntryText(pos=(0, 0), size=(2, 60), font=0, flags=RT_HALIGN_LEFT, text=''))
                res.append(MultiContentEntryText(pos=(75, 0), size=(540, 60), font=0, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER, text=self.events[i]))
                theevents.append(res)
                res = []

        else:
            self['list'].l.setItemHeight(38)
            self['list'].l.setFont(0, gFont('Regular', 26))
            for i in range(0, len(self.events)):
                res.append(MultiContentEntryText(pos=(0, 1), size=(2, 34), font=0, flags=RT_HALIGN_LEFT, text=''))
                res.append(MultiContentEntryText(pos=(50, 1), size=(540, 34), font=0, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER, text=self.events[i]))
                theevents.append(res)
                res = []

        self['list'].l.setList(theevents)
        self['list'].show()
        return

    def selectionChanged(self):
        currentEntry = self['list'].getSelectionIndex()
        if currentEntry == 0:
            self['info'].setText(_('\nBackup your Dreambox settings.') + self.oktext)
        if currentEntry == 1:
            self['info'].setText(_('\nRestore your Dreambox settings.') + self.oktext)
        if currentEntry == 2:
            self['info'].setText(_('\nRestore your backups by date.') + self.oktext)
        if currentEntry == 3:
            self['info'].setText('\n' + _('Current device: ') + config.plugins.configurationbackup.backuplocation.value + self.oktext)
        if currentEntry == 4:
            self['info'].setText('\n' + _('Select files for backup.') + self.oktext)
        return

    def layoutFinished(self):
        idx = 0
        self['list'].index = idx
        return

    def go(self):
        currentEntry = self['list'].getSelectionIndex()
        if currentEntry == 3:
            parts = [(r.description, r.mountpoint, self.session) for r in harddiskmanager.getMountedPartitions(onlyhotplug=False)]
            for x in parts:
                if not access(x[1], F_OK | R_OK | W_OK) or x[1] == '/':
                    parts.remove(x)

            if len(parts):
                self.session.openWithCallback(self.backuplocation_choosen, ChoiceBox, title=_('Please select medium to use as backup location'), list=parts)
        elif currentEntry == 4:
            self.session.openWithCallback(self.backupfiles_choosen, BackupSelection)
        elif currentEntry == 2:
            self.session.open(RestoreMenu, '/usr/lib/enigma2/python/Plugins')
        elif currentEntry == 0:
            self.session.openWithCallback(self.backupDone, BackupScreen, runBackup=True)
        elif currentEntry == 1:
            if path.exists(self.fullbackupfilename):
                self.session.openWithCallback(self.startRestore, MessageBox, _('Are you sure you want to restore your Enigma2 backup?\nEnigma2 will restart after the restore'))
            else:
                self.session.open(MessageBox, _('Sorry no backups found!'), MessageBox.TYPE_INFO, timeout=10)
        return

    def backupfiles_choosen(self, ret):
        self.backupdirs = (' ').join(config.plugins.configurationbackup.backupdirs.value)
        config.plugins.configurationbackup.backupdirs.save()
        config.plugins.configurationbackup.save()
        return

    def backuplocation_choosen(self, option):
        oldpath = config.plugins.configurationbackup.backuplocation.getValue()
        if option is not None:
            config.plugins.configurationbackup.backuplocation.value = str(option[1])
        config.plugins.configurationbackup.backuplocation.save()
        config.plugins.configurationbackup.save()
        newpath = config.plugins.configurationbackup.backuplocation.getValue()
        if newpath != oldpath:
            self.createBackupfolders()
        self.selectionChanged()
        return

    def createBackupfolders(self):
        print 'Creating backup folder if not already there...'
        self.backuppath = getBackupPath()
        try:
            if path.exists(self.backuppath) == False:
                makedirs(self.backuppath)
        except OSError:
            self.session.open(MessageBox, _('Sorry, your backup destination is not writeable.\n\nPlease choose another one.'), MessageBox.TYPE_INFO, timeout=10)

        return

    def backupDone(self, retval=None):
        if retval is True:
            self.session.open(MessageBox, _('Backup done.'), MessageBox.TYPE_INFO, timeout=10)
        else:
            self.session.open(MessageBox, _('Backup failed.'), MessageBox.TYPE_INFO, timeout=10)
        return

    def startRestore(self, ret=False):
        if ret == True:
            self.exe = True
            self.session.open(RestoreScreen, runRestore=True)
        return


return
