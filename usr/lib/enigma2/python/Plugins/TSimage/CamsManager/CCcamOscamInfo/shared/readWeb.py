# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/CamsManager/CCcamOscamInfo/shared/readWeb.py
# Compiled at: 2014-05-25 10:33:38
import urllib2

def read_Web(config, idx, address):
    ret = 0
    res = []
    http = cam = name = url = port = user = password = None
    try:
        try:
            user = config[idx]['user']
            password = config[idx]['password']
        except:
            pass

        cam = config[idx]['cam']
        http = config[idx]['http']
        name = config[idx]['name']
        url = config[idx]['url']
        port = config[idx]['port']
        res.append(name)
        if user == None:
            url = '%s://%s:%s/%s' % (http, url, port, address)
            res.append(urllib2.urlopen(url).read())
        else:
            url = '%s://%s:%s/%s' % (http, url, port, address)
            passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
            passman.add_password(None, url, user, password)
            if cam == 'Oscam':
                authhandler = urllib2.HTTPDigestAuthHandler(passman)
            if cam == 'CCcamLocal' or cam == 'CCcamRemote':
                authhandler = urllib2.HTTPBasicAuthHandler(passman)
            opener = urllib2.build_opener(authhandler)
            urllib2.install_opener(opener)
            request = urllib2.Request(url)
            res.append(urllib2.urlopen(request).read())
        ret = 1
    except:
        ret = 0
        res = []

    return (
     ret, res)


return
