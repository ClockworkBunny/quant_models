## Some SQL Command

1. Order By
```
SEKECT col, col2, ..., coln
FROM table
WHERE col3 LIKE "%somestring%"
ORDER BY col3
```
```
SELECT FirstName, SecondName from Actors ORDER BY NetWorthInMillions DESC LIMIT 4 OFFSET 3;
# retrueve the next 4 richest actors after the top three
```
2. Delete
```
DELETE FROM table
WHERE col3 > 5
ORDER BY col1
LIMIT 5;
```

```
DELETE FROM Actors ORDER BY NetWorthInMillions DESC LIMIT 3;
# we want to delete the top three actresses by net worth. We can accomplish that by using the ORDER BY and LIMIT clauses
```

Then, TRUNCATE table; will remove all rows in the table

3. Update Table
```
UPDATE table
SET col1=val1, col2=val2,...coln=valn
WHERE <condition?
ORDER BY col5
LIMIT 5;
```
