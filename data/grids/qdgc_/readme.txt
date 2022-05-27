QDGC tables delivered in geopackage file
- - - - - - - - - - - - - - - - - - - - - -
QDGC represents a way of making (almost) equal area squares covering a specific area to represent specific qualities of the area covered. The squares themselves are based on the degree squares covering earth. Around the equator we have 360 longitudinal lines , and from the north to the south pole we have 180 latitudinal lines. Together this gives us 64800 segments or tiles covering earth.

Within each geopackage file you will find a number of tables with these names:
-tbl_qdgc_01
-tbl_qdgc_02
-tbl_qdgc_03
-tbl_qdgc_04
-tbl_qdgc_05
-etc

The attributes for each table are:
qdgc  Unique Quarter Degree Grid Cell reference string
level_qdgc  QDGC level
cellsize  degrees decimal degree for the longitudal and latitudal length of the cell
lon_center  Longitude center of the cell
lat_center  Latitudal center of the cell
area_km2  Calculated area for the cell
geom  Geometry

Metadata
--------
Geodata GCS_WGS_1984
Datum: D_WGS_1984
Prime Meridian: 0

Areas are calculated with different versions of Albers Equal Area Conic using the PostGIS function st_area. For the African continent I have used Africa Albers Equal Area Conic which will look like this:
- st_area(st_transform(geom, 102022))/1000000)

Conditions
----------
Delivered to the user as-is. No guarantees. If you find errors, please tell me and I will try to fix it. Suggestions for improvements can be addressed to the github repository: https://github.com/ragnvald/qdgc

Thankyou!
--------
The work has over the years been supported and received advice and moral support from many organisations and stakeholders. Here are some of them:
- TAWIRI (http://tawiri.or.tz/)
- Dept of Biology, NTNU, Norway
- Norwegian Environment Agency
- Eivin Røskaft, Steven Prager, Howard Frederick, Julian Blanc, Honori Maliti, Paul Ramsey

References
----------
* http://en.wikipedia.org/wiki/QDGC
* http://www.mindland.com/wp/projects/quarter-degree-grid-cells/about-qdgc/
* http://en.wikipedia.org/wiki/Lambert_azimuthal_equal-area_projection
* http://www.safe.com
