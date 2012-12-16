#   Updated 8 January 2010 to remove any direct database calls with psycopg2
#       all calls now go through GeoNetwork xml -BC

import httplib, urllib, urllib2, requests
from lxml import etree
from pythonutils import OrderedDict
##from multipart import Multipart # no longer needed
from lxml.builder import E


class metadataRecord(object):
  
    
    def GetUserInfo(self, user, pword):

        txt = GNConnection.xmlcall('xml.user.list', '<request/>')
        print txt
        tree = etree.XML(txt)
        unames = tree.findall('.//username')
        record = None
        
        for uname in unames:
            if uname.text == user:                
                record = uname.getparent()
        
        name = "%s %s" % (record.find('name').text, record.find('surname').text)
        
        orgpos = record.find('organisation').text
        
        if orgpos:
            x = orgpos.find("--")
            if x:
                org = orgpos[:x]
                pos = orgpos[x+2:]
            else:
                org = orgpos
                pos = None
        else:
            org = None
            pos = None
            
        citstat = record.find('state').text
        
        if citstat:
            x = citstat.find("--")
            if x:
                city = citstat[:x]
                state = citstat[x+2:]
            else:
                city = orgpos
                state = None
        else:
            city = None
            state = None
        


        contact = OrderedDict()
        CIresparty = OrderedDict()
        csname = OrderedDict([('{http://www.isotc211.org/2005/gco}CharacterString',name)])
        CIresparty['{http://www.isotc211.org/2005/gmd}individualName'] = csname
        csorg = OrderedDict([('{http://www.isotc211.org/2005/gco}CharacterString',org)])
        CIresparty['{http://www.isotc211.org/2005/gmd}organisationName'] = csorg
        
        
        
        CIaddress = OrderedDict()
        csdeliv = OrderedDict([('{http://www.isotc211.org/2005/gco}CharacterString',record.find('address').text)])
        CIaddress['{http://www.isotc211.org/2005/gmd}deliveryPoint'] = csdeliv
        cscity = OrderedDict([('{http://www.isotc211.org/2005/gco}CharacterString',city)])
        CIaddress['{http://www.isotc211.org/2005/gmd}city'] = cscity
        csregion = OrderedDict([('{http://www.isotc211.org/2005/gco}CharacterString',state)])
        CIaddress['{http://www.isotc211.org/2005/gmd}administrativeArea'] = csregion
        cspost = OrderedDict([('{http://www.isotc211.org/2005/gco}CharacterString',record.find('zip').text)])
        CIaddress['{http://www.isotc211.org/2005/gmd}postalCode'] = cspost        
        cscountry = OrderedDict([('{http://www.isotc211.org/2005/gco}CharacterString',record.find('country').text)])
        CIaddress['{http://www.isotc211.org/2005/gmd}country'] = cscountry        
        csemail = OrderedDict([('{http://www.isotc211.org/2005/gco}CharacterString',record.find('email').text)])
        CIaddress['{http://www.isotc211.org/2005/gmd}electronicMailAddress'] = csemail        
        address = OrderedDict([('{http://www.isotc211.org/2005/gmd}CI_Address',CIaddress)])
        CIcontact = OrderedDict([('{http://www.isotc211.org/2005/gmd}address',address)])
        contactInfo = OrderedDict([('{http://www.isotc211.org/2005/gmd}CI_Contact',CIcontact)])
        CIresparty['{http://www.isotc211.org/2005/gmd}contactInfo'] = contactInfo
        cspos = OrderedDict([('{http://www.isotc211.org/2005/gco}CharacterString',pos)])
        CIresparty['{http://www.isotc211.org/2005/gmd}positionName'] = cspos
        contact['{http://www.isotc211.org/2005/gmd}CI_ResponsibleParty'] = CIresparty   
        
        return contact    
    

    def GetTemplateList(self, user, pword):
        

        tmpltList = {}

        # Select iso 19139 template metadata from GeoNework xml.search 
        
        txt = GNConnection.xmlcall('q', '<request><template>y</template><fast>index</fast></request>') 
        tree = etree.XML(txt)
        
        rows = tree.findall('.//metadata')
        n = 1
       
        for row in rows:
            
            #print etree.tostring(row)
            # Find the title and the guid
            title = row.find('title').text
            guid = row.find('{http://www.fao.org/geonetwork}info/uuid').text
            schema = row.find('{http://www.fao.org/geonetwork}info/schema').text
            id = row.find('{http://www.fao.org/geonetwork}info/id').text
            

            if title and guid:
                tmpltList[title + ' (' + id + ')'] = guid
                
            n = n + 1
                
        return tmpltList
    
            
    def getTemplateMDRecord(self, user, pword, fileID):

        # Select iso 19139 template metadata from the data column. 
        
        txt1 = GNConnection.xmlcall('xml.metadata.get', '<request><uuid>' + fileID + '</uuid></request>')    
        
        tree=etree.XML(txt1)
        print tree
##        geonetinfo = tree.find('{http://www.fao.org/geonetwork}info') 
##        print etree.tostring(geonetinfo, pretty_print=True)
##        tree.remove(geonetinfo) # No longer needed in GN 2.8
           
        tmpltXML = etree.tostring(tree,pretty_print=True)
                   
        return tree #tmpltXML    
    
    
    def displayMDRecord(self,mdrecord,i=0):

        rep = ""
        for item, value in mdrecord.iteritems(): 
            
                if type(value).__name__ == 'OrderedDict':
                    rep += i*'\t'
                    rep += '%s :\n' % item
                    i = i + 2
                    rep += self.displayMDRecord(value,i)
                    i = i - 2
                else:

                    rep += i*'\t'
                    rep += "%s : \t %s \n" % (item, value)
        return rep


##    def submitMDRecord(self, mdRecord, user, pword):
##        data = self.newGuid(mdRecord)
##        
##        n = {}
##
##        n['insert_mode'] = '1'
##        n['file_type'] = 'single'
##        n['data'] = ''
##        n.file('mefFile','c:\\temp\\text.mxl',data,{'Content-Type':'text/xml'})
##        n.field('template','n')
##        n.field('schema','iso19139')
##        n.field('title','')
##        n.field('uuidAction','generateUUID')
##        n.field('styleSheet','_none_')
##        n.field('group','2')
##        n.field('category','_none_')
##        ct,body = n.get()
##
##        header2 = {"Host":"Localhost:8080", 
##            "Content-type": ct, 
##            "Accept": "image/gif, image/jpeg, image/pjpeg, image/pjpeg, application/x-shockwave-flash, *",
##            "Connection": "Keep-Alive", 
##            "cookie": cookie}
##
##        file = {body}
##        r = requests.post("http://" + GN.GNServer + "/geonetwork/srv/mef.import, files=file")
##        httpServ = httplib.HTTPConnection("127.0.0.1", 8080)
##        httpServ.set_debuglevel(0)
##        httpServ.connect()
##        param1 = urllib.urlencode({'username':user, 'password':pword})
##
##        header1 = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Connection": "keep-alive", "Keep-Alive":"300"}
##        httpServ.request('POST', '/geonetwork/srv/en/xml.user.login', param1, header1)
##
##        conn = httpServ.getresponse()
##        print conn.status
##        print conn.reason
##        print conn.read()
##
##        cookie = conn.getheader('set-cookie')
##
##        #param2 = urllib.urlencode({'any':'Basins'})
##
##        #fo = open("C:\\temp\\text.xml","r")
##        #data = fo.read()
##        
##        data = self.newGuid(mdRecord)
##        print data
##        n = Multipart()
##
##        n.field('insert_mode','1')
##        n.field('file_type','single')
##        n.field('data','')
##        n.file('mefFile','c:\\temp\\text.mxl',data,{'Content-Type':'text/xml'})
##        n.field('template','n')
##        n.field('schema','iso19139')
##        n.field('title','')
##        n.field('uuidAction','generateUUID')
##        n.field('styleSheet','_none_')
##        n.field('group','2')
##        n.field('category','_none_')
##        ct,body = n.get()
##
##        header2 = {"Host":"Localhost:8080", "Content-type": ct, "Accept": "image/gif, image/jpeg, image/pjpeg, image/pjpeg, application/x-shockwave-flash, *", 'Connection': 'Keep-Alive', 'cookie': cookie}
##        print ct        
##        print body
##        print header2
##
##        httpServ.request('POST', '/geonetwork/srv/en/mef.import', body, header2 )
##        txt = 'Nothing Returned!'
##
##        response = httpServ.getresponse()
##        print response.reason, response.status
##        #print response.read()
##        if response.status == httplib.OK:
##            print "Output from CGI request"
##            txt = response.read()
##            lines = txt.split('\n')
##            for line in lines:
##                print line.strip()
##        httpServ.close()
##        
##        tree = etree.XML(txt)
##        id = tree.text
##        conn = psycopg2.connect("dbname='geonetwork' user='postgres' host='localhost' password='admin'")
##        cur = conn.cursor()
##        
##        cur.execute("""SELECT uuid
##                    FROM
##                     public.metadata
##                    WHERE public.metadata.id = '""" + id + """'""")
##        # Step through selected records
##        row = cur.fetchall()
##        
##        return row[0][0]
##    
                    
    def submitMDRecord(self, mdRecord, user, pword):
        
        #data = self.newGuid(mdRecord)

        param2 = E.request(E.data(mdRecord), 
                            E.template('n'),
                            E.title(''),
                            E.styleSheet('_none_'),
                            E.schema('iso19139'),
                            E.group('2'),
                            E.category('1'),
                            E.validate('off'),
                            E.uuidAction('generateUUID'))


        txt = GNConnection.xmlcall('xml.metadata.insert', etree.tostring(param2))

        print txt
        tree = etree.XML(txt)
        id = tree.find('./id').text
        #txt1 = GNConnection.xmlcall('xml.metadata.get', '<request><id>' + id + '</id></request>')
        #tree1 = etree.XML(txt1)
        uuid = tree.find('./uuid').text
 
        return uuid, id, GNConnection.cookie 

    
    def mergeInfo(self, node, tree, path):
        
        for item, value in node.iteritems():
             
            node = '/' + item
            path = path + node
            
            if type(value).__name__ == 'OrderedDict':
                
                self.mergeInfo(value, tree, path)              
                                
            else:
                values = str(value).split('--')
                element = tree.find(path)

                
                if (element is not None):
                    for val in values:    
                        elpar = element.getparent()
                        if elpar.get('{http://www.isotc211.org/2005/gco}nilReason'):
                            del elpar.attrib['{http://www.isotc211.org/2005/gco}nilReason']             

                        ival = str(val)
                        element.text = ival
                        if elpar.getnext() is not None:
                            element = elpar.getnext().getchildren()[0]

            lnode = len(node)
            path = path[:-lnode]

        return etree.tostring(tree)
    
    # No longer needed -- the UUID action argument deprecates this
    def newGuid(self, mdRecord):
        
        tree = etree.XML(mdRecord) 
        id = tree.find('.//{http://www.isotc211.org/2005/gmd}fileIdentifier')
        guid = id.find('{http://www.isotc211.org/2005/gco}CharacterString')
        guid.clear()
        
        return etree.tostring(tree)     
                    

class GNConnection(object):
    
    # Should these be in SMETconfig.xml -- check?
    GNServer = ""
    user = ""
    password = ""
    projData = ""
    rootDir = "c:\\"
    connection = None
    cookie = ""
    
        
    def getSettings(self, cdir):
        
        GN = GNConnection
        xfile = cdir +  '/SMETconfig.xml'
        doc = etree.parse ( xfile )
        GN.GNServer = doc.find("./GNServer").text
        GN.rootDir = doc.find("./rootDir").text
        GN.projData = doc.find("./projData").text
    
    
    def setUser(username):
        
        GNConnection.user = username
        
    setUser = staticmethod(setUser)
    
        
    def setPass(pword):
        
        GNConnection.password = pword
        
    setPass = staticmethod(setPass)
    
    
    def connect(username, pword):
        # Do we have security issues with clear case passwords?
##        GN = GNConnection
        path = '/geonetwork/srv/xml.user.login'      
        payload = {'username':username, 'password':pword}
        r = requests.post("http://" + GNConnection.GNServer + path, params=payload)
##        conn = urllib2.Request("http://" + GN.GNServer + path)
##        
##        try:
##            urllib2.urlopen(conn)
##            httpServ = httplib.HTTPConnection(GN.GNServer)
##            httpServ.set_debuglevel(0)
##            httpServ.connect()
##            param1 = urllib.urlencode({'username':username, 'password':pword})
##            header1 = {"Content-type": "application/x-www-form-urlencoded", 
##                        "Accept": "text/plain,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
##                        "Connection": "keep-alive", "Keep-Alive":"300"}
##            httpServ.request('POST', path, param1, header1)
##
##            conn = httpServ.getresponse()
##            conn.read()
##
##            ckstr = conn.getheader('set-cookie')
##            cook = ckstr.split(';')
##            GN.cookie = cook[0]
##
##            
##        except urllib2.URLError, e:
##            
##            conn.status = 400
##
##        return conn.status
        GNConnection.cookie = r.cookies['JSESSIONID']
        print r.status_code
        return r.status_code
        
    connect = staticmethod(connect)
    
    
    def xmlcall(service, param):
        
##        header = {'Accept': 'image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/x-shockwave-flash, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*, ',
##                    'Accept-Language': 'en-nz',
##                    'Content-Type': 'application/x-www-form-urlencoded',
##                    'Accept-Encoding': 'gzip, deflate',
##                    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; SC3_Customised_IE6.0_sp1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.1)',
##                    'Connection': 'Keep-Alive',
##                    'Cookie': GNConnection.cookie}
        
        path ='/geonetwork/srv/' + service
        print path
        #doc = urllib2.Request('http://' + GNConnection.GNServer + path, param, header)
        #r = requests.post("http://" + GNConnection.GNServer + path, data=param, headers={"Content-type":"text/xml"})#, cookies={'JSESSIONID':GNConnection.cookie})
        r = requests.post("http://"  + GNConnection.GNServer + path, 
                            data=param, 
                            headers={"Content-type":"text/xml"},
                            cookies={'JSESSIONID':GNConnection.cookie})
        txt = str(r.content) #r.text.encode("UTF-8")

        return txt
    
    xmlcall = staticmethod(xmlcall)
    
		# I don't think we need this anymore -- check
    def httpcall(service, param):
        
        header = {'Accept': 'image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, application/x-shockwave-flash, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*, ',
                    'Accept-Language': 'en-nz',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept-Encoding': 'gzip, deflate',
                    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; SC3_Customised_IE6.0_sp1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.1)',
                    'Connection': 'Keep-Alive',
                    'Cookie': GNConnection.cookie}
        
        path ='/geonetwork/srv/en/' + service
        httpServ.request('POST', '/geonetwork/srv/en/mef.import', body, header2 )
        response1 = httpServ.getresponse()
        txt = response1.read()
        
        return txt
    
    httpcall = staticmethod(httpcall)
