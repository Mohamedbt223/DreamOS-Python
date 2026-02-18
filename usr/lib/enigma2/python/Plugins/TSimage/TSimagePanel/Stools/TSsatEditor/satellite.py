# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/Stools/TSsatEditor/satellite.py
# Compiled at: 2025-09-17 10:29:58
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Components.ActionMap import HelpableActionMap, ActionMap
from Components.Sources.StaticText import StaticText
from Components.config import config, ConfigSubsection, ConfigSet, ConfigSelection, NoSave, ConfigYesNo
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.Sources.List import List
from enigma import eListbox
from os import path as os_path, remove
from Screens.HelpMenu import HelpableScreen
from Screens.MessageBox import MessageBox
from Tools.Directories import resolveFilename, SCOPE_CURRENT_SKIN, copyfile
from Tools.LoadPixmap import LoadPixmap
from Tools.Notifications import AddPopup
from twisted.web.client import getPage
import xml.etree.cElementTree as etree
from xml.parsers.expat import ParserCreate
from enigma import eTimer
from Components.ScrollLabel import ScrollLabel
FILEURL = 'http://dreambox4u.com/dreamarabia/xml/satellites.xml'
USERAGENT = 'Enima2 Satellite Editor Plugin'
SATFILE = '/etc/tuxbox/satellites.xml'
TMPFILE = '/tmp/satellites.xml'
config.plugins.sateditor = ConfigSubsection()
config.plugins.sateditor.satellites = ConfigSet(default=['192',
 '235',
 '282',
 '130'], choices=['192',
 '235',
 '282',
 '130'])
config.plugins.sateditor.sortby = ConfigSelection(default=1, choices=[(1, '1'), (2, '2'), (3, '3')])

class NewTSisatEditor(Screen, HelpableScreen):
    skin = '\n                \n                <screen name="NewTSisatEditor" position="center,center" size="920,600" title="Satellite.xml update"  >            \n\t        <widget source="satlist" render="Listbox"  position="20,30" size="880,400" scrollbarMode="showOnDemand" transparent="1" zPosition="2" >\n\t\t\t\t<convert type="TemplatedMultiContent">\n\t\t\t\t\t{"template": [\n\t\t\t\t\t\t\tMultiContentEntryText(pos = (50, 0), size = (460, 26), font=0, flags = RT_HALIGN_LEFT, text = 1),\n\t\t\t\t\t\t\tMultiContentEntryPixmapAlphaTest(pos = (5, 0), size = (25, 24), png = 2),\n\t\t\t\t\t\t],\n\t\t\t\t\t"fonts": [gFont("Regular", 22)],\n\t\t\t\t\t"itemHeight": 25\n\t\t\t\t\t}\n\t\t\t\t</convert>\n\t        </widget>\n\t        <eLabel position="20,470" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\n\t\t<widget name="info" position="20,460" zPosition="4" size="880,80" font="Regular;24" foregroundColor="yellow" transparent="1" halign="center" valign="center" />\n\t        <eLabel position="20,525" size="880,2" text="" font="Regular;24" zPosition="-1" backgroundColor="#ffffff"  />\n\t        <ePixmap name="red" position="70,545"   zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" transparent="1" alphatest="blend" />\n\t        <ePixmap name="green" position="280,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_green.png" transparent="1" alphatest="blend" />\n\t        <ePixmap name="yellow" position="490,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_yellow.png" transparent="1" alphatest="blend" /> \n        \t<ePixmap name="blue" position="700,545" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_blue.png" transparent="1" alphatest="blend" /> \n        \t<widget source="key_red" render="Label" position="70,550" size="140,40" valign="center" halign="center" zPosition="2"  font="Regular;21" transparent="1" /> \n        \t<widget source="key_green" render="Label" position="280,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;21" transparent="1" /> \n                <widget source="key_yellow" render="Label" position="490,550" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;20" transparent="1" />\n \t\t</screen>'

    def __init__(self, session):
        self.session = session
        Screen.__init__(self, session)
        self['info'] = Label()
        self['key_red'] = StaticText(_('Exit'))
        self['key_yellow'] = StaticText(_('Download'))
        self['key_green'] = StaticText('')
        self.satList = []
        self['satlist'] = List(self.satList)
        HelpableScreen.__init__(self)
        self['OkCancelActions'] = HelpableActionMap(self, 'OkCancelActions', {'cancel': (self.exit, _('Exit plugin')), 'ok': (
                self.changeSelection, _('Select/deselect satellite'))}, -1)
        self['ColorActions'] = HelpableActionMap(self, 'ColorActions', {'red': (self.exit, _('Exit plugin')), 'yellow': (
                    self.downloadSatellitesFile, _('Download satellites.xml file')), 
           'green': (
                   self.purgeSatellitesFile, _('Purge satellites.xml file'))}, -1)
        self['ChannelSelectBaseActions'] = HelpableActionMap(self, 'ChannelSelectBaseActions', {'nextBouquet': (self.changeSortingUp, _('Sorting up')), 'prevBouquet': (
                         self.changeSortingDown, _('Sorting down'))}, -1)
        self.showAccept = False
        self.useTmpFile = False
        self.purgePossible = False
        self.downloadPossible = True
        self.xmlVersion = ''
        self.xmlEncoding = ''
        self.xmlComment = ''
        self['info'].setText('Downloading satellite.xml file..please wait')
        self.onShown.append(self.loadCurrentSatellites)
        self.onShown.append(self.downloadSatellitesFile)
        return

    def exit(self):
        print '[TSsatEditor] closing'
        if os_path.exists(TMPFILE):
            try:
                remove(TMPFILE)
            except OSError as error:
                print '[TSsatEditor] unable to delete temp file', TMPFILE
                AddPopup(text=_('Unable to delete temp file.\n%s') % error, type=MessageBox.TYPE_ERROR, timeout=0, id='RemoveFileError')

        self.close()
        return

    def accept(self):
        print '[TSsatEditor] copying temp satellite file to target'
        if os_path.exists(TMPFILE):
            try:
                copyfile(TMPFILE, SATFILE)
            except OSError as error:
                print '[TSsatEditor] error during copying of', TMPFILE
                self.session.open(MessageBox, _('Unable to copy temp file.\n%s') % error, type=MessageBox.TYPE_ERROR)

        self.showAccept = False
        self['info'].setText('Satellite.xml saved')
        self.exit()
        return

    def changeSortingUp(self):
        if config.plugins.sateditor.sortby.value == 1:
            config.plugins.sateditor.sortby.value = 3
        else:
            config.plugins.sateditor.sortby.value -= 1
        self.setListSorted()
        return

    def changeSortingDown(self):
        if config.plugins.sateditor.sortby.value == 3:
            config.plugins.sateditor.sortby.value = 1
        else:
            config.plugins.sateditor.sortby.value += 1
        self.setListSorted()
        return

    def loadCurrentSatellites(self, fileName=SATFILE):
        print '[TSsatEditor] loading original satellite file', fileName
        self.mySat = []
        try:
            satFile = open(fileName, 'r')
        except IOError as error:
            print '[TSsatEditor] unable to open', fileName
            satFile = None
            AddPopup(text=_('Unable to open file.\n%s') % error, type=MessageBox.TYPE_ERROR, timeout=0, id='OpenFileError')
            self.exit()

        if not satFile:
            return
        else:
            curroot = etree.parse(satFile)
            for sat in curroot.findall('sat'):
                position = sat.attrib.get('position')
                self.mySat.append(position)

            satFile.close()
            return
            return

    def loadSatellitesFile(self, fileName=SATFILE):
        print '[TSsatEditor] loading satellite file', fileName
        self.satList = []
        try:
            satFile = open(fileName, 'r')
        except IOError as error:
            print '[TSsatEditor] unable to open', fileName
            satFile = None
            AddPopup(text=_('Unable to open file.\n%s') % error, type=MessageBox.TYPE_ERROR, timeout=0, id='OpenFileError')
            self.exit()

        if not satFile:
            return
        else:
            curroot = etree.parse(satFile)
            for sat in curroot.findall('sat'):
                position = sat.attrib.get('position')
                name = sat.attrib.get('name')
                if position in self.mySat:
                    print '[satPosition: yes]'
                    print position
                    png = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/images/lock_on.png'))
                    self.satList.append((position, name.encode('utf-8'), png))
                else:
                    print '[satPosition: no]'
                    print position
                    self.satList.append((position, name.encode('utf-8'), None))

            satFile.close()
            self['satlist'].setList(self.satList)
            self.setListSorted()
            return
            return

    def setListSorted(self):
        if config.plugins.sateditor.sortby.value == 1:
            s = sorted(self.satList, (lambda x, y: cmp(x[1], y[1])), reverse=False)
            self.satList = sorted(s, (lambda x, y: cmp(x[2], y[2])), reverse=True)
        elif config.plugins.sateditor.sortby.value == 2:
            s = sorted(self.satList, (lambda x, y: cmp(int(x[0]), int(y[0]))), reverse=False)
            self.satList = sorted(s, (lambda x, y: cmp(x[2], y[2])), reverse=True)
        else:
            s = sorted(self.satList, (lambda x, y: cmp(int(x[0]), int(y[0]))), reverse=True)
            self.satList = sorted(s, (lambda x, y: cmp(x[2], y[2])), reverse=True)
        self['satlist'].updateList(self.satList)
        if len(self.satList) > len(config.plugins.sateditor.satellites.value):
            self['key_green'].setText(_('Save'))
            self.purgePossible = True
        else:
            self['key_green'].setText('')
            self.purgePossible = False
        return

    def changeSelection(self):
        try:
            png = None
            idx = self['satlist'].getIndex()
            position = self.satList[idx][0]
            name = self.satList[idx][1]
            if position in config.plugins.sateditor.satellites.value:
                config.plugins.sateditor.satellites.value.remove(position)
            else:
                config.plugins.sateditor.satellites.value.append(position)
                png = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/images/lock_on.png'))
            config.plugins.sateditor.satellites.save()
            self.satList[idx] = (position, name, png)
            self.setListSorted()
        except:
            pass

        return

    def downloadSatellitesFile(self):
        if not self.downloadPossible:
            return
        print '[TSsatEditor] downloading satellite file'
        self['info'].setText('Downloading satellite.xml...please wait')
        self.timer = eTimer()
        self.timer_conn = self.timer.timeout.connect(self.startdownload)
        self.timer.start(100, 1)
        return

    def startdownload(self):
        getPage(FILEURL, agent=USERAGENT, timeout=20).addCallback(self.cbDownload).addErrback(self.cbDownloadError)
        return

    def commentHandler(self, data):
        self.xmlComment = data
        return

    def declarationHandler(self, version, encoding, standalone):
        self.xmlVersion = version
        self.xmlEncoding = encoding
        return

    def getXmlInfo(self):
        print '[TSsatEditor] trying to get the XML declaration and comment'
        parser = ParserCreate()
        parser.XmlDeclHandler = self.declarationHandler
        parser.CommentHandler = self.commentHandler
        satFile = open(TMPFILE, 'r')
        parser.ParseFile(satFile)
        satFile.close()
        return

    def cbDownload(self, data):
        print '[TSsatEditor] saving download to temp satellite file'
        try:
            tmpFile = open(TMPFILE, 'w')
            tmpFile.write(data)
            tmpFile.close()
        except IOError as error:
            print '[TSsatEditor] unable to save download to temp satellite file'
            self.session.open(MessageBox, _('Unable to save download to temp satellite file.\n'), MessageBox.TYPE_ERROR)
            return

        self.getXmlInfo()
        self.loadSatellitesFile(TMPFILE)
        self.useTmpFile = True
        self.showAccept = True
        self.downloadPossible = False
        self['key_yellow'].setText('')
        self['info'].setText('To edit satellite.xml, select satellites to be included, then Save')
        return

    def cbDownloadError(self, error):
        if error is not None:
            print '[TSsatEditor] error downloading satellite file:', str(error.getErrorMessage())
            self.session.open(MessageBox, _('Unable to download satellite file. Please try again later.\n%s') % str(error.getErrorMessage()), MessageBox.TYPE_ERROR)
            self['info'].setText('To edit satellite.xml,select satellites to be included,then save')
        return

    def purgeSatellitesFile(self):
        if not self.purgePossible:
            return
        print '[TSsatEditor] purging temp satellite file'
        self['info'].setText('Saving satellite.xml..please wait')
        if self.useTmpFile:
            satFile = TMPFILE
        else:
            satFile = SATFILE
        savesatellite(satFile, self.xmlVersion, self.xmlEncoding, self.xmlComment)
        self.postPurge()
        return

    def postPurge(self):
        self.loadSatellitesFile(TMPFILE)
        self.setListSorted()
        self.downloadPossible = True
        self['info'].setText('To edit satellite.xml,select satellites to be included,then save')
        self['key_yellow'].setText(_('Download'))
        self.showAccept = True
        self.accept()
        return


class savesatellite:

    def __init__(self, satFile, xmlVersion, xmlEncoding, xmlComment):
        self.satFile = satFile
        self.xmlVersion = xmlVersion
        self.xmlEncoding = xmlEncoding
        self.xmlComment = xmlComment
        self.purge()
        return

    def run(self):
        self.purge()
        return

    def stop(self):
        return

    def purge(self):
        satellites = config.plugins.sateditor.satellites.value
        newRoot = etree.Element('satellites')
        satFile = open(self.satFile, 'r')
        curroot = etree.parse(satFile)
        satFile.close()
        for sat in curroot.findall('sat'):
            position = sat.attrib.get('position')
            if position in satellites:
                newRoot.append(sat)

        header = ''
        if self.satFile == TMPFILE:
            if self.xmlVersion and self.xmlEncoding:
                header = '<?xml version="%s" encoding="%s"?>\n' % (self.xmlVersion, self.xmlEncoding)
            if self.xmlComment:
                modified = '\n     THIS FILE WAS MODIFIED BY THE ENIGMA2 PLUGIN SATELLITE EDITOR!\n'
                header += '<!-- %s%s-->\n' % (self.xmlComment, modified)
            if header:
                tmpFile = open(TMPFILE, 'w')
                tmpFile.writelines(header)
                tmpFile.close()
        if header:
            tmpFile = open(TMPFILE, 'a')
        else:
            tmpFile = open(TMPFILE, 'w')
        xmlString = etree.tostring(newRoot)
        tmpFile.writelines(xmlString)
        tmpFile.close()
        return


return
