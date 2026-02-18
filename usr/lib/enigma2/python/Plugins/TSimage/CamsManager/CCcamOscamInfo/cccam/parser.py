# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/CamsManager/CCcamOscamInfo/cccam/parser.py
# Compiled at: 2014-05-25 10:33:38
import string, os

def _caseIndependentSort(something, other):
    something, other = string.lower(something), string.lower(other)
    return cmp(something, other)


def _caseIndependentSortServerGeneral(something, other):
    something, other = string.lower(something).replace('green,', '').replace('red,', '').replace('yellow,', ''), string.lower(other).replace('green,', '').replace('red,', '').replace('yellow,', '')
    return cmp(something, other)


def read_Home(ret, web):
    res = ''
    if ret == 1:
        try:
            name = web[0]
            web = web[1]
            idx1 = web.index('Welcome')
            idx2 = web.index('server')
            idx3 = web.index('Current')
            idx4 = web.index('</BODY></HTML>')
            res = web[idx1:idx2 + 6] + ' on %s' % name.replace('\n\n', '')
            res = '%s\n\n%s' % (res, web[idx3 - 8:idx4].replace('<BR>', '\n').replace('\n\n', '\n').replace('\nCu', 'Cu'))
        except:
            res = _('No Data')

    else:
        res = _('No Data')
    return res


def read_Start(ret, web):
    res = []
    version = 'NA'
    uptime = _('Uptime') + ': NA'
    connected = _('Connected clients') + ': NA'
    active = _('Active clients') + ': NA'
    if ret == 1:
        try:
            web = web[1]
            idx1 = web.index('to CCcam')
            idx2 = web.index('server')
            idx3 = web.index('Current')
            idx4 = web.index('</BODY></HTML>')
            version = web[idx1 + 3:idx2 - 1]
            web = web[idx3 - 8:idx4].replace('<BR>', '\n').replace('\n\n', '\n').replace('\nCu', 'Cu').split('\n')
            for x in web:
                if x.startswith('Uptime'):
                    uptime = x
                if x.startswith('Connected'):
                    connected = x
                if x.startswith('Active'):
                    active = x

        except:
            pass

    res = [
     _('Version') + ': %s' % version, '%s' % uptime, '%s' % connected, '%s' % active]
    return res


def read_Clients(ret, web_clients, web_active, config, idx):
    res = []
    userList = {}
    userActive = {}
    userOffline = {}
    tmp_shareinfo = []
    if ret == 1:
        try:
            web_clients = web_clients[1].split('\n')
            for i in web_clients:
                i = i.split('|')
                if len(i) > 8 and i[2].strip() != 'Host':
                    if i[8].strip() == '':
                        userList[i[1].strip()] = 'green,blue,%s,%s,%s,%s,%s,%s,%s' % (i[2].strip(), i[3].strip(), i[4].strip(), i[5].strip(), i[6].strip(), i[7].strip(), i[8].strip().replace('', ' '))
                    else:
                        userList[i[1].strip()] = 'green,blue,%s,%s,%s,%s,%s,%s,%s' % (i[2].strip(), i[3].strip(), i[4].strip(), i[5].strip(), i[6].strip(), i[7].strip(), i[8].strip())
                elif len(i) == 4:
                    tmp_shareinfo.append('%s,%s' % (i[1].strip(), i[2].strip()))

            res.append(_('Username') + ',green,blue,' + _('Host') + ',' + _('Connected') + ',' + _('Idle time') + ',' + _('ECM') + ',' + _('EMM') + ',' + _('Version') + ',' + _('Last used share'))
            web_active = web_active[1].split('\n')
            for i in web_active:
                i = i.split('|')
                if len(i) > 8 and i[2].strip() != 'Host':
                    userActive[i[1].strip()] = 'green,green,%s,%s,%s,%s,%s,%s,%s' % (i[2].strip(), i[3].strip(), i[4].strip(), i[5].strip(), i[6].strip(), i[7].strip(), i[8].strip())

            for x in userActive.keys():
                userList[x] = userActive[x]

            try:
                if config[idx]['url'] == '127.0.0.1':
                    f = open('%s/CCcam.cfg' % config[idx]['path'], 'r')
                    for i in f.read().split('\n'):
                        if i.startswith('F:'):
                            userOffline[i.split('F:')[1].strip().split(' ')[0]] = 'red,red, , , , , , , '

                    for i in userList.keys():
                        userOffline[i] = userList[i]

                    userList = userOffline
            except:
                pass

            tmp = []
            for i in userList.keys():
                tmp.append('%s,%s' % (i, userList[i]))

            tmp.sort(_caseIndependentSort)
            res.append(tmp)
            tmp = []
            del tmp_shareinfo[0]
            data = 'nop'
            for x in tmp_shareinfo:
                if x.split(',')[0] != '':
                    data = '%s:::%s,%s' % (data, x.split(',')[0], x.split(',')[1])
                else:
                    data = '%s,%s' % (data, x.split(',')[1])

            tmp = data.split(':::')
            del tmp[0]
            res.append(tmp)
        except:
            res = []
            tmp = []
            res.append(_('Error') + ', , , , , , , , , ')
            tmp.append(' , , , , , , , , , ')
            res.append(tmp)
            res.append(',')

    else:
        res = []
        tmp = []
        res.append(_('Error') + ', , , , , , , , , ')
        tmp.append(' , , , , , , , , , ')
        res.append(tmp)
        res.append(',')
    return res


def read_ServersGeneral(ret, web):
    res = []
    HostList = []
    tmp_CAID = []
    if ret == 1:
        try:
            web = web[1].split('\n')
            test = False
            tmp = []
            for i in web:
                i = i.split('|')
                if len(i) > 8:
                    tmp_CAID.append('%s,%s' % (i[1].strip(), i[7].strip()))
                    if i[1].strip() != '':
                        if test == True:
                            if i[2].strip() == '' and i[6].strip() != '':
                                color = 'red'
                            elif i[6].strip() == '0':
                                color = 'yellow'
                            elif i[6].strip() != '0' and i[2].strip() != '':
                                color = 'green'
                            tmp.append('%s,%s,%s,%s,%s,%s,%s' % (color, i[1].strip(), i[2].strip(), i[3].strip(), i[4].strip(), i[5].strip(), i[6].strip()))
                        elif test == False:
                            res.append('%s,%s,%s,%s,%s,%s' % (i[1].strip(), i[2].strip(), i[3].strip(), i[4].strip(), i[5].strip(), i[6].strip()))
                            test = True
                continue

            tmp.sort(_caseIndependentSortServerGeneral)
            res.append(tmp)
            del tmp_CAID[0]
            data = 'nop'
            for x in tmp_CAID:
                if x.split(',')[0] != '':
                    data = '%s:::%s,%s' % (data, x.split(',')[0], x.split(',')[1])
                else:
                    data = '%s,%s' % (data, x.split(',')[1])

            tmp = data.split(':::')
            del tmp[0]
            res.append(tmp)
        except:
            res = [
             ' , , , , , ', [' ,' + _("Couldn't read the webinterface") + ', , , , , ']]

    else:
        res = [
         ' , , , , , ', [' ,' + _("Couldn't read the webinterface") + ', , , , , ']]
    return res


def read_ServersDetail(ret, web_servers, web_shares):
    res = []
    HostList = []
    StatusList = []
    Hope1List = []
    Hope2List = []
    Hope3List = []
    HopeXList = []
    TotCardList = []
    Locals = []
    TotalCards = []
    if ret == 1:
        try:
            web = web_servers[1].split('\n')
            for i in web:
                i = i.split('|')
                if len(i) > 8:
                    if i[1].strip() != '':
                        HostList.append(i[1].strip())
                    if i[2].strip() == '' and i[6].strip() != '':
                        StatusList.append('red')
                    elif i[6].strip() == '0':
                        StatusList.append('yellow')
                    elif i[6].strip() != '0' and i[2].strip() != '':
                        StatusList.append('green')

            del HostList[0]
            del StatusList[0]
            for i in HostList:
                globals()['%s%s' % (i.replace('.', '_xx_x_').replace(':', '_xx_xx_'), '_Hop0')] = 0
                globals()['%s%s' % (i.replace('.', '_xx_x_').replace(':', '_xx_xx_'), '_Hop1')] = 0
                globals()['%s%s' % (i.replace('.', '_xx_x_').replace(':', '_xx_xx_'), '_Hop2')] = 0
                globals()['%s%s' % (i.replace('.', '_xx_x_').replace(':', '_xx_xx_'), '_Hop3')] = 0
                globals()['%s%s' % (i.replace('.', '_xx_x_').replace(':', '_xx_xx_'), '_HopX')] = 0
                globals()['%s%s' % (i.replace('.', '_xx_x_').replace(':', '_xx_xx_'), '_HopTot')] = 0

            web = web_shares[1].replace('.', '_xx_x_').replace(':', '_xx_xx_').split('\n')
            LocalCards = 0
            for i in web:
                i = i.split('|')
                if len(i) > 7 and i[6].split(' ')[0] != 'Uphops' and i[6].split(' ')[0] != 'Maxdown':
                    if int(i[6].split(' ')[0].strip()) == 0:
                        LocalCards = LocalCards + 1
                    if int(i[6].split(' ')[0]) == 1:
                        globals()['%s%s' % (i[1].strip(), '_Hop1')] = globals()['%s%s' % (i[1].strip(), '_Hop1')] + 1
                        globals()['%s%s' % (i[1].strip(), '_HopTot')] = globals()['%s%s' % (i[1].strip(), '_HopTot')] + 1
                    if int(i[6].split(' ')[0]) == 2:
                        globals()['%s%s' % (i[1].strip(), '_Hop2')] = globals()['%s%s' % (i[1].strip(), '_Hop2')] + 1
                        globals()['%s%s' % (i[1].strip(), '_HopTot')] = globals()['%s%s' % (i[1].strip(), '_HopTot')] + 1
                    if int(i[6].split(' ')[0]) == 3:
                        globals()['%s%s' % (i[1].strip(), '_Hop3')] = globals()['%s%s' % (i[1].strip(), '_Hop3')] + 1
                        globals()['%s%s' % (i[1].strip(), '_HopTot')] = globals()['%s%s' % (i[1].strip(), '_HopTot')] + 1
                    if int(i[6].split(' ')[0]) > 3:
                        globals()['%s%s' % (i[1].strip(), '_HopX')] = globals()['%s%s' % (i[1].strip(), '_HopX')] + 1
                        globals()['%s%s' % (i[1].strip(), '_HopTot')] = globals()['%s%s' % (i[1].strip(), '_HopTot')] + 1

            for i in HostList:
                Hope1List.append(globals()['%s%s' % (i.replace('.', '_xx_x_').replace(':', '_xx_xx_'), '_Hop1')])
                if globals()['%s%s' % (i.replace('.', '_xx_x_').replace(':', '_xx_xx_'), '_Hop1')] != 0 and globals()['%s%s' % (i.replace('.', '_xx_x_').replace(':', '_xx_xx_'), '_HopTot')] != 0:
                    Locals.append('green')
                elif globals()['%s%s' % (i.replace('.', '_xx_x_').replace(':', '_xx_xx_'), '_Hop1')] == 0 and globals()['%s%s' % (i.replace('.', '_xx_x_').replace(':', '_xx_xx_'), '_HopTot')] == 0:
                    Locals.append('red')
                elif globals()['%s%s' % (i.replace('.', '_xx_x_').replace(':', '_xx_xx_'), '_Hop1')] == 0 and globals()['%s%s' % (i.replace('.', '_xx_x_').replace(':', '_xx_xx_'), '_HopTot')] != 0:
                    Locals.append('yellow')
                Hope2List.append(globals()['%s%s' % (i.replace('.', '_xx_x_').replace(':', '_xx_xx_'), '_Hop2')])
                Hope3List.append(globals()['%s%s' % (i.replace('.', '_xx_x_').replace(':', '_xx_xx_'), '_Hop3')])
                HopeXList.append(globals()['%s%s' % (i.replace('.', '_xx_x_').replace(':', '_xx_xx_'), '_HopX')])
                TotCardList.append(globals()['%s%s' % (i.replace('.', '_xx_x_').replace(':', '_xx_xx_'), '_HopTot')])

            Hope1Tot = 0
            Hope2Tot = 0
            Hope3Tot = 0
            HopexTot = 0
            TotalCards = 0
            for i in Hope1List:
                Hope1Tot = Hope1Tot + i

            for i in Hope2List:
                Hope2Tot = Hope2Tot + i

            for i in Hope3List:
                Hope3Tot = Hope3Tot + i

            for i in HopeXList:
                HopexTot = HopexTot + i

            for i in TotCardList:
                TotalCards = TotalCards + i

            res.append(LocalCards)
            res.append([_('Server'), _('Hop1'), _('Hop2'), _('Hop3'), _('HopX'), _('Total')])
            tmp = []
            tmp.append(_('Total') + ':')
            tmp.append('%s' % Hope1Tot)
            tmp.append('%s' % Hope2Tot)
            tmp.append('%s' % Hope3Tot)
            tmp.append('%s' % HopexTot)
            tmp.append('%s' % TotalCards)
            res.append(tmp)
            tmp = []
            i = 0
            while i < len(HostList):
                tmp.append('%s,%s,%s,%s,%s,%s,%s,%s' % (HostList[i], StatusList[i], Locals[i], Hope1List[i], Hope2List[i], Hope3List[i], HopeXList[i], TotCardList[i]))
                i = i + 1

            tmp.sort(_caseIndependentSort)
            res.append(tmp)
        except:
            res = []
            res.append(' ')
            tmp = [_('Error'), ' ', ' ', ' ', ' ', ' ']
            res.append(tmp)
            tmp = [25, 25, 25, 25, 25, 25]
            res.append(tmp)
            tmp = [' , , , , , , , ']
            res.append(tmp)

    else:
        res = []
        res.append(' ')
        tmp = [_('Error'), ' ', ' ', ' ', ' ', ' ']
        res.append(tmp)
        tmp = [25, 25, 25, 25, 25, 25]
        res.append(tmp)
        tmp = [' , , , , , , , ']
        res.append(tmp)
    return res


def read_Locals(ret, res_servers, res_shares, res_providers, idx_server):
    res = []
    HostList = []
    LocalList = []
    print ret
    if ret == 1:
        try:
            web = res_servers
            web = web[1].split('\n')
            for i in web:
                i = i.split('|')
                if len(i) > 8:
                    if i[1].strip() != '':
                        HostList.append(i[1].strip())

            del HostList[0]
            HostList.sort(_caseIndependentSort)
            web = res_shares
            web = web[1].split('\n')
            for i in web:
                tmp = []
                i = i.split('|')
                if len(i) > 7 and i[1].strip() == HostList[idx_server] and i[6].split(' ')[0] == '1':
                    tmp.append(i[3].strip())
                    tmp.append(i[4].strip())
                    tmp.append(i[5].strip())
                    LocalList.append(tmp)

            if len(LocalList) == 0:
                res = _('Server') + ' %s ' % HostList[idx_server] + _('has no local card') + '.\n'
            elif len(LocalList) != 0:
                if len(LocalList) == 1:
                    res = _('Server') + ' %s ' % HostList[idx_server] + _('has') + ' %s ' % len(LocalList) + _('local card') + '.\n\n'
                else:
                    res = _('Server') + ' %s ' % HostList[idx_server] + _('has') + ' %s ' % len(LocalList) + _('local cards') + '.\n\n'
                web = res_providers
                web = web[1].split('\n')
                count = 1
                for i in LocalList:
                    res = '%s\n' % res + _('Karte') + ' %s:\n' % count
                    count = count + 1
                    caid = i[0]
                    provider = i[2].split(',')
                    for j in web:
                        tmp = j.split('|')
                        if len(tmp) > 5 and caid == tmp[1].strip():
                            for k in provider:
                                if k == '0':
                                    k = ''
                                if k == tmp[2].strip():
                                    res = '%s' % res + _('Provider name') + ': %s\n' % tmp[3].strip() + _('System') + ': %s\n' % tmp[4].strip() + _('Caid') + ': %s  ' % tmp[1].strip() + _('Provider') + ': %s\n\n' % tmp[2].strip()

            else:
                res = _('Error')
        except:
            res = _('Error')

    else:
        res = _('Error')
    return res


def read_myLocals(ret, res_shares, res_providers):
    res = []
    LocalList = []
    if ret == 1:
        try:
            web = res_shares
            web = web[1].split('\n')
            for i in web:
                tmp = []
                i = i.split('|')
                if len(i) > 7 and i[6].split(' ')[0] == '0':
                    tmp.append(i[3].strip())
                    tmp.append(i[4].strip())
                    tmp.append(i[5].strip())
                    LocalList.append(tmp)

            if len(LocalList) == 0:
                res = _('Found no local card') + '.\n'
            elif len(LocalList) != 0:
                if len(LocalList) == 1:
                    res = '%s ' % len(LocalList) + _('lokal card') + '.\n\n'
                else:
                    res = '%s ' % len(LocalList) + _('lokal cards') + '.\n\n'
                web = res_providers
                web = web[1].split('\n')
                count = 1
                for i in LocalList:
                    res = '%s\n' % res + _('Ccard') + ' %s:\n' % count
                    count = count + 1
                    caid = i[0]
                    provider = i[2].split(',')
                    for j in web:
                        tmp = j.split('|')
                        if len(tmp) > 5 and caid == tmp[1].strip():
                            for k in provider:
                                if k == '0':
                                    k = ''
                                if k == tmp[2].strip():
                                    res = '%s' % res + _('Provider name') + ': %s\n' % tmp[3].strip() + _('System') + ': %s\n' % tmp[4].strip() + _('Caid') + ': %s  ' % tmp[1].strip() + _('Provider') + ': %s\n\n' % tmp[2].strip()

        except:
            res = _('Error')

    else:
        res = _('Error')
    return res


def read_Providers(ret, web):
    res = []
    if ret == 1:
        try:
            res = []
            web = web[1].split('\n')
            test = False
            tmp = []
            caid = []
            for i in web:
                i = i.split('|')
                if len(i) == 6:
                    if test == True:
                        caid.append(i[1].strip())
                        tmp.append('%s,%s,%s,%s' % (i[1].strip(), i[2].strip(), i[3].strip(), i[4].strip()))
                    elif test == False:
                        res.append('%s,%s,%s,%s' % (i[1].strip(), i[2].strip(), i[3].strip(), i[4].strip()))
                        test = True

            caid = list(set(caid))
            caid.sort()
            res.append(caid)
            res.append(tmp)
        except:
            res = [
             _('Caid') + ',' + _('Provider') + ',' + _('Provider name') + ',' + _('System'), [' '], [' , ,' + _("Couldn't read the webinterface") + '., ']]

    else:
        res = [
         _('Caid') + ',' + _('Provider') + ',' + _('Provider name') + ',' + _('System'), [' '], [' , ,' + _("Couldn't read the webinterface") + '., ']]
    return res


def read_Shares(ret, web):
    res = []
    if ret == 1:
        try:
            up0 = []
            up1 = []
            up2 = []
            up3 = []
            up4 = []
            upx = []
            web = web[1].split('\n')
            test = False
            tmp = []
            for i in web:
                i = i.split('|')
                if len(i) == 9:
                    if i[1].strip() != '':
                        if test == True:
                            if int(i[6].split('   ')[0].strip()) == 0:
                                up0.append('%s;;%s;;%s;;%s;;%s;;%s;;%s;;%s' % (i[1].strip(), i[2].strip(), i[3].strip(), i[4].strip(), i[5].strip(), i[6].split('   ')[0].strip(), i[6].split('   ')[1].strip(), i[7].strip()))
                            elif int(i[6].split('   ')[0].strip()) == 1:
                                up1.append('%s;;%s;;%s;;%s;;%s;;%s;;,%s;;%s' % (i[1].strip(), i[2].strip(), i[3].strip(), i[4].strip(), i[5].strip(), i[6].split('   ')[0].strip(), i[6].split('   ')[1].strip(), i[7].strip()))
                            elif int(i[6].split('   ')[0].strip()) == 2:
                                up2.append('%s;;%s;;%s;;%s;;%s;;%s;;,%s;;%s' % (i[1].strip(), i[2].strip(), i[3].strip(), i[4].strip(), i[5].strip(), i[6].split('   ')[0].strip(), i[6].split('   ')[1].strip(), i[7].strip()))
                            elif int(i[6].split('   ')[0].strip()) == 3:
                                up3.append('%s;;%s;;%s;;%s;;%s;;%s;;,%s;;%s' % (i[1].strip(), i[2].strip(), i[3].strip(), i[4].strip(), i[5].strip(), i[6].split('   ')[0].strip(), i[6].split('   ')[1].strip(), i[7].strip()))
                            elif int(i[6].split('   ')[0].strip()) == 4:
                                up4.append('%s;;%s;;%s;;%s;;%s;;%s;;,%s;;%s' % (i[1].strip(), i[2].strip(), i[3].strip(), i[4].strip(), i[5].strip(), i[6].split('   ')[0].strip(), i[6].split('   ')[1].strip(), i[7].strip()))
                            else:
                                upx.append('%s;;%s;;%s;;%s;;%s;;%s;;,%s;;%s' % (i[1].strip(), i[2].strip(), i[3].strip(), i[4].strip(), i[5].strip(), i[6].split('   ')[0].strip(), i[6].split('   ')[1].strip(), i[7].strip()))
                        elif test == False:
                            res.append('%s;;%s;;%s;;%s;;%s;;U;;D;;%s' % (i[1].strip(), i[2].strip(), i[3].strip(), i[4].strip(), i[5].strip(), i[7].strip()))
                            test = True

            tmp.append(up0)
            tmp.append(up1)
            tmp.append(up2)
            tmp.append(up3)
            tmp.append(up4)
            tmp.append(upx)
            tmp.append(up0 + up1 + up2 + up3 + up4 + upx)
            res.append(tmp)
        except:
            res = [
             _('Host') + ';;' + _('Type') + ';;' + _('Caid') + ';;' + _('System') + ';;' + _('Providers') + ';;U;;D;;' + _('Nodes'), [_("Couldn't read the webinterface") + '.;; ;; ;; ;; ;; ;; ;; ']]

    else:
        res = [
         _('Host') + ';;' + _('Type') + ';;' + _('Caid') + ';;' + _('System') + ';;' + _('Providers') + ';;U;;D;;' + _('Nodes'), [_("Couldn't read the webinterface") + '.;; ;; ;; ;; ;; ;; ;; ']]
    return res


def read_Entitlements(ret, web):
    if ret == 1:
        try:
            res = []
            tmp = []
            tmp1 = []
            name = web[0]
            web = web[1]
            idx1 = web.index('Welcome')
            idx2 = web.index('server')
            idx3 = web.index('card')
            idx4 = web.index('</PRE>')
            res.append(web[idx1:idx2 + 6] + ' on %s' % name)
            tmp = web[idx3:idx4].split('card reader ')
            del tmp[0]
            for x in tmp:
                tmp2 = []
                tmp2.append(x.split('\n')[0])
                tmp2.append(x)
                tmp1.append(tmp2)

            res.append(tmp1)
        except:
            res = [
             ' ', [[' ', _('no or unknown card inserted') + '\n']]]

    else:
        res = [
         ' ', [[' ', _('no or unknown card inserted') + '\n']]]
    return res


return
