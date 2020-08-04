import os
import pandas as pd

### Simply write a dataframe in Excel starting from a row, col  ###

def write_df_in_excel(df, excel_path, sheet, row, col):
    
    ### Connect workbook ###
    import xlwings as xw
    
    wb = xw.Book(excel_path)

    sht = wb.sheets[sheet]
    
    ### Itereate through frame and write in wb ###
    excel_row = row
    
    for index, row in df.iterrows():
        
        excel_col = col
        
        for c in df.columns:
            
            sht.range((excel_row, excel_col)).value = row[c]
            
            excel_col += 1
            
        excel_row += 1
        
    ## Save ###
    wb.save()



### Write a dataframe to Excel starting from a row, col ###
### Includes turning on and off autofilter + pre-clears everything from ###
### a given row (first_row) ###   
    
def write_df_in_excel_with_clear_autofilterproof(df, excel_path, sheet, row, col, autofilter_range, firts_row=2):
    
    ### Connect workbook ###
    import xlwings as xw
    
    wb = xw.Book(excel_path)

    sht = wb.sheets[sheet]
    
    ### Turn autofilter off when on ###
    if sht.api.AutoFilterMode == True:
          sht.api.AutoFilterMode = False

    ### Clear contents ###
    sht.range("A" + str(firts_row) + ":Z9999").clear_contents()

    ### Write Data ###
    write_df_in_excel(df, excel_path, sheet, row, col)

    ### Turn autofilter on again ###
    sht.range(autofilter_range).api.AutoFilter()
    
    ### Save ###
    wb.save()
    
### Read all files in a folder into a dataframe ###
### All file should have the same STRUCTURE and EXTENSION ###

def read_all_files_to_df(path, suffix='.xlsx', skiprows=0): 
    all_files = []
    
    for (dirpath, dirnames, filenames) in os.walk(path):
        all_files.append(filenames)
    
    all_files = all_files[0]
    
    first = True
    for file in all_files:
        try:
            pd.read_excel(path + '/' + file)
            if file[-len(suffix):] == suffix:
                if first:
                    df = pd.read_excel(path + '/' + file, skiprows=skiprows)
                    first = False
                else:
                    # df = pd.concat([df, pd.read_excel(path + '/' + file, skiprows=skiprows)])
                    df = pd.concat([df, pd.read_excel(path + '/' + file, skiprows=skiprows)], sort=True)
        except:
            pass
    return df

### Run macro from path and macro name ###
def run_macro(path, macroname, breakafterload=False):
    
    import xlwings as xw
    
    wb = xw.Book(path, ignore_read_only_recommended=True)

    app = wb.app
    
    if breakafterload:
        from time import sleep
        sleep(breakafterload)
    
    file = path.replace("/", '\\').rsplit('\\', 1)[-1]
    
    run = app.macro("'" + file + "'" + "!" + macroname)
    
    run()    
    
    wb.save()
    
    wb.close()
    
    app.quit()