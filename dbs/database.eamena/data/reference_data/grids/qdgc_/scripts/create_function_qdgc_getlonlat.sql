-- FUNCTION: public.qdgc_getlonlat(double precision, double precision)

-- DROP FUNCTION public.qdgc_getlonlat(double precision, double precision);

CREATE OR REPLACE FUNCTION public.qdgc_getlonlat(
	lon_value double precision,
	lat_value double precision)
    RETURNS text
    LANGUAGE 'plpython3u'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
"""Put character in front of longitudal value"""
if lon_value < 0:
	square = 'W'
else:
	square = 'E'
            
"""Find absolute value for longitude"""
lon_string=str(int(abs(lon_value)))

"""The longitudal value of the square is printed with three decimals"""
square = square + (lon_string).zfill(3)

"""Put character in front of latitudal value"""
if  lat_value < 0 :
	square = square + 'S'
else:
	square = square + 'N'

"""find absolute value for latitude"""
lat_string=str(int(abs(lat_value)))

"""find int lat. Remember that latitudes absolute values never excceed 90"""
square = square + (lat_string).zfill(2)
    
return square
$BODY$;

ALTER FUNCTION public.qdgc_getlonlat(double precision, double precision)
    OWNER TO postgres;
