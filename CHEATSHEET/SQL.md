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
