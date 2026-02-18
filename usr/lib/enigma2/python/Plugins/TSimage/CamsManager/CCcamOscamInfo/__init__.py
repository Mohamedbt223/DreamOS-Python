# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/CamsManager/CCcamOscamInfo/__init__.py
# Compiled at: 2014-05-25 12:11:21
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from os import environ
import gettext

def localeInit():
    lang = language.getLanguage()
    environ['LANGUAGE'] = lang[:2]
    gettext.bindtextdomain('enigma2', resolveFilename(SCOPE_LANGUAGE))
    gettext.textdomain('enigma2')
    gettext.bindtextdomain('CCcamOscamInfo', '%s%s' % (resolveFilename(SCOPE_PLUGINS), 'TSimage/CamsManager/CCcamOscamInfo/locale/'))
    return


def _(txt):
    t = gettext.dgettext('CCcamOscamInfo', txt)
    if t == txt:
        t = gettext.gettext(txt)
    return t


localeInit()
language.addCallback(localeInit)
return
