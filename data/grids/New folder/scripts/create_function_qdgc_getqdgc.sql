-- FUNCTION: public.qdgc_get_qdgc(double precision, double precision, integer)

-- DROP FUNCTION public.qdgc_get_qdgc(double precision, double precision, integer);

CREATE OR REPLACE FUNCTION public.qdgc_get_qdgc(
	lon_value double precision,
	lat_value double precision,
	depthlevel integer)
    RETURNS SETOF text 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
declare
	returnstring text;
	temp_row text;
	lonlat text;
	qdgc text;
begin

	return query select qdgc_getlonlat(lon_value,lat_value)||qdgc_getrecursivestring(lon_value,lat_value,depthlevel,'');

	
end
$BODY$;
