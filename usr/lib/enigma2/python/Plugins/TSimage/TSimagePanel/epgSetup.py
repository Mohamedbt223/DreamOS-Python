# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/epgSetup.py
# Compiled at: 2016-07-30 19:23:03
""" based on EPGdbBackup Plugin by gutemine """
epgdbbackup_version = '1.0'
from Components.ActionMap import ActionMap
from Components.Label import Label
from Tools.Directories import InitFallbackFiles, resolveFilename, SCOPE_CURRENT_SKIN, SCOPE_PLUGINS, SCOPE_CONFIG, SCOPE_LANGUAGE
from Components.config import config, configfile, ConfigText, ConfigYesNo, ConfigInteger, ConfigSelection, NoSave, ConfigSubsection, getConfigListEntry, ConfigDirectory
from Components.ConfigList import ConfigListScreen
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.InputBox import InputBox
from Components.Input import Input
from Screens.ChoiceBox import ChoiceBox
from Screens.Console import Console
from Components.MenuList import MenuList
from Components.Slider import Slider
from enigma import ePoint, getDesktop, eTimer, eActionMap, eEPGCache, cachestate
from sqlite3 import dbapi2 as sqlite
import sys, os
from Components.Button import Button
from Components.Language import language
from os import environ
import gettext, time, datetime

def localeInit():
    lang = language.getLanguage()
    environ['LANGUAGE'] = lang[:2]
    gettext.bindtextdomain('enigma2', resolveFilename(SCOPE_LANGUAGE))
    gettext.textdomain('enigma2')
    if os.path.exists('%s/TSimage/TSimagePanel/locale/%s' % (resolveFilename(SCOPE_PLUGINS), environ['LANGUAGE'])):
        gettext.bindtextdomain('EPGdbBackup', '%s%s' % (resolveFilename(SCOPE_PLUGINS), 'TSimage/TSimagePanel/locale/'))
    return


def _(txt):
    t = gettext.dgettext('EPGdbBackup', txt)
    if t == txt:
        t = gettext.gettext(txt)
    return t


localeInit()
language.addCallback(localeInit)
EPGdbBackupautoStartTimer = None
yes_no_descriptions = {False: (_('no')), True: (_('yes'))}
config.plugins.epgdbbackup = ConfigSubsection()
locations = []
locations.append(('/etc/enigma2', '/etc/enigma2'))
if os.path.exists('/media/hdd/backup'):
    locations.append(('/media/hdd/backup', '/media/hdd/backup'))
if os.path.exists('/media/ba/backup'):
    locations.append(('/media/ba/backup', '/media/ba/backup'))
if os.path.exists('/media/cf/backup'):
    locations.append(('/media/cf/backup', '/media/cf/backup'))
if os.path.exists('/media/sd/backup'):
    locations.append(('/media/sd/backup', '/media/sd/backup'))
if os.path.exists('/media/usb/backup'):
    locations.append(('/media/usb/backup', '/media/usb/backup'))
config.plugins.epgdbbackup.location = ConfigSelection(default='/etc/enigma2', choices=locations)
orilocations = []
orilocations.append(('/etc/enigma2/epg.db', '/etc/enigma2'))
m = open('/proc/mounts')
mounts = m.read()
m.close()
if mounts.find('/media/usb') is not -1:
    orilocations.append(('/media/usb/epg.db', '/media/usb'))
if mounts.find('/media/sd') is not -1:
    orilocations.append(('/media/sd/epg.db', '/media/sd'))
if mounts.find('/media/cf') is not -1:
    orilocations.append(('/media/cf/epg.db', '/media/cf'))
if mounts.find('/media/ba') is not -1:
    orilocations.append(('/media/ba/epg.db', '/media/ba'))
if mounts.find('/media/hdd') is not -1:
    orilocations.append(('/media/hdd/epg.db', '/media/hdd'))
config.plugins.epgdbbackup.orig_location = ConfigSelection(default='/etc/enigma2/epg.db', choices=orilocations)
config.plugins.epgdbbackup.time = ConfigInteger(default=0, limits=(0, 24))
pragmas = []
pragmas.append(('size', _('size info')))
pragmas.append(('quick_check', _('quick check')))
pragmas.append(('integrity_check', _('integritiy check')))
pragmas.append(('vacuum', _('vacuum cleaning')))
pragmas.append(('empty', _('empty database')))
pragmas.append(('remove', _('remove backup')))
pragmas.append(('delete', _('delete external events')))
pragmas.append(('degrade', _('degrade external events')))
pragmas.append(('timespan', _('remove events out of time span')))
config.plugins.epgdbbackup.check = ConfigSelection(default='quick_check', choices=pragmas)
config.plugins.epgdbbackup.keep = ConfigInteger(default=0, limits=(0, 9))
config.plugins.epgdbbackup.use = ConfigInteger(default=0, limits=(0, 9))
desktopSize = getDesktop(0).size()

class TSEpgSetup(Screen, ConfigListScreen):
    skin_1280 = '\n\t\t<screen name="TSEpgSetup" position="center,77" size="920,600" title="EPG setup" >\n\t\t        <eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\n\t                <ePixmap name="red"    position="70,545"   zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" transparent="1" alphatest="blend" />\n\t                <ePixmap name="green"  position="280,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_green.png" transparent="1" alphatest="blend" />\n\t                <ePixmap name="yellow" position="490,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_yellow.png" transparent="1" alphatest="blend" /> \n        \t        <ePixmap name="blue"   position="700,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_blue.png" transparent="1" alphatest="blend" /> \n        \t        <widget name="key_red" position="70,550" size="140,40" valign="center" halign="center" zPosition="2"  font="Regular;21" transparent="1" /> \n        \t        <widget name="key_green" position="280,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" /> \n                        <widget name="key_yellow" position="490,555" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;20" transparent="1" />\n        \t        <!--widget name="key_ok" position="870,550" size="30,30" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_ok.png" transparent="1" alphatest="blend" /> -->\n        \t        <widget name="key_blue" position="700,550" size="150,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" />\n                        <widget name="config" position="20,20" size="880,490" scrollbarMode="showOnDemand" transparent="1" zPosition="1" />\n\t\t</screen>'
    skin_1920 = '    <screen name="TSEpgSetup" position="center,200" size="1300,720" title="EPG Setup">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png" position="50,640" size="200,40" alphatest="blend" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green-big.png" position="360,640" size="200,40" alphatest="blend" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/yellow-big.png" position="670,640" size="200,40" alphatest="blend" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/blue-big.png" position="980,640" size="200,40" alphatest="blend" />\n    <widget name="key_red" position="50,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#940d0d" transparent="1" />\n    <widget name="key_green" position="360,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#2d872d" transparent="1" />\n    <widget name="key_yellow" position="670,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#bba502" transparent="1" />\n    <widget name="key_blue" position="980,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#18188b" transparent="1" />\n    <widget name="config" position="20,30" size="1260,600" zPosition="2" itemHeight="40" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background"  transparent="1" />\n    </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session, args=0):
        self.session = session
        Screen.__init__(self, session)
        self['key_red'] = Button(_('Cancel'))
        self['key_green'] = Button(_('Save'))
        self['key_yellow'] = Button(_('Restore'))
        self['key_blue'] = Button(_('Command'))
        self.onChangedEntry = []
        self.list = []
        ConfigListScreen.__init__(self, self.list, session=self.session, on_change=self.changedEntry)
        self.createSetup()
        self['setupActions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': (self.save), 'green': (self.backup), 
           'red': (self.save), 
           'yellow': (self.reload), 
           'blue': (self.command), 
           'cancel': (self.save)}, -1)
        self.epgdb_old = config.misc.epgcache_filename.value
        self.onLayoutFinish.append(self.setCustomTitle)
        return

    def setCustomTitle(self):
        self.setTitle(_('EPG setup'))
        return

    def save(self):
        for x in self['config'].list:
            x[1].save()

        if config.misc.epgcache_filename.value != config.plugins.epgdbbackup.orig_location.value:
            config.misc.epgcache_filename.value = config.plugins.epgdbbackup.orig_location.value
            config.misc.epgcache_filename.save()
        config.misc.epgcache_timespan.save()
        config.misc.epgcache_outdated_timespan.save()
        self.close(True)
        return

    def cancel(self):
        for x in self['config'].list:
            x[1].cancel()

        self.close(False)
        return

    def reload(self):
        self.epgdb_old = config.misc.epgcache_filename.value
        self.epgdb_backup = '%s/epg.db_%s' % (config.plugins.epgdbbackup.location.value, config.plugins.epgdbbackup.use.value)
        if not os.path.exists(self.epgdb_backup):
            self.session.open(MessageBox, _('Backup to EPG %s not found') % self.epgdb_backup, MessageBox.TYPE_ERROR)
            return
        config.misc.epgcache_filename.value = self.epgdb_backup
        config.misc.epgcache_filename.save()
        self.epginstance = eEPGCache.getInstance()
        self.cacheState_conn = self.epginstance.cacheState.connect(self.cacheStateChanged)
        eEPGCache.load(self.epginstance)
        return

    def cacheStateChanged(self, state):
        if state.state == cachestate.load_finished:
            print '[EPGDB] epgcache load finished'
            del self.cacheState_conn
            config.misc.epgcache_filename.value = self.epgdb_old
            config.misc.epgcache_filename.save()
            self.session.open(MessageBox, _('Restore of EPG was done from %s') % self.epgdb_backup, MessageBox.TYPE_INFO)
        elif state.state == cachestate.save_finished:
            print '[EPGDB] epgcache save finished'
            del self.cacheState_conn
            config.misc.epgcache_filename.value = self.epgdb_old
            config.misc.epgcache_filename.save()
            if os.path.exists(self.epgdb_backup):
                size = os.path.getsize(self.epgdb_backup) / 1024
                min_size = 23
                if size >= min_size:
                    if size < 1024:
                        self.session.open(MessageBox, _('Backup to EPG %s done with size %d kB') % (self.epgdb_backup, size), MessageBox.TYPE_INFO)
                    else:
                        sizef = float(size) / 1024.0
                        self.session.open(MessageBox, _('Backup to EPG %s done with size %4.2f MB') % (self.epgdb_backup, sizef), MessageBox.TYPE_INFO)
                    return
            else:
                self.session.open(MessageBox, _('Backup to EPG %s failed') % self.epgdb_backup, MessageBox.TYPE_ERROR)
        return

    def backup(self):
        self.epgdb_old = config.misc.epgcache_filename.value
        y = int(config.plugins.epgdbbackup.keep.value)
        for x in range(9, -1, -1):
            p = '%s/epg.db_%d' % (config.plugins.epgdbbackup.location.value, x)
            if x < y:
                overwrite = x + 1
                q = '%s/epg.db_%d' % (config.plugins.epgdbbackup.location.value, overwrite)
                if os.path.exists(q):
                    os.remove(q)
                if os.path.exists(p):
                    os.rename(p, q)
            elif os.path.exists(p):
                os.remove(p)

        self.epgdb_backup = '%s/epg.db_0' % config.plugins.epgdbbackup.location.value
        config.misc.epgcache_filename.value = self.epgdb_backup
        config.misc.epgcache_filename.save()
        self.epginstance = eEPGCache.getInstance()
        self.cacheState_conn = self.epginstance.cacheState.connect(self.cacheStateChanged)
        eEPGCache.save(self.epginstance)
        return

    def command(self):
        self.epgdb_backup = '%s/epg.db_%s' % (config.plugins.epgdbbackup.location.value, config.plugins.epgdbbackup.use.value)
        if config.plugins.epgdbbackup.check.value == 'empty' or config.plugins.epgdbbackup.check.value == 'remove':
            if os.path.exists(self.epgdb_backup):
                os.remove(self.epgdb_backup)
        elif not os.path.exists(self.epgdb_backup):
            self.session.open(MessageBox, _('Backup of EPG %s not found') % self.epgdb_backup, MessageBox.TYPE_ERROR)
            return
        if config.plugins.epgdbbackup.check.value == 'remove':
            self.session.open(MessageBox, _('Backup of EPG %s was removed'), MessageBox.TYPE_INFO)
            return
        if config.plugins.epgdbbackup.check.value == 'size':
            if not os.path.exists(self.epgdb_backup):
                self.session.open(MessageBox, _('Backup of EPG %s not found') % self.epgdb_backup, MessageBox.TYPE_ERROR)
                return
            size = os.path.getsize(self.epgdb_backup) / 1024
            if size < 1024:
                self.session.open(MessageBox, _('Size of Backup of EPG %s is %d kB') % (self.epgdb_backup, size), MessageBox.TYPE_INFO)
            else:
                sizef = float(size) / 1024.0
                self.session.open(MessageBox, _('Size of Backup of EPG %s is %4.2f MB') % (self.epgdb_backup, sizef), MessageBox.TYPE_INFO)
            return
        connection = sqlite.connect(self.epgdb_backup, timeout=10)
        connection.text_factory = str
        cursor = connection.cursor()
        if config.plugins.epgdbbackup.check.value == 'vacuum':
            self.oldsize = os.path.getsize(self.epgdb_backup) / 1024
            cmd = 'VACUUM'
            cursor.execute(cmd)
            self.newsize = os.path.getsize(self.epgdb_backup) / 1024
            if self.oldsize > 1024 and self.newsize > 1024:
                oldsizef = float(self.oldsize) / 1024.0
                newsizef = float(self.newsize) / 1024.0
                self.session.open(MessageBox, _('Backup of EPG %s was vacuumed\n\nfrom %4.2f MB to %4.2f MB') % (self.epgdb_backup, oldsizef, newsizef), MessageBox.TYPE_INFO)
            else:
                self.session.open(MessageBox, _('Backup of EPG %s was vacuumed\n\nfrom %d kB to %s kB') % (self.epgdb_backup, self.oldsize, self.newsize), MessageBox.TYPE_INFO)
        elif config.plugins.epgdbbackup.check.value == 'timespan':
            self.epg_outdated = int(config.misc.epgcache_outdated_timespan.value)
            self.epoch_time = int(time.time()) - self.epg_outdated * 3600
            self.epg_timespan = int(config.misc.epgcache_timespan.value)
            self.epg_cutoff_time = int(time.time()) + self.epg_timespan * 86400
            cmd = "DELETE FROM T_Event WHERE begin_time < datetime(%d, 'unixepoch')" % self.epoch_time
            cursor.execute(cmd)
            cmd = "DELETE FROM T_Event WHERE begin_time > datetime(%d, 'unixepoch')" % self.epg_cutoff_time
            cursor.execute(cmd)
            self.session.open(MessageBox, _('Events out of time span were removed from Backup of EPG %s') % self.epgdb_backup, MessageBox.TYPE_INFO)
        elif config.plugins.epgdbbackup.check.value == 'empty':
            cursor.execute('CREATE TABLE T_Service (id INTEGER PRIMARY KEY, sid INTEGER NOT NULL, tsid INTEGER, onid INTEGER, dvbnamespace INTEGER, changed DATETIME NOT NULL DEFAULT current_timestamp)')
            cursor.execute('CREATE TABLE T_Source (id INTEGER PRIMARY KEY, source_name TEXT NOT NULL, priority INTEGER NOT NULL, changed DATETIME NOT NULL DEFAULT current_timestamp)')
            cursor.execute('CREATE TABLE T_Title (id INTEGER PRIMARY KEY, hash INTEGER NOT NULL UNIQUE, title TEXT NOT NULL, changed DATETIME NOT NULL DEFAULT current_timestamp)')
            cursor.execute('CREATE TABLE T_Short_Description (id INTEGER PRIMARY KEY, hash INTEGER NOT NULL UNIQUE, short_description TEXT NOT NULL, changed DATETIME NOT NULL DEFAULT current_timestamp)')
            cursor.execute('CREATE TABLE T_Extended_Description (id INTEGER PRIMARY KEY, hash INTEGER NOT NULL UNIQUE, extended_description TEXT NOT NULL, changed DATETIME NOT NULL DEFAULT current_timestamp)')
            cursor.execute('CREATE TABLE T_Event (id INTEGER PRIMARY KEY, service_id INTEGER NOT NULL, begin_time INTEGER NOT NULL, duration INTEGER NOT NULL, source_id INTEGER NOT NULL, dvb_event_id INTEGER, changed DATETIME NOT NULL DEFAULT current_timestamp)')
            cursor.execute('CREATE TABLE T_Data (event_id INTEGER NOT NULL, title_id INTEGER, short_description_id INTEGER, extended_description_id INTEGER, iso_639_language_code TEXT NOT NULL, changed DATETIME NOT NULL DEFAULT current_timestamp)')
            cursor.execute('CREATE INDEX data_title ON T_Data (title_id)')
            cursor.execute('CREATE INDEX data_shortdescr ON T_Data (short_description_id)')
            cursor.execute('CREATE INDEX data_extdescr ON T_Data (extended_description_id)')
            cursor.execute('CREATE INDEX service_sid ON T_Service (sid)')
            cursor.execute('CREATE INDEX event_service_id_begin_time ON T_Event (service_id, begin_time)')
            cursor.execute('CREATE INDEX event_dvb_id ON T_Event (dvb_event_id)')
            cursor.execute('CREATE INDEX data_event_id ON T_Data (event_id)')
            cursor.execute('CREATE TRIGGER tr_on_delete_cascade_t_event AFTER DELETE ON T_Event FOR EACH ROW BEGIN DELETE FROM T_Data WHERE event_id = OLD.id; END')
            cursor.execute('CREATE TRIGGER tr_on_delete_cascade_t_service_t_event AFTER DELETE ON T_Service FOR EACH ROW BEGIN DELETE FROM T_Event WHERE service_id = OLD.id; END')
            cursor.execute('CREATE TRIGGER tr_on_delete_cascade_t_data_t_title AFTER DELETE ON T_Data FOR EACH ROW WHEN ((SELECT event_id FROM T_Data WHERE title_id = OLD.title_id LIMIT 1) ISNULL) BEGIN DELETE FROM T_Title WHERE id = OLD.title_id; END')
            cursor.execute('CREATE TRIGGER tr_on_delete_cascade_t_data_t_short_description AFTER DELETE ON T_Data FOR EACH ROW WHEN ((SELECT event_id FROM T_Data WHERE short_description_id = OLD.short_description_id LIMIT 1) ISNULL) BEGIN DELETE FROM T_Short_Description WHERE id = OLD.short_description_id; END')
            cursor.execute('CREATE TRIGGER tr_on_delete_cascade_t_data_t_extended_description AFTER DELETE ON T_Data FOR EACH ROW WHEN ((SELECT event_id FROM T_Data WHERE extended_description_id = OLD.extended_description_id LIMIT 1) ISNULL) BEGIN DELETE FROM T_Extended_Description WHERE id = OLD.extended_description_id; END')
            cursor.execute('CREATE TRIGGER tr_on_update_cascade_t_data AFTER UPDATE ON T_Data FOR EACH ROW WHEN (OLD.title_id <> NEW.title_id AND ((SELECT event_id FROM T_Data WHERE title_id = OLD.title_id LIMIT 1) ISNULL)) BEGIN DELETE FROM T_Title WHERE id = OLD.title_id; END')
            cursor.execute("INSERT INTO T_Source (id,source_name,priority) VALUES('0','Sky Private EPG','0')")
            cursor.execute("INSERT INTO T_Source (id,source_name,priority) VALUES('1','DVB Now/Next Table','0')")
            cursor.execute("INSERT INTO T_Source (id,source_name,priority) VALUES('2','DVB Schedule (same Transponder)','0')")
            cursor.execute("INSERT INTO T_Source (id,source_name,priority) VALUES('3','DVB Schedule Other (other Transponder)','0')")
            cursor.execute("INSERT INTO T_Source (id,source_name,priority) VALUES('4','Viasat','0')")
            connection.commit()
            self.session.open(MessageBox, _('Created empty EPG database %s') % self.epgdb_backup, MessageBox.TYPE_INFO)
        elif config.plugins.epgdbbackup.check.value == 'delete':
            cursor.execute('DELETE from T_Event where source_id>4;')
            connection.commit()
            self.session.open(MessageBox, _('External events of Backup EPG database %s were deleted') % self.epgdb_backup, MessageBox.TYPE_INFO)
        elif config.plugins.epgdbbackup.check.value == 'degrade':
            cursor.execute('UPDATE T_Event SET source_id=2 where source_id>4;')
            connection.commit()
            self.session.open(MessageBox, _('External events of Backup EPG database %s were degraded\n\nBe warned to load it!') % self.epgdb_backup, MessageBox.TYPE_WARNING)
        else:
            cmd = 'PRAGMA %s' % config.plugins.epgdbbackup.check.value
            cursor.execute(cmd)
            result = cursor.fetchall()
            text_result = ''
            for res in result:
                text_result = text_result + str(res[0])

            self.session.open(MessageBox, _('Check of Backup of EPG %s was executed\n\nResult: %s') % (self.epgdb_backup, text_result), MessageBox.TYPE_INFO)
        cursor.close()
        connection.close()
        return

    def createSetup(self):
        self.list = []
        self.list.append(getConfigListEntry(_('Cache timespan days [7-28]'), config.misc.epgcache_timespan))
        self.list.append(getConfigListEntry(_('Cache outdated timespan hours [0-96]'), config.misc.epgcache_outdated_timespan))
        self.list.append(getConfigListEntry(_('Original path'), config.plugins.epgdbbackup.orig_location))
        self.list.append(getConfigListEntry(_('Backup path'), config.plugins.epgdbbackup.location))
        self.list.append(getConfigListEntry(_('Backup every X hour [0-24, 0 is none]'), config.plugins.epgdbbackup.time))
        self.list.append(getConfigListEntry(_('Keep number of backups [0-9]'), config.plugins.epgdbbackup.keep))
        self.list.append(getConfigListEntry(_('Use number of backup [0-9]'), config.plugins.epgdbbackup.use))
        self.list.append(getConfigListEntry(_('Database Command'), config.plugins.epgdbbackup.check))
        self['config'].list = self.list
        self['config'].l.setList(self.list)
        return

    def changedEntry(self):
        self.createSetup()
        return


class EPGdbBackupAutoStartTimer:

    def __init__(self, session):
        self.session = session
        self.timer = eTimer()
        self.timer_conn = self.timer.timeout.connect(self.autobackup)
        self.timer.stop()
        self.epgdb_old = config.misc.epgcache_filename.value
        wake = 3600000
        self.timer.start(wake, True)
        return

    def autobackup(self):
        self.timer.stop()
        wake = 3600000 * int(config.plugins.epgdbbackup.time.value)
        if wake == 0:
            wake = 3600000
            print '[EPGdbBackup] automatic epg backup is disabled'
        else:
            print '[EPGdbBackup] automatic epg backup starts'
            self.epgdb_old = config.misc.epgcache_filename.value
            y = int(config.plugins.epgdbbackup.keep.value)
            for x in range(9, -1, -1):
                p = '%s/epg.db_%d' % (config.plugins.epgdbbackup.location.value, x)
                if x < y:
                    overwrite = x + 1
                    q = '%s/epg.db_%d' % (config.plugins.epgdbbackup.location.value, overwrite)
                    if os.path.exists(q):
                        os.remove(q)
                    if os.path.exists(p):
                        os.rename(p, q)
                elif os.path.exists(p):
                    os.remove(p)

            self.epgdb_backup = '%s/epg.db_0' % config.plugins.epgdbbackup.location.value
            config.misc.epgcache_filename.value = self.epgdb_backup
            config.misc.epgcache_filename.save()
            self.epginstance = eEPGCache.getInstance()
            self.cacheState_conn = self.epginstance.cacheState.connect(self.cacheStateChanged)
            eEPGCache.save(self.epginstance)
        self.timer.start(wake, True)
        return

    def cacheStateChanged(self, state):
        del self.cacheState_conn
        if state.state == cachestate.save_finished:
            print '[EPGDB] epgcache background save finished'
            config.misc.epgcache_filename.value = self.epgdb_old
            config.misc.epgcache_filename.save()
            if os.path.exists(self.epgdb_backup):
                size = os.path.getsize(self.epgdb_backup) / 1024
                min_size = 23
                if size >= min_size:
                    print '[EPGDB] %s is NOW saved with %d kB' % (self.epgdb_backup, size)
                    return
            print '[EPGDB] %s is NOT saved' % self.epgdb_backup
        return


return
