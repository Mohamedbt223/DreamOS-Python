import os
from Tools.IO import runPipe

def getTSimageVersionString():
    path = '/etc/tsimage-version'
    if not os.path.exists(path):
        return 'wrong'

    try:
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                key, val = line.split('=', 1)
                key = key.strip().lower()
                val = val.strip().strip('"').strip("'")
                if key == 'comment':
                    # e.g. comment=TSimage_6.0
                    return 'TSimage' if val.startswith('TSimage_') else 'wrong'
    except Exception:
        pass

    return 'wrong'


def getpaneltitle():
    return getTSimageVersionString()


class TSimagePanelImage:

    def __init__(self, session):
        pass
