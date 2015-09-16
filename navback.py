import wx
import subprocess
import wx.lib.scrolledpanel
import mm_menus


class TransparentAwareFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        self.transparency = 240
        self.background_color = '#CCCCCC'

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
        panel = wx.lib.scrolledpanel.ScrolledPanel(self,-1, size=(320,display_height),
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
            a = SPanel(panel, -1, curimage, o)

            #a = getattr(self, i)
            a.Show()
            a.register_trigger(self.clear_selection)
            a.regTriggerMsg(o)
            self.section_objects[o] = a

            titleSizer      = wx.BoxSizer(wx.HORIZONTAL)


            titleSizer.Add( a, 0, wx.ALL|wx.EXPAND, 5 )
            bSizer.Add(titleSizer, 0, wx.EXPAND)


        panel.SetSizer( bSizer )
        #bSizer.Fit(self)

    def clear_selection(self, msg):
        for i in self.section_objects.keys():
            if i != msg:
                self.section_objects[i].reset()
        self.listener(msg)
    
    def OnLeftClick(self, e):
        self.refocus_method()

    def registerListener(self, method):
        self.listener = method



class SPanel(wx.Panel):
    def __init__(self, parent, id, iconname, sectitle):
        wx.Panel.__init__(self, parent, id)
        self.background_color_ns = '#888888'
        self.background_color_s = '#444444'
        self.SetSize((300,90))
        self.icon_image        = iconname
        self.parent = parent
        self.sectitle = sectitle
        self.trigger = None
        icon_file = self.icon_image
        self.icon = wx.Image(icon_file, wx.BITMAP_TYPE_ANY)
        self.icon = self.icon.Scale(48, 48, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        self.icon = wx.StaticBitmap(self, -1, self.icon, (15, 15))
        self.text = wx.StaticText(self, -1, self.sectitle, (70, 30))
        self.text.SetForegroundColour((0,0,0))
        spacer = wx.EmptyBitmap( 300, 1 )
        wx.StaticBitmap(self, -1, spacer, (0, 0))
        wx.StaticBitmap(self, -1, spacer, (0, 80))
        self.SetBackgroundColour(self.background_color_ns)

        self.Bind(wx.EVT_LEFT_UP, self.OnLeftClick)
        self.text.Bind(wx.EVT_LEFT_UP, self.OnLeftClick)
        self.icon.Bind(wx.EVT_LEFT_UP, self.OnLeftClick)

    def changeState(self):
        self.text.SetForegroundColour((255,255,255))
        self.SetBackgroundColour(self.background_color_s)

    def reset(self):
        self.text.SetForegroundColour((0,0,0))
        self.SetBackgroundColour(self.background_color_ns)

    def regTriggerMsg(self, msg):
        self.trigger_msg = msg

    def register_trigger(self, trigger):
        self.trigger = trigger

    def OnLeftClick(self, e):
        #print self.trigger_msg
        self.trigger(self.trigger_msg)
        #self.trigger(e.EventObject.sectitle)
        self.changeState()



if __name__ == '__main__':
    wx.SystemOptions.SetOptionInt("msw.staticbitmap.htclient", 1)
    app = wx.App(False)
    style = ( wx.NO_BORDER  )
    back = BackgroundWindow(None, style = style, size=(320, 1000), pos=(0, 60))
    back.transparency = 195
    back.Show()
    app.MainLoop()


