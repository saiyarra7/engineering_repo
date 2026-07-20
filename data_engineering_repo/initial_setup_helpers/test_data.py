Customer
cust_id	products
1111	1234
1112	1235
1113	1236
1114	1237
1115	1238
1116	1239
 
 

 
 
Products	 	 	 	 	 
prod_if	group_id	state	gender	lob	dob
1234	123	TX	M	Large Group	3/25/1990
1235	121	MO	M	National	8/1/1982
1236	122	GA	F	Small Group	12/15/1994
1237	123	KS	M	Large Group	4/28/1962
1238	125	CA	F	Large Group	1/4/1975
1239	123	FL	F	National	9/12/1987
 
 
 
Call_Data	 	 	 
cust id	Prod_id	call_reason	complaims
1111	1234	benefits	benefits
1112	1235	claims	claims
1113	1236	otc	otc
1114	1237	pcp	pcp
1115	1238	benefits	benefits
1116	1239	claims	claims
 
 
db_name = external_db
host_name = ""
port = '5632'
username = 'readonly_user'
password = 'readonly_password'

with connection a

select cd.cust_id,cd.prod_id, cd.call_reason, cd.complains,  from call_date cd 
inner join products p on p.prod_id = cd.prod_id
order by cust_id asc;