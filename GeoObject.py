import os, time 
from osgeo import gdal
from osgeo import osr
from osgeo import ogr
from collections import OrderedDict
import pyproj
import MetadataRecord as MDR

#--Class: geoObject -main class----
class geoObject(object):
    
    def __init__(self, filepath):
        #--Set generic system file info attributes----
        
        self.file = os.path.basename(filepath)
        self.path = os.path.dirname(filepath)
        self.fullpath = filepath
        self.uncpath = util.getUNCName(self.path)
        self.createDate = os.path.getctime(self.fullpath)
        self.modDate = os.path.getmtime(self.fullpath)
        self.fileSize = os.path.getsize(self.fullpath)/1024
        

    def xMeta(self):
        #--Create ordered dictionary of generic system file info attributes----
        #--for user presentable display. Could this be refactored to use only x19139Meta?
        
        self.dsMetadata = OrderedDict()
        self.dsMetadata['File Name'] = self.file
        self.dsMetadata['Parent Directory'] = self.path
        self.dsMetadata['File Size (mb)'] = self.fileSize
        self.dsMetadata['UNC Path'] = self.uncpath
        self.dsMetadata['Create Date'] = time.asctime(time.localtime(self.createDate))
        self.dsMetadata['Modify Date'] = time.asctime(time.localtime(self.modDate))
        return self.dsMetadata
    

    def x19139Meta(self):
        #--Create ordered dictionary of generic system file info attributes in iso19139----
        
        self.isoMetadata = OrderedDict()
        identificationInfo = OrderedDict()
        self.MD_DataIdentification = OrderedDict()        
        citation = OrderedDict()
        CI_Citation = OrderedDict()
        title = OrderedDict([('{http://www.isotc211.org/2005/gco}CharacterString',self.file)])
        CI_Citation['{http://www.isotc211.org/2005/gmd}title'] = title
        citation['{http://www.isotc211.org/2005/gmd}CI_Citation'] = CI_Citation
        self.MD_DataIdentification['{http://www.isotc211.org/2005/gmd}citation'] = citation
        identificationInfo['{http://www.isotc211.org/2005/gmd}MD_DataIdentification'] = self.MD_DataIdentification
        self.isoMetadata['{http://www.isotc211.org/2005/gmd}identificationInfo'] = identificationInfo
        
        if self.uncpath :
            fpath = self.uncpath
        else:
            fpath = self.path
        #--Create nested ordered dictionary mirroring iso19139---    
        distributionInfo = OrderedDict()
        self.MD_Distribution = OrderedDict()
        transferOptions = OrderedDict()
        MD_DigitalTransferOptions = OrderedDict()
        onLine = OrderedDict()
        CI_OnlineResource = OrderedDict()
        linkage = OrderedDict([('{http://www.isotc211.org/2005/gmd}URL',fpath)])
        CI_OnlineResource['{http://www.isotc211.org/2005/gmd}linkage'] = linkage
        protocol = OrderedDict([('{http://www.isotc211.org/2005/gco}CharacterString',"Web address (URL)")])
        CI_OnlineResource['{http://www.isotc211.org/2005/gmd}protocol'] = protocol
        name = OrderedDict([('{http://www.isotc211.org/2005/gco}CharacterString',self.file)])
        CI_OnlineResource['{http://www.isotc211.org/2005/gmd}name'] = name
        description = OrderedDict([('{http://www.isotc211.org/2005/gco}CharacterString',self.file)])
        CI_OnlineResource['{http://www.isotc211.org/2005/gmd}description'] = description
        onLine['{http://www.isotc211.org/2005/gmd}CI_OnlineResource'] = CI_OnlineResource
        MD_DigitalTransferOptions['{http://www.isotc211.org/2005/gmd}onLine'] = onLine
        transferOptions['{http://www.isotc211.org/2005/gmd}MD_DigitalTransferOptions'] = MD_DigitalTransferOptions
        self.MD_Distribution['{http://www.isotc211.org/2005/gmd}transferOptions'] = transferOptions
        distributionInfo['{http://www.isotc211.org/2005/gmd}MD_Distribution'] = self.MD_Distribution
        self.isoMetadata['{http://www.isotc211.org/2005/gmd}distributionInfo'] = distributionInfo

        return self.isoMetadata

#--Class: RasterLayer, a subclass of geoObject----
class RasterLayer(geoObject):
        
    def __init__(self, filepath):
        #--Metadata for raster data----
        
        geoObject.__init__(self, filepath)
        raster = gdal.OpenShared(self.fullpath)
        self.DataType = "Raster Data"
        self.driver = raster.GetDriver().LongName
        self.rasterX = raster.RasterXSize
        self.rasterY = raster.RasterYSize
        self.bands = self.getBands(raster)
        rproj = raster.GetProjection()
    
        if rproj:
            sourceSrs = osr.SpatialReference()
            sourceSrs.ImportFromWkt(rproj)
            
            if sourceSrs is not None :
                self.Projection, self.isoproj = util.getProjMData(sourceSrs)
                self.Extents, self.isobox = self.getBBoxLL(raster,sourceSrs)
                
        else:
            self.Projection, self.isoproj = (None, None)
            self.Extents, self.isobox = (None, None)
            self.Projection = "no projection information"

        del raster
        
        
    def getBands(self,raster):
        #--Metadata for raster bands----
        
        resultsbands = OrderedDict()
        self.BandCount = raster.RasterCount
        bandsdata = OrderedDict()
        bandsdata['Band Count'] = self.BandCount
        for bandnum in range(self.BandCount):
            band = raster.GetRasterBand(bandnum+1)
            # ComputeRasterMinMax is slow for large images
            # Can we speed this up?

##            bmin, bmax = band.ComputeRasterMinMax()
            overviews = band.GetOverviewCount()
            resultseachband = OrderedDict()
            resultseachband['bandId'] = str(bandnum+1)
##            resultseachband['min'] = str(bmin)
##            resultseachband['max'] = str(bmax)
            resultseachband['Block_Size'] = band.GetBlockSize()
            resultseachband['Type'] = gdal.GetDataTypeName(band.DataType)
            bandColour = band.GetRasterColorInterpretation()
            resultseachband['Colour'] = gdal.GetColorInterpretationName(bandColour)
            resultseachband['overviews'] = str(overviews)
            resultsbands[str(bandnum+1)] = resultseachband
            bandsdata['band ' + str(bandnum+1)] = resultsbands[str(bandnum+1)]

        return bandsdata
        
    
    def getBBoxLL(self, raster, sourceSrs):
        #--Bounding box metadata for raster geodata----

        geotrans = raster.GetGeoTransform()
        minx = geotrans[0]
        maxy = geotrans[3]
        maxx = minx + (geotrans[1] * self.rasterX)
        miny = maxy + (geotrans[5] * self.rasterY)
        
        extents = [minx,maxx,miny,maxy]
        boundbox,isobox = util.transBBtoLL(sourceSrs,extents)

        return boundbox, isobox
    
            
    def xMeta(self):
        #--Create ordered dictionary of raster file attributes----
        #--for user presentable display. Could this be refactored to use only x19139Meta?
        
        geoObject.xMeta(self)
        self.dsMetadata['Data Type'] = self.DataType
        if self.BandCount:
            self.dsMetadata['Number of Bands'] = self.BandCount
        if self.driver:
            self.dsMetadata['File Type'] = self.driver
        if self.bands:
            self.dsMetadata['Raster Band'] = self.bands
        if self.Projection:
            self.dsMetadata['Projection'] = self.Projection
        if self.Extents:
            self.dsMetadata['Bounding Box'] = self.Extents
        
        return self.dsMetadata
    
    
    def x19139Meta(self):
        #--Create nested ordered dictionary mirroring iso19139---
        
        geoObject.x19139Meta(self)
        distributionFormat = OrderedDict()
        MD_Format = OrderedDict()
        name = OrderedDict([('{http://www.isotc211.org/2005/gco}CharacterString',self.driver)])
        MD_Format['{http://www.isotc211.org/2005/gmd}name'] = name
        distributionFormat['{http://www.isotc211.org/2005/gmd}MD_Format'] = MD_Format
        self.MD_Distribution['{http://www.isotc211.org/2005/gmd}distributionFormat'] = distributionFormat        
        self.MD_DataIdentification['{http://www.isotc211.org/2005/gmd}extent'] = self.isobox
        self.isoMetadata['{http://www.isotc211.org/2005/gmd}referenceSystemInfo'] = self.isoproj
        
        return self.isoMetadata

      
class VectorLayer(geoObject):
    
    def __init__(self, filepath):
        geoObject.__init__(self, filepath)
        
        # open the vector geoData object and set DataType
        vector = ogr.OpenShared(self.fullpath)        
        self.DataType = "Vector Data"
        
        # retreive the data type name
        self.DataFormat = vector.GetDriver().GetName()
        
        # get the number of datalayers in the object and select the first (and only)
        # To Do - set layer number as variable so as to retieve sublayers in a Geo Database
        self.LayerCount = vector.GetLayerCount()
        layer = vector.GetLayer(0)
        self.FeatCount = str(layer.GetFeatureCount())
        
        # Geometry type is retrieved in this section
        geomType = layer.GetLayerDefn().GetGeomType() # retrieve the WKB for the feature type
        if geomType != 100:

            featType = ogr.Geometry(geomType) # creates a Geometry object from the WKB
            
            self.FeatType = ogr.Geometry.ExportToWkt(featType) # creates a WKT from the Geometry object
            
            # Retrieve the projection definition and extents
            proj = layer.GetSpatialRef()
            if proj is not None:
                self.Projection, self.isoproj = util.getProjMData(proj)
                extents =  layer.GetExtent()
                self.Extents,self.isobox = util.transBBtoLL(proj,extents)
            else:
                self.Projection = None
                self.Extents = None
        else:
            featType = "None"
            
    
    def xMeta(self):
        
        geoObject.xMeta(self)
        self.dsMetadata['Data Type'] = self.DataType
        if self.DataFormat:
            self.dsMetadata['Data Format'] = self.DataFormat
        if self.LayerCount:
            self.dsMetadata['Layer Count'] = self.LayerCount
        if self.FeatCount:
            self.dsMetadata['Feature Count'] = self.FeatCount
        if self.FeatType:
            self.dsMetadata['Feature Type'] = self.FeatType
        if self.Projection:
            self.dsMetadata['Projection'] = self.Projection
        if self.Extents:
            self.dsMetadata['Bounding Box'] = self.Extents
            
        return self.dsMetadata
    
    
    def x19139Meta(self):
        #--Create nested ordered dictionary mirroring iso19139---
        
        geoObject.x19139Meta(self)

        distributionFormat = OrderedDict()
        MD_Format = OrderedDict()
        name = OrderedDict([('{http://www.isotc211.org/2005/gco}CharacterString',self.DataFormat)])
        MD_Format['{http://www.isotc211.org/2005/gmd}name'] = name
        distributionFormat['{http://www.isotc211.org/2005/gmd}MD_Format'] = MD_Format
        self.MD_Distribution['{http://www.isotc211.org/2005/gmd}distributionFormat'] = distributionFormat
        if self.isobox is not None:
            self.MD_DataIdentification['{http://www.isotc211.org/2005/gmd}extent'] = self.isobox
        self.isoMetadata['{http://www.isotc211.org/2005/gmd}referenceSystemInfo'] = self.isoproj
        
        return self.isoMetadata
    

     
class geoWorkspace(geoObject):
    
    def __init__(self, filepath):
        
        geoObject.__init__(self, filepath)
        vector = ogr.OpenShared(self.fullpath)        
        self.DataType = "Geodata collection"
        self.LayerCount = vector.GetLayerCount()        
        self.subLayers = self.getSubLayers(vector)
        del vector
        

    def getSubLayers(self, vector):
        
        subLayers = OrderedDict()
        for subLayerNum in range(self.LayerCount):
            subLayer = vector.GetLayer(subLayerNum)
            subLayerName = subLayer.GetName()            
            subLayers[subLayerName] = OrderedDict()
            subLayers[subLayerName]['Name'] = subLayerName
            geomType = subLayer.GetLayerDefn().GetGeomType()
            if geomType != 100:
                featType = ogr.Geometry(geomType)
                if geomType > 0:
                    subLayers[subLayerName]['Feature Type'] = ogr.Geometry.ExportToWkt(featType)
                else:
                    subLayers[subLayerName]['Feature Type'] = "N/A"
                subLayers[subLayerName]['FeatCount'] = str(subLayer.GetFeatureCount())
                proj = subLayer.GetSpatialRef()
                if proj is not None:
                    subLayers[subLayerName]['Projection'], iso = util.getProjMData(proj)
                    extents = subLayer.GetExtent()
                    subLayers[subLayerName]['Bounding Box'],isobox = util.transBBtoLL(proj,extents)
            else:
                 subLayers = 0 
                   
        return subLayers
    
    
    def xMeta(self):
        
        geoObject.xMeta(self)
        self.dsMetadata['Data Type'] = self.DataType
        if self.LayerCount:
            self.dsMetadata['Layer Count'] = self.LayerCount
        if self.subLayers:
            self.dsMetadata['Sub Layers'] = self.subLayers
        return self.dsMetadata
    
    
    def x19139Meta(self):
        
        geoObject.x19139Meta(self)
        

# Class: Directory - generic directory object. For objects not decernable as geodata
class Directory(geoObject): 
    
    
    def __init__(self, filepath):
        
        geoObject.__init__(self, filepath)
        self.DataType = 'Non-GIS formatted Directory'
        
        
    def xMeta(self):
        
        geoObject.xMeta(self)
        self.dsMetadata['Data Type'] = self.DataType
        
        return self.dsMetadata
    
    
    def x19139Meta(self):
        
        geoObject.x19139Meta(self)
        


class util(object):  # util class includes methods not dependent on geodatatype
    
    
    # getUNCName -Retrieves the UNC path of the data set selected to give 
    # unversal access on the network
		# -- Make cross platform
    def getUNCName(fullpath):
        try:
            import win32wnet
            uncname=win32wnet.WNetGetUniversalName(fullpath,1)
        except:
            uncname=""
        return uncname
    getUNCName = staticmethod(getUNCName)
 
    
    # getFileType -checks for the type of geodata selected 
    # returns the datatype class and icons, active and inactive         
    def getFileType(filepath):
        
        datatype = ''
        dsogr, dsgdal = False, False
        icon1, icon2 = 'fldr', 'fldropen'
        gdal.PushErrorHandler( "CPLQuietErrorHandler" )
        try:
            dsgdal = gdal.OpenShared(filepath)
            if dsgdal is not None:
                datatype = RasterLayer
                icon1 = 'img'
                icon2 = 'img'
                
       
            else:
                try:
                    dsogr = ogr.OpenShared(filepath) 
                    if dsogr:
                        if dsogr.GetLayerCount() > 1:
                            datatype = geoWorkspace
                            icon1 = 'gdb'
                            icon2 = 'gdb'
                        elif  os.path.isdir(filepath):
                            datatype = Directory
                            icon1 = 'fldr'
                            icon2 = 'fldropen'
                        else:
                            datatype = VectorLayer
                            icon1 = 'file'
                            icon2 = 'file'  
                                    
                except:
                    return False, icon1, icon2
        except:
            return False, icon1, icon2
 
        try:
            if os.path.isdir(filepath) and dsogr is None and dsgdal is None:
                datatype = Directory
                icon1 = 'fldr'
                icon2 = 'fldropen'
        except:
            return False, icon1, icon2    
        del dsogr
        del dsgdal
        
        return datatype, icon1, icon2
    
    getFileType = staticmethod(getFileType)
    
    
    # getProjMData -retrieves projection metadata from a WKT projection string
		# -- Can we connect to a live service? - low priority
		# -- At least provide method of lookup (Strategy Pattern)
    def getProjMData(sourceSrs):
        
        try:
            projection = OrderedDict()
            projType = 'GEOGCS' 
            
            if sourceSrs.IsProjected():
                projType = 'PROJCS'
                name = sourceSrs.GetAttrValue(projType,0)
                projection['Name'] = name
                
                if not name == "unnamed":
                
                    authority = sourceSrs.GetAttrValue("AUTHORITY",0)
                    codeVal = sourceSrs.GetAttrValue("AUTHORITY",1)
                    if authority is None:
                        import epsglookup
                        
                        epsg_file = os.path.join(MDR.GNConnection.projData, "epsg")
##                        print epsg_file
##                        print name
                        proj_lookup = epsglookup.ProjectionLookup(epsg_file)
                        codeVal = proj_lookup.find_by_name(name).id
                        authority = "epsg"
##                        print codeVal

                    projection['Authority'] = authority
                    projection['Code'] = codeVal
                else:
                    authority = ""
                    codeVal = ""
                project = sourceSrs.GetAttrValue("PROJECTION")
                projection['Projection'] = project
                centMer = sourceSrs.GetProjParm("central_meridian",1)
                projection['Central Meridian'] = centMer
            else:
                name = sourceSrs.GetAttrValue(projType,0)
                authority = sourceSrs.GetAttrValue("AUTHORITY",0)
                codeVal = sourceSrs.GetAttrValue("AUTHORITY",1)
                projection['Name'] = name
                projection['Authority'] = authority
                projection['Code'] = codeVal
            
            
            isoproj = OrderedDict()
            referenceSystemInfo = OrderedDict()
            MD_ReferenceSystem = OrderedDict()
            referenceSystemIdentifier = OrderedDict()
            RS_Identifier = OrderedDict()
            if (authority) and (codeVal):
                code = OrderedDict([('{http://www.isotc211.org/2005/gco}CharacterString',codeVal)])
                RS_Identifier['{http://www.isotc211.org/2005/gmd}code'] = code
                auth = OrderedDict([('{http://www.isotc211.org/2005/gco}CharacterString',authority)])
                RS_Identifier['{http://www.isotc211.org/2005/gmd}codeSpace'] = auth
            else :
                code = OrderedDict([('{http://www.isotc211.org/2005/gco}CharacterString',name)])
                RS_Identifier['{http://www.isotc211.org/2005/gmd}code'] = code
            
            referenceSystemIdentifier['{http://www.isotc211.org/2005/gmd}RS_Identifier'] = RS_Identifier
            MD_ReferenceSystem['{http://www.isotc211.org/2005/gmd}referenceSystemIdentifier'] = referenceSystemIdentifier
            referenceSystemInfo['{http://www.isotc211.org/2005/gmd}MD_ReferenceSystem'] = MD_ReferenceSystem
            isoproj['{http://www.isotc211.org/2005/gmd}referenceSystemInfo'] = referenceSystemInfo
        
        except:
            projection = "Faulty projection parameters"
            isoproj = None
        
        return projection, isoproj
    
    getProjMData = staticmethod(getProjMData)
    
    
    # transBBtoLL -Translates a list of coordinate values (minx, maxx, miny, maxy) 
    # from native projection to WGS84 lat long coordinates
    def transBBtoLL(sourceSrs,extents):
        
        try:
            minx = extents[0]
            maxx = extents[1]
            miny = extents[2]
            maxy = extents[3]
            
            newsrs = sourceSrs.ExportToProj4() 

            # The following lines have been replaced to use pyproj instead of osr due
            # to the current flakiness of TransformPoint not acceptint arguements.
            # i.e. (NotImplementedError: Wrong number of arguments for overloaded function 
            # 'CoordinateTransformation_TransformPoint'.)
    ##        targetSrs = osr.SpatialReference()
    ##        targetSrs.ImportFromEPSG(4326)
    ##        
    ##        transform = osr.CoordinateTransformation(sourceSrs,targetSrs)
    ##        
    ##        ulcoord = transform.TransformPoint(minx, maxy, 0.0)
    ##        llcoord = transform.TransformPoint(minx, miny, 0.0)
    ##        lrcoord = transform.TransformPoint(maxx, miny, 0.0)
    ##        urcoord = transform.TransformPoint(maxx, maxy, 0.0)
            
            
            boundbox = OrderedDict()
            if sourceSrs.GetAttrValue("AUTHORITY",1) == "4326" and not sourceSrs.IsProjected():
                boundbox['maxx'] = maxx
                boundbox['maxy'] = maxy
                boundbox['minx'] = minx
                boundbox['miny'] = miny
                
            else:
               # pyproj section 
                pyproj.set_datapath(MDR.GNConnection.projData)
                pyproj.pyproj_datadir = MDR.GNConnection.projData
                
                pyproj.set_datapath(MDR.GNConnection.projData)
                
                p1 = pyproj.Proj(newsrs)
                
                p2 = pyproj.Proj(init='epsg:4326')

                ulcoord = pyproj.transform(p1, p2, minx, maxy)
                lrcoord = pyproj.transform(p1, p2, maxx, miny)
                llcoord = pyproj.transform(p1, p2, minx, miny)
                urcoord = pyproj.transform(p1, p2, maxx, maxy)
                
                # end pyproj section
                
                boundbox['maxx'] = max(lrcoord[0], urcoord[0])
                boundbox['maxy'] = max(ulcoord[1], urcoord[1])
                boundbox['minx'] = min(llcoord[0], ulcoord[0])
                boundbox['miny'] = min(llcoord[1], lrcoord[1])
     
            extent = OrderedDict()
            EX_Extent = OrderedDict()
            geographicElement = OrderedDict()
            EX_GeographicBoundingBox = OrderedDict()
            minx = OrderedDict([('{http://www.isotc211.org/2005/gco}Decimal',boundbox['minx'])])
            EX_GeographicBoundingBox['{http://www.isotc211.org/2005/gmd}westBoundLongitude'] = minx
            maxx = OrderedDict([('{http://www.isotc211.org/2005/gco}Decimal',boundbox['maxx'])])
            EX_GeographicBoundingBox['{http://www.isotc211.org/2005/gmd}eastBoundLongitude'] = maxx
            miny = OrderedDict([('{http://www.isotc211.org/2005/gco}Decimal',boundbox['miny'])])
            EX_GeographicBoundingBox['{http://www.isotc211.org/2005/gmd}southBoundLatitude'] = miny
            maxy = OrderedDict([('{http://www.isotc211.org/2005/gco}Decimal',boundbox['maxy'])])
            EX_GeographicBoundingBox['{http://www.isotc211.org/2005/gmd}northBoundLatitude'] = maxy
            geographicElement['{http://www.isotc211.org/2005/gmd}EX_GeographicBoundingBox'] = EX_GeographicBoundingBox
            EX_Extent['{http://www.isotc211.org/2005/gmd}geographicElement'] = geographicElement
            extent['{http://www.isotc211.org/2005/gmd}EX_Extent'] = EX_Extent
        
        except:
            boundbox = "Faulty proj4 parameters"
            extent = None
            
        
        return boundbox, extent
        
    
    transBBtoLL = staticmethod(transBBtoLL)
