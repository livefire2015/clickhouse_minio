/* Q1. Maximum loss with a 95% confidence (5% quantile) for a single dimension. */

SELECT
    str0,
    arraySort(sumForEach(arrFloat))[50] AS arr1
FROM factTable
GROUP BY str0;

/* Q2. Maximum loss with a 95% confidence (5% quantile) for a group of 6 dimensions. */

SELECT
    str0, str1, int10, int11, dttime10, dttime11,
    arraySort(sumForEach(arrFloat))[50] AS arr1
FROM factTable
GROUP BY
    str0, str1, int10, int11, dttime10, dttime11;
    
/* Q3. Maximum loss with a 95% confidence (5% quantile) for a group of 12 dimensions. */

SELECT
    str0, str1, str2, str3, int10, int11, int12, int13, dttime10, dttime11, dttime12, dttime13,
    arraySort(sumForEach(arrFloat))[50] AS arr1
FROM factTable
GROUP BY
    str0, str1, str2, str3, int10, int11, int12, int13, dttime10, dttime11, dttime12, dttime13

/* Q4. Query with a filter and unfold results to rows. */

SELECT
    str0, num, pl
FROM (
    SELECT str0, 
              sumForEach(arrFloat) AS arr1
    FROM factTable
    WHERE str1 = 'KzORBHFRuFFOQm'
    GROUP BY str0
)
ARRAY JOIN
    arr1 AS pl,
    arrayEnumerate(arr1) AS num;
