--620. Not Boring Movies
--https://leetcode.com/problems/not-boring-movies/description/?envType=study-plan-v2&envId=top-sql-50
select * from cinema
where id%2=1 and description <> 'boring'
order by rating desc;


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


--511. Game Play Analysis I
--https://leetcode.com/problems/game-play-analysis-i/description/
select player_id, min(event_date) first_login
from activity
group by player_id;





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

-- Optimized using min window functions, runtime : 491 ms
select round(sum(is_retained::int)::decimal/count(distinct player_id),2) as fraction
from 
(select player_id, 
(event_date = (min(event_date) over (partition by player_id) + interval '1 day'))::int as is_retained
from activity)

-- optimized using array_agg and filter clause, runtime
with player_stats as 
(select player_id, min(event_date) = Any(array_agg(event_date - interval '1 day')) as qualified
from activity
group by player_id)
select round(count(*) filter (where qualified)::decimal /count(player_id),2) as fraction
from player_stats;

--usine lead function
WITH temp AS (
    SELECT 
        player_id, 
        event_date,
        DENSE_RANK() OVER (PARTITION BY player_id ORDER BY event_date) AS login_rank, 
        -- Corrected: Get the NEXT date, THEN compare it
        LEAD(event_date) OVER (PARTITION BY player_id ORDER BY event_date) = (event_date + INTERVAL '1 day') AS next_date_qualify
    FROM activity
)
SELECT 
    ROUND(
        COUNT(DISTINCT player_id) FILTER (WHERE next_date_qualify)::DECIMAL 
        / COUNT(DISTINCT player_id), 
        2
    ) AS fraction
FROM temp
WHERE login_rank = 1;


--2356. Number of Unique Subjects Taught by Each Teacher
-- https://leetcode.com/problems/number-of-unique-subjects-taught-by-each-teacher/description/?envType=study-plan-v2&envId=top-sql-50
select teacher_id, count(distinct subject_id) cnt
from teacher 
group by teacher_id;

--619. Biggest Single Number
--https://leetcode.com/problems/biggest-single-number/description/?envType=study-plan-v2&envId=top-sql-50
-- first thoughts
select max(num) num from 
(select num
from mynumbers
group by num having count(num)=1);