-- 给定商品的id为4600

select shopname
from merchant
where mer_id in (
	select mer_id
    from mergoods
    where goods_id = 4600
    order by price
    )
limit 0,5