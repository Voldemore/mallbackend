select user_id, goods_id, count(*)
from orderitem
group by user_id