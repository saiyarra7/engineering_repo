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


-- 1731. The Number of Employees Which Report to Each Employee
-- https://leetcode.com/problems/the-number-of-employees-which-report-to-each-employee/?envType=study-plan-v2&envId=top-sql-50
with manager_data as (select reports_to employee_id, count(*) reports_count, round(avg(age::decimal),0) average_age
from employees
where reports_to is not null 
group by reports_to)
select manager_data.employee_id, e.name, manager_data.reports_count, manager_data.average_age 
from manager_data inner join employees e on e.employee_id = manager_data.employee_id
order by manager_data.employee_id;


--1978. Employees Whose Manager Left the Company
-- https://leetcode.com/problems/employees-whose-manager-left-the-company/?envType=study-plan-v2&envId=top-sql-50
--initial thoughts
select employee_id 
from employees 
where salary<30000
and manager_id not in (select employee_id from employees where manager_id is not null)
order by employee_id asc;

-- optimized
select e.employee_id
from employees e 
left join employees m on m.employee_id=e.manager_id
where e.salary<30000
and e.manager_id is not null
and m.employee_id is null
order by 1 asc;

--https://leetcode.com/problems/list-the-products-ordered-in-a-period/submissions/?envType=study-plan-v2&envId=top-sql-50
--1327. List the Products Ordered in a Period
-- Initial thoughts
select p.product_name, uc.unit
from products p
inner join (select product_id, sum(unit) as unit
from orders 
where to_char(order_date, 'YYYY-MM') = '2020-02'
group by product_id) as uc
on uc.product_id=p.product_id
where uc.unit>=100;

--optimized
select p.product_name, sum(o.unit) unit
from products p inner join orders o
on o.product_id=p.product_id
where order_date>='2020-02-01' and order_date<'2020-03-01'
group by 1 having sum(o.unit)>= 100;

--https://leetcode.com/problems/user-activity-for-the-past-30-days-i/description/?envType=study-plan-v2&envId=top-sql-50
--1141. User Activity for the Past 30 Days I
select activity_date as day, count(distinct user_id) active_users
from activity
where activity_date > ('2019-07-27'::date - interval '30 day') and activity_date<= '2019-07-27'
group by activity_date;


--https://leetcode.com/problems/product-sales-analysis-iii/description/?envType=study-plan-v2&envId=top-sql-50
--1070. Product Sales Analysis III
with fy as 
(select product_id, min(year) as first_year
from sales
group by product_id)
select fy.product_id, fy.first_year, quantity, price
from sales s inner join fy on s.product_id = fy.product_id 
and s.year=fy.first_year;


--https://leetcode.com/problems/classes-with-at-least-5-students/description/?envType=study-plan-v2&envId=top-sql-50
--596. Classes With at Least 5 Students
select class 
from
(select class, count(student) no_of_students
from courses
group by class) a
where no_of_students>=5;

--other way
select class 
from courses 
group by class having count(student)>=5;

--https://leetcode.com/problems/find-followers-count/description/?envType=study-plan-v2&envId=top-sql-50
--1729. Find Followers Count
select user_id, count(follower_id) as followers_count
from followers
group by user_id
order by user_id asc;

--https://leetcode.com/problems/customers-who-bought-all-products/description/?envType=study-plan-v2&envId=top-sql-50
--1045. Customers Who Bought All Products
--first thoughts
with cnt as (select customer_id, count(distinct c.product_key) cnt
from customer c inner join product p on p.product_key = c.product_key
group by customer_id)
select cnt.customer_id 
from cnt 
where cnt.cnt = (select count(product_key) from product);
--better, no need to even join the tables.
with cnt as (select customer_id, count(distinct c.product_key) cnt
from customer c
group by customer_id)
select cnt.customer_id 
from cnt 
where cnt.cnt = (select count(product_key) from product);
-- KISS
select customer_id
from customer 
group by customer_id 
having count(distinct product_key) = (select count(product_key) from product);


--https://leetcode.com/problems/triangle-judgement/description/?envType=study-plan-v2&envId=top-sql-50
--610. Triangle Judgement
--initial thoughts, but looses on edge cases cause any side can be negative too
select x,y,z, case when x+y>z and y+z>x and x+z>y then 'Yes' else 'No' end as triangle
from triangle;

--edge case 
select x,y,z, 
case when least(x,y,z)<=0 then 'No' 
when x+y>z and y+z>x and x+z>y then 'Yes' 
else 'No' end as triangle
from triangle;


-- https://leetcode.com/problems/primary-department-for-each-employee/?envType=study-plan-v2&envId=top-sql-50
-- 1789. Primary Department for Each Employee
--first thoughts.
select e.employee_id, e.department_id
from employee e
where e.primary_flag = 'Y'
union all
select employee_id, department_id
from employee where employee_id in 
(select employee_id
from employee
group by employee_id
having count(department_id) = 1);

--window function optimized approach
with temp as 
(select employee_id, department_id, primary_flag, count(*) over (partition by employee_id) cnt
from employee)
select employee_id, department_id
from temp
where primary_flag = 'Y' or cnt = 1;


-- https://leetcode.com/problems/consecutive-numbers/?envType=study-plan-v2&envId=top-sql-50
-- 180. Consecutive Numbers
-- Brute force logic
with temp as (select a.id, a.num as num_1, b.num as num_2, c.num as num_3
 from logs a
left join logs b on a.id +1 = b.id
left join  logs c on a.id +2 = c.id)
select distinct ConsecutiveNums from (select case when num_1 = num_2 and num_1=num_3 then num_1 else null end as ConsecutiveNums
from temp)
where ConsecutiveNums is not null;

-- self join simple
select distinct a.num as ConsecutiveNums
 from logs a
left join logs b on a.id +1 = b.id
left join  logs c on a.id +2 = c.id
where a.num=b.num and a.num=c.num;

--Optimized
with temp as 
(select num as num1, lead(num,1) over (order by id) as num2,
lead(num,2) over (order by id) as num3
from logs)
select distinct num1 as ConsecutiveNums
from temp
where num1=num2 and num1=num3;

