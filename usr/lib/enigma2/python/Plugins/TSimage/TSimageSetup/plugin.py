# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/TSimageSetup/plugin.py
# Compiled at: 2016-11-22 07:46:06
from Plugins.Plugin import PluginDescriptor
from Components.config import config
from Tools.Directories import fileExists, SCOPE_LANGUAGE, SCOPE_PLUGINS, resolveFilename
from Plugins.TSimage.TSMediaPanel.plugin import TSMediaPanelAutostart
from Plugins.TSimage.TSimageSetup.SecondInfobar import SIBautostart
from Plugins.TSimage.TSimageSetup.Setup import TSSkinSetup
from PermanentClock import *
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

def sessionstart(reason, **kwargs):
    session = kwargs['session']
    if reason == 0:
        pClock.gotSession(session)
    return


def main(session, **kwargs):
    session.open(TSSkinSetup)
    return


def menu(menuid, **kwargs):
    if menuid == 'system':
        return [
         (_('TSimage Setup'),
          main,
          'tsskinssetup_system',
          44)]
    return []


def Plugins(**kwargs):
    list = []
    list.append(PluginDescriptor(where=[PluginDescriptor.WHERE_SESSIONSTART], fnc=sessionstart))
    if config.plugins.TSSkinSetup.TSiMediaPanelenabled.value:
        list.append(PluginDescriptor(where=PluginDescriptor.WHERE_SESSIONSTART, fnc=TSMediaPanelAutostart))
    list.append(PluginDescriptor(where=PluginDescriptor.WHERE_SESSIONSTART, fnc=SIBautostart))
    list.append(PluginDescriptor(name='TSi-imageSetup', description=_('Setup for TSimage'), where=PluginDescriptor.WHERE_MENU, fnc=menu))
    return list


def startConfig(session, **kwargs):
    session.open(PermanentClockMenu)
    return


return
