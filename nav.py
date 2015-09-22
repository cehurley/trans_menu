import wx
import subprocess
import wx.lib.scrolledpanel
import mm_menus
# from wx.lib.agw import gradientbutton as GB
from CatButton import CatButton
import wx.lib.platebtn as platebtn

class TransparentAwareFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        self.transparency = 240
        self.background_color = '#888888'

    def SetTransparent(self, value):
        self.transparency = value
        wx.Frame.SetTransparent(self, value)

    def GetTransparent(self):
        return self.transparency        

class LeftNav(TransparentAwareFrame):
    def __init__(self, *args, **kwargs):
        data, order = kwargs.pop('data')
        self.background_color = '#CCCCCC'
        TransparentAwareFrame.__init__(self, *args, **kwargs)
        self.SetBackgroundColour(self.background_color)
        self.Show()
        self.SetTransparent(self.GetTransparent())
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftClick)
        self.refocus_method = None
        display_width, display_height = wx.GetDisplaySize()
        panel = wx.lib.scrolledpanel.ScrolledPanel(self,-1, size=(200,display_height),
                                                   pos=(0,0),
                                                   style=(wx.NO_BORDER | wx.EXPAND | wx.ALL)
                                                   )
        panel.SetupScrolling()
        panel.SetBackgroundColour(self.background_color)
        self.SetTransparent(240)

        bSizer = wx.BoxSizer( wx.VERTICAL )
        self.section_objects = {}

        for o in order:
            print o
            i = data[o]['icon']
            curimage = mm_menus.clean_cat_path(i)
            #icon = wx.Image(curimage, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            icon = wx.Image(curimage, wx.BITMAP_TYPE_ANY)
            icon = icon.Scale(32, 32, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
            #icon = wx.Image(curimage, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            #a = GB.GradientButton(panel, -1, icon, o, size = (150,40))
            a = CatButton(panel, -1, icon, o, size = (190,40))
            font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
            pencolor = (255,255,255)
            a.SetFont(font)
            self.Bind(wx.EVT_BUTTON, self.OnButton, a)
            a.Show()
            self.section_objects[o] = a
            titleSizer      = wx.BoxSizer(wx.HORIZONTAL)
            titleSizer.Add( a, 0, wx.ALL|wx.EXPAND, 5 )
            bSizer.Add(titleSizer, 0, wx.EXPAND)


        panel.SetSizer( bSizer )
        

    def OnButton(self, event):
        obj = event.GetEventObject()
        self.listener(obj.GetLabel())
        #self.log.write("You clicked %s\n"%obj.GetLabel())    

    
    def OnLeftClick(self, e):
        self.refocus_method()

    def registerListener(self, method):
        self.listener = method






if __name__ == '__main__':
    wx.SystemOptions.SetOptionInt("msw.staticbitmap.htclient", 1)
    app = wx.App(False)
    style = ( wx.NO_BORDER  )
    back = BackgroundWindow(None, style = style, size=(320, 1000), pos=(0, 60))
    back.transparency = 195
    back.Show()
    app.MainLoop()


