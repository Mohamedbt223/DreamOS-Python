# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/TSimageSetup/TSyWeatherSetup.py
# Compiled at: 2016-11-22 07:46:06
from enigma import getDesktop, eListboxPythonMultiContent, gFont, RT_HALIGN_LEFT, RT_VALIGN_CENTER
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.MenuList import MenuList
from Components.Label import Label
from Components.Sources.List import List
from Components.Button import Button
from Components.Pixmap import Pixmap
from Components.ActionMap import ActionMap
from Components.ConfigList import ConfigList, ConfigListScreen
from Components.config import ConfigSubsection, ConfigText, ConfigSelection, ConfigSearchText, getConfigListEntry, config, configfile
from twisted.web.client import getPage
from urllib import quote as urllib_quote
from xml.dom.minidom import parseString
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import SCOPE_LANGUAGE, SCOPE_PLUGINS, SCOPE_CURRENT_SKIN, resolveFilename
import simplejson
from Components.Language import language
from os import environ
import gettext

def localeInit():
    lang = language.getLanguage()
    environ['LANGUAGE'] = lang[:2]
    gettext.bindtextdomain('enigma2', resolveFilename(SCOPE_LANGUAGE))
    gettext.textdomain('enigma2')
    gettext.bindtextdomain('TSimageSetup', '%s%s' % (resolveFilename(SCOPE_PLUGINS), 'TSimage/TSimageSetup/locale/'))
    return


def _(txt):
    t = gettext.dgettext('TSimageSetup', txt)
    if t == txt:
        t = gettext.gettext(txt)
    return t


localeInit()
language.addCallback(localeInit)
desktopSize = getDesktop(0).size()

class TSyWeatherEntries(Screen):
    skin_1280 = '\n\t\t<screen name="TSyWeatherEntries" position="center,center" size="560,400">\n\t\t\t<widget name="city" position="20,60" size="200,30" font="Regular;22" valign="center" halign="center" transparent="1" zPosition="1" />\n\t\t\t<widget name="defaultentry" position="300,60" size="220,30" font="Regular;22" valign="center" halign="right" transparent="1" zPosition="1" />\n\t\t\t<eLabel position="5,95" zPosition="4" size="550,1" text=" " backgroundColor="foreground" transparent="0" />\n\t\t\t<widget source="entrylist" render="Listbox" position="10,100" size="540,240" scrollbarMode="showOnDemand" enableWrapAround="1" transparent="1" zPosition="1">\n\t\t\t      <convert type="TemplatedMultiContent">\n\t\t\t\t{"template": [\n\t\t\t\t\t                MultiContentEntryText(pos = (10, 5), size = (200, 30), flags = RT_HALIGN_CENTER | RT_VALIGN_CENTER, text = 0) ,\n\t\t\t\t\t                MultiContentEntryPixmapAlphaBlend(pos = (430, 5), size = (30, 30), png = 2),\n\t\t\t\t\t                ],\n\t\t\t\t\t\t\t"fonts": [gFont("Regular", 22)],\n\t\t\t\t\t\t\t"itemHeight": 40\n\t\t\t\t\t\t\t}\n\t\t\t\t\t\t</convert>\n\t\t\t</widget>\n\t\t\t<widget name="key_red" position="0,10" size="140,40" zPosition="5" valign="center" halign="center" backgroundColor="red" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />\n\t\t\t<widget name="key_green" position="140,10" size="140,40" zPosition="5" valign="center" halign="center" backgroundColor="green" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />\n\t\t\t<widget name="key_yellow" position="280,10" size="140,40" zPosition="5" valign="center" halign="center" backgroundColor="yellow" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />\n\t\t\t<widget name="key_blue" position="420,10" zPosition="5" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />\n\t\t\t<widget name="key_ok" position="500,350" size="30,30" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_ok.png" transparent="1" alphatest="blend" />\n\t\t\t<ePixmap position="0,10" zPosition="4" size="140,40" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="blend" />\n\t\t\t<ePixmap position="140,10" zPosition="4" size="140,40" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="blend" />\n\t\t\t<ePixmap position="280,10" zPosition="4" size="140,40" pixmap="skin_default/buttons/yellow.png" transparent="1" alphatest="blend" />\n\t\t\t<ePixmap position="420,10" zPosition="4" size="140,40" pixmap="skin_default/buttons/blue.png" transparent="1" alphatest="blend" />\n\t\t</screen>'
    skin_1920 = '    <screen name="TSyWeatherEntries" position="center,200" size="1300,720" title="TSyWeather Entries">\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png" position="50,640" size="200,40" alphatest="blend" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green-big.png" position="360,640" size="200,40" alphatest="blend" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/yellow-big.png" position="670,640" size="200,40" alphatest="blend" />\n    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/blue-big.png" position="980,640" size="200,40" alphatest="blend" />\n    <widget name="key_red" position="50,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#940d0d" transparent="1" />\n    <widget name="key_green" position="360,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#2d872d" transparent="1" />\n    <widget name="key_yellow" position="670,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#bba502" transparent="1" />\n    <widget name="key_blue" position="980,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#18188b" transparent="1" />\n    <widget name="key_ok" position="1220,636" size="48,48" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/key_ok-big.png" transparent="1" alphatest="blend" />\n    <widget name="city" position="40,20" size="1000,40" foregroundColor="foreground" backgroundColor="background" font="Regular;32" valign="center" halign="left" transparent="1" zPosition="1" />    <widget name="defaultentry" position="920,20" size="320,40" foregroundColor="foreground" backgroundColor="background" font="Regular;32" valign="center" halign="right" transparent="1" zPosition="1" />\n    <eLabel position="10,70" zPosition="4" size="1280,1" backgroundColor="foreground" />\n    <widget source="entrylist" render="Listbox" position="20,80" size="1260,600" zPosition="2" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background"  transparent="1" >\n    <convert type="TemplatedMultiContent">\n    {"template": [\n    MultiContentEntryText(pos = (20, 0), size = (1000, 40), flags = RT_HALIGN_LEFT | RT_VALIGN_CENTER, text = 0) ,\n    MultiContentEntryPixmapAlphaBlend(pos = (1100, 0), size = (40, 40), png = 2),\n    ],\n    "fonts": [gFont("Regular", 32)],\n    "itemHeight": 40\n    }\n    </convert>\n    </widget>\n    </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session, index, locations, woeids):
        Screen.__init__(self, session)
        self.locations = locations
        self.woeids = woeids
        self.index = index
        self.title = _('Weather location entries')
        self['key_red'] = Label(_('Back'))
        self['key_green'] = Label(_('Add'))
        self['key_yellow'] = Label(_('Edit'))
        self['key_blue'] = Button(_('Delete'))
        self['key_ok'] = Pixmap()
        self['city'] = Label(_('City'))
        self['defaultentry'] = Label(_('Default entry'))
        self['entrylist'] = List([])
        self['actions'] = ActionMap(['WizardActions', 'MenuActions', 'ShortcutActions'], {'ok': (self.keySetDefault), 'back': (self.keyClose), 
           'red': (self.keyClose), 
           'green': (self.keyAdd), 
           'yellow': (self.keyEdit), 
           'blue': (self.keyRemove)}, -1)
        self.pixmap_on = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/images/enabled.png'))
        self.createList()
        self.onShown.append(self.updateSelection)
        self['entrylist'].onSelectionChanged.append(self.updateKeys)
        return

    def updateKeys(self):
        index = self['entrylist'].getIndex()
        if len(self.locationList) > 1 and self.locationList[index][2] == None:
            self['key_ok'].show()
            self['key_blue'].show()
        else:
            self['key_ok'].hide()
            self['key_blue'].hide()
        return

    def updateSelection(self):
        self['entrylist'].setIndex(self.index)
        self.updateKeys()
        return

    def createList(self):
        self.locationList = []
        for index in range(len(self.locations)):
            self.locationList.append((self.locations[index][0], self.woeids[index][0], None))

        self.locationList[self.index] = (self.locationList[self.index][0], self.locationList[self.index][1], self.pixmap_on)
        self['entrylist'].setList(self.locationList)
        self['entrylist'].setIndex(self.index)
        return

    def updateList(self, result):
        if not result == None:
            self.locations[self.index] = (
             result.city.value, _(result.city.value))
            self.woeids[self.index] = (result.weatherlocationcode.value, _(result.weatherlocationcode.value))
            self.locationList[self.index] = (result.city.value, result.weatherlocationcode.value, self.locationList[self.index][2])
            locationList_val = self.locations[0][0]
            woeidList_val = self.woeids[0][0]
            for index in range(1, len(self.locations)):
                locationList_val += '|' + self.locations[index][0]
                woeidList_val += '|' + self.woeids[index][0]

            config.plugins.TSWeather.locationList.value = locationList_val
            config.plugins.TSWeather.woeidList.value = woeidList_val
            config.plugins.TSWeather.locationList.save()
            config.plugins.TSWeather.woeidList.save()
            config.plugins.TSWeather.save()
            configfile.save()
            self['entrylist'].setList(self.locationList)
            self['entrylist'].setIndex(self.index)
        return

    def addToList(self, result):
        if not result == None:
            self.index = len(self.locationList)
            self.locations.append((result.city.value, _(result.city.value)))
            self.woeids.append((result.weatherlocationcode.value, _(result.weatherlocationcode.value)))
            self.locationList.append((result.city.value, result.weatherlocationcode.value, None))
            config.plugins.TSWeather.locationList.value = config.plugins.TSWeather.locationList.value + '|' + result.city.value
            config.plugins.TSWeather.woeidList.value = config.plugins.TSWeather.woeidList.value + '|' + result.weatherlocationcode.value
            config.plugins.TSWeather.locationList.save()
            config.plugins.TSWeather.woeidList.save()
            configfile.save()
            self['entrylist'].setList(self.locationList)
            self['entrylist'].setIndex(self.index)
        return

    def RemoveFromList(self, result):
        if result:
            if self.index == 0:
                config.plugins.TSWeather.locationList.value = config.plugins.TSWeather.locationList.value.replace(self.locationList[self.index][0] + '|', '')
                config.plugins.TSWeather.woeidList.value = config.plugins.TSWeather.woeidList.value.replace(self.locationList[self.index][1] + '|', '')
            else:
                config.plugins.TSWeather.locationList.value = config.plugins.TSWeather.locationList.value.replace('|' + self.locationList[self.index][0], '')
                config.plugins.TSWeather.woeidList.value = config.plugins.TSWeather.woeidList.value.replace('|' + self.locationList[self.index][1], '')
            config.plugins.TSWeather.locationList.save()
            config.plugins.TSWeather.woeidList.save()
            configfile.save()
            del self.locations[self.index]
            del self.woeids[self.index]
            del self.locationList[self.index]
            if config.plugins.TSWeather.locationIndex.value > self.index:
                config.plugins.TSWeather.locationIndex.value = config.plugins.TSWeather.locationIndex.value - 1
                config.plugins.TSWeather.locationIndex.save()
                configfile.save()
            self.index = self.index - 1
            self['entrylist'].setList(self.locationList)
            self['entrylist'].setIndex(self.index)
        return

    def keyClose(self):
        self.close(config.plugins.TSWeather.locationIndex.value, self.locations, self.woeids)
        return

    def keySetDefault(self):
        self.index = self['entrylist'].getIndex()
        if self.locationList[self.index][2] == None:
            self.locationList[config.plugins.TSWeather.locationIndex.value] = (
             self.locationList[config.plugins.TSWeather.locationIndex.value][0], self.locationList[config.plugins.TSWeather.locationIndex.value][1], None)
            self.index = self['entrylist'].getIndex()
            config.plugins.TSWeather.locationIndex.value = self.index
            config.plugins.TSWeather.locationIndex.save()
            configfile.save()
            self.locationList[self.index] = (self.locationList[self.index][0], self.locationList[self.index][1], self.pixmap_on)
            self['entrylist'].setList(self.locationList)
            self['entrylist'].setIndex(self.index)
        return

    def keyAdd(self):
        entry = ConfigSubsection()
        entry.city = ConfigSearchText(default=_('new city name'), visible_width=100, fixed_size=False)
        entry.weatherlocationcode = ConfigSelection(default=' ', choices=[(' ', _(' '))])
        self.session.openWithCallback(self.addToList, TSyWeatherSearch, entry)
        return

    def keyEdit(self):
        self.index = self['entrylist'].getIndex()
        entry = ConfigSubsection()
        entry.city = ConfigSearchText(default=self.locationList[self.index][0], visible_width=100, fixed_size=False)
        entry.weatherlocationcode = ConfigSelection(default=self.locationList[self.index][1], choices=[(self.locationList[self.index][1], _(self.locationList[self.index][1])), (self.locationList[self.index][1], _(self.locationList[self.index][1]))])
        self.session.openWithCallback(self.updateList, TSyWeatherSearch, entry)
        return

    def keyRemove(self):
        self.index = self['entrylist'].getIndex()
        if len(self.locationList) > 1 and self.locationList[self.index][2] == None:
            self.session.openWithCallback(self.RemoveFromList, MessageBox, _('Really delete the location entry %s?') % self.locationList[self.index][0])
        return


class TSyWeatherSearch(ConfigListScreen, Screen):
    skin_1280 = '\n\t\t<screen name="TSyWeatherSearch" position="center,center" size="560,400">\n\t\t\t<widget name="config" position="20,60" size="520,300" scrollbarMode="showOnDemand" />\n\t\t\t<ePixmap position="0,10" zPosition="4" size="140,40" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="blend" />\n\t\t\t<ePixmap position="140,10" zPosition="4" size="140,40" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="blend" />\n\t\t\t<ePixmap position="280,10" zPosition="4" size="140,40" pixmap="skin_default/buttons/yellow.png" transparent="1" alphatest="blend" />\n\t\t\t<ePixmap position="420,10" zPosition="4" size="140,40" pixmap="skin_default/buttons/blue.png" transparent="1" alphatest="blend" />\n\t\t\t<widget name="key_red" position="0,10" zPosition="5" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />\n\t\t\t<widget name="key_green" position="140,10" zPosition="5" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />\n\t\t\t<widget name="key_yellow" position="280,10" size="140,40" zPosition="5" valign="center" halign="center" backgroundColor="yellow" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />\n\t\t</screen>'
    skin_1920 = '    <screen name="TSyWeatherSearch" position="center,200" size="1300,720" title="TSyWeather Search">\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png" position="50,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green-big.png" position="360,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/yellow-big.png" position="670,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/blue-big.png" position="980,640" size="200,40" alphatest="blend" />\n        <widget name="key_red" position="50,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#940d0d" transparent="1" />\n        <widget name="key_green" position="360,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#2d872d" transparent="1" />\n        <widget name="key_yellow" position="670,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#bba502" transparent="1" />\n        <widget name="config" position="20,30" size="1260,600" zPosition="2" itemHeight="40" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background"  transparent="1" />\n        </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session, entry):
        Screen.__init__(self, session)
        self.current = entry
        self.title = _('Weather location search')
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'red': (self.keyCancel), 'green': (self.keySave), 
           'yellow': (self.searchLocation), 
           'ok': (self.searchLocation), 
           'cancel': (self.keyCancel)}, -2)
        self['key_red'] = Button(_('Cancel'))
        self['key_green'] = Button(_('Save'))
        self['key_yellow'] = Button(_('Search'))
        self['key_green'].hide()
        self.search_ready = False
        self.list = []
        ConfigListScreen.__init__(self, self.list, session)
        self.createSetup()
        return

    def createSetup(self):
        self.list = []
        self.list.append(getConfigListEntry(_('City'), self.current.city))
        self.list.append(getConfigListEntry(_('Location ID'), self.current.weatherlocationcode))
        self['config'].setList(self.list)
        return

    def searchLocation(self):
        if self.current.city.value != '':
            url = 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20geo.places%20where%20woeid%20in%20(select%20woeid%20from%20geo.places%20where%20text%3D%22' + urllib_quote(self.current.city.value) + '%2C%20ak%22)&format=json'
            getPage(url).addCallback(self.xmlCallback).addErrback(self.error)
        else:
            self.session.open(MessageBox, _('You need to enter a valid city name before you can search for the location ID.'), MessageBox.TYPE_ERROR)
        return

    def keySave(self):
        if self.current.city.value != '' and self.search_ready:
            self.close(self.current)
        elif self.current.city.value == '':
            self.session.open(MessageBox, _('Please enter a valid city name.'), MessageBox.TYPE_ERROR)
        return

    def keyCancel(self):
        self.close(None)
        return

    def xmlCallback(self, xmlstring):
        if xmlstring:
            self['config'].setCurrentIndex(1)
            self.session.openWithCallback(self.searchCallback, TSyWeatherSearchResult, xmlstring)
        return

    def error(self, error=None):
        if error is not None:
            print error
        return

    def searchCallback(self, result):
        self['config'].setCurrentIndex(0)
        if result:
            self.current.weatherlocationcode.setChoices([(result[0], _(result[0])), (result[0], _(result[0]))])
            if result[1] == 'None':
                if result[2] == 'None':
                    self.current.city.value = result[3]
                else:
                    self.current.city.value = result[2]
            else:
                self.current.city.value = result[1]
            self['key_green'].show()
            self.search_ready = True
        return


class TSyWeatherSearchResult(Screen):
    skin_1280 = '\n\t\t<screen name="TSyWeatherSearchResult" position="center,center" size="560,400">\n\t\t\t<widget name="searchlist" position="0,60" size="550,300" scrollbarMode="showOnDemand"/>\n\t\t\t<widget name="key_red" position="0,10" size="140,40" zPosition="5" valign="center" halign="center" backgroundColor="red" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />\n\t\t\t<widget name="key_green" position="140,10" size="140,40" zPosition="5" valign="center" halign="center" backgroundColor="green" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />\n\t\t\t<ePixmap position="0,10" zPosition="4" size="140,40" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="blend" />\n\t\t\t<ePixmap position="140,10" zPosition="4" size="140,40" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="blend" />\n\t\t</screen>'
    skin_1920 = '    <screen name="TSyWeatherSearchResult" position="center,200" size="1300,720" title="TSyWeather Search Results">\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/red-big.png" position="375,640" size="200,40" alphatest="blend" />\n        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/buttons/green-big.png" position="725,640" size="200,40" alphatest="blend" />\n        <widget name="key_red" position="375,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#940d0d" transparent="1" />\n        <widget name="key_green" position="725,640" size="200,40" zPosition="1" font="Regular;28" halign="center" valign="center" foregroundColor="foreground" backgroundColor="#2d872d" transparent="1" />\n        <widget name="searchlist" position="20,30" size="1260,600" zPosition="2" itemHeight="60" enableWrapAround="1" scrollbarMode="showOnDemand" foregroundColor="foreground" backgroundColor="background"  transparent="1" />\n    </screen>'
    if desktopSize.width() == 1920:
        skin = skin_1920
    else:
        skin = skin_1280

    def __init__(self, session, xmlstring):
        Screen.__init__(self, session)
        self.title = _('Location search result')
        self['key_red'] = Button(_('Back'))
        self['key_green'] = Button(_('OK'))
        self['searchlist'] = TSyWeatherSearchResultList([])
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': (self.keyOK), 'green': (self.keyOK), 
           'cancel': (self.keyClose), 
           'red': (self.keyClose)}, -1)
        self.updateList(xmlstring)
        return

    def updateList(self, xmlstring):
        self['searchlist'].buildList(xmlstring)
        return

    def keyClose(self):
        self.close(None)
        return

    def keyOK(self):
        try:
            sel = self['searchlist'].l.getCurrentSelection()[0]
        except:
            sel = None

        self.close(sel)
        return


class TSyWeatherSearchResultList(MenuList):

    def __init__(self, list, enableWrapAround=False):
        MenuList.__init__(self, list, enableWrapAround, eListboxPythonMultiContent)
        if desktopSize.width() == 1920:
            self.l.setFont(0, gFont('Regular', 34))
            self.l.setFont(1, gFont('Regular', 28))
        else:
            self.l.setFont(0, gFont('Regular', 22))
            self.l.setFont(1, gFont('Regular', 18))
        return

    def postWidgetCreate(self, instance):
        MenuList.postWidgetCreate(self, instance)
        if desktopSize.width() == 1920:
            instance.setItemHeight(90)
        else:
            instance.setItemHeight(60)
        return

    def getCurrentIndex(self):
        return self.instance.getCurrentIndex()

    def buildList(self, json):
        data = simplejson.loads(json)
        list = []
        results_nr = int(data['query']['count'])
        for idx in range(results_nr):
            searchlocation = ''
            searchstate = ''
            searchlocation_ext = ''
            searchcountry = ''
            weatherlocationcode = ''
            if results_nr == 1:
                searchlocation = str(data['query']['results']['place']['name'])
                if data['query']['results']['place'].get('admin1'):
                    if data['query']['results']['place']['admin1'].get('content'):
                        searchstate = str(data['query']['results']['place']['admin1']['content'])
                searchlocation_ext = '%s (%s)' % (searchlocation, searchstate)
                searchlocation_ext = searchlocation_ext.replace('()', '')
                if data['query']['results']['place'].get('country'):
                    if data['query']['results']['place']['country'].get('content'):
                        searchcountry = str(data['query']['results']['place']['country']['content'])
                if data['query']['results']['place'].get('woeid'):
                    weatherlocationcode = str(data['query']['results']['place']['woeid'])
            else:
                searchlocation = str(data['query']['results']['place'][idx]['name'])
                if data['query']['results']['place'][idx].get('admin1'):
                    if data['query']['results']['place'][idx]['admin1'].get('content'):
                        searchstate = str(data['query']['results']['place'][idx]['admin1']['content'])
                searchlocation_ext = '%s (%s)' % (searchlocation, searchstate)
                searchlocation_ext = searchlocation_ext.replace('()', '')
                if data['query']['results']['place'][idx].get('country'):
                    if data['query']['results']['place'][idx]['country'].get('content'):
                        searchcountry = str(data['query']['results']['place'][idx]['country']['content'])
                if data['query']['results']['place'][idx].get('woeid'):
                    weatherlocationcode = str(data['query']['results']['place'][idx]['woeid'])
            if desktopSize.width() == 1920:
                res = [
                 (
                  weatherlocationcode,
                  searchlocation,
                  searchstate,
                  searchcountry),
                 (eListboxPythonMultiContent.TYPE_TEXT,
                  7,
                  5,
                  780,
                  45,
                  0,
                  RT_HALIGN_LEFT | RT_VALIGN_CENTER,
                  searchlocation_ext),
                 (eListboxPythonMultiContent.TYPE_TEXT,
                  7,
                  45,
                  780,
                  38,
                  1,
                  RT_HALIGN_LEFT | RT_VALIGN_CENTER,
                  searchcountry)]
            else:
                res = [
                 (
                  weatherlocationcode,
                  searchlocation,
                  searchstate,
                  searchcountry),
                 (eListboxPythonMultiContent.TYPE_TEXT,
                  5,
                  8,
                  520,
                  30,
                  0,
                  RT_HALIGN_LEFT | RT_VALIGN_CENTER,
                  searchlocation_ext),
                 (eListboxPythonMultiContent.TYPE_TEXT,
                  5,
                  30,
                  520,
                  25,
                  1,
                  RT_HALIGN_LEFT | RT_VALIGN_CENTER,
                  searchcountry)]
            list.append(res)

        self.list = list
        self.l.setList(list)
        self.moveToIndex(0)
        return


return
