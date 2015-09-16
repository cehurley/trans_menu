__author__ = 'churley'

import wx
import mm_menus
import subprocess
from nav import LeftNav
from links import LinkBox


class TransMenu(object):

    def __init__(self):
        self.app = None
        self.vert_buffer = 10
        self.cats = {}
        self.cat_tree, self.cat_order = mm_menus.getAll()
        self.link_objects    = []
        self.width_sub = 560
        self.trans = 250
        self.mode = 5

    def boot(self):
        wx.SystemOptions.SetOptionInt("msw.staticbitmap.htclient", 1)
        self.app = wx.App(False)
        self.data = mm_menus.getAll()
        style = ( wx.NO_BORDER )
        display_width, display_height = wx.GetDisplaySize()
        self.back = LeftNav(None, style = style, pos=(0, 0),size=(180, display_height), data= self.data)
        self.back.registerListener(self.change_category)
        self.app.MainLoop()

    def setMode(self, mode, trans):
        self.mode = mode
        if mode == 4:
            self.width_sub = 360
        elif mode == 3:
            self.width_sub = 525
        self.trans = trans

    def change_category(self, msg):
        self.clear_selection(msg)
        style = ( wx.NO_BORDER )
        if hasattr(self, 'drilldown') == True:
            self.drilldown.Destroy()
        display_width, display_height = wx.GetDisplaySize()
        self.drilldown = LinkBox(None, style = style, pos=(200, 20), size=(800,500),
                                 links=self.cat_tree[msg]['items'], mode=(self.mode, self.width_sub),
                                 trans=self.trans) #size=(600, display_height),size=(display_width-self.width_sub, display_height),
        self.drilldown.SetTransparent(self.trans)
        self.drilldown.registerListener(self.launch_app)



    def launch_app(self, command):
        if '%' in command:
            command = command[:command.index('%')]
            subprocess.Popen([command], shell=True)
        else:
            subprocess.Popen([command], shell=True)

    def clear_selection(self, msg):
        pass




if __name__ == '__main__':
    d = TransMenu()
    #set Mode num columns, transparency
    d.setMode(3,245)
    d.boot()