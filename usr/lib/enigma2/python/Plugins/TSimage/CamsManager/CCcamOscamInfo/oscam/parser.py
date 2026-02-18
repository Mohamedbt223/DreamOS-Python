# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/CamsManager/CCcamOscamInfo/oscam/parser.py
# Compiled at: 2014-05-25 10:33:38
import os, xml.dom.minidom

def _read_node(knoten):
    return eval("%s('%s')" % (knoten.getAttribute('typ'), knoten.firstChild.data.strip()))


def _parse_time(secs):
    res = []
    days, secs = divmod(int(secs), 86400)
    hours, secs = divmod(int(secs), 3600)
    mins, secs = divmod(int(secs), 60)
    res = '%dd:%02dh:%02dm:%02ds' % (days, hours, mins, secs)
    return res


def _parse_xml_info(data):
    ret = 0
    res = {}
    try:
        dom = xml.dom.minidom.parseString(data)
        for oscam in dom.getElementsByTagName('oscam'):
            res = {}
            res.update({'Version': ('%s' % str(oscam.getAttribute('version')))})
            res.update({'Revision': ('%s' % str(oscam.getAttribute('revision')))})
            res.update({'Starttime': ('%s' % str(oscam.getAttribute('starttime')))})
            res.update({'Uptime': ('%s' % _parse_time(str(oscam.getAttribute('uptime'))))})
            res.update({'Readonly': ('%s' % str(oscam.getAttribute('readonly')))})

        ret = 1
    except:
        ret = 0
        dom = ''
        res = {'Version': '', 'Revision': '0', 'Starttime': '', 'Uptime': '', 'Readonly': ''}

    return (
     ret, res, dom)


def _parse_xml_userstatus(ret, data):
    oscam = {}
    users = []
    total = {}
    oscam_version = 0
    if ret == 1:
        try:
            ret, oscam, dom = _parse_xml_info(data[1])
            for user in dom.getElementsByTagName('user'):
                tmp = {}
                tmp.update({'Name': ('%s' % str(user.getAttribute('name')))})
                tmp.update({'Status': ('%s' % str(user.getAttribute('status')))})
                tmp.update({'IP': ('%s' % str(user.getAttribute('ip')))})
                tmp.update({'Protocol': ('%s' % str(user.getAttribute('protocol')))})
                for stats in user.getElementsByTagName('stats'):
                    if stats.nodeName == 'stats':
                        for node in stats.childNodes:
                            if node.nodeName == 'cwok':
                                tmp.update({'CWOK': ('%s' % _read_node(node))})
                            elif node.nodeName == 'cwnok':
                                tmp.update({'CWNOK': ('%s' % _read_node(node))})
                            elif node.nodeName == 'cwignore':
                                tmp.update({'CWIgnore': ('%s' % _read_node(node))})
                            elif node.nodeName == 'cwtimeout':
                                tmp.update({'CWTtimeout': ('%s' % _read_node(node))})
                            elif node.nodeName == 'cwcache':
                                tmp.update({'CWCache': ('%s' % _read_node(node))})
                            elif node.nodeName == 'cwtun':
                                tmp.update({'CWTun': ('%s' % _read_node(node))})
                            elif node.nodeName == 'cwlastresptime':
                                tmp.update({'CWLlastresptime': ('%s' % _read_node(node))})
                            elif node.nodeName == 'emmok':
                                tmp.update({'EMMOK': ('%s' % _read_node(node))})
                            elif node.nodeName == 'emmnok':
                                tmp.update({'EMMNOK': ('%s' % _read_node(node))})
                            elif node.nodeName == 'cwrate':
                                tmp.update({'CWRate': ('%s' % _read_node(node))})

                users.append(tmp)

            for totals in dom.getElementsByTagName('totals'):
                tmp = {}
                if totals.nodeName == 'totals':
                    for node in totals.childNodes:
                        check = 0
                        if node.nodeName == 'cwok':
                            total.update({'CWOK': ('%s' % _read_node(node))})
                        elif node.nodeName == 'cwnok':
                            total.update({'CWNOK': ('%s' % _read_node(node))})
                        elif node.nodeName == 'cwignore':
                            total.update({'CWIgnore': ('%s' % _read_node(node))})
                        elif node.nodeName == 'cwtimeout':
                            total.update({'CWTtimeout': ('%s' % _read_node(node))})
                        elif node.nodeName == 'cwcache':
                            total.update({'CWCache': ('%s' % _read_node(node))})
                        elif node.nodeName == 'cwtun':
                            total.update({'CWTun': ('%s' % _read_node(node))})
                        if int(oscam['Revision']) >= 6214:
                            if node.nodeName == 'usertotal':
                                total.update({'UserTotal': ('%s' % _read_node(node))})
                            if node.nodeName == 'userdisabled':
                                total.update({'UserDisabled': ('%s' % _read_node(node))})
                            if node.nodeName == 'userexpired':
                                total.update({'UserExpired': ('%s' % _read_node(node))})
                            if node.nodeName == 'useractive':
                                total.update({'UserActive': ('%s' % _read_node(node))})
                            if node.nodeName == 'userconnected':
                                total.update({'UserConnected': ('%s' % _read_node(node))})
                            if node.nodeName == 'useronline':
                                total.update({'UserOnline': ('%s' % _read_node(node))})
                        else:
                            total.update({'UserTotal': ''})
                            total.update({'UserDisabled': ''})
                            total.update({'UserExpired': ''})
                            total.update({'UserActive': ''})
                            total.update({'UserConnected': ''})
                            total.update({'UserOnline': ''})

        except:
            users = [{'Name': 'Error', 'Status': '', 'IP': '', 'Protocol': '', 'CWOK': '', 'CWNOK': '', 'CWIgnore': '', 'CWTtimeout': '', 'CWCache': '', 'CWTun': '', 'CWLlastresptime': '', 'EMMOK': '', 'EMMNOK': '', 'CWRate': ''}]
            oscam = {'Version': '', 'Revision': '0', 'Starttime': '', 'Uptime': '', 'Readonly': ''}
            total = {'CWOK': '', 'CWNOK': '', 'CWIgnore': '', 'CWTtimeout': '', 'CWCache': '', 'CWTun': '', 'UserTotal': '', 'UserDisabled': '', 'UserExpired': '', 'UserActive': '', 'UserConnected': '', 'UserOnline': ''}

    else:
        users = [{'Name': 'Error', 'Status': '', 'IP': '', 'Protocol': '', 'CWOK': '', 'CWNOK': '', 'CWIgnore': '', 'CWTtimeout': '', 'CWCache': '', 'CWTun': '', 'CWLlastresptime': '', 'EMMOK': '', 'EMMNOK': '', 'CWRate': ''}]
        oscam = {'Version': '', 'Revision': '0', 'Starttime': '', 'Uptime': '', 'Readonly': ''}
        total = {'CWOK': '', 'CWNOK': '', 'CWIgnore': '', 'CWTtimeout': '', 'CWCache': '', 'CWTun': '', 'UserTotal': '', 'UserDisabled': '', 'UserExpired': '', 'UserActive': '', 'UserConnected': '', 'UserOnline': ''}
    return (
     oscam, users, totals)


def _parse_xml_status(ret, data):
    oscam = {}
    clients = []
    if ret == 1:
        try:
            ret, oscam, dom = _parse_xml_info(data[1])
            for client in dom.getElementsByTagName('client'):
                tmp = {}
                tmp.update({'Type': ('%s' % str(client.getAttribute('type')))})
                tmp.update({'Name': ('%s' % str(client.getAttribute('name')))})
                tmp.update({'Desc': ('%s' % str(client.getAttribute('desc')))})
                tmp.update({'Protocol': ('%s' % str(client.getAttribute('protocol')))})
                tmp.update({'Protocolext': ('%s' % str(client.getAttribute('protocolext')))})
                tmp.update({'AU': ('%s' % str(client.getAttribute('au')))})
                for request in client.getElementsByTagName('request'):
                    tmp.update({'CaID': ('%s' % str(request.getAttribute('caid')))})
                    tmp.update({'SrvID': ('%s' % str(request.getAttribute('srvid')))})
                    tmp.update({'ECMTime': ('%s' % str(request.getAttribute('ecmtime')))})
                    tmp.update({'ECMHistory': ('%s' % str(request.getAttribute('ecmhistory')))})
                    tmp.update({'Answered': ('%s' % str(request.getAttribute('answered')))})
                    try:
                        tmp.update({'CurrentChannel': ('%s' % _read_node(request))})
                    except:
                        tmp.update({'CurrentChannel': ''})

                for times in client.getElementsByTagName('times'):
                    tmp.update({'Login': ('%s' % str(times.getAttribute('login')))})
                    tmp.update({'Online': ('%s' % _parse_time(str(times.getAttribute('online'))))})
                    tmp.update({'Idle': ('%s' % _parse_time(str(times.getAttribute('idle'))))})

                for connection in client.getElementsByTagName('connection'):
                    tmp.update({'IP': ('%s' % str(connection.getAttribute('ip')))})
                    tmp.update({'Port': ('%s' % str(connection.getAttribute('port')))})
                    tmp.update({'Status': ('%s' % _read_node(connection))})

                clients.append(tmp)

        except:
            oscam = {'Version': '', 'Revision': '0', 'Starttime': '', 'Uptime': '', 'Readonly': ''}
            clients = [{'Type': '', 'Name': '', 'Desc': '', 'Protocol': '', 'Protocolext': '', 'AU': '', 'CaID': '', 'SrvID': '', 'ECMTime': '', 'ECMHistory': '', 'Answered': '', 'CurrentChannel': '', 'Login': '', 'Online': '', 'Idle': '', 'IP': '', 'Port': '', 'Status': ''}]

    else:
        oscam = {'Version': '', 'Revision': '0', 'Starttime': '', 'Uptime': '', 'Readonly': ''}
        clients = [{'Type': '', 'Name': '', 'Desc': '', 'Protocol': '', 'Protocolext': '', 'AU': '', 'CaID': '', 'SrvID': '', 'ECMTime': '', 'ECMHistory': '', 'Answered': '', 'CurrentChannel': '', 'Login': '', 'Online': '', 'Idle': '', 'IP': '', 'Port': '', 'Status': ''}]
    return (
     oscam, clients)


def restart_shutdown_oscam(ret, data):
    res = {}
    if ret == 1:
        try:
            ret, oscam, dom = _parse_xml_info(data[1])
            res = oscam
        except:
            res = {'Version': 'NA', 'Revision': 'NA', 'Starttime': 'NA', 'Uptime': 'NA', 'Readonly': 'NA'}

    else:
        res = {'Version': 'NA', 'Revision': 'NA', 'Starttime': 'NA', 'Uptime': 'NA', 'Readonly': 'NA'}
    return res


def read_start_oscam(ret, data0, data1):
    res = {}
    if ret == 1:
        try:
            ret, oscam, dom = _parse_xml_info(data0[1])
            res.update({'Version': ('%s' % oscam['Version'])})
            res.update({'Uptime': ('%s' % oscam['Uptime'])})
            idx1 = data1[1].index('>Readers ')
            idx2 = data1[1].index('</TD></TR>')
            res.update({'Readers': ('%s' % data1[1][idx1 + 9:idx2])})
            idx1 = data1[1].index('>Clients ')
            idx2 = data1[1].index(')</TD></TR>')
            res.update({'Clients': ('%s' % data1[1][idx1 + 9:idx2 + 1])})
        except:
            res = {'Version': 'NA', 'Uptime': 'NA', 'Readers': 'NA', 'Clients': 'NA'}

    else:
        res = {'Version': 'NA', 'Uptime': 'NA', 'Readers': 'NA', 'Clients': 'NA'}
    return res


def _parse_xml_readerlist(ret, data):
    readerlist = []
    if ret == 1:
        try:
            ret, oscam, dom = _parse_xml_info(data[1])
            for reader in dom.getElementsByTagName('reader'):
                tmp = {}
                tmp.update({'Label': ('%s' % str(reader.getAttribute('label')))})
                tmp.update({'Protocol': ('%s' % str(reader.getAttribute('protocol')))})
                tmp.update({'Type': ('%s' % str(reader.getAttribute('type')))})
                tmp.update({'Enabled': ('%s' % str(reader.getAttribute('enabled')))})
                readerlist.append(tmp)

        except:
            readerlist = [{'Type': 'r', 'Protocol': '', 'Enabled': '', 'Label': 'Error'}]

    else:
        readerlist = [{'Type': 'r', 'Protocol': '', 'Enabled': '', 'Label': 'Error'}]
    return readerlist


def parse_xml_summary(ret, data):
    oscam = {}
    total = {}
    if ret == 1:
        try:
            ret, oscam, dom = _parse_xml_info(data[1])
            for totals in dom.getElementsByTagName('totals'):
                tmp = {}
                if totals.nodeName == 'totals':
                    for node in totals.childNodes:
                        check = 0
                        if node.nodeName == 'cwok':
                            total.update({'CWOK': ('%s' % _read_node(node))})
                        elif node.nodeName == 'cwnok':
                            total.update({'CWNOK': ('%s' % _read_node(node))})
                        elif node.nodeName == 'cwignore':
                            total.update({'CWIgnore': ('%s' % _read_node(node))})
                        elif node.nodeName == 'cwtimeout':
                            total.update({'CWTtimeout': ('%s' % _read_node(node))})
                        elif node.nodeName == 'cwcache':
                            total.update({'CWCache': ('%s' % _read_node(node))})
                        elif node.nodeName == 'cwtun':
                            total.update({'CWTun': ('%s' % _read_node(node))})
                        if int(oscam['Revision']) >= 6214:
                            if node.nodeName == 'usertotal':
                                total.update({'UserTotal': ('%s' % _read_node(node))})
                            if node.nodeName == 'userdisabled':
                                total.update({'UserDisabled': ('%s' % _read_node(node))})
                            if node.nodeName == 'userexpired':
                                total.update({'UserExpired': ('%s' % _read_node(node))})
                            if node.nodeName == 'useractive':
                                total.update({'UserActive': ('%s' % _read_node(node))})
                            if node.nodeName == 'userconnected':
                                total.update({'UserConnected': ('%s' % _read_node(node))})
                            if node.nodeName == 'useronline':
                                total.update({'UserOnline': ('%s' % _read_node(node))})
                        else:
                            total.update({'UserTotal': ''})
                            total.update({'UserDisabled': ''})
                            total.update({'UserExpired': ''})
                            total.update({'UserActive': ''})
                            total.update({'UserConnected': ''})
                            total.update({'UserOnline': ''})

        except:
            oscam = {'Version': '', 'Revision': '0', 'Starttime': '', 'Uptime': '', 'Readonly': ''}
            total = {'CWOK': '', 'CWNOK': '', 'CWIgnore': '', 'CWTtimeout': '', 'CWCache': '', 'CWTun': '', 'UserTotal': '', 'UserDisabled': '', 'UserExpired': '', 'UserActive': '', 'UserConnected': '', 'UserOnline': ''}

    else:
        oscam = {'Version': '', 'Revision': '0', 'Starttime': '', 'Uptime': '', 'Readonly': ''}
        total = {'CWOK': '', 'CWNOK': '', 'CWIgnore': '', 'CWTtimeout': '', 'CWCache': '', 'CWTun': '', 'UserTotal': '', 'UserDisabled': '', 'UserExpired': '', 'UserActive': '', 'UserConnected': '', 'UserOnline': ''}
    return (
     oscam, total)


return
