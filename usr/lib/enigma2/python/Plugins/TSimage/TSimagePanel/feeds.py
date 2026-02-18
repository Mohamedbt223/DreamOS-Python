# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/feeds.py
# Compiled at: 2016-12-01 21:03:48
from tsimage import TSimagePanelImage
from urllib2 import urlopen, Request, HTTPError
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.InputBox import InputBox
from Components.ActionMap import ActionMap, NumberActionMap
from Components.ScrollLabel import ScrollLabel
from Components.Label import Label
from Components.MenuList import MenuList
from Components.Input import Input
from Screens.Console import Console
from Plugins.Plugin import PluginDescriptor
from Tools.LoadPixmap import LoadPixmap
from xml.dom.minidom import parse, getDOMImplementation, parseString
from enigma import eListboxPythonMultiContent, gFont, RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, RT_VALIGN_CENTER, loadPNG, eTimer, getDesktop
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from os import path as os_path, system as os_system
import ssl
if os_path.exists('/usr/lib/enigma2/python/Plugins/Extensions/Browser'):
    from Plugins.Extensions.Browser.Browser import Browser
    HbbTVbrowser = True
else:
    HbbTVbrowser = False
myname = 'TSiPanel-RSS Reader'

def main(session, **kwargs):
    session.open(TSFeedScreenList)
    return


def autostart(reason, **kwargs):
    return


def Plugins(**kwargs):
    return PluginDescriptor(name=myname, description='Read RSS feeds', where=PluginDescriptor.WHERE_PLUGINMENU, fnc=main)


desktopSize = getDesktop(0).size()

class TSFeedScreenList(Screen):
    skin_1280 = '\n        \t<screen name="TSFeedScreenList" position="center,130" size="920,510" title="RSS Reader" >\n                <widget name="mylist" position="20,15" size="880,490" scrollbarMode="showOnDemand" transparent="1" zPosition="1" />\n                </screen>'
    skin_1920 = '    <screen name="TSFeedScreenList" position="center,200" size="1300,720" title="RSS Reader">\n        <widget name="mylist" position="20,20" size="1260,600" zPosition="2" itemHeight="100" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background"  transparent="1" />\n        </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session, args=0):
        self.session = session
        Screen.__init__(self, session)
        self.menu = args
        self.config = FeedreaderConfig()
        self['mylist'] = MenuList([], True, eListboxPythonMultiContent)
        if desktopSize.width() == 1920:
            self['mylist'].l.setItemHeight(100)
            self['mylist'].l.setFont(0, gFont('Regular', 32))
        else:
            self['mylist'].l.setItemHeight(70)
            self['mylist'].l.setFont(0, gFont('Regular', 23))
        self['info'] = Label('RSS Reader')
        self['actions'] = ActionMap(['WizardActions', 'DirectionActions', 'MenuActions'], {'ok': (self.go), 'back': (self.close)}, -1)
        self.timer = eTimer()
        self.timer_conn = self.timer.timeout.connect(self.getFeedList)
        self.timer.start(200, 1)
        self.onClose.append(self.cleanup)
        return

    def cleanup(self):
        if self.config:
            self.config.cleanup()
        return

    def go(self):
        try:
            i = 1
            i = self['mylist'].getSelectedIndex()
            feed = self.feedlist[i][1]
            if feed:
                self.showFeed(feed)
            else:
                print '[' + myname + '] section in config not found'
        except:
            self['info'].setText('Sorry, no feeds available, try later')

        return

    def showFeed(self, feed):
        try:
            self.session.open(TSFeedScreenContent, feed)
        except IOError as e:
            self['info'].setText('Loading feeddata failed!')
        except URLError as e:
            if hasattr(e, 'reason'):
                self['info'].setText(str(e.reason))
                print 'Reason: %s' % str(e.reason)
            elif hasattr(e, 'code'):
                self['info'].setText(str(e.code))
                print 'Error code: %s' % str(e.code)
            else:
                self['info'].setText('Sorry, feeds not available')
                print 'URLError'
        except:
            print 'no feed data'
            self['info'].setText('Sorry feeds not available')

        return

    def getFeedList(self):
        list = []
        feedlist = []
        try:
            for feed in self.config.getFeeds():
                res = []
                feedname = feed.getName()
                if feedname.startswith('TunisiaSat'):
                    png = '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/images/tunisiasat.png'
                else:
                    png = '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/images/default.png'
                if desktopSize.width() == 1920:
                    res.append(MultiContentEntryText(pos=(0, 5), size=(5, 40), font=0, flags=RT_HALIGN_LEFT, text='', color=16777215))
                    res.append(MultiContentEntryPixmapAlphaTest(pos=(0, 5), size=(90,
                                                                                  90), png=loadPNG(png)))
                    res.append(MultiContentEntryText(pos=(120, 5), size=(800, 90), font=0, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER, text=feedname))
                else:
                    res.append(MultiContentEntryText(pos=(0, 5), size=(5, 30), font=0, flags=RT_HALIGN_LEFT, text='', color=16777215))
                    res.append(MultiContentEntryPixmapAlphaTest(pos=(0, 5), size=(60,
                                                                                  60), png=loadPNG(png)))
                    res.append(MultiContentEntryText(pos=(100, 5), size=(500, 60), font=0, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER, text=feedname))
                feedlist.append((feedname, feed))
                list.append(res)
                res = []

            self.feedlist = feedlist
            self['mylist'].l.setList(list)
            self['mylist'].show()
        except:
            self['info'].setText('error in parsing feed xml')

        return


class FeedreaderConfig:
    configfile = '/etc/tsipanelfeeds.xml'

    def __init__(self):
        self.node = None
        self.feeds = []
        self.readConfig()
        return

    def cleanup(self):
        if self.node:
            self.node.unlink()
            del self.node
            self.node = None
            self.feeds = []
        return

    def readConfig(self):
        self.cleanup()
        try:
            self.node = parse(self.configfile)
        except:
            print 'Illegal xml file'
            print self.configfile
            return

        self.node = self.node.documentElement
        self.getFeeds()
        return

    def writeConfig(self):
        impl = getDOMImplementation()
        newdoc = impl.createDocument(None, 'feeds', None)
        for feed in self.feeds:
            node = newdoc.createElement('feed')
            name = newdoc.createElement('name')
            name.appendChild(newdoc.createTextNode(feed.getName()))
            node.appendChild(name)
            url = newdoc.createElement('url')
            url.appendChild(newdoc.createTextNode(feed.getURL()))
            node.appendChild(url)
            if feed.getDescription():
                description = newdoc.createElement('description')
                description.appendChild(newdoc.createTextNode(feed.getDescription()))
                node.appendChild(description)
            newdoc.documentElement.appendChild(node)

        newdoc.writexml(file(self.configfile, 'w'))
        return

    def getFeeds(self):
        if self.feeds:
            return self.feeds
        for node in self.node.getElementsByTagName('feed'):
            name = ''
            description = ''
            url = ''
            nodes = node.getElementsByTagName('name')
            if nodes and nodes[0].childNodes:
                name = str(nodes[0].childNodes[0].data)
            nodes = node.getElementsByTagName('description')
            if nodes and nodes[0].childNodes:
                description = str(nodes[0].childNodes[0].data)
            nodes = node.getElementsByTagName('url')
            if nodes and nodes[0].childNodes:
                url = str(nodes[0].childNodes[0].data)
            self.feeds.append(Feed(name, description, url, True))

        return self.feeds

    def isFeed(self, feedname):
        for feed in self.feeds:
            if feed.getName() == feedname:
                return True

        return False

    def getFeedByName(self, feedname):
        for feed in self.feeds:
            if feed.getName() == feedname:
                return feed

        return

    def getProxysettings(self):
        proxynodes = self.node.getElementsByTagName('proxy')
        for node in proxynodes:
            if self.node.getElementsByTagName('useproxy'):
                proxysettings = {}
                httpnodes = node.getElementsByTagName('http')
                if httpnodes and httpnodes[0].childNodes:
                    proxysettings['http'] = str(httpnodes[0].childNodes[0].data)
                ftpnodes = node.getElementsByTagName('ftp')
                if ftpnodes and ftpnodes[0].childNodes:
                    proxysettings['ftp'] = str(ftpnodes[0].childNodes[0].data)
                return proxysettings

        return

    def addFeed(self, feed):
        if self.isFeed(feed.getName()):
            return (False, _('Feed already exists!'))
        feed.setFavorite()
        self.feeds.append(feed)
        self.writeConfig()
        return (True, _('Feed added'))

    def changeFeed(self, feedold, feednew):
        for index in range(0, len(self.feeds)):
            if self.feeds[index].getName() == feedold.getName():
                self.feeds[index] = feednew
                self.writeConfig()
                return (
                 True, _('Feed updated'))

        return (
         False, _('Feed not found in config'))

    def deleteFeedWithName(self, feedname):
        for index in range(0, len(self.feeds)):
            if self.feeds[index].getName() == feedname:
                self.feeds.pop(index)
                self.writeConfig()
                break

        return


class Feed:
    isfavorite = False

    def __init__(self, name, description, url, isfavorite=False):
        self.name = name
        self.description = description
        self.url = url
        self.isfavorite = isfavorite
        return

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description

    def getURL(self):
        self.url = self.url.replace('zz', '&')
        return self.url

    def setName(self, name):
        self.name = name
        return

    def setDescription(self, description):
        self.description = description
        return

    def setURL(self, url):
        self.url = url
        return

    def setFavorite(self):
        self.isfavorite = True
        return

    def isFavorite(self):
        return self.isfavorite


class TSFeedScreenContent(Screen):
    skin_1280 = '\n        \t<screen name="TSFeedScreenContent" position="center,130" size="920,510" title="RSS Reader" >\n                <widget name="mylist" position="20,15" size="880,420" scrollbarMode="showOnDemand" transparent="1" zPosition="1" />\n\t        <ePixmap name="red"    position="70,475"   zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" transparent="1" alphatest="blend" />\n\t        <widget name="key_red" position="70,480" size="140,40" valign="center" halign="center" zPosition="2"  font="Regular;21" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n\t        <widget name="info" position="20,15" size="880,420" valign="center" halign="center" zPosition="2"  font="Regular;21" foregroundColor="foreground" backgroundColor="background" transparent="1" /> \n        \t</screen>'
    skin_1920 = '    <screen name="TSFeedScreenContent" position="center,200" size="1300,720" title="RSS Reader">\n    <widget name="mylist" position="center,20" size="1260,480" zPosition="2" itemHeight="40" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background"  transparent="1" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png" position="70,640" size="200,40" alphatest="blend" />\n    <widget name="key_red" position="70,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#940d0d" transparent="1" />\n\t        <widget name="info" position="center,center" size="1260,480" valign="center" halign="center" zPosition="2"  font="Regular;28" foregroundColor="foreground" backgroundColor="background" transparent="1" /> \n        \t</screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session, args=0):
        self.feed = args
        self.session = session
        Screen.__init__(self, session)
        self.feedname = self.feed.getName()
        self['info'] = Label()
        self['mylist'] = MenuList([], True, eListboxPythonMultiContent)
        if desktopSize.width() == 1920:
            self['mylist'].l.setItemHeight(45)
            self['mylist'].l.setFont(0, gFont('Regular', 30))
        else:
            self['mylist'].l.setItemHeight(35)
            self['mylist'].l.setFont(0, gFont('Regular', 23))
        self.menu = args
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': (self.go), 'red': (self.close), 
           'cancel': (self.close)}, -2)
        self['key_red'] = Label(_('Back'))
        self['info'].setText(_('Loading feed content..'))
        self.setTitle(self.feedname)
        self.timer = eTimer()
        self.timer_conn = self.timer.timeout.connect(self.filllist)
        self.timer.start(200, 1)
        return

    def filllist(self):
        list = []
        self.itemlist = []
        newlist = []
        itemnr = 0
        for item in self.getFeedContent(self.feed):
            list.append((item['title'], itemnr))
            self.itemlist.append(item)
            itemnr = itemnr + 1
            res = []
            if desktopSize.width() == 1920:
                res.append(MultiContentEntryText(pos=(0, 0), size=(5, 45), font=0, flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER, text='', color=16777215))
                res.append(MultiContentEntryText(pos=(5, 0), size=(1240, 45), font=0, flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER, text=item['title']))
            else:
                res.append(MultiContentEntryText(pos=(0, 0), size=(5, 35), font=0, flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER, text='', color=16777215))
                res.append(MultiContentEntryText(pos=(5, 0), size=(830, 35), font=0, flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER, text=item['title']))
            newlist.append(res)
            res = []

        self['info'].setText('')
        if len(self.itemlist) == 0:
            self['info'].setText('Sorry, feed not available, try later')
        else:
            self['mylist'].l.setList(newlist)
            self['mylist'].show()
        return

    def getFeedContent(self, feed):
        print '[' + myname + "] reading feedurl '%s' ..." % feed.getURL()
        try:
            self.rss = RSS()
            self.feedc = self.rss.getList(feed.getURL())
            print '[' + myname + '] have got %i items in newsfeed ' % len(self.feedc)
            return self.feedc
        except IOError:
            print '[' + myname + '] IOError by loading the feed! feed adress correct?'
            self['info'].setText('IOError by loading the feed! feed adress correct')
            return []
        except:
            self['info'].setText('Loading feeddata failed!')
            return []

        return

    def go(self):
        i = self['mylist'].getSelectedIndex()
        self.currentindex = i
        selection = self['mylist'].l.getCurrentSelection()
        if selection is not None:
            item = self.itemlist[i]
            if item['type'].startswith('folder') is True:
                newitem = Feed(item['title'], item['desc'], item['link'])
                self.session.open(TSFeedScreenContent, newitem)
            elif item['type'].startswith('pubfeed') is True:
                newitem = Feed(item['title'], item['desc'], item['link'])
                self.session.open(TSFeedScreenContent, newitem)
            else:
                try:
                    self.session.open(TSFeedScreenItemviewer, [self.feed,
                     item,
                     self.currentindex,
                     self.itemlist])
                except AssertionError:
                    self.session.open(MessageBox, _('Error processing feeds'), MessageBox.TYPE_ERROR)

        return


class TSFeedScreenItemviewer(Screen):
    skin_1280 = '\n        \t<screen name="TSFeedScreenItemviewer" position="center,130" size="920,510"  title="RSS Reader"  >\t\n\t\t\t\t        <widget name="leagueNumberWidget" position="800,485" size="90,35" transparent="1" halign="right" font="Regular;20" foregroundColor="yellow"/>\n                                        <ePixmap position="850,445" zPosition="4" size="60,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/images/arrows.png" transparent="1" alphatest="on" />\n\t\t\t\t        <widget name="text" position="20,20" size="900,400" font="Regular;23" foregroundColor="foreground" backgroundColor="background" transparent="1"/>\n                                        <ePixmap name="red"    position="70,475"   zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" transparent="1" alphatest="blend" />\n\t        <widget name="key_red" position="70,480" size="140,40" valign="center" halign="center" zPosition="2"  font="Regular;21" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n\t        <ePixmap name="yellow" position="312,475" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_yellow.png" transparent="1" alphatest="blend" /> \n        \t<ePixmap name="blue"   position="554,475" zPosition="2" size="150,30" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_blue.png" transparent="1" alphatest="blend" /> \n                                        <widget name="key_yellow" position="312,480" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;20" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n        \t<widget name="key_blue" position="554,480" size="150,40" valign="center" halign="center" zPosition="4"  foregroundColor="foreground" backgroundColor="background" font="Regular;20" transparent="1" />\n\t                        </screen>'
    skin_1920 = '     <screen name="TSFeedScreenItemviewer" position="center,200" size="1300,720"  title="RSS Reader"  >\t\n\t\t\t\t        <widget name="leagueNumberWidget" position="1180,680" size="90,30" transparent="1" halign="right" font="Regular;27" foregroundColor="yellow"/>\n                                        <ePixmap position="1220,635" zPosition="4" size="60,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/images/arrows.png" transparent="1" alphatest="on" />\n\t\t\t\t        <widget name="text" position="20,60" size="1260,500" font="Regular;32" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n                                        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png" position="70,640" size="200,40" alphatest="blend" />\n    <widget name="key_red" position="70,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#940d0d" transparent="1" />\n\t        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/yellow-big.png" position="350,640" size="200,40" alphatest="blend" />\n    <widget name="key_yellow" position="350,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#bba502" transparent="1" />\n    <ePixmap name="blue"   position="670,640" zPosition="2" size="200,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/blue-big.png" transparent="1" alphatest="blend" /> \n                                        <widget name="key_blue" position="670,640" size="200,40" valign="center" halign="center" zPosition="4"  foregroundColor="foreground" backgroundColor="#18188b" font="Regular;28" transparent="1" />\n\t                        </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session, args=0):
        self.feed = args[0]
        self.item = args[1]
        self.itemlist = args[3]
        self.url = self.item['link']
        self.currentindex = args[2]
        Screen.__init__(self, session)
        self.itemscount = len(self.itemlist)
        self['leagueNumberWidget'] = Label(str(self.currentindex + 1) + '/' + str(self.itemscount))
        self.setTitle(self.item['title'])
        self['text'] = ScrollLabel(self.item['desc'] + '\n\n' + self.item['date'] + '\n\n\nSource:\n%s' % self.item['link'])
        self['actions'] = ActionMap(['PiPSetupActions', 'WizardActions', 'ColorActions'], {'size-': (self.previousitem), 'size+': (self.nextitem), 
           'ok': (self.openmore), 
           'red': (self.close), 
           'yellow': (self.openbrowser), 
           'blue': (self.openmore), 
           'back': (self.close), 
           'left': (self['text'].pageUp), 
           'right': (self['text'].pageDown), 
           'up': (self['text'].pageUp), 
           'down': (self['text'].pageDown)}, -1)
        self['key_red'] = Label(_('Back'))
        self['key_yellow'] = Label(_('Browse'))
        self['key_blue'] = Label('')
        if 'tunisia-sat' in self.item['link']:
            self['key_blue'].setText(_('More'))
        return

    def gofill(self):
        i = self.currentindex
        selection = self.itemlist
        if selection is not None:
            item = self.itemlist[i]
            self.item = item
            self.filllist()
        return

    def filllist(self):
        self.itemscount = len(self.itemlist)
        self['leagueNumberWidget'].setText(str(self.currentindex + 1) + '/' + str(self.itemscount))
        self.setTitle(self.item['title'])
        self['text'].setText(self.item['desc'] + '\n\n' + self.item['date'] + '\n\n\nSource:\n%s' % self.item['link'])
        return

    def nextitem(self):
        currentindex = int(self.currentindex) + 1
        if currentindex == self.itemscount:
            currentindex = 0
        self.currentindex = currentindex
        self.gofill()
        return

    def previousitem(self):
        currentindex = int(self.currentindex) - 1
        if currentindex < 0:
            currentindex = self.itemscount - 1
        self.currentindex = currentindex
        self.gofill()
        return

    def openbrowser(self):
        if HbbTVbrowser == True:
            if self.item['link']:
                self.session.open(Browser, fullscreen=False, url=self.item['link'])
        else:
            self.session.open(MessageBox, _('Web Browser not installed!'), MessageBox.TYPE_INFO, timeout=10)
        return

    def openmore(self):
        if 'tunisia-sat' in self.item['link']:
            self.session.open(TSFeedScreenMore, self.item['link'], self.item['title'])
        return


class TSFeedScreenMore(Screen):
    skin_1280 = '\n        \t<screen name="TSFeedScreenMore" position="center,130" size="920,510"  title="RSS Reader"  >\t\n\t\t\t\t<widget name="leagueNumberWidget" position="800,485" size="90,35" transparent="1" halign="right" font="Regular;20" foregroundColor="yellow"/>\n                                        <ePixmap position="850,445" zPosition="4" size="60,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/images/arrows.png" transparent="1" alphatest="on" />\n\t\t\t\t        <widget name="text" position="20,20" size="900,400" font="Regular;23" foregroundColor="foreground" backgroundColor="background" transparent="1"/>\n                                        <ePixmap name="red"    position="70,475"   zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_red.png" transparent="1" alphatest="blend" />\n\t        <widget name="key_red" position="70,480" size="140,40" valign="center" halign="center" zPosition="2"  font="Regular;21" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n\t        <ePixmap name="yellow" position="312,475" zPosition="1" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_yellow.png" transparent="1" alphatest="blend" /> \n        \t<widget name="key_yellow" position="312,480" size="140,40" valign="center" halign="center" zPosition="2" font="Regular;20" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n        \t<widget name="waiting" position="20,20" size="880,400" valign="center" halign="center" zPosition="2"  font="Regular;21" foregroundColor="foreground" backgroundColor="background" transparent="1" /> \n        \t</screen>'
    skin_1920 = '     <screen name="TSFeedScreenMore" position="center,200" size="1300,720"  title="RSS Reader"  >\t\n\t\t\t\t        <widget name="leagueNumberWidget" position="1180,680" size="90,30" transparent="1" halign="right" font="Regular;27" foregroundColor="yellow"/>\n                                        <ePixmap position="1220,635" zPosition="4" size="60,40" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/images/arrows.png" transparent="1" alphatest="on" />\n\t\t\t\t        <widget name="text" position="20,60" size="1260,500" font="Regular;32" foregroundColor="foreground" backgroundColor="background" transparent="1" />\n                                        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png" position="70,640" size="200,40" alphatest="blend" />\n    <widget name="key_red" position="70,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#940d0d" transparent="1" />\n\t        <widget name="waiting" position="center,center" size="1260,500" valign="center" halign="center" zPosition="2"  font="Regular;28" foregroundColor="foreground" backgroundColor="background" transparent="1" /> \n        \t<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/yellow-big.png" position="350,640" size="200,40" alphatest="blend" />\n    <widget name="key_yellow" position="350,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#bba502" transparent="1" />\n    </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session, url, title, args=0):
        self.url = url
        self.urlfull = url
        Screen.__init__(self, session)
        self.setTitle(title)
        self['text'] = ScrollLabel('')
        self['actions'] = ActionMap(['PiPSetupActions', 'WizardActions', 'ColorActions'], {'size-': (self.previouspage), 'size+': (self.nextpage), 
           'ok': (self.close), 
           'red': (self.close), 
           'yellow': (self.openbrowser), 
           'back': (self.close), 
           'left': (self['text'].pageUp), 
           'right': (self['text'].pageDown), 
           'up': (self['text'].pageUp), 
           'down': (self['text'].pageDown)}, -1)
        self['key_red'] = Label(_('Back'))
        self['key_yellow'] = Label(_('Browse'))
        self['waiting'] = Label(_('Loading page content, please wait...'))
        self.currentpage = 1
        self.pagescount = 1
        self['leagueNumberWidget'] = Label()
        self.timer = eTimer()
        self.timer_conn = self.timer.timeout.connect(self.getPagesCount)
        self.timer.start(500, 1)
        return

    def getPagesCount(self):
        self.timer.stop()
        pagescount = 1
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            req = Request(self.url)
            req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36')
            url_req = urlopen(req, context=ctx)
            html_src = url_req.read()
            p = html_src.split('data-last="')
            if len(p) > 1:
                pages_list = p[1].strip().split('"')
            if len(pages_list) > 0:
                pagescount_str = pages_list[0].strip()
            pagescount = int(pagescount_str)
        except:
            pagescount = 1

        self.pagescount = pagescount
        self.timer = eTimer()
        self.timer_conn = self.timer.timeout.connect(self.getPageContent)
        self.timer.start(500, 1)
        return

    def getPageContent(self):
        pagescount = self.currentpage
        self.timer.stop()
        if pagescount > 1:
            self.urlfull = self.url + 'page-' + str(pagescount)
        else:
            self.urlfull = self.url
        labeltext = ''
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            req = Request(self.urlfull)
            req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36')
            url_req = urlopen(req, context=ctx)
            html_src = url_req.read()
            a = html_src.split('<article>')
            data_time = html_src.split('<div class="messageMeta">')
            data_author = html_src.split('<div class="bbCodeBlock bbCodeQuote" data-author=')
            count = 0
            for item in a:
                pubDate = data_time[count].split('</span>')[0].strip()
                author = ''
                text = item.split('</article>')[0].strip()
                if count > 0:
                    labeltext += '##newmessage##\n' + author.replace('>', '') + '\n' + pubDate.replace('<span class="item muted">', '')
                    labeltext += text
                count = count + 1

        except HTTPError as e:
            self['waiting'].setText('No more data')
        except:
            self['waiting'].setText('an error occur')

        if labeltext != '':
            rss = RSS()
            labeltext = rss.convertHTMLTags(labeltext)
            labeltext = ('\n').join([ll.rstrip() for ll in labeltext.splitlines() if ll.strip()])
            labeltext = labeltext.replace('##newmessage##', '\n\n')
            self['text'].setText(labeltext)
            self['leagueNumberWidget'].setText(str(self.currentpage) + '/' + str(self.pagescount))
            self['waiting'].setText('')
        return

    def nextpage(self):
        if self.pagescount > 1:
            currentpage = self.currentpage + 1
            if currentpage == self.pagescount + 1:
                currentpage = 1
            self.currentpage = currentpage
            self.LoadPage()
        return

    def previouspage(self):
        if self.pagescount > 1:
            currentpage = self.currentpage - 1
            if currentpage < 1:
                currentpage = self.pagescount
            self.currentpage = currentpage
            self.LoadPage()
        return

    def LoadPage(self):
        self['waiting'].setText(_('Loading page content, please wait...'))
        self['leagueNumberWidget'].setText('')
        self['text'].setText('')
        self.timer.start(500, 1)
        return

    def openbrowser(self):
        if HbbTVbrowser == True:
            if self.urlfull:
                self.session.open(Browser, fullscreen=False, url=self.urlfull)
        else:
            self.session.open(MessageBox, _('Web Browser not installed!'), MessageBox.TYPE_INFO, timeout=10)
        return


class RSS:
    DEFAULT_NAMESPACES = (None, 'http://purl.org/net/rss1.1#', 'http://purl.org/rss/1.0/',
                          'http://my.netscape.com/rdf/simple/0.9/')
    DUBLIN_CORE = {'dc': 'http://purl.org/dc/elements/1.1/', 'content': 'http://purl.org/rss/1.0/modules/content/'}

    def getElementsByTagName(self, node, tagName, possibleNamespaces=DEFAULT_NAMESPACES):
        for namespace in possibleNamespaces:
            children = node.getElementsByTagNameNS(namespace, tagName)
            if len(children):
                return children

        return []

    def node_data(self, node, tagName, possibleNamespaces=DEFAULT_NAMESPACES):
        children = self.getElementsByTagName(node, tagName, possibleNamespaces)
        node = len(children) and children[0] or None
        return node and ('').join([child.data.encode('utf-8') for child in node.childNodes]) or None

    def get_txt(self, node, tagName, default_txt=''):
        """
        Liefert den Inhalt >tagName< des >node< zurueck, ist dieser nicht
        vorhanden, wird >default_txt< zurueck gegeben.
        """
        return self.node_data(node, tagName) or self.node_data(node, tagName, self.DUBLIN_CORE) or default_txt

    def print_txt(self, node, tagName, print_string):
        """
        Formatierte Ausgabe
        """
        item_data = self.get_txt(node, tagName)
        if item_data == '':
            return
        print print_string % {'tag': tagName, 'data': item_data}
        return

    def print_txt2(self, node, tagName, print_string):
        """
        Formatierte Ausgabe
        """
        item_data = self.convertHTMLTags(self.get_txt(node, tagName))
        if item_data == '':
            return
        print print_string % {'tag': tagName, 'data': item_data}
        return

    def print_rss(self, url):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = Request(url)
        req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36')
        configproxies = FeedreaderConfig().getProxysettings()
        if configproxies:
            rssDocument = parseString(urlopen(req, context=ctx, proxies=configproxies).read().replace('content:encoded', 'content'))
        else:
            rssDocument = parseString(urlopen(req, context=ctx).read().replace('content:encoded', 'content'))
        for node in self.getElementsByTagName(rssDocument, 'item'):
            print '<ul class="RSS">'
            print '<li><h1><a href="%s">' % self.get_txt(node, 'link', '#')
            print self.get_txt(node, 'title', '<no title>')
            print '</a></h1></li>'
            self.print_txt(node, 'date', '<li><small>%(data)s</li>')
            self.print_txt2(node, 'content', '<li>%(data)s</li>')
            self.print_txt2(node, 'description', '<li>%(data)s</li>')
            print '</ul>'

        return

    def getList(self, url):
        """
        returns the content of the given URL as array
        """
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = Request(url)
        req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36')
        configproxies = FeedreaderConfig().getProxysettings()
        if configproxies:
            rssDocument = parseString(urlopen(req, context=ctx, proxies=configproxies).read().replace('content:encoded', 'content'))
        else:
            rssDocument = parseString(urlopen(req, context=ctx).read().replace('content:encoded', 'content'))
        channelname = self.get_txt(rssDocument, 'title', 'no channelname')
        data = []
        for node in self.getElementsByTagName(rssDocument, 'item'):
            nodex = {}
            nodex['channel'] = channelname
            nodex['type'] = self.get_txt(node, 'type', 'feed')
            nodex['link'] = self.get_txt(node, 'link', '')
            nodex['title'] = self.convertHTMLTags(self.get_txt(node, 'title', '<no title>'))
            nodex['date'] = self.get_txt(node, 'pubDate', self.get_txt(node, 'date', ''))
            nodex['desc'] = self.convertHTMLTags(self.get_txt(node, 'content', ''))
            if nodex['desc'] == '':
                nodex['desc'] = self.convertHTMLTags(self.get_txt(node, 'description', ''))
            data.append(nodex)

        return data

    def convertHTMLTags(self, text_with_html):
        """
        removes all undisplayable things from text
        """
        charlist = []
        charlist.append(('&#224;', 'à'))
        charlist.append(('&agrave;', 'à'))
        charlist.append(('&#225;', 'á'))
        charlist.append(('&aacute;', 'á'))
        charlist.append(('&#226;', 'â'))
        charlist.append(('&acirc;', 'â'))
        charlist.append(('&#228;', 'ä'))
        charlist.append(('&auml;', 'ä'))
        charlist.append(('&#249;', 'ù'))
        charlist.append(('&ugrave;', 'ù'))
        charlist.append(('&#250;', 'ú'))
        charlist.append(('&uacute;', 'ú'))
        charlist.append(('&#251;', 'û'))
        charlist.append(('&ucirc;', 'û'))
        charlist.append(('&#252;', 'ü'))
        charlist.append(('&uuml;', 'ü'))
        charlist.append(('&#242;', 'ò'))
        charlist.append(('&ograve;', 'ò'))
        charlist.append(('&#243;', 'ó'))
        charlist.append(('&oacute;', 'ó'))
        charlist.append(('&#244;', 'ô'))
        charlist.append(('&ocirc;', 'ô'))
        charlist.append(('&#246;', 'ö'))
        charlist.append(('&ouml;', 'ö'))
        charlist.append(('&#236;', 'ì'))
        charlist.append(('&igrave;', 'ì'))
        charlist.append(('&#237;', 'í'))
        charlist.append(('&iacute;', 'í'))
        charlist.append(('&#238;', 'î'))
        charlist.append(('&icirc;', 'î'))
        charlist.append(('&#239;', 'ï'))
        charlist.append(('&iuml;', 'ï'))
        charlist.append(('&#232;', 'è'))
        charlist.append(('&egrave;', 'è'))
        charlist.append(('&#233;', 'é'))
        charlist.append(('&eacute;', 'é'))
        charlist.append(('&#234;', 'ê'))
        charlist.append(('&ecirc;', 'ê'))
        charlist.append(('&#235;', 'ë'))
        charlist.append(('&euml;', 'ë'))
        charlist.append(('&#192;', 'À'))
        charlist.append(('&Agrave;', 'À'))
        charlist.append(('&#193;', 'Á'))
        charlist.append(('&Aacute;', 'Á'))
        charlist.append(('&#194;', 'Â'))
        charlist.append(('&Acirc;', 'Â'))
        charlist.append(('&#196;', 'Ä'))
        charlist.append(('&Auml;', 'Ä'))
        charlist.append(('&#217;', 'Ù'))
        charlist.append(('&Ugrave;', 'Ù'))
        charlist.append(('&#218;', 'Ú'))
        charlist.append(('&Uacute;', 'Ú'))
        charlist.append(('&#219;', 'Û'))
        charlist.append(('&Ucirc;', 'Û'))
        charlist.append(('&#220;', 'Ü'))
        charlist.append(('&Uuml;', 'Ü'))
        charlist.append(('&#210;', 'Ò'))
        charlist.append(('&Ograve;', 'Ò'))
        charlist.append(('&#211;', 'Ó'))
        charlist.append(('&Oacute;', 'Ó'))
        charlist.append(('&#212;', 'Ô'))
        charlist.append(('&Ocirc;', 'Ô'))
        charlist.append(('&#214;', 'Ö'))
        charlist.append(('&Ouml;', 'Ö'))
        charlist.append(('&#204;', 'Ì'))
        charlist.append(('&Igrave;', 'Ì'))
        charlist.append(('&#205;', 'Í'))
        charlist.append(('&Iacute;', 'Í'))
        charlist.append(('&#206;', 'Î'))
        charlist.append(('&Icirc;', 'Î'))
        charlist.append(('&#207;', 'Ï'))
        charlist.append(('&Iuml;', 'Ï'))
        charlist.append(('&#223;', 'ß'))
        charlist.append(('&szlig;', 'ß'))
        charlist.append(('&#038;', '&'))
        charlist.append(('&#38;', '&'))
        charlist.append(('&#8230;', '...'))
        charlist.append(('&#8211;', '-'))
        charlist.append(('&#160;', ' '))
        charlist.append(('&#039;', "'"))
        charlist.append(('&#39;', "'"))
        charlist.append(('&lt;', '<'))
        charlist.append(('&gt;', '>'))
        charlist.append(('&nbsp;', ' '))
        charlist.append(('&amp;', '&'))
        charlist.append(('&quot;', '"'))
        charlist.append(('&apos;', "'"))
        charlist.append(('&#8216;', "'"))
        charlist.append(('&#8217;', "'"))
        charlist.append(('&8221;', '”'))
        charlist.append(('&8482;', '™'))
        charlist.append(('&#8203;', ''))
        charlist.append(('&raquo;', '"'))
        charlist.append(('&laquo;', '"'))
        charlist.append(('&bdquo;', '"'))
        charlist.append(('&ldquo;', '"'))
        for repl in charlist:
            text_with_html = text_with_html.replace(repl[0], repl[1])

        from re import sub as re_sub
        text_with_html = re_sub('<(.*?)>(?uism)', '', text_with_html)
        return text_with_html


return
