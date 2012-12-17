#   Updated 8 January 2010 to remove any direct database calls with psycopg2
#       all calls now go through GeoNetwork xml -BC

import httplib, urllib, urllib2, requests
from lxml import etree
from pythonutils import OrderedDict

from lxml.builder import E


class metadataRecord(object):
  
    
    def GetUserInfo(self, user, pword):

        tree = GNConnection.xmlcall('xml.user.list')
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
        
        tree = GNConnection.xmlcall('q', template='y', fast='index') 
        
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
        return GNConnection.xmlcall('xml.metadata.get', uuid=fileID)
                    
    def submitMDRecord(self, mdRecord, user, pword):
        tree = GNConnection.xmlcall('xml.metadata.insert', 
                                    data=mdRecord,
                                    title='',
                                    stylesheet='__non__',
                                    schema='iso19139',
                                    group=2, # get user group?
                                    category=1, # ask for category?
                                    validate='off', #validation would need additional interfaces
                                    uuidAction='generateUUID)

        id = tree.find('./id').text
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
    
    @staticmethod
    def setUser(username):
        GNConnection.user = username
    
    @staticmethod
    def setPass(pword):
        GNConnection.password = pword

    
    @staticmethod
    def connect(username, pword):
        # Do we have security issues with clear case passwords?
        path = '/geonetwork/srv/xml.user.login'      
        payload = {'username':username, 'password':pword}
        r = requests.post("http://" + GNConnection.GNServer + path, params=payload)
        GNConnection.cookie = r.cookies['JSESSIONID']
        print r.status_code
        return r.status_code
    
    @staticmethod
    def xmlcall(_service, _param=E.request(), **kwargs):
        for key, value in kwargs.items():
            _param.append(E(key, value))
        param = etree.tostring(_param)
        print param

        path ='/geonetwork/srv/' + _service
        r = requests.post("http://"  + GNConnection.GNServer + path, 
                            data=param, 
                            headers={"Content-type":"text/xml"},
                            cookies={'JSESSIONID':GNConnection.cookie})

        return etree.XML(str(r.content))
