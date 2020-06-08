# This script will automatically run a specified query against an Oracle database for large number of items in a WHERE clause. 
# This script requires several arguments and files to run:

# *Note: Files must be in the same directy as the script to be able to run

# 1a) Excel workbook with the list of items for the WHERE clause - argument: -w "WorkbookName.xlsx"
# 1b) The name of the sheet in the workbook with the list of items - argument: -s "SheetName"
# 1c) The name of the columns in the sheet with the list of items - argument: -c "ColumnName"
# 2) A text file containing the query you would like to run. Note that you can add/modify parameters 
# in the query, however you will have to also modify the script below - argument: -q "QueryName.txt"
# 3) Limit of the items you want to query at once, or limit of RDMS in your WHERE clause 
# # (i.e. PL/SQL limits only 1000 items in WHERE clause) - argument: -l int (Ex: -l 1000)

# The script will also prompt the user for their Oracle DB host, port, service name, username, and password

import argparse
import pandas as pd
import cx_Oracle
import csv

def generate_header(writer):
    print("Generating headers")
    col_names = [row[0] for row in cursor.description]
    writer.writerow(col_names)

# Generate query    
def generate_query(working_list, number, query):
    
    subset = working_list[:number]
    #print("Subset: %s" % subset) # DEBUG
    
    batch_size = 1000

    q_file = open(query, "r")
    query = q_file.read()

    join1a = 'data1.table_a'
    join2a = 'data1.table_b'

    join1b = 'data2.table_a'
    join2b = 'data2.table_b'

    sql_a = query % (join1a, join2a, (' '.join(subset)))
    sql_b = query % (join1b, join2b, (' '.join(subset)))

    try:
        cursor.execute(sql_a)
        #print("SQL Query: %s" % sql_a) #DEBUG

    except:
        cursor.execute(sql_b)
        #print("SQL Query: %s" % sql_b) #DEBUG

    print("Executing SQL query...")

    writer = csv.writer(csv_file, delimiter=',', lineterminator="\n", quoting=csv.QUOTE_NONNUMERIC)

    generate_header(writer)
    
    # retrieve query results
    try:
        while True:
            rows = cursor.fetchmany(batch_size)
            #rows = cursor.fetchall()
            #print("Results: %s" % rows)  #DEBUG

            if not rows:
                break

            for row in rows:
                writer.writerow(row)

    except cx_Oracle.Error as error:
        print(error)
        error_file = open("error_log.txt", "a")
        error_file.write(str(error))
        error_file.close()

    del working_list[:number]
    print("Updated workling list - remaining list items: %s" % str(len(working_list)))
    

# Prep data for querying
def prep_data(workbook, sheet, limit, column, query):
    print("Opening workbook..")
    w = pd.ExcelFile(workbook)

    # Read entire sheet
    print("Reading '%s' workbook and '%s' sheet." % (workbook, sheet))
    s = w.parse(sheet)

    # find column indicated in args and convert series to list
    print("Converting column to list..")
    col_ind = s.columns.get_loc(column)
    excel_list = s.iloc[ :, col_ind].tolist()

    #print("excel list: %s" % excel_list) #DEBUG
    #print() #DEBUG

    working_list = []

    x = limit
    #print("limit %s" % limit) #DEBUG
    string = ''

    # prep list for WHERE clause by adding ' ', around each element
    while len(excel_list) != 0:
        try:
            for n in range(x):
                if n != x-1:
                    string = "'%s'," % excel_list[n]
                    working_list.append(string)
                else:
                    string = "'%s'" % excel_list[n]
                    working_list.append(string)
        except:
            break

        del excel_list[:x]
        #print("working list: %s " % working_list) #DEBUG
        #print() #DEBUG
        #print("excel_list:  %s " % excel_list) #DEBUG

    # remove comma from last item in list for WHERE clause
    last_item = working_list[-1]
    working_list[-1] = last_item.replace(",", "")
    
    #print("working_list: %s " % working_list) #DEBUG
    # print()  #DEBUG
    # print("excel_list:  %s " % excel_list) #DEBUG

    counter = 1
    while len(working_list) != 0:
        print("\nExecuting query batch #%s" % counter)
        generate_query(working_list, limit, query)
        counter += 1


# Run the program
if __name__ == "__main__":
    try:
        # Argument Parser
        parser = argparse.ArgumentParser()
        parser.add_argument("-w", "--workbook", required=True, 
            help="Name of workbook")
        parser.add_argument("-s", "--sheet", required=True, 
            help="Name of sheet")
        parser.add_argument("-l", "--limit", required=True, 
            help="Limit of items in where clause")
        parser.add_argument("-c", "--column", required=True, 
            help="Choose column name")
        parser.add_argument("-q", "--query", required=True, 
            help="Name of query file")

        args = parser.parse_args()

        workbook = args.workbook
        sheet = args.sheet
        limit = args.limit
        column = args.column
        query = args.query

        # convert limit to int from args
        limit = int(limit)

        # connect to Oracle DB. Prompt user for host, port, service name, username, and password
        host = input("Enter the Oracle DB host: ")
        port = input("Enter the Oracle DB port: ")
        servicename = input("Enter the Oracle DB service name: ")
        dsn_tns = cx_Oracle.makedsn(host=host, port=port, service_name=servicename) 

        user = input("Enter your Oracle DB Username: ")
        password = input("Enter your Oracle DB Password: ")
        conn = cx_Oracle.connect(user=user, password=password, dsn=dsn_tns) 
        cursor = cx_Oracle.Cursor(conn)

        #  create csv file for outputting query results
        csv_file = open("query_results.csv", "w")
        writer = csv.writer(csv_file, delimiter=',', lineterminator="\n", quoting=csv.QUOTE_NONNUMERIC)

        print("Prepping data..")
        prep_data(workbook, sheet, limit, column, query)

        cursor.close()
        conn.close()
        csv_file.close()

        print("Queries completed!")
    
    except Exception as e:
        print("Error: %s" % e)