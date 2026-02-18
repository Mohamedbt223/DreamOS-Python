#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fcntl import ioctl
from struct import pack, unpack
import os

def getFPVersion():
	ret = None
	try:
		ret = float(open("/proc/stb/fp/version", "r").read().strip())
	except IOError:
		try:
			fp = open("/dev/dbox/fp0")
			ret = ioctl(fp.fileno(),0)
		except IOError:
			print "getFPVersion failed!"
	return ret

def setFPWakeuptime(wutime):
	try:
		open("/proc/stb/fp/wakeup_time", "w").write(str(wutime))
	except IOError:
		try:
			fp = open("/dev/dbox/fp0")
			ioctl(fp.fileno(), 6, pack('L', wutime)) # set wake up
		except IOError:
			print "setFPWakeupTime failed!"

def setRTCtime(wutime):
	try:
		open("/proc/stb/fp/rtc", "w").write(str(wutime))
	except IOError:
		try:
			fp = open("/dev/dbox/fp0")
			ioctl(fp.fileno(), 0x101, pack('L', wutime)) # set wake up
		except IOError:
			print "setRTCtime failed!"

def getFPWakeuptime():
	ret = 0
	try:
		ret = long(open("/proc/stb/fp/wakeup_time", "r").read())
	except IOError:
		try:
			fp = open("/dev/dbox/fp0")
			ret = unpack('L', ioctl(fp.fileno(), 5, '    '))[0] # get wakeuptime
		except IOError:
			print "getFPWakeupTime failed!"
	return ret

def getFPWasTimerWakeup():
	was_wakeup = False
	try:
		was_wakeup = int(open("/proc/stb/fp/was_timer_wakeup", "r").read()) and True or False
	except:
		try:
			fp = open("/dev/dbox/fp0")
			was_wakeup = unpack('B', ioctl(fp.fileno(), 9, ' '))[0] and True or False
		except IOError:
			print "wasTimerWakeup failed!"
	return was_wakeup

def clearFPWasTimerWakeup():
	try:
		open("/proc/stb/fp/was_timer_wakeup", "w").write('0')
	except:
		try:
			fp = open("/dev/dbox/fp0")
			ioctl(fp.fileno(), 10)
		except IOError:
			print "clearFPWasTimerWakeup failed!"

def _read_temp_value(path):
    try:
        v = open(path, 'r').read().strip()
        if not v:
            return None
        # Some kernels expose milli-Celsius (e.g. 59234), others Celsius (e.g. 59)
        val = float(v)
        if val > 200:  # very likely m°C
            val = val / 1000.0
        return val
    except IOError:
        return None
    except ValueError:
        return None

def getCPUTemp():
    candidates = [
        "/proc/stb/fp/temp",                     # some DreamOS images
        "/proc/stb/sensors/temp0/value",         # Broadcom boxes
        "/sys/class/thermal/thermal_zone0/temp", # generic
        "/sys/devices/virtual/thermal/thermal_zone0/temp",
    ]
    for p in candidates:
        if os.path.exists(p):
            val = _read_temp_value(p)
            if val is not None:
                return val

    # Scan thermal zones and prefer CPU-like types
    zones_base = "/sys/class/thermal"
    preferred_types = ("cpu", "cpu-thermal", "soc-thermal", "a55", "a73", "big-thermal", "little-thermal")
    best = None
    best_is_cpu = False

    if os.path.isdir(zones_base):
        for name in os.listdir(zones_base):
            if not name.startswith("thermal_zone"):
                continue
            zdir = os.path.join(zones_base, name)
            tfile = os.path.join(zdir, "temp")
            typefile = os.path.join(zdir, "type")
            if not os.path.exists(tfile):
                continue
            tval = _read_temp_value(tfile)
            if tval is None:
                continue
            # read type label if available
            ztype = ""
            try:
                ztype = open(typefile, 'r').read().strip().lower()
            except IOError:
                ztype = ""
            # If it looks like CPU, take it immediately (pick hottest among CPU types)
            if any(x in ztype for x in preferred_types):
                if (best is None) or (not best_is_cpu) or (tval > best):
                    best = tval
                    best_is_cpu = True
            # Otherwise, remember the hottest as a fallback
            elif not best_is_cpu:
                if (best is None) or (tval > best):
                    best = tval
                    best_is_cpu = False

    return best

def getAllTemps():
    temps = {}

    # Legacy/proc sensors
    if os.path.exists("/proc/stb/sensors"):
        for name in os.listdir("/proc/stb/sensors"):
            val = _read_temp_value(os.path.join("/proc/stb/sensors", name, "value"))
            if val is not None:
                temps["proc:%s" % name] = val

    # Common single files
    for label, path in (
        ("fp", "/proc/stb/fp/temp"),
        ("zone0", "/sys/class/thermal/thermal_zone0/temp"),
    ):
        if os.path.exists(path):
            val = _read_temp_value(path)
            if val is not None:
                temps[label] = val

    # hwmon tree (labels + inputs)
    hwmon_base = "/sys/class/hwmon"
    if os.path.isdir(hwmon_base):
        for hw in os.listdir(hwmon_base):
            hdir = os.path.join(hwmon_base, hw)
            # optional device name
            try:
                hname = open(os.path.join(hdir, "name"), 'r').read().strip()
            except IOError:
                hname = hw
            # find temp*_input (+ optional temp*_label)
            for fn in os.listdir(hdir):
                if fn.startswith("temp") and fn.endswith("_input"):
                    base = fn[:-6]  # strip "_input"
                    label_path = os.path.join(hdir, base + "_label")
                    if os.path.exists(label_path):
                        try:
                            lbl = open(label_path, 'r').read().strip()
                        except IOError:
                            lbl = base
                    else:
                        lbl = base
                    val = _read_temp_value(os.path.join(hdir, fn))
                    if val is not None:
                        temps["%s:%s" % (hname, lbl)] = val

    # thermal zones with types
    zones_base = "/sys/class/thermal"
    if os.path.isdir(zones_base):
        for name in os.listdir(zones_base):
            if not name.startswith("thermal_zone"):
                continue
            zdir = os.path.join(zones_base, name)
            tfile = os.path.join(zdir, "temp")
            typefile = os.path.join(zdir, "type")
            if os.path.exists(tfile):
                val = _read_temp_value(tfile)
                if val is not None:
                    try:
                        ztype = open(typefile, 'r').read().strip()
                    except IOError:
                        ztype = name
                    temps["zone:%s" % ztype] = val

    return temps
