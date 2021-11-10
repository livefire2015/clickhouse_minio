
-- list partition values
select distinct partition from factTable format TabSeparated

-- SQL select to export partition data i to Redshift in a flatten format
-- replace i in the SQL statement
select factTable.*, num from factTable ARRAY JOIN arrFloat as arrFloat, arrayEnumerate(arrFloat) as num where partition = {i} format CSV
