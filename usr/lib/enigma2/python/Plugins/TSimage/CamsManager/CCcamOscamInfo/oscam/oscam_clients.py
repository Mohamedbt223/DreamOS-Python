# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/CamsManager/CCcamOscamInfo/oscam/oscam_clients.py
# Compiled at: 2014-05-25 10:33:38
import os, string
from parser import _parse_xml_userstatus
from parser import _parse_xml_status

def _caseIndependentSort(something, other):
    something, other = string.lower(something['Name']), string.lower(other['Name'])
    return cmp(something, other)


def oscamClients(ret, status, select):
    res = []
    clients = []
    if ret == 1:
        try:
            oscam, clients = _parse_xml_status(1, status)
            for x in clients:
                try:
                    if x['Type'] == 'c' and select == 'Clients':
                        res.append(x)
                    elif x['Type'] == 'r' and select == 'Readers':
                        res.append(x)
                    elif x['Type'] == 'p' and select == 'Proxys':
                        res.append(x)
                except:
                    pass

            res.sort(_caseIndependentSort)
        except:
            res = [{'Type': '', 'Name': '', 'Desc': '', 'Protocol': '', 'Protocolext': '', 'AU': '', 'CaID': '', 'SrvID': '', 'ECMTime': '', 'ECMHistory': '', 'Answered': '', 'CurrentChannel': '', 'Login': '', 'Online': '', 'Idle': '', 'IP': '', 'Port': '', 'Status': ''}]

    else:
        res = [{'Type': '', 'Name': '', 'Desc': '', 'Protocol': '', 'Protocolext': '', 'AU': '', 'CaID': '', 'SrvID': '', 'ECMTime': '', 'ECMHistory': '', 'Answered': '', 'CurrentChannel': '', 'Login': '', 'Online': '', 'Idle': '', 'IP': '', 'Port': '', 'Status': ''}]
    if len(res) == 0:
        res = [{'Type': '', 'Name': '', 'Desc': '', 'Protocol': '', 'Protocolext': '', 'AU': '', 'CaID': '', 'SrvID': '', 'ECMTime': '', 'ECMHistory': '', 'Answered': '', 'CurrentChannel': '', 'Login': '', 'Online': '', 'Idle': '', 'IP': '', 'Port': '', 'Status': ''}]
    return res


def oscamAllClients(ret, userstatus):
    res = []
    users = []
    if ret == 1:
        try:
            oscam, users, totals = _parse_xml_userstatus(1, userstatus)
            users.sort(_caseIndependentSort)
            for x in users:
                if 'disabled' in x['Status']:
                    x.update({'Protocol': 'User is disabled'})
                res.append(x)

        except:
            res = [{'Name': '', 'Status': '', 'IP': '', 'Protocol': '', 'CWOK': '', 'CWNOK': '', 'CWIgnore': '', 'CWTtimeout': '', 'CWCache': '', 'CWTun': '', 'CWLlastresptime': '', 'EMMOK': '', 'EMMNOK': '', 'CWRate': ''}]

    else:
        res = [{'Name': '', 'Status': '', 'IP': '', 'Protocol': '', 'CWOK': '', 'CWNOK': '', 'CWIgnore': '', 'CWTtimeout': '', 'CWCache': '', 'CWTun': '', 'CWLlastresptime': '', 'EMMOK': '', 'EMMNOK': '', 'CWRate': ''}]
    if len(res) == 0:
        res = [{'Name': '', 'Status': '', 'IP': '', 'Protocol': '', 'CWOK': '', 'CWNOK': '', 'CWIgnore': '', 'CWTtimeout': '', 'CWCache': '', 'CWTun': '', 'CWLlastresptime': '', 'EMMOK': '', 'EMMNOK': '', 'CWRate': ''}]
    return res


return
