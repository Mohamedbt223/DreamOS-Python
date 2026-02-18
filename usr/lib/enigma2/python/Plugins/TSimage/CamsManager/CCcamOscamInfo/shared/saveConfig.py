# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/CamsManager/CCcamOscamInfo/shared/saveConfig.py
# Compiled at: 2014-05-25 10:33:38
import os
from time import localtime
from readConfig import read_Config
[{'partnerbox': 'no'}]

def save_Config(config):
    ret = 0
    if os.path.isdir('/etc/enigma2') == True:
        try:
            os.rename('/etc/enigma2/cccamoscaminfo.xml', '/etc/enigma2/cccamoscaminfo.xml_old')
        except:
            pass

    else:
        os.mkdir('/etc/enigma2')
    f = open('/etc/enigma2/cccamoscaminfo.xml', 'w')
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<dictionary>\n')
    for x in config:
        if len(config):
            try:
                f.write('    <account>\n')
                f.write('        <default>%s</default>\n' % x['default'])
                f.write('        <cam>%s</cam>\n' % x['cam'])
                f.write('        <http>%s</http>\n' % x['http'])
                f.write('        <name>%s</name>\n' % x['name'])
                f.write('        <url>%s</url>\n' % x['url'])
                f.write('        <port>%s</port>\n' % x['port'])
                f.write('        <user>%s</user>\n' % x['user'])
                f.write('        <password>%s</password>\n' % x['password'])
                if x['cam'] == 'CCcamLocal':
                    f.write('        <changeconfig>%s</changeconfig>\n' % x['changeconfig'])
                    if x['changeconfig'] == 'yes':
                        f.write('        <path>%s</path>\n' % x['path'])
                elif x['cam'] == 'CCcamRemote':
                    f.write('        <partnerbox>%s</partnerbox>\n' % x['partnerbox'])
                    if x['partnerbox'] == 'yes':
                        f.write('        <partnerboxpassword>%s</partnerboxpassword>\n' % x['partnerboxpassword'])
                        f.write('        <partnerboxsshport>%s</partnerboxsshport>\n' % x['partnerboxsshport'])
                f.write('    </account>\n')
                ret += 1
            except:
                ret = 0

    f.write('</dictionary>\n')
    f.close()
    if ret != len(config) or len(config) == 0:
        ret = 0
        try:
            os.remove('/etc/enigma2/cccamoscaminfo.xml')
            os.rename('/etc/enigma2/cccamoscaminfo.xml_old', '/etc/enigma2/cccamoscaminfo.xml')
        except:
            pass

    else:
        ret = 1
    return ret


def del_Config():
    try:
        os.remove('/etc/enigma2/cccamoscaminfo.xml')
        ret = 1
        try:
            os.remove('/etc/enigma2/cccamoscaminfo.xml_old')
        except:
            pass

    except:
        ret = 0

    return ret


def backup_Config(path):
    try:
        os.system('cp /etc/enigma2/cccamoscaminfo.xml /etc/enigma2/config_%s.xml' % ('%04i:%02i:%02i_%02i:%02i:%02i' % localtime()[0:6]))
        ret = 1
    except:
        ret = 0

    return ret


def del_backupConfig():
    try:
        os.remove('/etc/enigma2/config_*.xml')
        ret = 1
        try:
            os.remove('/etc/enigma2/cccamoscaminfo.xml_old')
        except:
            pass

    except:
        ret = 0

    return ret


def restore_config(path):
    return


return
