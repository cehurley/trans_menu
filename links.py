import wx
import subprocess
import wx.lib.scrolledpanel
import mm_menus
from wx.lib.agw import gradientbutton as GB
import wx.lib.platebtn as platebtn

class TransparentAwareFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        self.transparency = 250
        self.background_color = '#444444'

    def SetTransparent(self, value):
        self.transparency = value
        wx.Frame.SetTransparent(self, value)

    def GetTransparent(self):
        return self.transparency        

class LinkBox(TransparentAwareFrame):
    def __init__(self, *args, **kwargs):
        links = kwargs.pop('links')
        trans = kwargs.pop('trans')
        self.mode, self.width_sub = kwargs.pop('mode')
        TransparentAwareFrame.__init__(self, *args, **kwargs)
        #self.SetBackgroundColour(self.background_color)
        
        self.SetTransparent(self.GetTransparent())
        
        display_width, display_height = wx.GetDisplaySize()
        
        self.SetTransparent(trans)
        self.triggers = {}
        #bSizer = wx.BoxSizer( wx.VERTICAL )
        #titleSizer      = wx.BoxSizer(wx.HORIZONTAL)
        self.section_objects = {}
        row_size = self.mode
        x,y = 10,10
        curnum = 0
        for o in links:
            print 'pfdsfsdfsfsdfsfsdfsdfsdfsdfsdfsdfsdfsfd'
            print o
            i = o['icon']
            curimage = mm_menus.clean_cat_path(i)
            icon = wx.Image(curimage, wx.BITMAP_TYPE_ANY)
            icon = icon.Scale(52, 52, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
            t = o['title']
            a = GB.GradientButton(self, -1, icon, t, size=(250,72), pos=(x,y), style=wx.DEFAULT)
            self.Bind(wx.EVT_BUTTON, self.OnButton, a)
            
            a.Show()
            self.triggers[t]=o['command']
            
            x+=260
            #titleSizer.Add( a, 0, wx.ALL, 5 )
            curnum += 1
            if curnum == row_size:
                y+=80
                x = 10
                #bSizer.Add(titleSizer, 0, wx.EXPAND)
                #titleSizer      = wx.BoxSizer(wx.HORIZONTAL)
                curnum = 0
        #if curnum > 0:
            #bSizer.Add(titleSizer, 0, wx.EXPAND)
            
        if y == 10:
            y = 82
        self.SetSize((800,y))
        self.Show()
        #self.SetSizer( bSizer )
        #bSizer.Fit(self)
        
        


    def OnButton(self, event):
        obj = event.GetEventObject()
        self.listener(self.triggers[obj.GetLabel()])

    
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


