# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebComponents/Sources/RemoteControl.py
# Compiled at: 2025-09-18 23:33:40
from enigma import eActionMap
from Components.Sources.Source import Source
from Tools.HardwareInfo import HardwareInfo
from Components.config import config

class RemoteControl(Source):
    FLAG_MAKE = 0
    FLAG_BREAK = 1
    FLAG_REPEAT = 2
    FLAG_LONG = 3
    FLAG_ASCII = 4
    TYPE_STANDARD = 'dreambox remote control (native)'
    TYPE_ADVANCED = 'dreambox advanced remote control (native)'
    TYPE_KEYBOARD = 'dreambox ir keyboard'

    def __init__(self, session):
        self.cmd = None
        self.session = session
        Source.__init__(self)
        self.res = (False, _('Missing or wrong argument'))
        self.eam = eActionMap.getInstance()
        if config.misc.rcused.value == 1:
            self.remotetype = self.TYPE_STANDARD
        else:
            self.remotetype = self.TYPE_ADVANCED
        print "[RemoteControl.__init__] Configured RCU-Type is '%s'" % self.remotetype
        return

    def handleCommand(self, cmd):
        self.cmd = cmd
        self.res = self.sendEvent()
        return

    def sendEvent(self):
        if not self.cmd:
            print '[RemoteControl.sendEvent] cmd is empty or None'
            return self.res
        else:
            key = self.cmd.get('command', None)
            if key is None:
                print "[RemoteControl.sendEvent] Obligatory parameter 'command' is missing!"
                return (
                 False, _("Obligatory parameter 'command' is missing!"))
            key = int(key)
            if key <= 0:
                print '[RemoteControl.sendEvent] command <= 0 (%s)' % key
                return (
                 False, _('the command was not > 0'))
            type = self.cmd.get('type', '')
            flag = self.FLAG_MAKE
            if type == 'long':
                flag = self.FLAG_LONG
            elif type == 'ascii':
                flag = self.FLAG_ASCII
            remotetype = self.cmd.get('rcu', None)
            if remotetype == 'standard':
                remotetype = self.TYPE_STANDARD
            elif remotetype == 'advanced':
                remotetype = self.TYPE_ADVANCED
            elif remotetype == 'keyboard':
                remotetype == self.TYPE_KEYBOARD
            else:
                remotetype = self.remotetype
            if flag == self.FLAG_LONG:
                self.eam.keyPressed(remotetype, key, self.FLAG_MAKE)
            self.eam.keyPressed(remotetype, key, flag)
            self.eam.keyPressed(remotetype, key, self.FLAG_BREAK)
            print '[RemoteControl.sendEvent] command was was sent (key: %s, flag: %s)' % (key, flag)
            return (True, _("RC command '%s' has been issued") % str(key))

    result = property((lambda self: self.res))


return
