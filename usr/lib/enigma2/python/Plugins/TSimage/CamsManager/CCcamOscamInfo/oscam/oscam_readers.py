# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/CamsManager/CCcamOscamInfo/oscam/oscam_readers.py
# Compiled at: 2014-05-25 10:33:38
import os, string
from parser import _parse_xml_userstatus
from parser import _parse_xml_status
from parser import _parse_xml_readerlist

def _caseIndependentSort(something, other):
    try:
        something, other = string.lower(something['Label']), string.lower(other['Label'])
    except:
        something, other = string.lower(something['Name']), string.lower(other['Name'])

    return cmp(something, other)


def oscamAllReaders(ret, readers):
    res = []
    reader = []
    proxy = []
    try:
        res = _parse_xml_readerlist(ret, readers)
        res.sort(_caseIndependentSort)
        for x in res:
            if x['Protocol'] in ('mouse', 'smartreader', 'internal', 'sc8in1', 'pcsc',
                                 'serial', 'constcw', 'mouse_test', 'smargo'):
                reader.append(x)
            elif x['Protocol'] in ('mp35', 'camd33', 'camd35', 'cs378x', 'newcand',
                                   'newcamd524', 'cccam', 'gbox', 'radegast'):
                proxy.append(x)

    except:
        pass

    res = []
    res.append(reader)
    res.append(proxy)
    return res


def oscamEnableDisable(ret, readers, clients):
    res = []
    reader = []
    proxy = []
    client = []
    try:
        res = _parse_xml_readerlist(ret, readers)
        res.sort(_caseIndependentSort)
        for x in res:
            if x['Protocol'] in ('mouse', 'smartreader', 'internal', 'sc8in1', 'pcsc',
                                 'serial', 'constcw', 'mouse_test', 'smargo'):
                reader.append(x)
            elif x['Protocol'] in ('mp35', 'camd33', 'camd35', 'cs378x', 'newcand',
                                   'newcamd524', 'cccam', 'gbox', 'radegast'):
                proxy.append(x)

        oscam, res, total = _parse_xml_userstatus(ret, clients)
        res.sort(_caseIndependentSort)
        for x in res:
            if 'disabled' in x['Status']:
                tmp = '0'
            else:
                tmp = '1'
            tmp_dic = {'Name': (x['Name']), 'Protocol': (x['Protocol']), 'Status': tmp}
            client.append(tmp_dic)

    except:
        pass

    return (
     reader, proxy, client)


return
