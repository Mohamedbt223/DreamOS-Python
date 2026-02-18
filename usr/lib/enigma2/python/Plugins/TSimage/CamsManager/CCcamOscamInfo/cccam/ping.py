# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/CamsManager/CCcamOscamInfo/cccam/ping.py
# Compiled at: 2016-11-22 07:53:26
import string, os

def _caseIndependentSort(something, other):
    something, other = string.lower(something), string.lower(other)
    return cmp(something, other)


def ping_Servers(ret, web, path):
    HostList = []
    res = []
    if ret == 1:
        try:
            web = web[1].split('\n')
            for i in web:
                i = i.split('|')
                if len(i) > 8:
                    if i[1].strip() != '':
                        HostList.append(i[1].strip())

            del HostList[0]
            tmp = []
            res.append(_('Host') + ',' + _('Min') + ',' + _('Max') + ',' + _('Average'))
            for x in HostList:
                ping = str(os.popen("ping  -c 5 '%s'" % x.split(':')[0]).read()).split('\n')
                if len(ping) == 11:
                    color = 'red'
                    if int(ping[9].split(' ')[3].split('/')[1].split('.')[0]) < 40:
                        color = 'green'
                    elif int(ping[9].split(' ')[3].split('/')[1].split('.')[0]) < 100:
                        color = 'blue'
                    elif int(ping[9].split(' ')[3].split('/')[1].split('.')[0]) < 160:
                        color = 'yellow'
                    ping = '%s,%s,%s ms,%s ms,%s ms' % (x.split(':')[0],
                     color,
                     ping[9].split(' ')[3].split('/')[0].split('.')[0],
                     ping[9].split(' ')[3].split('/')[2].split('.')[0],
                     ping[9].split(' ')[3].split('/')[1].split('.')[0])
                else:
                    ping = '%s,red,- ms,- ms,- ms' % x.split(':')[0]
                tmp.append(ping)

            tmp.sort(_caseIndependentSort)
            res.append(tmp)
            if not os.path.exists('%s/daten' % path):
                os.mkdir('%s/daten' % path)
            datei = open('%s/daten/ping.txt' % path, 'w')
            for x in res[1]:
                datei.write('%s\n' % x)

            datei.close()
        except:
            res = [
             _('Host') + ',' + _('Min') + ',' + _('Max') + ',' + _('Average'), [_('Ping failed') + '.,red, , , ']]

    else:
        res = [
         _('Host') + ',' + _('Min') + ',' + _('Max') + ',' + _('Average'), [_('Ping failed') + '.,red, , , ']]
    return res


def read_Ping(path):
    res = []
    try:
        res = [
         _('Host') + ',' + _('Min') + ',' + _('Max') + ',' + _('Average')]
        tmp_res = []
        datei = open('%s/daten/ping.txt' % path, 'r')
        tmp = datei.read()
        datei.close()
        tmp = tmp.split('\n')
        for x in tmp:
            tmp_res.append(x)

        tmp_res.remove('')
        res.append(tmp_res)
    except:
        res = [
         _('Host') + ',' + _('Min') + ',' + _('Max') + ',' + _('Average'), [' , , , , ']]

    return res


def ping_oneServers(host):
    text = ''
    try:
        ping = os.popen("ping -c 5 '%s'" % host).read()
        ping = str(ping)
        ping = ping.split('\n')
        x = len(ping)
        if x == 11:
            text = '%s\n%s\n%s\n' % (ping[7].replace('--- ', '').replace(' ---', ''), ping[8], ping[9])
        else:
            text = _('The Server') + ' %s ' % host + _("don't response") + '.'
    except:
        text = 'Uups, das ist nicht gut'

    return text


return
