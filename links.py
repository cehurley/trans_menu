import wx
import wx.lib.scrolledpanel
import mm_menus
from LinkButton import LinkButton

class TransparentAwareFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        self.transparency = 250
        self.background_color = '#888888'

    def SetTransparent(self, value):
        self.transparency = value
        wx.Frame.SetTransparent(self, value)

    def GetTransparent(self):
        return self.transparency        

class LinkBox(TransparentAwareFrame):
    def __init__(self, *args, **kwargs):
        links = kwargs.pop('links')
        trans = kwargs.pop('trans')
        self.settings = kwargs.pop('settings')
        self.mode, self.width = kwargs.pop('mode')
        TransparentAwareFrame.__init__(self, *args, **kwargs)
        self.SetBackgroundColour(self.background_color)
        
        self.SetTransparent(self.GetTransparent())
        
        display_width, display_height = wx.GetDisplaySize()
        
        self.SetTransparent(trans)
        self.triggers = {}
        self.section_objects = {}
        row_size = self.mode
        x,y = 10,10
        curnum = 0
        total = 0
        for o in links:
            print o['title']
            i = o['icon']
            curimage = mm_menus.clean_cat_path(i)
            icon = wx.Image(curimage, wx.BITMAP_TYPE_ANY)
            icon = icon.Scale(64, 64, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
            t = o['title']
            #a = GB.GradientButton(self, -1, icon, t, size=(250,72), pos=(x,y), style=wx.DEFAULT)
            a = LinkButton(self, -1, icon, t,
                           size=(self.settings.BUTTONWIDTH,self.settings.BUTTONHEIGHT),
                           pos=(x,y),
                           style=wx.DEFAULT,
                           settings = self.settings)
            self.Bind(wx.EVT_BUTTON, self.OnButton, a)
            
            a.Show()
            self.triggers[t]=o['command']
            
            x+=self.settings.BUTTONWIDTH+self.settings.BUTTONMARGIN
            #titleSizer.Add( a, 0, wx.ALL, 5 )
            curnum += 1
            total += 1
            if curnum == row_size:
                y+=self.settings.BUTTONHEIGHT+self.settings.BUTTONMARGIN
                x = self.settings.BUTTONMARGIN
                #bSizer.Add(titleSizer, 0, wx.EXPAND)
                #titleSizer      = wx.BoxSizer(wx.HORIZONTAL)
                curnum = 0
        #if curnum > 0:
            #bSizer.Add(titleSizer, 0, wx.EXPAND)
            
        if y == self.settings.BUTTONMARGIN:
            y = self.settings.BUTTONHEIGHT+self.settings.BUTTONMARGIN
        if curnum > 0 and total%self.mode > 0 and total > 3:
            y+=self.settings.BUTTONHEIGHT+(self.settings.BUTTONMARGIN*2)
        if total < self.mode:
            self.width = (self.settings.BUTTONWIDTH*total)+(self.settings.BUTTONMARGIN*(total+1))
            y+=self.settings.BUTTONMARGIN
        self.SetSize((self.width,y))
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


