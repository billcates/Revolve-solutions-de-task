Sql Assignment solutions 

1)Which manufacturer's planes had most no of flights? And how many flights?


Ans-
BOEING, 1630

select manufacturer,count(distinct tailnum) as ct_planes
from planes
group by 1
order by 2 desc
limit 1


2)Which manufacturer's planes had most no of flying hours? And how many hours?

Ans-
BOEING , 236463

select a.manufacturer,sum(cast((case when air_time= 'NA' then '0' else air_time end) as int)) 
from planes a 
join flights b on a.tailnum=b.tailnum
group by 1 
order by 2 desc 


3) Which plane flew the most number of hours? And how many hours?

Ans-
N322AA ,2038

select tailnum,sum(cast((case when air_time= 'NA' then '0' else air_time end) as int)) as total_fly_hours
from flights 
group by 1
order by 2 desc

4)Which destination had most delay in flights?

Ans-

Dallas/Fort Worth International Airport, DFW, 1618

select b.airport,a.dest,sum(cast((case when a.arr_delay= 'NA' then '0' else a.arr_delay end) as int)) as total_delay_hours 
from flights a 
join airports b
on a.dest=b.IATA_CODE
group by 1 
order by 2 desc limit 1

5) Which manufactures planes had covered most distance? And how much distance?

Ans-

BOEING, 1644180

select b.manufacturer,sum(a.distance) as s
from flights a
join planes b
on a.tailnum=b.tailnum
group by 1 
order by 2 DESC

6) Which airport had most flights on weekends?

Ans -

John F. Kennedy International Airport (New York International Airport) , 324

with cte as(
select origin,dest,tailnum,format('%s-%s-%s', "year", "month", "day")::date as dt
from flights
),
final as(
select origin as code,dt,tailnum
from cte
WHERE EXTRACT(ISODOW FROM dt) IN (6, 7)
union ALL
select dest as code,dt,tailnum
from cte
WHERE EXTRACT(ISODOW FROM dt) IN (6, 7)
)
select b.AIRPORT,count(a.tailnum)
from FINAL a
join airports b
on a.code=b.IATA_CODE
group by 1
order by 2 desc


