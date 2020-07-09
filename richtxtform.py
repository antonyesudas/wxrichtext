#------------------------------------
# Application: Rich Text Editor
# Dated: 08-July-2020
# Author: Antony Yesudas
# Description: Sample App demonstrates the Rich Text Editor
#              We can add table with 2 rows and 2 columns inside the Editor. It retrieves the XML output correctly.
#              But cannot retrieve the <table> tag while using the HTMLHandler. Please find a solution.
#------------------------------------


import wx
import wx.richtext as rt
import images
from io import BytesIO

#----------------------------------------------------------------------

class MainPanel(wx.Panel):

    def __init__(self, parent):

        wx.Panel.__init__(self, parent)
        
        # Sizers
        outSizer = wx.BoxSizer(wx.VERTICAL)
        iconSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Bitmap Icons (Bold, Underline, Dialog icon to insert Table)
        self.bmpBold =wx.BitmapButton(self, -1, images._rt_bold.GetBitmap(), wx.DefaultPosition, wx.DefaultSize)
        self.bmpBold.Bind( wx.EVT_BUTTON, self.OnBold);
        iconSizer.Add(self.bmpBold, 0, wx.ALL, 4)
        self.bmpUL =wx.BitmapButton(self, -1, images._rt_underline.GetBitmap(), wx.DefaultPosition, wx.DefaultSize)
        self.bmpUL.Bind( wx.EVT_BUTTON, self.OnUnderLine);
        iconSizer.Add(self.bmpUL, 0, wx.ALL, 4)
        self.bmpRefer =wx.BitmapButton(self, -1, images.dialog.GetBitmap())
        self.bmpRefer.Bind( wx.EVT_BUTTON, self.OnTableCreate);
        iconSizer.Add(self.bmpRefer, 0, wx.ALL, 4)
        outSizer.Add(iconSizer, 0, wx.EXPAND|wx.ALL, 0)
        
        
        # Description Label
        lblDesc = wx.StaticText(self, label=u"Use the above icons to Bold, Underline or Insert Table")
        outSizer.Add(lblDesc, 0, wx.EXPAND|wx.ALL, 4)
        
        # RichText
        self.richEditor = rt.RichTextCtrl(self);
        outSizer.Add(self.richEditor, 1, wx.EXPAND|wx.ALL, 4)
        
        # Button
        self.button = wx.Button(self, -1, "Show Output")
        self.button.Bind(wx.EVT_BUTTON, self.OnOutputResult)
        outSizer.Add(self.button, 0, wx.ALL, 4)
        
        # Description Label
        lblDesc = wx.StaticText(self, label=u"See Result on your Console Screen. \nProblem: HTML Output does not contain the <Table> Tag. \nPlease find a solution. Thanks!", size=wx.Size(-1,50))
        outSizer.Add(lblDesc, 0, wx.EXPAND|wx.ALL, 4)
        
        #Layout
        self.SetSizer(outSizer)
        self.Layout()
        
    def OnBold(self, event):
        "Change the selected text to Bold"
        self.richEditor.ApplyBoldToSelection()
        
    def OnUnderLine(self, event):
        "Change the selected text to Underline"
        self.richEditor.ApplyUnderlineToSelection()

    def OnTableCreate(self, event):
        "Insert the Table with 2 rows and 2 columns"
        self.richEditor.WriteTable(2, 2)
    
    def OnOutputResult(self, event):
        
        if self.richEditor.Value.strip() != "" :
            #Method 1) Output using XMLHandler
            byts = BytesIO()
            handler = wx.richtext.RichTextXMLHandler()
            handler.SaveFile(self.richEditor.GetBuffer(), byts)
            byts.seek(0)
            xmlResult = byts.getvalue().decode('utf-8')
            print(xmlResult)
            
            #Method 2) Output using HTMLHandler
            byts = BytesIO()
            htmhandler = wx.richtext.RichTextHTMLHandler()
            htmhandler.SaveFile(self.richEditor.GetBuffer(), byts)
            htmlResult = byts.getvalue()
            print(htmlResult)
            
        else:
            wx.MessageBox("Please enter some text inside the Editor", "Warning", wx.OK | wx.ICON_EXCLAMATION)

        #PROBLEM: HTML Output does not contain the <Table> Tag. Kindly find a solution.. Thanks!


if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None, title="Rich Text Editor", size=wx.Size(-1,300))
    panel = MainPanel(frame)
    frame.Show()
    app.MainLoop()