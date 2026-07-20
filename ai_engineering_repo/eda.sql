-- SELECT distinct sector FROM "sp500_company_data"."main"."sp500_company_data"
-- order by 1 asc;

-- SELECT * FROM "sp500_company_data"."main"."sp500_company_data"
-- where lower(name) like 'john%'
-- order by 1 asc;


select * from "sp500_company_data"."main"."sp500_company_data"
where sector in ('Health Care Facilities','Biotechnology','Pharmaceuticals');
