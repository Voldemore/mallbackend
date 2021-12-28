select mer_id, round(sum(price * sales))
from mergoods
where goods_id in (
	select goods_id
    from orderitem
    where add_time > '2021-01-01'
    and add_time < '2021-12-31' )
group by mer_id
order by mer_id