-- create table provincecheck
-- (	province varchar(10), 
-- 		cnprovince varchar(10)
-- )

select provincecheck.cnprovince, round(avg(amount)), max(amount), min(amount)
from provincecheck, users, orderitem
where users.user_id = orderitem.user_id
and provincecheck.province = users.province
group by cnprovince
order by avg(amount) desc