-- We want to mimick a cube dataset with 1 fact column stored as vectors 
-- (like for example daily P&L values or MtM values like in the financial risk domain)

-- VAR 5% simulation of P&L vectors
select str0, arraySort(sumForEach(arrFloat))[50] as arr1 from factTable group by str0
select str0, str1, int10, int11, dttime10, dttime11, arraySort(sumForEach(arrFloat))[50] as arr1 from factTable group by str0, str1, int10, int11, dttime10, dttime11
select str0, str1, str2, str3, int10, int11, int12, int13, dttime10, dttime11, dttime12, dttime13, arraySort(sumForEach(arrFloat))[50] as arr1 from factTable group by str0, str1, str2, str3, int10, int11, int12, int13, dttime10, dttime11, dttime12, dttime13
-- Flatten vectors of P&L
select str0, num, pl from (select str0, sumForEach(arrFloat) as arr1 from factTable WHERE str1= 'KzORBHFRuFFOQm' group by str0) array join arr1 as pl, arrayEnumerate(arr1) as num
