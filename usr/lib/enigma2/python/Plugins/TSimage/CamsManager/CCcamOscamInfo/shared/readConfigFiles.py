# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/CamsManager/CCcamOscamInfo/shared/readConfigFiles.py
# Compiled at: 2014-05-25 10:33:38
import os, string

def read_Config_Files():
    foundcccam = 0
    foundoscam = 0
    ret = 0
    cccamconfig = {}
    oscamconfig = {}
    res = []
    tasks = os.popen('ps -ef')
    tasks = [zeile.strip() for zeile in tasks]
    for x in tasks:
        cccam = string.count(x, 'cccam')
        oscam = string.count(x, 'oscam')
        if foundcccam == 0 or foundoscam == 0:
            if cccam > 0 and foundcccam == 0:
                foundcccam = x
            elif oscam > 0 and foundoscam == 0:
                foundoscam = x

    if foundcccam != 0:
        try:
            foundcccam = foundcccam.split('-C')[1].strip()
        except:
            foundcccam = 1

    if foundoscam != 0:
        try:
            foundoscam = foundoscam.split('-c')[1].strip()
        except:
            foundoscam = 1

    if foundcccam != 0:
        cccamconfig = {}
        try:
            port = user = password = None
            if foundcccam == 1:
                foundcccam = '/etc/CCcam.cfg'
                text = open(foundcccam, 'r')
            else:
                text = open('%s' % foundcccam, 'r')
            for line in text:
                if line.startswith('WEBINFO LISTEN PORT'):
                    port = line.split(':')[1].strip()
                elif line.startswith('WEBINFO USERNAME'):
                    user = line.split(':')[1].strip()
                elif line.startswith('WEBINFO PASSWORD'):
                    password = line.split(':')[1].strip()

            text.close()
            cccamconfig = {'cam': 'CCcamLocal', 'default': '0', 'http': 'http', 'name': 'localhost', 'url': '127.0.0.1', 'port': port, 'user': user, 'password': password, 'changeconfig': 'yes', 'path': (foundcccam.replace('/CCcam.cfg', ''))}
        except:
            cccamconfig = {'cam': 'CCcamLocal', 'default': '0', 'http': 'http', 'name': 'localhost', 'url': '127.0.0.1', 'port': '16001', 'user': None, 'password': None, 'changeconfig': 'no'}

        ret = ret + 2
        res.append(cccamconfig)
    if foundoscam != 0:
        oscamconfig = {}
        try:
            port = user = password = None
            if foundcccam == 1:
                foundoscam = '/var/tuxbox/config/oscam.conf'
                text = open('%s/oscam.conf' % foundoscam, 'r')
            else:
                text = open('%s/oscam.conf' % foundoscam, 'r')
            for line in text:
                if line.startswith('httpport'):
                    port = line.split('=')[1].strip()
                elif line.startswith('httpuser'):
                    user = line.split('=')[1].strip()
                elif line.startswith('httppwd'):
                    password = line.split('=')[1].strip()

            text.close()
            oscamconfig = {'cam': 'Oscam', 'default': '0', 'http': 'http', 'name': 'localhost', 'url': '127.0.0.1', 'port': port, 'user': user, 'password': password}
        except:
            oscamconfig = {'cam': 'Oscam', 'default': '0', 'http': 'http', 'name': 'localhost', 'url': '127.0.0.1', 'port': '83', 'user': None, 'password': None}

        ret = ret + 1
        res.append(oscamconfig)
    return (
     ret, res, foundoscam, foundcccam)


return
