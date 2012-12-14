
# -*- coding: iso-8859-1 -*-
# smet version 0.1 -Spatial Metadata Extraction tool -Byron Cochrane 14,Sept,2007
#      version 0.3 -Spatial Metadata Extraction Tool -Byron Cochrane 17, Oct 2008

import wx, wx.gizmos, os, urllib2, urllib, dircache, webbrowser, MetadataRecord as MDR, GeoObject as GO
from lxml import etree 
#import wx.lib.agw.hyperlink as hl

if wx.Platform == '__WXMSW__':
    import wx.lib.iewin as iewin
    

#--------------------------------------------------------------------


#---MyFrame---#000000#FFFFFF----------------------------------------------------
#---window object---------------

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__

        self.path = ''
        self.dlg = ''
        self.fc = ''
        cdir = os.getcwd()
        con = MDR.GNConnection().getSettings(cdir)
        
 
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        kwds["size"] =(900,500)
        wx.Frame.__init__(self, *args, **kwds)
        self.controller = MyControls(self)
        
        self.bkgnd = wx.Panel(self, -1)
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText("Statusbar")
        #--Layout------
##        self.contents = wx.gizmos.TreeListCtrl(self.bkgnd, -1, style=wx.TR_HIDE_ROOT|wx.TR_ROW_LINES)
##        self.contents.AddColumn('property')
##        self.contents.AddColumn('description')
##        self.contents.SetMainColumn(0)
##        self.dataRoot = self.contents.AddRoot("root")
##        self.contents.Expand(self.dataRoot)
##        self.contents.SetColumnWidth(0, 200)
##        self.contents.SetColumnWidth(1, 400)
        self.contents = wx.TextCtrl(self.bkgnd, -1, "", style=wx.TE_MULTILINE)

        self.tree_ctrl = wx.TreeCtrl(self.bkgnd, -1, style=wx.TR_TWIST_BUTTONS|wx.TR_LINES_AT_ROOT|wx.TR_DEFAULT_STYLE|wx.SUNKEN_BORDER,size=(200,300))
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.controller.xtrct, self.tree_ctrl)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.controller.OnItemSelected, self.tree_ctrl)
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnRightUp, self.tree_ctrl)
        #self.Bind(wx.EVT_CLOSE, MDR.GNConnection.closeDB())
        #---Icons -------default images here
        isz = (16,16)
        il = wx.ImageList(isz[0], isz[1])
        self.idx = {}
        self.idx['fldr']     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, isz))
        self.idx['fldropen'] = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN,   wx.ART_OTHER, isz))
        self.idx['file']     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_LIST_VIEW, wx.ART_OTHER, isz))
        self.idx['img']      = il.Add(wx.ArtProvider_GetBitmap(wx.ART_MISSING_IMAGE, wx.ART_OTHER, isz))
        self.idx['gdb']      = il.Add(wx.ArtProvider_GetBitmap(wx.ART_HARDDISK, wx.ART_OTHER, isz))
        self.tree_ctrl.SetImageList(il)
        self.il = il

        #---Toolbar section---#move new method MyFrame.ToolBar
        self.ToolBar()
        
        self.__set_properties()
        self.__do_layout()
        
        # end wxGlade
        
        # register the self.onExpand function to be called
        wx.EVT_TREE_ITEM_EXPANDING(self.tree_ctrl, self.tree_ctrl.GetId(), self.onExpand)


    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("Spatial Metadata Extractor Tool")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        
        hbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.tb, proportion=0, border=5)
        self.vbox.Add(self.tree_ctrl, proportion=0, flag=wx.EXPAND|wx.FIXED_MINSIZE|wx.TR_HAS_BUTTONS, border=7)
        self.vbox.Add(self.contents, proportion=1, flag=wx.EXPAND|wx.ALL, border=5)
        hbox.Add(self.vbox, proportion=1, flag=wx.EXPAND|wx.ALL, border=5)
        self.bkgnd.SetSizer(self.vbox)
        self.Layout()
        # end wxGlade
        
        
    def postMessage(self, message, clr=0):
##        if clr==0:
##            self.contents.DeleteChildren(self.dataRoot)
##
##        if type(message).__name__ == 'str':
##            data = stringIterator(message)
##        elif type(message).__name__ == 'OrderedDict':
##            data = dictIterator(message)
##        elif type(message).__name__ == "_Element":
##            data = xmlIterator(message)
##
##        self.extendData(data, self.dataRoot)

        def prettyDict(dict, indent=0):
            rep = ''
            for key, value in dict.items():
                rep += ('\t' * indent) + key + ":\t"
                if type(value).__name__ == 'OrderedDict':
                    rep += '\n' + prettyDict(value, indent+1) + '\n'
                else: rep += str(value) + '\n'
            return rep

        if clr:
            self.contents.SetValue("")
        
        print "before if:", message
        print type(message).__name__
        if type(message).__name__ ==  '_Element':
            message = etree.tostring(message)
        elif type(message).__name__ == 'OrderedDict':
            message = prettyDict(message)
        else:
            message = str(message)
        print message
            
        self.contents.AppendText(message)
            
        
        
    def extendData(self, content, parent):
        
        while content.hasNext():
            content.Next()
            newItem = self.contents.AppendItem(parent, content.getLabel())
            self.contents.SetItemText(newItem, str(content.getValue()), 1)
            if content.getImage():
                self.contents.SetItemImage(newItem, content.getImage(), wx.TreeItem_Normal)
            if content.getChildren():
                self.extendData(content.getChildren(), newItem)
            
            
    
    def postHTML(self, page):
        upstr = 'http://' + MDR.GNConnection.GNServer + "/geonetwork/srv/en/user.login?username=" + self.controller.user + "&password=" + self.controller.pword
        login = webbrowser.open(upstr)        
        webbrowser.open(page)
        
##        self.ie = iewin.IEHtmlWindow(self.bkgnd,  wx.ID_ANY, pos=wx.Point(150, 100), size=wx.Size(300, 300), style=0, name='IEHtmlWindow')
##        
##        self.vbox.Add(self.ie,proportion=1, flag=wx.EXPAND|wx.ALL, border=5)
##        self.bkgnd.SetSizer(self.vbox)
##
##        self.ie.LoadUrl(page)
##    
    
    def ToolBar(self):

            
        tsize = (24,24)
        
        folder_bmp = wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_TOOLBAR, tsize)
        self.tb = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TAB_TRAVERSAL)
        
        self.tb.AddLabelTool(20, "Select", folder_bmp, shortHelp="Select", longHelp="Select root directory")
        self.Bind(wx.EVT_TOOL, self.controller.getRootDir, id=20)
        
        self.tb.AddSeparator()
        
        self.filename = wx.TextCtrl(self.tb, -1, size=(200,-1), style=wx.TE_LEFT | wx.TB_NOICONS | wx.TE_PROCESS_ENTER)
        self.tb.AddControl(self.filename)
       #self.filename.SetValue(MDR.GNConnection.rootDir)
        self.Bind(wx.EVT_TEXT_ENTER, self.controller.getRootDir, self.filename)
        self.buildTree()

        self.tb.AddSeparator()
        
        self.tb.SetToolBitmapSize(tsize)
        


        # This combobox is created with no values initially.
        #samplelist = ["  --- Template List ---                           "]
        self.cb = wx.Choice(self.tb, -1, size=(200, -1))
        self.Bind(wx.EVT_CHOICE, self.tmpltChoice, self.cb) 
        self.cb.Append("Template List - Please log in", None)
        self.cb.Select(0)
        self.tmpltXML = None
        
        
        
        self.tb.AddControl(self.cb)
        
        self.loginControls = ()

        self.tb.Realize()
        self.loginTB()
        
        
    def loginTB(self):
        
        for control in self.loginControls:
            id = control.GetId()
            self.tb.RemoveTool(id)
        pacetxt = 10*" " + "Username :  "
        
        self.utext = wx.StaticText(self.tb, -1, pacetxt, pos=wx.Point(800,-1), style=wx.ALIGN_RIGHT)
        self.tb.AddControl(self.utext)   
        self.userbox = wx.TextCtrl(self.tb, 34, size=(50,-1))
        self.userbox.SetHelpText("Enter your GeoNetwork User Name Here")
        self.tb.AddControl(self.userbox)
        
        
        ptext = wx.StaticText(self.tb, -1, "  Password : ", style=wx.ALIGN_RIGHT) 
        self.tb.AddControl(ptext)   
        self.passwordbox = wx.TextCtrl(self.tb, 35, size=(50,-1), style=wx.TE_PASSWORD )
        self.passwordbox.SetHelpText("Enter your GeoNetwork Password Here")
        self.Bind(wx.EVT_TEXT_ENTER, self.loginButton, self.passwordbox)
        self.tb.AddControl(self.passwordbox)
        self.tb.AddSeparator()
        
        self.libttn = wx.Button(self.tb, 36, "Log In", (120, -1))
        self.Bind(wx.EVT_BUTTON, self.loginButton, self.libttn)
        self.tb.AddControl(self.libttn)
        
        self.loginControls = (self.userbox, ptext, self.passwordbox, self.libttn)
        self.tb.Realize()


    def logoutTB(self):
        for control in self.loginControls:
            id = control.GetId()
            self.tb.RemoveTool(id)
            
        pacetxt = 20*" " + self.controller.user + 20*" "
        itext = wx.StaticText(self.tb, -1, pacetxt, style=wx.ALIGN_RIGHT)
        self.tb.AddControl(itext)
        self.tb.AddSeparator()
        self.lobttn = wx.Button(self.tb, 36, " Log Out ", (120, -1))
        self.Bind(wx.EVT_BUTTON, self.controller.logout, self.lobttn)
        self.tb.AddControl(self.lobttn)
        self.tb.Realize()
        
        self.loginControls = (self.utext, itext, self.lobttn)
        
        
    def OnRightUp(self, event):
        self.currentItem = event.GetItem()
        id = event.GetItem()
        menu = wx.Menu()
        self.item1 = menu.Append(-1, "Display")
        self.item2 = menu.Append(wx.ID_ANY, "Merge")
        self.item3 = menu.Append(wx.ID_ANY, "Submit")
        #self.item4 = menu.Append(wx.ID_ANY, "Make root dir") # needs separation in controller.getRootDir
        self.Bind(wx.EVT_MENU, self.controller.xtrct, self.item1)
        self.Bind(wx.EVT_MENU, self.controller.merge, self.item2)
        self.Bind(wx.EVT_MENU, self.controller.submitGN, self.item3)
        #self.Bind(wx.EVT_MENU, self.buildTree, self.item4)
        
        self.PopupMenu(menu)
        menu.Destroy()


    def popTmpltList(self, keys):
        self.cb.Clear()
        self.cb.Append("Select Template", None)
        for item in keys:
            self.cb.Append(item, item.upper())
        self.cb.Select(0)
        

    def tmpltChoice(self, event):
        
        if self.cb.GetSelection():
            selString = self.cb.GetString(self.cb.GetSelection())
            selId = self.controller.tmpltList[selString]        
            self.tmpltXML = MDR.metadataRecord().getTemplateMDRecord(self.controller.user, self.controller.pword, selId)        
            self.postMessage(self.tmpltXML, 1)
        

        
    def onExpand(self, event):
        '''onExpand is called when the user expands a node on the tree
        object. It checks whether the node has been previously expanded. If
        not, the extendTree function is called to build out the node, which
        is then marked as expanded.'''
        
        # get the wxID of the entry to expand and check it's validity
        itemID = event.GetItem()
        #prin itemID
        if not itemID.IsOk():
            itemID = self.tree_ctrl.GetSelection()
            
        # only build that tree if not previously expanded
        old_pydata = self.tree_ctrl.GetPyData(itemID)

        if old_pydata[3] == False:
            # clean the subtree and rebuild it
            self.tree_ctrl.DeleteChildren(itemID)
            self.extendTree(itemID)
            self.tree_ctrl.SetPyData(itemID,(old_pydata[0], old_pydata[1], old_pydata[2], True))
            




    def buildTree(self):
        
        self.statusbar.SetStatusText("Loading......")
        if self.filename.GetValue():
            self.tree_ctrl.DeleteAllItems()
            rDir = self.filename.GetValue()  
            self.rootID = self.tree_ctrl.AddRoot(rDir)
            self.tree_ctrl.SetPyData(self.rootID, (rDir, rDir, rDir, 1))
            print rDir
            self.extendTree(self.rootID)
            self.tree_ctrl.Expand(self.rootID)
        else:
            pass
        self.statusbar.SetStatusText("Status Bar")
        
        
    def extendTree(self, parentID):
        '''extendTree is a semi-lazy directory tree builder. It takes
        the ID of a tree entry and fills in the tree with its child
        subdirectories and their children - updating 2 layers of the
        tree. This function is called by buildTree and onExpand methods'''
        #from osgeo import gdal
        
        '''This is something to work around, because Windows will list
        this directory but throw a WindowsError exception if you
        try to use the listdir() command on it. I need a better workaround
        for this...this is a temporary kludge.'''
        excludeDirs=["c:\\System Volume Information","/System Volume Information","C:\System Volume Information"]
        
        statxt = "Extending Tree"
        self.statusbar.SetStatusText(statxt)
        
        # retrieve the associated absolute path of the parent
        parentDir = self.tree_ctrl.GetPyData(parentID)[1]
        print parentDir
        # Check for geodata type to assign the proper Icons
        datatype, idx1, idx2 = GO.util.getFileType(str(parentDir))
        
        #record = datatype(str(parentDir))
        
        # check if geodatabase and add layers to tree
        # doubleclick to extract does not work for now
        ## util could return "what are the sublayers" 'subdirs' and not need this 'if'
        #if record.DataType == "Geodata collection" and os.path.isfile(parentDir):
        if datatype == GO.Directory and os.path.isfile(parentDir):
            record = datatype(str(parentDir))
            statxt += "."
            self.statusbar.SetStatusText(statxt)
            subdirs = []
            dataset = record.subLayers
            for item, value in  dataset.iteritems():
                statxt += "."
                self.statusbar.SetStatusText(statxt)
                icon1 = self.idx[idx1]
                icon2 = self.idx[idx2]
                pdata = [dataset, item, item, False]
                childID = self.tree_ctrl.AppendItem(parentID, item, icon1, icon2)
                self.tree_ctrl.SetPyData(childID, pdata)
                
        # For all other non Geodatabase geodata
        else:
            subdirs = dircache.listdir(parentDir)
            subdirs.sort()
            for child in subdirs:
                statxt += "."
                self.statusbar.SetStatusText(statxt)
                child_path = os.path.join(parentDir,child)
                rname, ext = os.path.splitext(child)
                ##is this checking for folder?
                if not os.path.islink(child):
                    icon1, icon2 = self.idx['fldr'], self.idx['fldropen']
                    if child_path in excludeDirs:
                        continue  # (aka skip )         
                    
                    datatype, idx1, idx2 = GO.util.getFileType(str(child_path))

                    if datatype:
                        icon1 = self.idx[idx1]
                        icon2 = self.idx[idx2]
                        #record = datatype(str(child_path))
                        
                        pdata = [child, child_path, child_path, False]
                        
                        # add the child to the parent                        
                        childID = self.tree_ctrl.AppendItem(parentID, child, icon1, icon2)
                        
                        # associate the full child path with its tree entry
                        self.tree_ctrl.SetPyData(childID, pdata)
                        
                        # Now the child entry will show up, but it current has no
                        # known children of its own and will not have a '+' showing
                        # that it can be expanded to step further down the tree.
                        # Solution is to go ahead and register the child's children,
                        # meaning the grandchildren of the original parent
                        try:
                            newParent = child
                            newParentID = childID
                            newParentPath = child_path
                            ## util could return "what are the sublayers and not need this 'if'
                            #if record.DataType == "Geodata collection" and os.path.isfile(parentDir):
                            if datatype == GO.Directory and os.path.isfile(parentDir):
                                record = datatype(str(parentDir))
                                statxt += "."
                                self.statusbar.SetStatusText(statxt)
                                dataset = record.subLayers
                                for grandchild, value in  dataset.iteritems():
                                    grandchild_path = os.path.join(newParentPath,grandchild)
                                    pdata = [grandchild, grandchild_path, grandchild_path, False]                      
                                    grandchildID = self.tree_ctrl.AppendItem(newParentID, grandchild)
                                    self.tree_ctrl.SetPyData(grandchildID, pdata)
                                    break

                                
                            else:
                                statxt += "."
                                self.statusbar.SetStatusText(statxt)
                                newsubdirs = dircache.listdir(str(newParentPath))
                                for grandchild in newsubdirs:
                                    grandchild_path = os.path.join(newParentPath,grandchild)
                                    
                                    if not os.path.islink(grandchild_path): 
                                        pdata = [grandchild, grandchild_path, grandchild_path, False]                      
                                        grandchildID = self.tree_ctrl.AppendItem(newParentID, grandchild)
                                        self.tree_ctrl.SetPyData(grandchildID, pdata)
                                        break
                        except:
                            pass
        self.statusbar.SetStatusText("Status Bar")


    def loginButton(self, evt):
        username = self.userbox.GetValue()
        password = self.passwordbox.GetValue() 
##        print username
##        print password 
        if username and password:
            stat = MDR.GNConnection.connect(username, password)
            #print stat
            if (stat == 200):
                self.controller.loginAction(username, password)            
                self.logoutTB()
                
            else:
                self.postMessage("Log On Failed. Please try again.")
                
        else:
            self.postMessage("Username and Password need valid values.")
        
        
        
class MyControls(object):
    
    def __init__(self, frame):
        self.frame = frame
        self.merged = ''
        self.user = ''
        self.pword = ''
        self.tmpltList = {}
        self.userinfo = ()
    
    def OnItemSelected(self, event):
        self.frame.currentItem = event.GetItem()
        
    def getRootDir(self, event):
        # In this case we include a "New directory" button. 
        dpath = ''
        if self.frame.filename.GetValue():
            dpath = self.frame.filename.GetValue()
        dlg = wx.DirDialog(self.frame, "Choose a directory:",
                            defaultPath = dpath,
                          style=wx.DD_DEFAULT_STYLE
                           | wx.DD_CHANGE_DIR
                           )
        
        # If the user selects OK, then we process the dialog's data.
        # This is done by getting the path data from the dialog - BEFORE
        # we destroy it. 
        if dlg.ShowModal() == wx.ID_OK:
            self.frame.filename.Clear()
            rDir = dlg.GetPath()
            self.frame.filename.SetValue(rDir)
            self.frame.buildTree()
        
        # Only destroy a dialog after you're done with it.
        

        dlg.Destroy()
        
        
    def xtrct(self, event): # wxGlade: MyFrame.<event_handler>
        
        ## status bar is not clearing - done 14-3-9 BC
        self.frame.statusbar.SetStatusText("Loading......")
        itemID = self.frame.currentItem
        self.frame.tree_ctrl.SelectItem(itemID, select=True)
        pydata = self.frame.tree_ctrl.GetPyData(itemID)
        
        #check for existing metadata xml or html or htm file
        fname,ext = os.path.splitext(str(pydata[1]))
        mdl = 0
        mdf = []
        mdf.append(fname + '.htm')
        mdf.append(fname + '.html')
        mdf.append(fname + '.xml')
        print mdf

        for name in mdf :
            if os.path.exists(name):
                mdl = 1
                self.frame.postMessage("Metadata link exist!")
                self.frame.postMessage(2*'\n'+80*'_'+3*'\n',1)
                fo = open(name, 'r')
                self.frame.postMessage(fo.read(),mdl)
                self.frame.postMessage(2*'\n'+80*'_'+3*'\n',1)
            
        # new stuff for _0_3
        ## refactor - move to util so util checks datatype
        datatype, idx1, idx2 = GO.util.getFileType(str(pydata[2]))
        print datatype, idx1, idx2
        
        if datatype:
            record = datatype(str(pydata[2]))
            print 'record', record
            mdrecord = record.xMeta()
            print 'mdrecord', mdrecord
            md = MDR.metadataRecord()
            print 'md'
            ## Can I find a way to avoid passing self?
            ##display = md.displayMDRecord(mdrecord)
            self.frame.postMessage(mdrecord, mdl)
            del mdrecord
            self.frame.postMessage(80*'_'+3*'\n',0)
            
        # end new stuff

        else :
            self.frame.postMessage("Non-gis Data",mdl)
        self.frame.statusbar.SetStatusText("Statusbar")


    def merge(self, event): 
        
        if self.frame.tmpltXML is not None:
            self.frame.statusbar.SetStatusText("Loading......")
            itemID = self.frame.currentItem
            self.frame.tree_ctrl.SelectItem(itemID, select=True)
            pydata = self.frame.tree_ctrl.GetPyData(itemID)
            # new stuff for _0_3
            ## refactor - move to util so util checks datatype
            datatype, idx1, idx2 = GO.util.getFileType(str(pydata[2]))
            #print datatype
            if datatype:
                record = datatype(str(pydata[2]))
                isoMDRecord = record.x19139Meta()
                isoMDRecord['{http://www.isotc211.org/2005/gmd}contact'] = self.userinfo
                #print isoMDRecord
                mdrecord = record.xMeta()
                md = MDR.metadataRecord()
                root = "."
                
                self.merged = md.mergeInfo(isoMDRecord, self.frame.tmpltXML, root)
                
                self.frame.postMessage(self.merged)
            out = 1
        else:
            self.frame.postMessage("Please login and select template metadata record.")
            out = 0

        self.frame.statusbar.SetStatusText("Statusbar")
        
        return out
        
    def submitGN(self, event):
        
        if self.merge(event):
        
            self.frame.statusbar.SetStatusText("Loading......")
            md = MDR.metadataRecord()
            uuid, id, cookie = md.submitMDRecord(self.merged, self.user, self.pword)
            GNServer = MDR.GNConnection.GNServer
            
            edlink = 'http://' + GNServer + '/geonetwork/srv/en/metadata.edit?id='+ id
            link = 'http://' + GNServer + '/geonetwork/srv/en/metadata.show?uuid='+ uuid

            #self.frame.postMessage(link)
            
            self.frame.statusbar.SetStatusText(link)
            
            htxt = """<!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.0 Transitional//EN">
                    <html>
                    <head>
                    <meta http-equiv="REFRESH" content="0;""" + link + """">
                    </head>
                    <BODY></BODY>
                    </HTML>"""
                    
            itemID = self.frame.currentItem
            pydata = self.frame.tree_ctrl.GetPyData(itemID)
            fname = os.path.splitext(str(pydata[1]))
            htfn = fname[0] + ".htm"
            hfile = open(htfn, 'w')
            hfile.write(htxt)
            self.frame.postMessage(uuid)
            self.frame.postHTML(edlink)

    ##        self._hyper1 = hl.HyperLinkCtrl(self, wx.ID_ANY, "GeoNetwork Edit Page",
    ##                                        URL=link)
    ##        contents.Add(self._hyper1, 0, wx.ALL, 10)
    ##        

        else:
            self.frame.postMessage("Please login and select template metadata record.")
            
        self.frame.statusbar.SetStatusText("Statusbar")
        
        
    def loginAction(self, username, password):
        

        self.user = username
        self.pword = password
                
        MDR.GNConnection.setUser(self.user)
        MDR.GNConnection.setPass(self.pword)
        md = MDR.metadataRecord()
        self.tmpltList = md.GetTemplateList(self.user, self.pword)
        self.userinfo = md.GetUserInfo(self.user, self.pword)      
        keys = self.tmpltList.keys()
        keys.sort()
        
        self.frame.popTmpltList(keys)
            
        
    def logout(self, event):
        self.user = None
        self.password = None
        MDR.GNConnection.setUser(self.user)
        MDR.GNConnection.setPass(self.pword)
        self.frame.cb.Clear()
        self.frame.cb.Append("Template List - Please log in", None)
        self.frame.cb.Select(0)
        self.frame.loginTB()
        
        
class  stringIterator(object):
    
    def __init__(self, string):
        self.string = string
        self.index = True
        
    def hasNext(self):
        return self.index
    
    def Next(self):
        self.index = False
        
    def getImage(self):
        return None
    
    def getChildren(self):
        return None
    
    def getLabel(self):
        return "Message"
    
    def getValue(self):
        return self.string
    
class dictIterator(object):
    from pythonutils import OrderedDict
        
    def __init__(self, dict):
        self.dict = dict
        self.index = 0
        
    def hasNext(self):
        index = self.index + 1
        if index >= len(self.dict) or not self.dict.keys()[index]:
            return False
    
        return True
    
    def Next(self):
        self.index += 1
        
    def getImage(self):
        return None
    
    def getChildren(self):
        child = self.dict.values()[self.index]
        if type(child).__name__ == 'OrderedDict':
           return dictIterator(child) 
            
        return None
    
    def getLabel(self):
        keys = self.dict.keys()
        return keys[self.index]
    
    def getValue(self):
        child = self.dict.values()[self.index]
        if not type(child).__name__ == 'OrderedDict':
           return child
        return ""
    
class xmlIterator(object):
    
    def __init__(self, xml):
        self.xml = xml
        self.index = 0
        
    def hasNext(self):
        index = self.index + 1
        if index >= len(self.xml) or not self.xml.getchildren()[index]:
            return False
    
        return True
    
    def Next(self):
        self.index += 1
        
    def getImage(self):
        return None
    
    def getChildren(self):
        child = self.xml.getchildren()[self.index]
        if not child:
            return None
        return xmlIterator(child) 
    
    def getLabel(self):
        return self.xml.tag
    
    def getValue(self):
        return self.xml.text



if __name__ == "__main__":
    app = wx.App(0)
 #   wx.InitAllImageHandlers()
    win = MyFrame(None, -1, title="Spatial Metadata Extraction Tool", size=(700,500))
    app.SetTopWindow(win)
    win.Show()
    app.MainLoop()
