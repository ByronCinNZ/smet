"""
InfoView -- SMET

A view for displaying (and editing) highly structured data communicated in XML.
Inspired by METlite and GeoNetwork.
"""
import wx
from wx.lib import stattext
from pythonutils import OrderedDict

data = OrderedDict()
data['Title'] = "InfoView"
data['Component of'] = "SMET"
data['Status'] = "Cool"
data['Some Label'] = "A value"
data['Developer'] = dev = OrderedDict()
dev['Type'] = "Company"
dev['Name'] = "Cochrane Open Geospatial Solutions"
dev['Founder/leader'] = "Byron Cochrane"
dev['First Employee'] = "Adrian Cochrane"
data['Another label'] = "Another Value"

class InfoView(wx.Panel):
	def __init__(self, *args, **kwargs):
		wx.Panel.__init__(self, *args, **kwargs)
		self.SetBackgroundColour("white")
		self.Bind(wx.EVT_PAINT, self.onPaint)

		self.labelFont = wx.Font(12, wx.SWISS, wx.ITALIC, wx.BOLD)
		self.valueFont = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, underline=True)
		self.valueFont.SetUnderlined(True)

		self.sizer = wx.GridBagSizer(hgap=5, vgap=5)
		self.sizer.AddGrowableCol(2)
		self.row = 0

		# activate sizer
		self.SetSizer(self.sizer)
		self.sizer.Fit(self)
		self.sizer.SetSizeHints(self)

	def onPaint(self, evt):
		dc = wx.PaintDC(self)
		dc.SetPen(wx.Pen("blue", 2))
		dc.DrawLine(8,0, 8,self.GetSize()[1])

	def addTextRow(self, label, value):
		labelText = wx.StaticText(self, -1, str(label)+": ")
		labelText.SetFont(self.labelFont)
		valueText = stattext.GenStaticText(self, -1, str(value))
		valueText.SetFont(self.valueFont)

		self.sizer.Add(labelText, (self.row, 1), flag=wx.ALIGN_CENTER_VERTICAL)
		self.sizer.Add(valueText, (self.row, 2))

		self.row += 1

	def addInfoRow(self, label, value):
		labelText = wx.StaticText(self, -1, str(label)+": ")
		labelText.SetFont(self.labelFont)
		valueView = InfoView(self, -1)
		valueView.showDict(value)
		
		self.sizer.Add(labelText, (self.row, 1), flag=wx.ALIGN_CENTER_VERTICAL)
		self.row += 1
		self.sizer.Add(valueView, (self.row, 1), (valueView.row + 1,2), wx.EXPAND, 5)
		self.row += valueView.row + 1

	def addRow(self, label, value):
		if isinstance(value, OrderedDict): self.addInfoRow(label, value)
		else: self.addTextRow(label, value)

	def showDict(self, dict_):
		for key, value in dict_.items():
			self.addRow(key, value)

if __name__ == '__main__':
	app = wx.PySimpleApp()
	frame = wx.Frame(parent=None, title='InfoView')
	info = InfoView(frame, -1)
	info.showDict(data)
	frame.Show()
	app.MainLoop()
