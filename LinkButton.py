__author__ = 'churley'

import wx
from wx.lib.agw.gradientbutton import *

class LinkButton(wx.lib.agw.gradientbutton.GradientButton):


    def __init__(self, *args, **kwargs):
        wx.lib.agw.gradientbutton.GradientButton.__init__(self, *args, **kwargs)

    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` event for L{GradientButton}.

        :param `event`: a `wx.PaintEvent` event to be processed.
        """

        dc = wx.BufferedPaintDC(self)
        gc = wx.GraphicsContext.Create(dc)
        dc.SetBackground(wx.Brush(self.GetParent().GetBackgroundColour()))
        dc.Clear()

        clientRect = self.GetClientRect()
        gradientRect = wx.Rect(*clientRect)
        capture = wx.Window.GetCapture()

        x, y, width, height = clientRect

        gradientRect.SetHeight(gradientRect.GetHeight()/2 + ((capture==self and [1] or [0])[0]))
        if capture != self:
            if self._mouseAction == HOVER:
                topStart, topEnd = self.LightColour(self._topStartColour, 10), self.LightColour(self._topEndColour, 10)
            else:
                topStart, topEnd = self._topStartColour, self._topEndColour

            rc1 = wx.Rect(x, y, width, height/2)
            path1 = self.GetPath(gc, rc1, 8)
            br1 = gc.CreateLinearGradientBrush(x, y, x, y+height/2, topStart, topEnd)
            gc.SetBrush(br1)
            gc.FillPath(path1) #draw main

            path4 = gc.CreatePath()
            path4.AddRectangle(x, y+height/2-8, width, 8)
            path4.CloseSubpath()
            gc.SetBrush(br1)
            gc.FillPath(path4)

        else:

            rc1 = wx.Rect(x, y, width, height)
            path1 = self.GetPath(gc, rc1, 8)
            gc.SetPen(wx.Pen(self._pressedTopColour))
            gc.SetBrush(wx.Brush(self._pressedTopColour))
            gc.FillPath(path1)

        gradientRect.Offset((0, gradientRect.GetHeight()))

        if capture != self:

            if self._mouseAction == HOVER:
                bottomStart, bottomEnd = self.LightColour(self._bottomStartColour, 10), self.LightColour(self._bottomEndColour, 10)
            else:
                bottomStart, bottomEnd = self._bottomStartColour, self._bottomEndColour

            rc3 = wx.Rect(x, y+height/2, width, height/2)
            path3 = self.GetPath(gc, rc3, 8)
            br3 = gc.CreateLinearGradientBrush(x, y+height/2, x, y+height, bottomStart, bottomEnd)
            gc.SetBrush(br3)
            gc.FillPath(path3) #draw main

            path4 = gc.CreatePath()
            path4.AddRectangle(x, y+height/2, width, 8)
            path4.CloseSubpath()
            gc.SetBrush(br3)
            gc.FillPath(path4)

            shadowOffset = 0
        else:

            rc2 = wx.Rect(x+1, gradientRect.height/2, gradientRect.width, gradientRect.height)
            path2 = self.GetPath(gc, rc2, 8)
            gc.SetPen(wx.Pen(self._pressedBottomColour))
            gc.SetBrush(wx.Brush(self._pressedBottomColour))
            gc.FillPath(path2)
            shadowOffset = 1

        font = gc.CreateFont(self.GetFont(), self.GetForegroundColour())
        gc.SetFont(font)

        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        pencolor = (255,255,255)
        gc.SetFont(font, pencolor)

        label = self.GetLabel()
        tw, th = gc.GetTextExtent(label)

        if self._bitmap:
            bw, bh = self._bitmap.GetWidth(), self._bitmap.GetHeight()
        else:
            bw = bh = 0

        pos_x = (width-bw)/2+shadowOffset      # adjust for bitmap and text to centre
        if self._bitmap:
            pos_y =  (height-bh)/2+shadowOffset-20
            gc.DrawBitmap(self._bitmap, pos_x, pos_y, bw, bh) # draw bitmap if available
            pos_x = pos_x + 2   # extra spacing from bitmap

        #gc.DrawText(label, pos_x + bw + shadowOffset, (height-th)/2+shadowOffset)


        #gc.SetPen(wx.Pen(pencolor, 2))
        #colorbrush = wx.Brush(pencolor)
        #gc.SetBrush(colorbrush)

        #gc.SetPen(wx.WHITE_PEN)

        if len(label) <= 25:
            gc.DrawText(label, (width-tw)/2 + shadowOffset, (height-th)/2+shadowOffset+30)
        else:
            temp = label.split()
            ns = ''
            x = 0
            for i in temp:
                ns += i +' '
                x += 1
                if len(ns) > 20:
                    break

            nse = ' '.join(temp[x:])
            print nse
            tw1, th1 = gc.GetTextExtent(ns)
            tw2, th2 = gc.GetTextExtent(nse)
            gc.DrawText(ns, (width-tw1)/2 + shadowOffset, (height-(2*th))/2+shadowOffset+30)
            gc.DrawText(nse, (width-tw2)/2 + shadowOffset, (height-th + 10)/2+shadowOffset+30)



