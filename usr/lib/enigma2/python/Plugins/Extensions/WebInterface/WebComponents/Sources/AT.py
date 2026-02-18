# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/WebInterface/WebComponents/Sources/AT.py
# Compiled at: 2025-09-18 23:33:40
from Components.Sources.Source import Source
from Tools.Directories import resolveFilename, SCOPE_HDD

class AT(Source):
    LIST = 0
    WRITE = 1

    def __init__(self, session, func=LIST):
        print 'AutoTimer: init: ', func
        Source.__init__(self)
        self.func = func
        self.session = session
        self.result = []
        return

    def handleCommand(self, cmd):
        print 'AutoTimer: handleCommand: ', cmd
        if cmd is not None:
            self.cmd = cmd
            if self.func is self.LIST:
                self.result = self.timerList(cmd)
            elif self.func is self.WRITE:
                self.result = self.writeTimer(cmd)
        return

    def timerList(self):
        print 'timerList'
        try:
            from Plugins.Extensions.AutoTimer.plugin import autotimer
            if not autotimer:
                from Plugins.Extensions.AutoTimer.AutoTimer import AutoTimer
                autotimer = AutoTimer()
        except ImportError:
            return []

        returnList = []
        for timer in autotimer.getTimerList():
            print 'TIMER: ', timer
            innerList = [
             timer.getName(),
             timer.getMatch()]
            if timer.hasAfterEvent():
                innerList.append(timer.getAfterEvent())
            else:
                innerList.append('')
            innerList.extend((
             timer.getExcludedTitle(),
             timer.getExcludedShort(),
             timer.getExcludedDescription(),
             timer.getExcludedDays()))
            innerList.extend((
             timer.getIncludedTitle(),
             timer.getIncludedShort(),
             timer.getIncludedDescription(),
             timer.getIncludedDays()))
            innerList.extend((
             timer.getServices(),
             timer.getBouquets()))
            if timer.hasTimespan():
                innerList.extend((
                 timer.getTimespanBegin(),
                 timer.getTimespanEnd()))
            else:
                innerList.extend(('', ''))
            if timer.hasDuration():
                innerList.append(timer.getDuration())
            else:
                innerList.append('')
            if timer.hasCounter():
                innerList.extend((
                 timer.getCounter(),
                 timer.getCounterLeft()))
            else:
                innerList.extend((0, 0))
            innerList.append(timer.getCounterLimit())
            if timer.hasDestination():
                innerList.append(timer.destination)
            else:
                innerList.append(resolveFilename(SCOPE_HDD))
            if timer.hasCounterFormatString():
                innerList.append(timer.getCounterFormatString())
            else:
                innerList.append('')
            innerList.extend((
             timer.getLastBegin(),
             timer.getJustplay(),
             timer.getAvoidDuplicateDescription()))
            if timer.hasTags():
                innerList.append(timer.getTags())
            else:
                innerList.append('')
            print 'Enabled', timer.getEnabled()
            innerList.append(timer.getEnabled())
            innerList.append('off')
            returnList.append(innerList)

        return returnList

    def writeTimer(self, param):
        print 'writeTimer: ', param
        return

    def command(self, param):
        print 'command: ', param
        return
        param = int(param)

    list = property(timerList)
    lut = {'Name': 0, 'Match': 1, 
       'AfterEvent': 2, 
       'ExcludedTitle': 3, 
       'ExcludedShort': 4, 
       'ExcludedDescription': 5, 
       'ExcludedDays': 6, 
       'IncludedTitle': 7, 
       'IncludedShort': 8, 
       'IncludedDescription': 9, 
       'IncludedDays': 10, 
       'Services': 11, 
       'Bouquets': 12, 
       'TimespanBegin': 13, 
       'TimespanEnd': 14, 
       'Duration': 15, 
       'Counter': 16, 
       'CounterLeft': 17, 
       'CounterLimit': 18, 
       'Destination': 19, 
       'CounterFormatString': 20, 
       'LastBegin': 21, 
       'Justplay': 22, 
       'AvoidDuplicateDescription': 23, 
       'Tags': 24, 
       'Enabled': 25, 
       'toggleDisabledIMG': 26}


return
