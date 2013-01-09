"""
InfoView -- SMET

A view for displaying (and editing) highly structured data communicated in XML.
Inspired by METlite and GeoNetwork.
"""
import wx
from wx.lib import stattext, scrolledpanel
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
		data = kwargs.pop('data', ())
		wx.Panel.__init__(self, *args, **kwargs)
		self.SetBackgroundColour("white")
		self.Bind(wx.EVT_PAINT, self.onPaint)

		self.labelFont = wx.Font(12, wx.SWISS, wx.ITALIC, wx.BOLD)
		self.valueFont = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, underline=True)
		self.valueFont.SetUnderlined(True)

		self.sizer = wx.GridBagSizer(hgap=5, vgap=5)
		self.sizer.AddGrowableCol(2)
		self.row = 0

		self.showValue(data)

		# activate sizer
		self.SetSizer(self.sizer)
		self.sizer.Fit(self)
		self.sizer.SetSizeHints(self)
		self.FitInside()

	def onPaint(self, evt):
		dc = wx.PaintDC(self)
		dc.SetPen(wx.Pen("blue", 2))
		dc.DrawLine(8,0, 8,self.GetSize()[1])

	def showValue(self, val):
		for data in types.get(type(val).__name__, lambda a:val)(val):
			self.addTextInfoRow(*data)

	def addTextInfoRow(self, label, value, info):
		labelText = wx.StaticText(self, -1, str(label)+": " if label else "")
		labelText.SetFont(self.labelFont)
		valueText = stattext.GenStaticText(self, -1, str(value) if value else "") # Necessary for underline
		valueText.SetFont(self.valueFont)
		if info:
			valueView = InfoView(self, -1, data=info)

		self.sizer.Add(labelText, (self.row, 1), flag=wx.ALIGN_CENTER_VERTICAL)
		self.sizer.Add(valueText, (self.row, 2))
		self.row += 1
		if info:
			self.sizer.Add(valueView, (self.row, 1), (valueView.row,2), wx.EXPAND, 5)
			self.row += valueView.row

#--
types = {}
def key(key, dict_=types):
	def inner(value): 
		dict_[key] = value
		return value
	return inner

@key('str')
@key('int')
def _(string):
	yield "Message", string, None


@key('OrderedDict')
def _(dict_):
	for key, value in dict_.items():
		yield (key, "", value) if type(value).__name__ in types else (key, value, None)

@key('_Element')
@key('Element')
def _(xml):
	def iterator(el):
		for child in el:
			yield tag(child)
			if child.tail:
				yield "", child.tail, None
	tag = lambda tag: (tag.tag, tag.text, iterator(tag) if len(tag) else None)
	yield tag(xml)

@key('list')
@key('tuple')
def _(iter_):
	for child in iter_:
		yield "", "", child

if __name__ == '__main__':
	from xml.etree.ElementTree import XML
	app = wx.PySimpleApp()

	frame = wx.Frame(parent=None, title='InfoView')

	data_ = data, "Hello World!", XML('<html><head><title>...</title>...</head><body>...</body></html>')
	# Setup a data selection menu
	def switchDisplay(data):
		def inner(evt):
			global info
			info.Destroy()
			info = InfoView(scroll, -1, data=data)
			scroll.SetScrollbars(1,1, *info.GetSize())
		return inner

	menuBar = wx.MenuBar()
	menu = wx.Menu()
	frame.Bind(wx.EVT_MENU, switchDisplay(data_), menu.AppendRadioItem(-1, "tuple"))
	frame.Bind(wx.EVT_MENU, switchDisplay(data_[0]), menu.AppendRadioItem(-1, "OrderedDictionary"))
	frame.Bind(wx.EVT_MENU, switchDisplay(data_[1]), menu.AppendRadioItem(-1, "str"))
	frame.Bind(wx.EVT_MENU, switchDisplay(data_[2]), menu.AppendRadioItem(-1, "XML"))
	menuBar.Append(menu, "Data")
	frame.SetMenuBar(menuBar)


	scroll = wx.ScrolledWindow(frame, -1)
	info = InfoView(scroll, -1)
	scroll.SetScrollbars(1,1, *info.GetSize())

	frame.Show()

	app.MainLoop()
