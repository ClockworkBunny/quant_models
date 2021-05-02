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
4. Alter Table
```
ALTER TABLE table
CHANGE oldColumnName newColumnName <datatype> <restrictions>;
```

```
ALTER TABLE Actors MODIFY First_Name varchar(20) DEFAULT "Anonymous";
ALTER TABLE Actors MODIFY First_Name varchar(300);
ALTER TABLE Actors ADD MiddleName varchar(100);
ALTER TABLE Actors DROP MiddleName;
ALTER TABLE Actors ADD MiddleName varchar(100) AFTER DoB;
#we'll drop the middle name column and add it after the date of birth (DoB) column as follows
```

5.
```
SELECT * FROM Actors WHERE NOT EXISTS (SELECT * FROM DigitalAssets WHERE BINARY URL LIKE "%good%");
```
Here, BINARY is makeing the string comparsion as case-sensitive.
```
