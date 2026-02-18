# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebChilds/ServiceListSave.py
# Compiled at: 2025-09-18 23:33:39
from glob import glob
from os import unlink
from os.path import isfile, join
from twisted.web import resource, http, server
from enigma import eDVBDB
from Tools.Directories import resolveFilename, SCOPE_CONFIG
from xml.dom.minidom import parseString as xml_dom_minidom_parseString
from urllib import unquote as urllib_unquote
import Components.ParentalControl

class ServiceList(resource.Resource):

    def __init__(self, session):
        self.session = session
        resource.Resource.__init__(self)
        self.putChild('reload', ServiceListReload())
        self.putChild('save', ServiceListSave())
        return


class ServiceListReload(resource.Resource):

    def render(self, request):
        request.setHeader('Content-type', 'application/xhtml+xml;')
        request.setHeader('charset', 'UTF-8')
        try:
            db = eDVBDB.getInstance()
            db.reloadBouquets()
            Components.ParentalControl.parentalControl.open()
            request.setResponseCode(http.OK)
            return '<?xml version="1.0" encoding="UTF-8"?>\n\t\t\t\t\t\t<e2simplexmlresult>\n\t\t\t\t\t\t\t<e2state>True</e2state>\n\t\t\t\t\t\t\t<e2statetext>Servicelist reloaded</e2statetext>\n\t\t\t\t\t\t</e2simplexmlresult>'
        except Exception:
            request.setResponseCode(http.OK)
            return '<?xml version="1.0" encoding="UTF-8"?>\n\t\t\t\t\t\t<e2simplexmlresult>\n\t\t\t\t\t\t\t<e2state>False</e2state>\n\t\t\t\t\t\t\t<e2statetext>Error while loading Servicelist!</e2statetext>\n\t\t\t\t\t\t</e2simplexmlresult>'

        return


class ServiceListSave(resource.Resource):
    TYPE_TV = 0
    TYPE_RADIO = 1
    EXTENSIONS = ['.tv', '.radio']
    DIR = resolveFilename(SCOPE_CONFIG)
    undefinded_tag = '%n/a%'
    undefinded_and = '%und%'

    def render(self, request):
        request.setHeader('Content-type', 'application/xhtml+xml;')
        request.setHeader('charset', 'UTF-8')
        try:
            content = request.args['content'][0].replace('<n/a>', self.undefinded_tag).replace('&', self.undefinded_and)
            if content.find('undefined') != -1:
                fp = open('/tmp/savedlist', 'w')
                fp.write(content)
                fp.close()
                result = '<?xml version="1.0" encoding="UTF-8" ?>\n\n\t\t\t\t\t\t<e2simplexmlresult>\n\n\t\t\t\t\t\t\t<e2state>False</e2state>\n\t\t\t\t\t\t\t<e2statetext>found string \'undefined\' in XML DATA... a copy was saved to \'/tmp/savedlist\'.</e2statetext>\n\t\t\t\t\t\t</e2simplexmlresult>\n\n\t\t\t\t\t '
                request.setResponseCode(http.OK)
                request.write(result)
            bouquets_tv, bouquets_radio = self.parseXML(content)
            for filename in glob(self.DIR + 'userbouquet*.tv'):
                unlink(filename)

            for filename in glob(self.DIR + 'userbouquet*.radio'):
                unlink(filename)

            for filename in ('bouquets.radio', 'bouquets.tv'):
                path = join(self.DIR, filename)
                if isfile(path):
                    unlink(path)

            self.createIndexFile(self.TYPE_TV, bouquets_tv)
            counter = 0
            for bouquet in bouquets_tv:
                self.createBouquetFile(self.TYPE_TV, bouquet['bname'], bouquet['services'], counter)
                counter = counter + 1

            self.createIndexFile(self.TYPE_RADIO, bouquets_radio)
            counter = 0
            for bouquet in bouquets_radio:
                self.createBouquetFile(self.TYPE_RADIO, bouquet['bname'], bouquet['services'], counter)
                counter = counter + 1

            db = eDVBDB.getInstance()
            db.reloadBouquets()
            print 'servicelists reloaded'
            result = '<?xml version="1.0" encoding="UTF-8" ?>\n\n\t\t\t\t\t\t<e2simplexmlresult>\n\n\t\t\t\t\t\t\t<e2state>True</e2state>\n\t\t\t\t\t\t\t<e2statetext>servicelist saved with %i TV und %i Radio Bouquets and was reloaded</e2statetext>\n\t\t\t\t\t\t</e2simplexmlresult>\n\n\t\t\t\t\t ' % (len(bouquets_tv), len(bouquets_radio))
            request.setResponseCode(http.OK)
            request.write(result)
        except Exception as e:
            print e
            result = '<?xml version="1.0" encoding="UTF-8" ?>\n\n\t\t\t\t\t\t<e2simplexmlresult>\n\n\t\t\t\t\t\t\t<e2state>False</e2state>\n\t\t\t\t\t\t\t<e2statetext>%s</e2statetext>\n\t\t\t\t\t\t</e2simplexmlresult>\n\n\t\t\t\t\t ' % e
            request.setResponseCode(http.OK)
            request.write(result)

        request.finish()
        return server.NOT_DONE_YET

    def parseXML(self, xmldata):
        print 'parsing xmldata with length', len(xmldata)
        xmldoc = xml_dom_minidom_parseString(xmldata)
        blist = xmldoc.getElementsByTagName('e2bouquetlist')[0]
        print 'Num TV Bouquets', len(blist.getElementsByTagName('e2tvbouquetlist')[0].getElementsByTagName('e2bouquet'))
        print 'Num RADIO Bouquets', len(blist.getElementsByTagName('e2radiobouquetlist')[0].getElementsByTagName('e2bouquet'))
        bouquets_tv = self.parseBouquets(blist.getElementsByTagName('e2tvbouquetlist')[0])
        bouquets_radio = self.parseBouquets(blist.getElementsByTagName('e2radiobouquetlist')[0])
        return (bouquets_tv, bouquets_radio)

    def parseBouquets(self, xmlnode):
        list = []
        for bouquet in xmlnode.getElementsByTagName('e2bouquet'):
            bref = urllib_unquote(bouquet.getElementsByTagName('e2bouquetreference')[0].childNodes[0].data)
            bname = urllib_unquote(bouquet.getElementsByTagName('e2bouquetname')[0].childNodes[0].data)
            list.append({'bname': bname, 'bref': bref, 'services': (self.parseServices(bouquet))})

        return list

    def parseServices(self, xmlnode):
        list = []
        for service in xmlnode.getElementsByTagName('e2servicelist')[0].getElementsByTagName('e2service'):
            sref = urllib_unquote(service.getElementsByTagName('e2servicereference')[0].childNodes[0].data)
            sname = urllib_unquote(service.getElementsByTagName('e2servicename')[0].childNodes[0].data)
            sname = sname.replace(self.undefinded_tag, '<n/a>').replace(self.undefinded_and, '&')
            list.append({'sref': sref, 'sname': sname})

        return list

    def createBouquetFile(self, type, bname, list_services, counter):
        print 'creating file for bouquet', bname, 'with', len(list_services), 'services for type', type
        filename = self.getFilenameForBouquet(type, bname, counter)
        fcontent = '#NAME %s\n' % bname
        for service in list_services:
            fcontent += '#SERVICE %s\n' % service['sref']
            fcontent += '#DESCRIPTION %s\n' % service['sname']

        fcontent = fcontent.encode('utf-8')
        fp = open(self.DIR + filename, 'w')
        fp.write(fcontent)
        fp.close()
        return

    def createIndexFile(self, type, bouquets):
        print 'creating Indexfile with', len(bouquets), 'num bouquets for type', type
        filename = self.getFilenameForIndex(type)
        if type == self.TYPE_TV:
            fcontent = '#NAME User - bouquets (TV)\n'
        else:
            fcontent = '#NAME User - bouquets (Radio)\n'
        counter = 0
        for bouquet in bouquets:
            fcontent += '#SERVICE: 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "%s" ORDER BY bouquet\n' % self.getFilenameForBouquet(type, bouquet['bname'], counter)
            counter = counter + 1

        fp = open(self.DIR + filename, 'w')
        fp.write(fcontent)
        fp.close()
        return

    def getFilenameForBouquet(self, type, bouquetname, counter):
        if bouquetname == 'Favourites (TV)' and type == self.TYPE_TV:
            s = 'userbouquet.favourites%s' % self.EXTENSIONS[type]
        elif bouquetname == 'Favourites (Radio)' and type == self.TYPE_RADIO:
            s = 'userbouquet.favourites%s' % self.EXTENSIONS[type]
        else:
            s = 'userbouquet.%i%s' % (counter, self.EXTENSIONS[type])
        return s

    def getFilenameForIndex(self, type):
        return 'bouquets' + self.EXTENSIONS[type]


return
