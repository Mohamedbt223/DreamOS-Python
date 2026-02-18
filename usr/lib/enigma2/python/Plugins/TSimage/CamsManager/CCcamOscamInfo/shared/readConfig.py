# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/CamsManager/CCcamOscamInfo/shared/readConfig.py
# Compiled at: 2014-05-25 10:33:38
import xml.dom.minidom as dom

def read_Config(dateiname):
    ret = 0
    tmpList = {'cam': 'CCcamLocal', 'default': '9', 'http': 'http', 'name': 'none', 'url': 'none', 'port': '16001', 'user': 'none', 'password': 'none', 'path': 'none', 'partnerbox': 'no', 'partnerboxpassword': 'no', 'changeconfig': 'no', 'partnerboxsshport': 22}
    res = []
    try:
        tree = dom.parse(dateiname)
        for x in tree.firstChild.childNodes:
            if x.nodeName == 'account':
                tmpList = {'cam': 'CCcamLocal', 'default': '9', 'http': 'http', 'name': 'none', 'url': 'none', 'port': '16001', 'user': 'none', 'password': 'none', 'path': 'none', 'partnerbox': 'no', 'partnerboxpassword': 'no', 'changeconfig': 'no', 'partnerboxsshport': 22}
                tmp = {}
                for y in x.childNodes:
                    if y.nodeName == 'cam':
                        tmp['cam'] = eval("('%s')" % y.firstChild.data.strip())
                    elif y.nodeName == 'name':
                        tmp['name'] = eval("('%s')" % y.firstChild.data.strip())
                    elif y.nodeName == 'url':
                        tmp['url'] = eval("('%s')" % y.firstChild.data.strip())
                    elif y.nodeName == 'port':
                        tmp['port'] = eval("('%s')" % y.firstChild.data.strip())
                    elif y.nodeName == 'user':
                        tmp['user'] = eval("('%s')" % y.firstChild.data.strip())
                    elif y.nodeName == 'password':
                        tmp['password'] = eval("('%s')" % y.firstChild.data.strip())
                    elif y.nodeName == 'http':
                        tmp['http'] = eval("('%s')" % y.firstChild.data.strip())
                    elif y.nodeName == 'path':
                        tmp['path'] = eval("('%s')" % y.firstChild.data.strip())
                    elif y.nodeName == 'default':
                        tmp['default'] = eval("('%s')" % y.firstChild.data.strip())
                    elif y.nodeName == 'changeconfig':
                        tmp['changeconfig'] = eval("('%s')" % y.firstChild.data.strip())
                    elif y.nodeName == 'partnerbox':
                        tmp['partnerbox'] = eval("('%s')" % y.firstChild.data.strip())
                    elif y.nodeName == 'partnerboxpassword':
                        tmp['partnerboxpassword'] = eval("('%s')" % y.firstChild.data.strip())
                    elif y.nodeName == 'partnerboxsshport':
                        tmp['partnerboxsshport'] = eval("('%s')" % y.firstChild.data.strip())

                xtmp = tmpList
                xtmp.update(tmp)
                res.append(xtmp)

        ret = 1
    except:
        res.append(tmpList)
        ret = 0

    return (
     ret, res)


return
