--Query will group values from rows into a single column
--separated by delimiter specified. In the example below,
--query will group by ID and YEAR_DateField and then create two
--new columns each containing all their respective unique values.
--All unique values for item1 will be in all_item_1 column 
--separated by ; for each grouping of ID and YEAR_DateField. Same
--for the new colum for all_item_2

SELECT c.ID, c.YEAR_DateField,
    STUFF((SELECT DISTINCT '; ' + x.item1
            FROM   table_x x
            WHERE  c.ID = x.ID
            AND c.YEAR_DateField = x.YEAR_DateField
            FOR XML PATH ('')),1,2,'') AS all_item_1,
   
   STUFF((SELECT DISTINCT '; ' + x.item2
            FROM   table_x x
            WHERE  c.ID = x.ID
            AND c.YEAR_DateField = x.YEAR_DateField
            FOR XML PATH ('')),1,2,'') AS all_item_2
FROM table_x c
GROUP BY c.ID, c.YEAR_DateField