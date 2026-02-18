# uncompyle6 version 3.9.3
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.12.3 (main, Jan 22 2026, 20:57:42) [GCC 13.3.0]
# Embedded file name: python/Plugins/TSimage/CamsManager/CCcamOscamInfo/shared/Setup.py
# Compiled at: 2015-12-26 14:33:46
from enigma import *
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.ActionMap import ActionMap, NumberActionMap
from readConfig import read_Config

class CCcamOscamInfoConfigScreen(Screen):
    raw_skin = '\n        <screen position="center,center" size="{size.screen}" title="{title.screen}">\n            <widget name="header" position="{pos.header}" size="{size.header}" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label1}" size="{size.label1}" font="Regular;14" backgroundColor="#ffffff" />\n            <widget name="list" position="{pos.list}" size="{size.list}" scrollbarMode="showOnDemand" />\n            <eLabel text="" position="{pos.label2}" size="{size.label2}" font="Regular;14" backgroundColor="#ffffff" />\n            <ePixmap name="ButtonRed" pixmap="%s/pictures/button_red_%s.png" position="{pos.but_red}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonRedText" position="{pos.but_red}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonGreen" pixmap="%s/pictures/button_green_%s.png" position="{pos.but_green}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonGreenText" position="{pos.but_green}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonYellow" pixmap="%s/pictures/button_yellow_%s.png" position="{pos.but_yellow}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonYellowText" position="{pos.but_yellow}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n            <ePixmap name="ButtonBlue" pixmap="%s/pictures/button_blue_%s.png" position="{pos.but_blue}" size="{size.but}" zPosition="4" transparent="1" alphatest="on"/>\n            <widget render="Label" source= "ButtonBlueText" position="{pos.but_blue}" size="{size.but}" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;%s"/>\n        </screen>' % (self.path, self.used_skin, int('%.0f' % (self.font_size * self.scale_y)), self.path, self.used_skin, int('%.0f' % (self.font_size * self.scale_y)), self.path, self.used_skin, int('%.0f' % (self.font_size * self.scale_y)), self.path, self.used_skin, int('%.0f' % (self.font_size * self.scale_y)))

    def __init__(self, session, used_skin, font_size, scale_y, scale_x):
        self.dict_text = {'title.screen': ('CCcamOscamInfos Select-Cam Ver. %s' % version)}
        self.dict_var = {'size.screen': '610,480', 
           'pos.header': '10,10', 
           'size.header': '590,20', 
           'pos.label1': '10,40', 
           'size.label1': '590,2', 
           'pos.list': '10,50', 
           'size.list': '590,360', 
           'pos.label2': '10,430', 
           'size.label2': '590,2', 
           'size.but': '140,40', 
           'pos.but_red': '10,440', 
           'pos.but_green': '160,440', 
           'pos.but_yellow': '310,440', 
           'pos.but_blue': '460,440'}
        self.session = session
        self.used_skin = used_skin
        self.font_size = font_size
        self.scale_y = scale_y
        self.scale_x = scale_x
        self.skin = SkinVars(CCcamOscamInfoConfigScreen.raw_skin, self.dict_text, self.dict_var)
        Screen.__init__(self, session)
        self['header'] = Menu([])
        self['list'] = Menu([])
        self['ButtonRedText'] = StaticText('New')
        self['ButtonGreenText'] = StaticText('Edit')
        self['ButtonYellowText'] = StaticText('Delete')
        self['ButtonBlueText'] = StaticText('')
        self['actions'] = ActionMap(['CCcamOscamInfoActions'], {'ok': (self.green), 'cancel': (self.close), 'red': (self.red), 'green': (self.green), 'blue': (self.blue), 'yellow': (self.yellow), 'down': (self.down), 'up': (self.up)}, -1)
        self.onLayoutFinish.append(self.makeList)
        return

    def red(self):
        return

    def green(self):
        return

    def yellow(self):
        return

    def blue(self):
        self.close()
        return

    def up(self):
        self[self.currList].up()
        return

    def down(self):
        self[self.currList].down()
        return


def SkinVars(skin, dict_text, dict_var):
    for key in dict_text.keys():
        skin = skin.replace('{' + key + '}', dict_text[key])

    for key in dict_var.keys():
        if used_skin == 'hd':
            skin = skin.replace('{' + key + '}', '%.0f,%.0f' % (float(dict_var[key].split(',')[0]) * scale_x, float(dict_var[key].split(',')[1]) * scale_y))
        else:
            skin = skin.replace('{' + key + '}', dict_var[key])

    return skin


return
