select a.mer_id, goods.goods_name, a.sales_, a.sales_rank
from
(
	select 
    mer_id, 
	goods_id, 
    sales AS sales_, 
    row_number() over (partition by mer_id order by sales desc) as sales_rank
    from mergoods
    group by mer_id, goods_id) a
    left join goods on a.goods_id = goods.goods_id
where a.sales_rank <=3
order by mer_id, sales_rank