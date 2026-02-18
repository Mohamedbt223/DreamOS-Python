# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebChilds/External/__init__.py
# Compiled at: 2025-09-18 23:33:39
from os import listdir
from os.path import abspath, splitext
from Tools.Directories import resolveFilename, SCOPE_PLUGINS

def importExternalModules():
    dir = abspath(resolveFilename(SCOPE_PLUGINS) + 'Extensions/WebInterface/WebChilds/External/')
    for file in listdir(dir):
        module_name, ext = splitext(file)
        if ext == '.py' and module_name != '__init__':
            try:
                exec 'import ' + module_name
                print '[Toplevel.importExternalModules] Imported external module: %s' % module_name
            except ImportError as e:
                print '[Toplevel.importExternalModules] Could NOT import external module: %s' % module_name
                print '[Toplevel.importExternalModules] Exception Caught\n%s' % e

    return


return
