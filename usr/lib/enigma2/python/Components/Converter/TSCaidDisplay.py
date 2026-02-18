# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Components/Converter/TSCaidDisplay.py
# Compiled at: 2014-03-14 00:21:56
from Components.Converter.Converter import Converter
from Tools.Directories import fileExists
from enigma import iServiceInformation, iPlayableService
from Components.Element import cached
from Poll import Poll

class TSCaidDisplay(Poll, Converter, object):

    def __init__(self, type):
        Poll.__init__(self)
        Converter.__init__(self, type)
        self.type = type
        self.systemCaids = {'06': 'I', '01': 'S', 
           '18': 'N', 
           '05': 'V', 
           '0B': 'CO', 
           '17': 'B', 
           '0D': 'CW', 
           '4A': 'DC', 
           '09': 'ND'}
        self.poll_interval = 2000
        self.poll_enabled = True
        return

    @cached
    def get_caidlist(self):
        caidlist = {}
        service = self.source.service
        if service:
            info = service and service.info()
            if info:
                caids = info.getInfoObject(iServiceInformation.sCAIDs)
                if caids:
                    for cs in self.systemCaids:
                        caidlist[cs] = (
                         self.systemCaids.get(cs), 0)

                    for caid in caids:
                        c = '%x' % int(caid)
                        if len(c) == 3:
                            c = '0%s' % c
                        c = c[:2].upper()
                        if self.systemCaids.has_key(c):
                            caidlist[c] = (
                             self.systemCaids.get(c), 1)

                    ecm_info = self.ecmfile()
                    if ecm_info:
                        emu_caid = ecm_info.get('caid', '')
                        if emu_caid and emu_caid != '0x000':
                            c = emu_caid.lstrip('0x')
                            if len(c) == 3:
                                c = '0%s' % c
                            c = c[:2].upper()
                            caidlist[c] = (self.systemCaids.get(c), 2)
        return caidlist

    getCaidlist = property(get_caidlist)

    @cached
    def getText(self):
        if self.type == 'EcmInfo':
            textvalue = ''
            service = self.source.service
            if service:
                info = service and service.info()
                if info:
                    if info.getInfoObject(iServiceInformation.sCAIDs):
                        ecm_info = self.ecmfile()
                        if ecm_info:
                            caid = ecm_info.get('caid', '')
                            caid = caid.lstrip('0x')
                            caid = caid.upper()
                            caid = caid.zfill(4)
                            caid = 'CAID: %s' % caid
                            hops = ecm_info.get('hops', None)
                            hops = 'Hops: %s' % hops
                            ecm_time = ecm_info.get('ecm time', None)
                            if ecm_time:
                                if 'msec' in ecm_time:
                                    ecm_time = 'ECM Time: %s' % ecm_time
                                else:
                                    ecm_time = 'ECM Time: %s s' % ecm_time
                            address = 'Source: %s ' % ecm_info.get('address', '')
                            using = ecm_info.get('using', '')
                            if using:
                                if using == 'emu':
                                    textvalue = 'Source: Softcam  %s' % ecm_time
                                elif using == 'CCcam-s2s':
                                    textvalue = '%s  %s  %s' % (address, hops, ecm_time)
                                else:
                                    textvalue = '%s  %s  %s' % (address, hops, ecm_time)
                            else:
                                source = ecm_info.get('source', None)
                                if source:
                                    if source == 'emu':
                                        textvalue = '(EMU) %s' % caid
                                    else:
                                        textvalue = '%s - %s - %s' % (caid, source, ecm_time)
                                oscsource = ecm_info.get('from', None)
                                if oscsource:
                                    textvalue = '%s - %s - %s - %s' % (caid,
                                     oscsource,
                                     hops,
                                     ecm_time)
                                decode = ecm_info.get('decode', None)
                                if decode:
                                    if decode == 'Internal':
                                        textvalue = '(EMU) %s' % caid
                                    else:
                                        textvalue = '%s - %s' % (caid, decode)
        elif self.type == 'EcmType':
            textvalue = ' '
            service = self.source.service
            if service:
                info = service and service.info()
                if info:
                    if info.getInfoObject(iServiceInformation.sCAIDs):
                        ecm_info = self.ecmfile()
                        if ecm_info:
                            using = ecm_info.get('using', '')
                            if using:
                                if using == 'emu':
                                    textvalue = 'EMU'
                                elif using == 'CCcam-s2s':
                                    textvalue = 'NET'
                            else:
                                source = ecm_info.get('source', None)
                                if source:
                                    if source == 'emu':
                                        textvalue = 'EMU'
                                oscsource = ecm_info.get('from', None)
                                if oscsource:
                                    textvalue = 'CRD'
                                decode = ecm_info.get('decode', None)
                                if decode:
                                    if decode == 'Internal':
                                        textvalue = 'EMU'
        elif self.type == 'EcmType2':
            textvalue = ' '
            service = self.source.service
            if service:
                info = service and service.info()
                if info:
                    textvalue = '-----------------'
                    if info.getInfoObject(iServiceInformation.sCAIDs):
                        ecm_info = self.ecmfile()
                        textvalue = ' '
                        if ecm_info:
                            using = ecm_info.get('using', '')
                            if using:
                                if using == 'emu':
                                    textvalue = 'EMULATOR'
                                elif using == 'CCcam-s2s':
                                    textvalue = 'NETWORK'
                            else:
                                source = ecm_info.get('source', None)
                                if source:
                                    if source == 'emu':
                                        textvalue = 'EMULATOR'
                                oscsource = ecm_info.get('from', None)
                                if oscsource:
                                    textvalue = 'CARD'
                                decode = ecm_info.get('decode', None)
                                if decode:
                                    if decode == 'Internal':
                                        textvalue = 'EMULATOR'
        elif self.type == 'EcmTime':
            textvalue = ' '
            service = self.source.service
            if service:
                info = service and service.info()
                if info:
                    if info.getInfoObject(iServiceInformation.sCAIDs):
                        ecm_info = self.ecmfile()
                        ecm_time = ecm_info.get('ecm time', None)
                        if ecm_info:
                            if ecm_time is not None:
                                if 'msec' in ecm_time:
                                    textvalue = 'ECM Time: %s' % ecm_time
                                else:
                                    textvalue = 'ECM Time: %s s' % ecm_time
        elif self.type == 'Cryptname':
            textvalue = ' '
            service = self.source.service
            if service:
                info = service and service.info()
                if info:
                    textvalue = 'FREE TO AIR'
                    if info.getInfoObject(iServiceInformation.sCAIDs):
                        ecm_info = self.ecmfile()
                        textvalue = ' '
                        caid = ecm_info.get('caid', '')
                        caid = caid.lstrip('0x')
                        caid = caid.upper()
                        caid = caid.zfill(4)
                        if caid[:2] == '06':
                            textvalue = 'IRDETO'
                        elif caid[:2] == '01':
                            textvalue = 'SECA'
                        elif caid[:2] == '18':
                            textvalue = 'NAGRAVISION'
                        if caid[:2] == '05':
                            textvalue = 'VIACCESS'
                        elif caid[:2] == '0B':
                            textvalue = 'CONAX'
                        elif caid[:2] == '17':
                            textvalue = 'BETACRYPT'
                        if caid[:2] == '0D':
                            textvalue = 'CRYPTOWORKS'
                        elif caid[:2] == '4A':
                            textvalue = 'DREAMCRYPT'
                        elif caid[:2] == '09':
                            textvalue = 'NDS'
        return textvalue

    text = property(getText)

    def ecmfile(self):
        ecm = None
        info = {}
        service = self.source.service
        if service:
            frontendInfo = service.frontendInfo()
            if frontendInfo:
                try:
                    ecmpath = '/tmp/ecm%s.info' % frontendInfo.getAll(False).get('tuner_number')
                    ecm = open(ecmpath, 'rb').readlines()
                except:
                    try:
                        ecm = open('/tmp/ecm.info', 'rb').readlines()
                    except:
                        pass

            if ecm:
                for line in ecm:
                    x = line.lower().find('msec')
                    if x != -1:
                        info['ecm time'] = line[0:x + 4]
                    else:
                        if line[0] == '=':
                            info['pid'] = line.split(' ')[7]
                        item = line.split(':', 1)
                        if len(item) > 1:
                            info[item[0].strip().lower()] = item[1].strip()
                            if info.has_key('pid') and fileExists('/tmp/pid.info'):
                                pid = open('/tmp/pid.info', 'rb').readlines()
                                for line in pid:
                                    if line.lower().find(info['pid']) != -1:
                                        s = line.split(' ')
                                        info['caid'] = s[3]
                                        print '[TSCaidsDisplay] caid: %s' % info['caid']
                                        break

                        elif not info.has_key('caid'):
                            x = line.lower().find('caid')
                            if x != -1:
                                y = line.find(',')
                                if y != -1:
                                    info['caid'] = line[x + 5:y]

        return info

    def changed(self, what):
        if what[0] == self.CHANGED_SPECIFIC and what[1] == iPlayableService.evUpdatedInfo or what[0] == self.CHANGED_POLL:
            Converter.changed(self, what)
        return


return
