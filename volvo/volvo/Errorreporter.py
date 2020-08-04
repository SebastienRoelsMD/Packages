### Send error or succes to database ###
def Report_error_succes(updatename, error=True, errorcode="",  type="PYTHON", debug=False):
    
    import pyodbc
    
    ### Boolean to string ###
    if error:
        error = "ERROR"
    else:
        error = "SUCCESS"
        
    if error and debug:
        error = "DEBUG"
        
    ### Clean errorcode ###
    errorcode = str(repr(errorcode)).replace("'","")
    
    ### Connect to db ###
#    conn = pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER=BEGENTN396\sql1;DATABASE=OS;Trusted_connection=yes')
#    cursor = conn.cursor()
    
    ### Connect to 714 ###
    conn_714 = pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER=BEGENTN714\sql1;DATABASE=OS;Trusted_connection=yes')
    cursor_714 = conn_714.cursor()

    ### Write to db ###
    string="""
    INSERT INTO [OS].[dbo].[LOG__AutoUpdates] ([UpdateName]
      ,[ErrorSucces]
      ,[Message]
      ,[Type])
    VALUES ('{}', '{}', '{}', '{}')
    """.format(updatename, error, errorcode, type)

#    cursor.execute(string)
    cursor_714.execute(string)    
    
    ### Write to terminal ###
    print(updatename + " WAS A " + error + "   " + errorcode)
    
    ### Commit & close ###
#    conn.commit()
#    conn.close()
    
    conn_714.commit()
    conn_714.close()