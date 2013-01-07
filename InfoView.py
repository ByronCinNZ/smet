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

	def showIterator(self, iter_):
		while iter_.hasNext():
			iter_.next()
			self.addTextInfoRow(iter_.getLabel(), iter_.getValue(), iter_.getChildren())

	def addTextInfoRow(self, label, value, info):
		labelText = wx.StaticText(self, -1, str(label)+": ")
		labelText.SetFont(self.labelFont)
		valueText = stattext.GenStaticText(self, -1, str(value)) # Necessary for underline
		valueText.SetFont(self.valueFont)
		if info:
			valueView = InfoView(self, -1)
			valueView.showIterator(info)

		self.sizer.Add(labelText, (self.row, 1), flag=wx.ALIGN_CENTER_VERTICAL)
		self.sizer.Add(valueText, (self.row, 2))
		self.row += 1
		if info:
			self.sizer.Add(valueView, (self.row, 1), (valueView.row + 1,2), wx.EXPAND, 5)
			self.row += valueView.row + 1

#--

class  StringIterator(object):
    
    def __init__(self, string):
        self.string = string
        self.index = True
        
    def hasNext(self):
        return self.index
    
    def next(self):
        self.index = False
    
    def getChildren(self):
        return None
    
    def getLabel(self):
        return "Message"
    
    def getValue(self):
        return self.string
    
class DictIterator(object):
    from pythonutils import OrderedDict
        
    def __init__(self, dict):
        self.dict = dict
        self.index = 0
        
    def hasNext(self):
        index = self.index + 1
        if index >= len(self.dict) or not self.dict.keys()[index]:
            return False
    
        return True
    
    def next(self):
        self.index += 1
    
    def getChildren(self):
        child = self.dict.values()[self.index]
        if type(child).__name__ == 'OrderedDict':
           return DictIterator(child) 
            
        return None
    
    def getLabel(self):
        keys = self.dict.keys()
        return keys[self.index]
    
    def getValue(self):
        child = self.dict.values()[self.index]
        if not type(child).__name__ == 'OrderedDict':
           return child
        return ""
'''   
class XmlIterator(object):
    
    def __init__(self, xml):
        self.xml = xml
        self.index = 0
        
    def hasNext(self):
        index = self.index + 1
        if index >= len(self.xml) or not self.xml.getchildren()[index]:
            return False
    
        return True
    
    def next(self):
        self.index += 1
    
    def getChildren(self):
        child = self.xml.getchildren()[self.index]
        if not child:
            return None
        return xmlIterator(child) 
    
    def getLabel(self):
        return self.xml.tag
    
    def getValue(self):
        return self.xml.text
'''
class _XmlSeqIterator(object):
	"""Private iterator for iterator over a sequence of elements."""
	def __init__(self, xml):
		self.xml, self.index = xml, 0

	def hasNext(self):
		index = self.index + 1
		return index < len(self.xml)

	def next(self):
		self.index += 1

	def getChildren(self):
		return _XmlSeqIterator(self.xml[self.index]) if self.xml[self.index] else None

	def getLabel(self):
		return self.xml[self.index].tag

	def getValue(self):
		return self.xml.text

def XmlIterator(xml):
	return _XmlSeqIterator((xml,))

if __name__ == '__main__':
	from xml.etree.ElementTree import XML
	app = wx.PySimpleApp()

	frame = wx.Frame(parent=None, title='InfoView')
	info = InfoView(frame, -1)
	info.showIterator(DictIterator(data))
	frame.Show()

	textFrame = wx.Frame(None, title="HelloWorld!")
	info = InfoView(textFrame, -1)
	info.showIterator(StringIterator("Hello World!"))
	textFrame.Show()

	xmlFrame = wx.Frame(None, title="Basic HTML")
	info = InfoView(xmlFrame, -1)
	info.showIterator(XmlIterator(XML('<html><head>...<title>...</title></head><body>...</body></html>')))
	xmlFrame.Show()

	app.MainLoop()
