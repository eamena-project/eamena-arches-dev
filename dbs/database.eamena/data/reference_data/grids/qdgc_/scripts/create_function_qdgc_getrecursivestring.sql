-- FUNCTION: public.qdgc_get_recursivestring(double precision, double precision, integer, text)

-- DROP FUNCTION public.qdgc_getrecursivestring(double precision, double precision, integer, text);

CREATE OR REPLACE FUNCTION public.qdgc_getrecursivestring(lon_value double precision, 
														   lat_value double precision, 
														   depthlevel integer, 
														   square text)
RETURNS setof text
LANGUAGE plpgsql
as $$

declare
	stringlength int;
	lon_value_passon double precision;
	lat_value_passon double precision;
begin   
	if lon_value >1 then
		lon_value = lon_value - floor(lon_value);
	elseif (lon_value<-1) then
		lon_value = lon_value + abs(ceil(lon_value));
	end if;
	
	if  lat_value >1 then
		lat_value = lat_value - floor(lat_value);
	elseif (lat_value<-1) then
		lat_value = lat_value + abs(ceil(lat_value));
	end if;

	if ((lon_value>=0) and (lat_value>=0)) then

		if ((lon_value <0.5) and (lat_value>=0.5)) then
			square =  square||'A';
			lon_value=lon_value*2;
			lat_value=(lat_value-0.5)*2;

		elseif ((lon_value>=0.5) and (lat_value>=0.5)) then
			square = square||'B';
			lon_value=(lon_value-0.5)*2;
			lat_value=(lat_value-0.5)*2;

		elseif ((lon_value<0.5) and (lat_value<0.5)) then
			square = square||'C';
			lat_value=lat_value*2;
			lon_value=lon_value*2;


		elseif ((lon_value>=0.5) and (lat_value<0.5)) then
			square =  square||'D';
			lon_value = ((lon_value-0.5)*2);
			lat_value = lat_value*2;
	
		end if;

	elseif ((lon_value>=0) and (lat_value<=0)) then

		if ((lon_value <0.5) and (lat_value>-0.5)) then
			square = square||'A';
			lon_value=lon_value*2;
			lat_value=lat_value*2;

		elseif ((lon_value>=0.5) and (lat_value>-0.5)) then
			square = square||'B';
			lon_value=(lon_value-0.5)*2;
			lat_value=lat_value*2;

		elseif ((lon_value<0.5) and (lat_value<=-0.5)) then
			square = square||'C';
			lon_value=lon_value*2;
			lat_value=(lat_value+0.5)*2;

		elseif ((lon_value>=0.5) and (lat_value<=-0.5)) then
			square = square||'D';
			lon_value=(lon_value-0.5)*2;
			lat_value=(lat_value+0.5)*2;
			
		end if;

	elseif ((lon_value<=0) and (lat_value<=0)) then

		if ((lon_value<=-0.5) and (lat_value>-0.5)) then
			square = square||'A';
			lon_value=(lon_value+0.5)*2;
			lat_value=lat_value*2;

		elseif ((lon_value>-0.5) and (lat_value>-0.5)) then
			square = square||'B';
			lon_value=lon_value*2;
			lat_value=lat_value*2;

		elseif ((lon_value<=-0.5) and (lat_value<=-0.5)) then
			square = square||'C';
			lon_value=(lon_value+0.5)*2;
			lat_value=(lat_value+0.5)*2;

		elseif ((lon_value>-0.5) and (lat_value<=-0.5)) then
			square = square||'D';
			lon_value=lon_value*2;
			lat_value=(lat_value+0.5)*2;
		end if;

	elseif ((lon_value<=0) and (lat_value>=0)) then

		if ((lon_value <=-0.5) and (lat_value>=0.5)) then
			square = square||'A';
			lon_value=(lon_value+0.5)*2;
			lat_value=(lat_value-0.5)*2;

		elseif ((lon_value>-0.5) and (lat_value>=0.5)) then
			square = square||'B';
			lon_value=lon_value*2;
			lat_value=(lat_value-0.5)*2;

		elseif ((lon_value<=-0.5) and (lat_value<0.5)) then
			square = square||'C';
			lon_value=(lon_value+0.5)*2;
			lat_value=(lat_value)*2;

		elseif ((lon_value>-0.5) and (lat_value<0.5)) then
			square = square||'D';
			lon_value=lon_value*2;
			lat_value=lat_value*2;
		
		end if;
		
	end if;
	

	stringlength = length(square);

	if (stringlength < depthlevel) then
		lon_value_passon = lon_value;
		lat_value_passon = lat_value;

		return query select * from qdgc_getrecursivestring(lon_value,lat_value,depthlevel,square);

	else	
		return next square;
	
    end if;
	
end $$;
