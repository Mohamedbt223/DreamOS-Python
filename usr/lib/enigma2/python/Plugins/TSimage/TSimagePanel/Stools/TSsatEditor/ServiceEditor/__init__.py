# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/TSimagePanel/Stools/TSsatEditor/ServiceEditor/__init__.py
# Compiled at: 2015-12-26 14:33:51
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from os import environ as os_environ
import gettext

def localeInit():
    lang = language.getLanguage()[:2]
    os_environ['LANGUAGE'] = lang
    gettext.bindtextdomain('ServiceEditor', resolveFilename(SCOPE_PLUGINS, 'SystemPlugins/ServiceEditor/po/'))
    return


def _(txt):
    t = gettext.dgettext('ServiceEditor', txt)
    if t == txt:
        t = gettext.gettext(txt)
    return t


localeInit()
language.addCallback(localeInit)
return
