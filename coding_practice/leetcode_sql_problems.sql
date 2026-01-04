-- 1174. Immediate Food Delivery II
-- https://leetcode.com/problems/immediate-food-delivery-ii/description/?envType=study-plan-v2&envId=top-sql-50

-- First thoughts:

select round(avg(case when order_date = customer_pref_delivery_date then 100.00 else 0.00 end),2) immediate_percentage
from (select row_number() over (partition by customer_id order by order_date asc,delivery_id asc) first_order, *
from delivery) as t1
where first_order =1;

-- If we order by delivery_id asc we handle multple orders on the same day as well but it's not required for this question.
select round(avg(case when order_date = customer_pref_delivery_date then 100.00 else 0.00 end),2) immediate_percentage
from (select row_number() over (partition by customer_id order by order_date asc,delivery_id asc) first_order, *
from delivery) as t1
where first_order =1;

-- Optimized,different way of doing it if there are indexes, if no index then this is terrible
select round(avg(case when order_date = customer_pref_delivery_date then 100.00 else 0.00 end),2) immediate_percentage
from delivery
where (customer_id, order_date) in 
(select customer_id, min(order_date)
from delivery 
group by customer_id );

--550. Game Play Analysis IV
--https://leetcode.com/problems/game-play-analysis-iv/description/?envType=study-plan-v2&envId=top-sql-50
-- Non optimized way
select round(count(a.player_id)*1.00/(select count(distinct player_id) from activity),2) as fraction
from
(select player_id,min(event_date) first_login
from activity
group by player_id) first_login 
left join activity a on a.player_id = first_login.player_id
and a.event_date = first_login.first_login + interval '1 day';

-- Optimized using window functions
