-- SELECT distinct sector FROM "sp500_company_data"."main"."sp500_company_data"
-- order by 1 asc;

-- SELECT * FROM "sp500_company_data"."main"."sp500_company_data"
-- where lower(name) like 'john%'
-- order by 1 asc;


select symbol,name,sector,price,("market cap")/1000000000 as market_cap_in_Billion from "sp500_company_data"."main"."sp500_company_data"
where sector in ('Health Care Facilities','Biotechnology','Pharmaceuticals')
order by "Market Cap" desc;


select * from news_articles;

