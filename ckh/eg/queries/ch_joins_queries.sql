/* Q1 */

SELECT 
    str0,
    quantileExact(0.05)(val)
FROM (
    SELECT 
        str0,
        sum(value) AS val
    FROM factCube
    INNER JOIN factTable_join USING (index)
    GROUP BY str0, position
)
GROUP BY str0
ORDER BY str0

/* Same query using LIMIT BY is more compact: */

SELECT
    str0,
    sum(value) AS val
FROM factCube
INNER JOIN factTable_join USING (index)
GROUP BY str0, position
ORDER BY str0, val
LIMIT 49, 1 BY str0

/* Q2 */

SELECT
    str0, str1, int10, int11, dttime10, dttime11,
    sum(value) AS val
FROM factCube
INNER JOIN factTable_join USING (index)
GROUP BY
    str0, str1, int10, int11, dttime10, dttime11,
    position
ORDER BY
    str0, str1, int10, int11, dttime10, dttime11,
    val
LIMIT 49, 1 BY
    str0, str1, int10, int11, dttime10, dttime11;

/* Q3 */

SELECT
    str0, str1, str2, str3, int10, int11, int12, int13, dttime10, dttime11, dttime12, dttime13,
    sum(value) AS val
FROM factCube
INNER JOIN factTable_join USING (index)
GROUP BY
    str0, str1, str2, str3, int10, int11, int12, int13, dttime10, dttime11, dttime12, dttime13,
    position
ORDER BY
    str0, str1, str2, str3, int10, int11, int12, int13, dttime10, dttime11, dttime12, dttime13,
    val
LIMIT 49, 1 BY
    str0, str1, str2, str3, int10, int11, int12, int13, dttime10, dttime11, dttime12, dttime13; 
    
/* Q4 */

SELECT
    str0,
    sum(value) AS val,
    position
FROM factCube
INNER JOIN factTable_join USING (index)
WHERE str1 = 'KzORBHFRuFFOQm'
GROUP BY str0, position;