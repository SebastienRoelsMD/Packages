import pandas as pd
import pyodbc

### Convert a pyodbc cursor object to a dataframe ###
def to_df(cursor):
    return pd.DataFrame([tuple(t) for t in cursor.fetchall()])

### Connect to database and return cursor and connection ###
def connect_trusted(db='OS', server='BEGENTN714\sql1'): 
    conn = pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER=' + server + ';DATABASE='+ db + ';Trusted_connection=yes')
    return conn.cursor(), conn

### Send SQL to database. Query will return a dataframe ###
def get_df(qryStr, db='OS', server='BEGENTN714\sql1'):
    cursor, conn = connect_trusted(db, server)
    cursor.execute(qryStr)
    try:
        out = to_df(cursor)
        out.columns = [column[0] for column in cursor.description]
    except:
        return 'Sql was not a query'
        conn.commit()
    
    conn.close()
    return out

### Write to db ###
    
def write(qryStr, db='OS', server='BEGENTN714\sql1'):
    cursor, conn = connect_trusted(db, server)
    cursor.execute(qryStr)
    conn.commit()
    conn.close()
    
    
### Execute USP ###
### Arguments should be added in same order as defined in USP ###
### SQL Server can not return a table through an usp ###
def exec_usp(usp, *args, db='OS', server='BEGENTN714\sql1'):
    cursor, conn = connect_trusted(db, server)
    sql = 'EXEC {}'
    for i in range(len(args) - 1):
        sql = sql + ' ?,'
    sql = sql + '?'
    try:
        cursor.execute(sql.format(usp), (args))
        success = True
    except Exception as e:
        success = e
    conn.commit()
    conn.close()
    return success
