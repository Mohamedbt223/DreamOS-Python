# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebComponents/Sources/SleepTimer.py
# Compiled at: 2025-09-18 23:33:40
from Components.Sources.Source import Source
from Components.config import config
from Screens.MessageBox import MessageBox
import Screens.SleepTimerEdit

class SleepTimer(Source):

    def __init__(self, session):
        Source.__init__(self)
        self.session = session
        self.res = (False,
         config.SleepTimer.defaulttime.value,
         config.SleepTimer.action.value,
         config.SleepTimer.ask.value,
         _('Obligatory parameters missing [cmd [set,get], time [0-999], action [standby,shutdown], enabled [True,False]'))
        return

    def handleCommand(self, cmd):
        print '[WebComponents.SleepTimer].handleCommand'
        self.res = self.setSleeptimer(cmd)
        return

    def setSleeptimer(self, cmd):
        print '[WebComponents.SleepTimer].setSleeptimer, cmd=%s' % cmd
        from Screens.Standby import inStandby
        if inStandby == None:
            if cmd['cmd'] is None or cmd['cmd'] == 'get':
                if self.session.nav.SleepTimer.isActive():
                    return (self.session.nav.SleepTimer.isActive(),
                     self.session.nav.SleepTimer.getCurrentSleepTime(),
                     config.SleepTimer.action.value,
                     config.SleepTimer.ask.value,
                     _('Sleeptimer is enabled'))
                else:
                    return (
                     self.session.nav.SleepTimer.isActive(),
                     config.SleepTimer.defaulttime.value,
                     config.SleepTimer.action.value,
                     config.SleepTimer.ask.value,
                     _('Sleeptimer is disabled'))

            else:
                if cmd['cmd'] == 'set':
                    if cmd['enabled'] == 'True':
                        enabled = True
                    elif cmd['enabled'] == 'False':
                        enabled = False
                    else:
                        return (
                         self.session.nav.SleepTimer.isActive(),
                         config.SleepTimer.defaulttime.value,
                         config.SleepTimer.action.value,
                         config.SleepTimer.ask.value,
                         _("ERROR: Obligatory parameter 'enabled' [True,False] has unspecified value '%s'") % cmd['enabled'])
                    if cmd['time'] is None:
                        if enabled:
                            return (self.session.nav.SleepTimer.isActive(),
                             config.SleepTimer.defaulttime.value,
                             config.SleepTimer.action.value,
                             config.SleepTimer.ask.value,
                             _("ERROR: Obligatory parameter 'time' [0-999] is missing"))
                    else:
                        time = int(float(cmd['time']))
                        if time > 999:
                            time = 999
                        elif time < 0:
                            time = 0
                        config.SleepTimer.defaulttime.setValue(time)
                        config.SleepTimer.defaulttime.save()
                    if cmd['confirmed'] is not None:
                        confirmed = True if cmd['confirmed'].lower() == 'true' else False
                        config.SleepTimer.ask.value = confirmed
                        config.SleepTimer.ask.save()
                    if cmd['action'] == 'shutdown':
                        config.SleepTimer.action.value = 'shutdown'
                    else:
                        config.SleepTimer.action.value = 'standby'
                    config.SleepTimer.action.save()
                    if not enabled:
                        self.session.nav.SleepTimer.clear()
                        self.session.open(MessageBox, _('The sleep timer has been disabled.'), MessageBox.TYPE_INFO)
                        text = _('Sleeptimer has been disabled')
                    else:
                        self.session.nav.SleepTimer.setSleepTime(time)
                        self.session.open(MessageBox, _('The sleep timer has been activated for %s minutes.') % time, MessageBox.TYPE_INFO)
                        text = _('Sleeptimer set to %s minutes') % (time,)
                    return (
                     self.session.nav.SleepTimer.isActive(),
                     config.SleepTimer.defaulttime.value,
                     config.SleepTimer.action.value,
                     config.SleepTimer.ask.value,
                     text)
                else:
                    return (
                     self.session.nav.SleepTimer.isActive(),
                     config.SleepTimer.defaulttime.value,
                     config.SleepTimer.action.value,
                     config.SleepTimer.ask.value,
                     _("ERROR: Obligatory parameter 'cmd' [get,set] has unspecified value '%s'") % cmd['cmd'])

        else:
            return (
             self.session.nav.SleepTimer.isActive(),
             config.SleepTimer.defaulttime.value,
             config.SleepTimer.action.value,
             config.SleepTimer.ask.value,
             _('ERROR: Cannot set SleepTimer while device is in Standby-Mode'))
        return

    def getResult(self):
        return self.res

    timer = property(getResult)


return
