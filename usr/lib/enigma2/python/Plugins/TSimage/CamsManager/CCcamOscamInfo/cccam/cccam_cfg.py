# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: /usr/lib/enigma2/python/Plugins/TSimage/CamsManager/CCcamOscamInfo/cccam/cccam_cfg.py
# Compiled at: 2016-11-22 07:53:26
import os, string
from time import localtime

def _caseIndependentSort(something, other):
    something, other = string.lower(something).split(' ')[1], string.lower(other).split(' ')[1]
    return cmp(something, other)


def readClineFline(path):
    ret = ''
    res_fline = []
    res_cline = []
    try:
        file = open('%s/CCcam.cfg' % path, 'r')
        for line in file:
            if line.startswith('F:') or line.startswith('#F:'):
                res_fline.append(line.replace('\n', ''))
            elif line.startswith('C:') or line.startswith('#C:'):
                res_cline.append(line.replace('\n', ''))

        res_fline.sort(_caseIndependentSort)
        res_cline.sort(_caseIndependentSort)
        ret = 1
    except:
        ret = 0
        res_fline = [_('Error') + ' ' + _('Error') + ' ' + _('Error')]
        res_fline = [_('Error') + ' ' + _('Error') + ' ' + _('Error')]

    return (ret, res_fline, res_cline)


def writeCCcam_cfg(path, changes):
    ret = ''
    tmp = []
    try:
        file = open('%s/CCcam.cfg' % path, 'r')
        for line in file:
            if line.startswith('F') or line.startswith('#F') or line.startswith('C') or line.startswith('#C'):
                nochangedline = 0
                for key in changes:
                    if key == line.split(' ')[1] or key == line.split(' ')[1] + ':' + line.split(' ')[2]:
                        nochangedline = 1
                        if line.startswith('C:'):
                            tmp.append(line.replace('C:', '#C:', 1))
                        elif line.startswith('#C:'):
                            tmp.append(line.replace('#C:', 'C:', 1))
                        elif line.startswith('F:'):
                            tmp.append(line.replace('F:', '#F:', 1))
                        elif line.startswith('#F:'):
                            tmp.append(line.replace('#F:', 'F:', 1))

                if nochangedline == 0:
                    tmp.append(line)
            else:
                tmp.append(line)

        file.close()
        file = open('%s/CCcam.cfg' % path, 'w')
        for line in tmp:
            file.write(line)

        file.close()
        ret = 1
    except:
        ret = 0

    return ret


def changesCCcam_cfg(changes, F_or_C, idx, fline, cline):
    try:
        if F_or_C == 'C':
            if fline[idx].split(' ')[1] not in changes:
                changes['%s' % fline[idx].split(' ')[1]] = 'F'
            else:
                del changes[fline[idx].split(' ')[1]]
            if fline[idx].startswith('F'):
                fline[idx] = fline[idx].replace('F', '#F', 1)
            elif fline[idx].startswith('#F'):
                fline[idx] = fline[idx].replace('#F', 'F', 1)
        elif F_or_C == 'F':
            if '%s:%s' % (cline[idx].split(' ')[1], cline[idx].split(' ')[2]) not in changes:
                changes['%s:%s' % (cline[idx].split(' ')[1], cline[idx].split(' ')[2])] = 'C'
            else:
                del changes['%s:%s' % (cline[idx].split(' ')[1], cline[idx].split(' ')[2])]
            if cline[idx].startswith('C'):
                cline[idx] = cline[idx].replace('C', '#C', 1)
            elif cline[idx].startswith('#C'):
                cline[idx] = cline[idx].replace('#C', 'C', 1)
    except:
        pass

    return (
     len(changes),
     changes,
     fline,
     cline)


def backupConfig(path):
    try:
        os.system('cp %s/CCcam.cfg %s/CCcam.cfg_%s' % (path, path, '%04i:%02i:%02i_%02i:%02i:%02i' % localtime()[0:6]))
        ret = 1
    except:
        ret = 0

    return ret


def delConfigFile(path, file):
    try:
        os.unlink('%s/%s' % (path, file))
        ret = 1
    except:
        ret = 0

    return ret


def restoreConfigFile(path, file):
    try:
        os.system('cp %s/%s %s/CCcam.cfg' % (path, file, path))
        ret = 1
    except:
        ret = 0

    return ret


return
