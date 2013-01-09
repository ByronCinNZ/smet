
# -*- coding: iso-8859-1 -*-
# smet version 0.1 -Spatial Metadata Extraction tool -Byron Cochrane 14,Sept,2007
#      version 0.3 -Spatial Metadata Extraction Tool -Byron Cochrane 17, Oct 2008

import wx, wx.gizmos, os, urllib2, urllib, dircache, webbrowser
import MetadataRecord as MDR, GeoObject as GO, InfoView
from lxml import etree 
#import wx.lib.agw.hyperlink as hl

if wx.Platform == '__WXMSW__':
    import wx.lib.iewin as iewin
    

#--------------------------------------------------------------------


#---MyFrame---#000000#FFFFFF----------------------------------------------------
#---window object---------------

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        self.path = self.dlg = self.fc = ''
        cdir = os.getcwd()
        con = MDR.GNConnection().getSettings(cdir)
        
        kwds.update({"style":wx.DEFAULT_FRAME_STYLE, "size":(900,500)}) 
        wx.Frame.__init__(self, *args, **kwds)
        self.controller = MyControls(self)
        
        self.bkgnd = wx.Panel(self, -1)
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText("Statusbar")

        #--Layout------
##        self.contents = wx.TextCtrl(self.bkgnd, -1, "", style=wx.TE_MULTILINE)
        self.contentsScroller = wx.ScrolledWindow(self.bkgnd, -1)
        self.contents = InfoView.InfoView(self.contentsScroller, -1)
        self.tree_ctrl = wx.TreeCtrl(self.bkgnd, -1, style=wx.TR_TWIST_BUTTONS|wx.TR_LINES_AT_ROOT|wx.TR_DEFAULT_STYLE|wx.SUNKEN_BORDER,size=(200,300))
        self.bind_(self.tree_ctrl, {wx.EVT_TREE_ITEM_ACTIVATED: 'xtrct', wx.EVT_TREE_SEL_CHANGED: 'OnItemSelected', 
                    wx.EVT_TREE_ITEM_RIGHT_CLICK: self.OnRightUp, wx.EVT_TREE_ITEM_EXPANDING: self.onExpand})

        #---Icons -------default images here
        isz = (16,16)
        self.il = wx.ImageList(isz[0], isz[1])

        idx = {'fldr':wx.ART_FOLDER, 'fldropen':wx.ART_FILE_OPEN, 'file':wx.ART_LIST_VIEW, 'img':wx.ART_MISSING_IMAGE, 'gdb':wx.ART_HARDDISK}
        self.idx = {k:self.il.Add(wx.ArtProvider_GetBitmap(v, wx.ART_OTHER, isz)) for k, v in idx.items()}
        self.tree_ctrl.SetImageList(self.il)


        self.ToolBar()
        self.SetTitle("Spatial Metadata Extractor Tool")
        self.__do_layout()

    def __do_layout(self):
        hbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox = wx.BoxSizer(wx.HORIZONTAL)

        hbox.Add(self.tb, proportion=0, border=5)
        self.vbox.Add(self.tree_ctrl, proportion=0, flag=wx.EXPAND|wx.FIXED_MINSIZE|wx.TR_HAS_BUTTONS, border=7)
        self.vbox.Add(self.contentsScroller, proportion=1, flag=wx.EXPAND|wx.ALL, border=5)
        hbox.Add(self.vbox, proportion=1, flag=wx.EXPAND|wx.ALL, border=5)

        self.bkgnd.SetSizer(self.vbox)
        self.Layout()
        
    def bind_(self, view, evts):
        for evt, action in evts.items(): 
            if type(action) == str: action = getattr(self.controller, action)
            self.Bind(evt, action, view)

    def postMessage(self, message, clr=1):
        '''
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
        
        print type(message).__name__
        if type(message).__name__ ==  '_Element':
            message = etree.tostring(message)
        elif type(message).__name__ == 'OrderedDict':
            message = prettyDict(message)
        elif hasattr(message, '__iter__') and not type(message) == str:
            for item in message:
                self.postMessage(item, clr)
                self.postMessage(2*'\n'+80*'_'+3*'\n', False)
                clr = 0
            return # No additional message to post, all recursion.
        else:
            message = str(message)
            
        self.contents.AppendText(message)
        '''
        self.contents.Destroy()
        del self.contents # Fixes weird GC bug (something to do with C++)
        self.contents = InfoView.InfoView(self.contentsScroller, -1, data=message)
        self.contentsScroller.SetScrollbars(1,1, *self.contents.GetSize())
    
    def postHTML(self, page):
        upstr = 'http://' + MDR.GNConnection.GNServer + "/geonetwork/srv/en/user.login?username=" + self.controller.user + "&password=" + self.controller.pword
        login = webbrowser.open(upstr)        
        webbrowser.open(page)
    
    def ToolBar(self):
        # TODO: Replace with panel for better sizing
        tsize = (24,24)
        
        folder_bmp = wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_TOOLBAR, tsize)
        self.tb = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TAB_TRAVERSAL)
        
        self.tb.AddLabelTool(20, "Select", folder_bmp, shortHelp="Select", longHelp="Select root directory")
        self.Bind(wx.EVT_TOOL, self.controller.getRootDir, id=20)
        
        self.tb.AddSeparator()
        
        self.filename = wx.TextCtrl(self.tb, -1, size=(200,-1), style=wx.TE_LEFT | wx.TB_NOICONS | wx.TE_PROCESS_ENTER)
        self.tb.AddControl(self.filename)
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
        def addTextEntry(label, style, helptext):
            label = wx.StaticText(self.tb, -1, label, style=wx.ALIGN_RIGHT)
            self.tb.AddControl(label)
            entry = wx.TextCtrl(self.tb, 34, size=(50, -1), style=style)
            entry.SetHelpText(helptext)
            self.tb.AddControl(entry)
            return label, entry

        for control in self.loginControls:
            id = control.GetId()
            self.tb.RemoveTool(id)
        pacetxt = 10*" " + "Username :  " #TODO: Use sizers (or equiv) to aid frame resizing.
        
        self.utext, self.userbox = addTextEntry(pacetxt, 0, "Enter your GeoNetwork User Name here.")
        ptext, self.passwordbox = addTextEntry("  Password : ", wx.TE_PASSWORD, "Enter your GeoNetwork Password here.")
        self.Bind(wx.EVT_TEXT_ENTER, self.loginButton, self.passwordbox)
        self.tb.AddSeparator()
        
        self.libttn = self.createTbButton("Log In", self.loginButton)
        
        self.loginControls = (self.userbox, ptext, self.passwordbox, self.libttn)
        self.tb.Realize()

    def createTbButton(self, label, action):
        bttn = wx.Button(self.tb, 36, label, (120, -1))
        self.Bind(wx.EVT_BUTTON, action, bttn)
        self.tb.AddControl(bttn)
        return bttn

    def logoutTB(self):
        for control in self.loginControls:
            id = control.GetId()
            self.tb.RemoveTool(id)
            
        pacetxt = 20*" " + self.controller.user + 20*" "
        itext = wx.StaticText(self.tb, -1, pacetxt, style=wx.ALIGN_RIGHT)
        self.tb.AddControl(itext)
        self.tb.AddSeparator()
        self.lobttn = wx.Button(" Log Out ", self.controller.logout)
        self.tb.Realize()
        
        self.loginControls = (self.utext, itext, self.lobttn)
        
        
    def OnRightUp(self, event):
        print "Heard right click."
        def createMenuItem(label, action):
            item = menu.Append(wx.ID_ANY, label)
            self.Bind(wx.EVT_MENU, getattr(self.controller, action), item)
            return item

        self.currentItem = event.GetItem()
        menu = wx.Menu()
        createMenuItem("Display", 'xtrct')
        createMenuItem("Merge", 'merge')
        createMenuItem("Submit", 'submitGN')
        #TODO: A "make root dir" option would be handy
        
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
            self.tmpltXML, self.schema = MDR.metadataRecord().getTemplateMDRecord(self.controller.user, self.controller.pword, selId)  
            print "hi", self.schema      
            self.postMessage(self.tmpltXML)
        

        
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
        output = []
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
                with open(name, 'r') as fo:
                    output += ("Metadata link exists!", fo.read())
            
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
            output.append(mdrecord)
            del mdrecord
            self.frame.postMessage(output)
            
        # end new stuff

        else :
            self.frame.postMessage("Non-gis Data")
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


if __name__ == "__main__":
    app = wx.App(0)
 #   wx.InitAllImageHandlers()
    win = MyFrame(None, -1, title="Spatial Metadata Extraction Tool", size=(700,500))
    app.SetTopWindow(win)
    win.Show()
    app.MainLoop()
