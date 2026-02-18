# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/CamsManager/CCcamOscamInfo/cccam/pairs.py
# Compiled at: 2016-11-22 07:53:26
import string, os

def _caseIndependentSort(something, other):
    something, other = string.lower(something), string.lower(other)
    return cmp(something, other)


def read_Mapping(ret, res_servers, res_clients):
    if ret == 1:
        try:
            res = []
            HostList = {}
            unknownHost = []
            ClientList = {}
            mappedList = []
            unknownClient = []
            remove = []
            for i in res_servers[1].split('\n'):
                i = i.split('|')
                if len(i) > 8 and i[1].strip() != 'Host':
                    if i[1].strip() != '':
                        x = os.popen('nslookup %s' % i[1].strip().split(':')[0]).read().split('\n')
                        if len(x) == 6:
                            HostList[x[4].split(':')[1].strip().split(' ')[0]] = x[3].split(':')[1].strip()
                        else:
                            unknownHost.append('%s,NA' % i[1].strip().split(':')[0])

            for i in res_clients[1].split('\n'):
                i = i.split('|')
                if len(i) > 8 and i[2].strip() != 'Host':
                    if i[2].strip() not in ClientList:
                        ClientList[i[2].strip()] = i[1].strip()
                    else:
                        ClientList[i[2].strip()] = '%s;;;%s' % (ClientList[i[2].strip()], i[1].strip())

            for i in HostList.keys():
                try:
                    mappedList.append('%s,%s,%s' % (HostList[i], ClientList[i], i))
                    del HostList[i]
                    del ClientList[i]
                except:
                    unknownHost.append('%s,%s' % (HostList[i], i))

            tmp = []
            for x in mappedList:
                if len(x.split(',')[1].split(';;;')) > 1:
                    y = x.split(',')[1].split(';;;')
                    for z in y:
                        tmp.append('%s,%s,%s' % (x.split(',')[0], z, x.split(',')[2]))

                else:
                    tmp.append(x)

            mappedList = tmp
            mappedList.sort(_caseIndependentSort)
            unknownHost.sort(_caseIndependentSort)
            for i in ClientList.keys():
                unknownClient.append('%s,%s' % (ClientList[i], i))

            unknownClient.sort(_caseIndependentSort)
            res.append(mappedList)
            res.append(unknownHost)
            res.append(unknownClient)
        except:
            res = [
             [
              _('Error') + ',' + _('Error') + ',' + _('Error')], [_('Error') + ',' + _('Error')], [_('Error') + ',' + _('Error')]]

    else:
        res = [
         [
          _('Error') + ',' + _('Error') + ',' + _('Error')], [_('Error') + ',' + _('Error')], [_('Error') + ',' + _('Error')]]
    return res


return
