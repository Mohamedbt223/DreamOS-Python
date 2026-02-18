# uncompyle6 version 3.9.0
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.8.10 (default, Nov 22 2023, 10:22:35) 
# [GCC 9.4.0]
# Embedded file name: /usr/lib/enigma2/python/Components/TSUpdater.py
# Compiled at: 2025-08-26 13:21:43
from enigma import eConsoleAppContainer, eTimer
from os import path as os_path, remove as os_remove
import urllib2
from Components.config import config, configfile
HEADER = '\x1b[95m'
OKBLUE = '\x1b[94m'
OKGREEN = '\x1b[92m'
WARNING = '\x1b[93m'
FAIL = '\x1b[91m'
ENDC = '\x1b[0m'

def _set_update_available(n):
    try:
        n = int(n or 0)
    except Exception:
        n = 0

    try:
        item = config.plugins.TSUpdater.UpdateAvailable
        cls = getattr(item, '__class__', type(item)).__name__
        if hasattr(item, 'setValue'):
            if cls == 'ConfigText':
                item.setValue(str(n))
            else:
                item.setValue(n)
        elif cls == 'ConfigText':
            item.value = str(n)
        else:
            item.value = n
        config.plugins.TSUpdater.save()
        print '[TSUpdater] UpdateAvailable set to %d' % n
    except Exception as e:
        print '[TSUpdater] _set_update_available failed: %s' % e


class TSUpdater:

    def __init__(self):
        self.timer = eTimer()
        self.cache = None
        self.errors = None
        return

    def cleantmp(self):
        print '[dpkgUpdater] clean tmp files'
        self.saveUpdateAvailable(0)
        if os_path.exists('/tmp/.dpkg_updater'):
            os_remove('/tmp/.dpkg_updater')
        if os_path.exists('/tmp/.dpkg_busy'):
            os_remove('/tmp/.dpkg_busy')
        if os_path.exists('/tmp/.dpkg_ready'):
            os_remove('/tmp/.dpkg_ready')
        if os_path.exists('/tmp/.dpkg_ugradable'):
            os_remove('/tmp/.dpkg_ugradable')
        if os_path.exists('/tmp/.newsettings'):
            os_remove('/tmp/.newsettings')
        if os_path.exists('/tmp/.newskin'):
            os_remove('/tmp/.newskin')
        if os_path.exists('/tmp/.newlang'):
            os_remove('/tmp/.newlang')
        if os_path.exists('/tmp/.restart_e2'):
            os_remove('/tmp/.restart_e2')
        if os_path.exists('/tmp/.dpkglist'):
            os_remove('/tmp/.dpkglist')
        if os_path.exists('/tmp/.tmplist'):
            os_remove('/tmp/.tmplist')
        if os_path.exists('/tmp/.plugin_info'):
            os_remove('/tmp/.plugin_info')

    def dpkgUpdate(self):
        self.timer.stop()
        self.cleantmp()
        if self.checkConnection():
            print '[dpkgUpdater] start dpkg update'
            self.cache = None
            self.errors = None
            cmd = 'touch /tmp/.dpkg_updater; touch /tmp/.dpkg_busy ; apt-get update'
            self.container = eConsoleAppContainer()
            self.container_appClosed = self.container.dataAvail.connect(self.cmdData)
            self.container_conn = self.container.appClosed.connect(self.dpkgListUpgradable)
            self.container.execute(cmd)
        if config.plugins.TSUpdater.enable.value:
            self.timer_conn = self.timer.timeout.connect(self.dpkgUpdate)
            self.timer.startLongTimer(int(config.plugins.TSUpdater.refreshInterval.value) * 3600)
        return

    def checkConnection(self):
        try:
            response = urllib2.urlopen('http://tunisia-dreambox.info', timeout=5)
            print '%s[dpkgUpdater] Update server check: ok%s' % (OKGREEN, ENDC)
            return True
        except urllib2.URLError as e:
            if hasattr(e, 'reason'):
                err = str(e.reason)
                print FAIL + '%s[dpkgUpdater] Update server check exception with reason: %s%s' % (FAIL, err, ENDC)
            else:
                if hasattr(e, 'code'):
                    err = str(e.code)
                    print '%s[dpkgUpdater] Update server check error code: %s%s' % (FAIL, err, ENDC)
                else:
                    print '%s[dpkgUpdater] Update server check URLError%s' % (FAIL, ENDC)
        except:
            print '%s[dpkgUpdater] Update server check: Exception!%s' % (FAIL, ENDC)

        return False

    def cmdData(self, data):
        if self.cache is None:
            self.cache = data
        else:
            self.cache += data
        if '\n' in data:
            splitcache = self.cache.split('\n')
            if self.cache[-1] == '\n':
                iteration = splitcache
                self.cache = None
            else:
                iteration = splitcache[:-1]
                self.cache = splitcache[-1]
            for mydata in iteration:
                if mydata != '':
                    self.parseLine(mydata)

        return

    def parseLine(self, data):
        if data.find('Ign') == 0:
            print '[dpkgUpdater] Downloading %s' % data.split(' ', 5)[1].strip()
        elif data.find('Get') == 0:
            print '[dpkgUpdater] Inflating %s' % data.split(' ', 5)[1].strip()
        elif data.find('E:') == 0:
            self.errors = data
            print '%s[dpkgUpdater] error dpkg_download: %s%s' % (FAIL, self.errors, ENDC)
        elif data.find('E:') == 0:
            self.errors = data.replace(' * dpkg_download: ', '')
            print '%s[dpkgUpdater] error dpkg_download: %s%s' % (FAIL, self.errors, ENDC)
        elif data.find('Collected errors:') == 0:
            self.errors = data
            print '%s[dpkgUpdater] %s%s' % (FAIL, self.errors, ENDC)

    def dpkgListUpgradable(self, status=True):
        self.container_appClosed = None
        self.container_conn = None
        if self.errors is None:
            cmd = 'apt-opkg list_upgradable > /tmp/.dpkg_ugradable'
            extra = ''
            print '[dpkgUpdater] start apt-opkg list_upgradable' + extra
            self.container_appClosed = self.container.appClosed.connect(self.dpkgList)
            self.container_conn = self.container.dataAvail.connect(self.cmdData)
            self.container.execute(cmd)
        else:
            if os_path.exists('/tmp/.dpkg_busy'):
                os_remove('/tmp/.dpkg_busy')
            if os_path.exists('/tmp/.dpkg_updater'):
                os_remove('/tmp/.dpkg_updater')
        return

    def dpkgList(self, status=True):
        self.container_appClosed = None
        self.container_conn = None
        if self.errors is None:
            self.dpkgUpgradable()
            print '[dpkgUpdater] start dpkg list'
            cmd = "apt-opkg list | grep -E 'enigma2-plugin-extensions-|enigma2-plugin-systemplugins-|enigma2-skin-ts-|enigma2-cams-|nodejs-module-|exfat|ntfs-|kernel-' > /tmp/.dpkglist ; touch /tmp/.dpkg_ready ; rm /tmp/.dpkg_busy; rm /tmp/.dpkg_updater"
            self.container_appClosed = self.container.appClosed.connect(self.ondpkgListClose)
            self.container.execute(cmd)
        return

    def ondpkgListClose(self, status=True):
        self.container_appClosed = None
        self.container_conn = None
        print '%s[dpkgUpdater] dpkg updated successfully...%s' % (OKGREEN, ENDC)
        if config.plugins.TSUpdater.enable.value:
            print '[dpkgUpdater] next dpkg update in %d hours' % int(config.plugins.TSUpdater.refreshInterval.value)
        else:
            print '[dpkgUpdater] dpkg updater is disabled'
        return

    def dpkgUpgradable(self):
        if os_path.exists('/tmp/.dpkg_ugradable'):
            self.saveUpdateAvailable(self.getdpkgUpgradable())
        else:
            print '%s[dpkgUpdater] dpkg not ready --> resources busy...%s' % (WARNING, ENDC)

    def getdpkgUpgradable(self):
        count = 0
        try:
            f = open('/tmp/.dpkg_ugradable', 'r')
            try:
                for line in f:
                    if line.strip():
                        count += 1

            finally:
                f.close()

        except Exception as e:
            print '[dpkgUpdater] read failed: %s' % e

        print '%s[dpkgUpdater] available updates: %d package(s)%s' % (WARNING, count, ENDC)
        return count

    def saveUpdateAvailable(self, upgradable_nr):
        _set_update_available(upgradable_nr)
        try:
            configfile.save()
        except Exception as e:
            print '[TSUpdater] configfile.save() skipped: %s' % e