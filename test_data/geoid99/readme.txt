Can be obtained from: http://www.ngs.noaa.gov/GEOID/

goes from upper left to lower right corner
n       GEOID99 grid #1 for CONUS (40-58N, 230-249E)
 g1999u02.bin       GEOID99 grid #2 for CONUS (40-58N, 247-266E)
 g1999u03.bin       GEOID99 grid #3 for CONUS (40-58N, 264-283E)
 g1999u04.bin       GEOID99 grid #4 for CONUS (40-58N, 281-300E)
 g1999u05.bin       GEOID99 grid #5 for CONUS (24-42N, 230-249E)
 g1999u06.bin       GEOID99 grid #6 for CONUS (24-42N, 247-266E)
 g1999u07.bin       GEOID99 grid #7 for CONUS (24-42N, 264-283E)
 g1999u08.bin       GEOID99 grid #8 for CONUS (24-42N, 281-300E)
 g1999a01.bin       GEOID99 grid #1 for Alaska (60-72N, 172-204E)
 g1999a02.bin       GEOID99 grid #2 for Alaska (60-72N, 202-234E)
 g1999a03.bin       GEOID99 grid #3 for Alaska (49-61N, 172-204E)
 g1999a04.bin       GEOID99 grid #4 for Alaska (49-61N, 202-234E)
 g1999h01.bin       GEOID99 grid #1 for Hawaii (18-24N, 199-206E)
 g1999p01.bin       GEOID99 grid #1 for Puerto Rico/VI (15-21N, 291-296E)

What do the filenames indicate about the type of data they contain? 
      A typical filename, "tyyyyrnn.fff", would indicate: 
            t: The type of data contained in the file 
                  t = g means hybrid geoid model undulations (i.e. GEOID96, GEOID99) 
                  t = s means gravimetric geoid model undulations (i.e. G99SSS, G96SSS) 
                  t = x means Deflections of the vertical in the North/South direction (Xi) 
                  t = e means Deflections of the vertical in the East/West direction (Eta) 
            yyyy: The year the data was created 
            r: The main region where the data are located 
                  r = u means "Conterminous USA" 
                  r = a means "Alaska" 
                  r = h means "Hawaii" 
                  r = p means "Puerto Rico and the American Virgin Islands" 
            nn: The sub-region number of this file 
                  CONUS, has 8 overlapping sub-regions (nn=01 to 08) 
                  Alaska, has 4 overlapping sub-regions (nn=01 to 04) 
                  Hawaii has1 sub-region (nn=01) 
                  Puerto Rico and the American Virgin Islands has 1 sub-region (nn=01) 
            fff: The format of the data file 
                  fff = bin means FORTRAN 77 direct access binary file 
                  fff = asc means ASCII file 
      So, for example, "g1999u01.bin" means "GEOID99 in CONUS, sub-grid #1, in binary" 


file formats:
Bytes    Data    Variab     Variable
               Type    Name       Description
       1- 8    real*8  glamn      Southermost Latitude of grid (decimal degrees)
       9-16    real*8  glomn      Westernmost Longitude of grid (decimal degrees) 
      17-24    real*8  dla        Latitude spacing of grid (decimal degrees)
      25-32    real*8  dlo        Longitude spacing of grid (decimal degrees)
      33-36    int*4   nla        Number of rows of grid
      37-40    int*4   nlo        Number of columns of grid
      41-44    int*4   ikind      Set to "1", meaning the gridded data is "real*4"

      45-48    real*4  data(1,1)  Gridded value at element 1,1 (Southwest corner)

real*8 is an 8 byte double value
real*4 is a  4 byte float value
int*4  is a 4 byte integer value


The actual numbers of rows (nla) and columns (nlo) for each sub-grid is the same within each region but varies between regions: 

              REGION                          ROWS  COLUMNS
                                              (nla) (nlo)

          Conterminous United States          1081   1141
          Alaska                               721   1921
          Hawaii                               361    421
          Puerto Rico and the Virgin Islands   361    301

