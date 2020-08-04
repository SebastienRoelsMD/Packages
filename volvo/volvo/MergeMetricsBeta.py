from volvo import SQL
import numpy as np

def merge_with_metrics(left, right, left_cols, right_cols, how):
    
    left = left.copy()
    right = right.copy()
    
    for col_left, col_right in zip(left_cols, right_cols):
        
        l = left[col_left] 
        r = right[col_right]
        
        l_dtype = l.dtype
        r_dtype = r.dtype
        
        print("{} (LEFT) has data type '{}'".format(col_left, l_dtype))
        print("{} (RIGHT) has data type '{}'".format(col_right, r_dtype))
        if l_dtype == r_dtype:
            print(">>>>> TEST PASSED <<<<<")
            proceed = True
        else:
            print("DATA TYPES DO NOT MATCH. Trying to convert data ...")
            proceed = False
            ### Do something to fix the problem ###
            try:
                if r_dtype != 'object':
                    left[col_left] = left[col_left].astype(r_dtype)
                    print("Data type of '{}' has sucessfully been changed to '{}'".format(col_left, r_dtype))
                    proceed = True
                else:
                    raise Exception('Do not convert to Object')
            except Exception as e:
                print(e)
                print("Data conversion did not work, trying the other way'round ...")
                try:
                    if l_dtype != 'object':
                        right[col_right] = right[col_right].astype(l_dtype)
                        print("Data type of '{}' has sucessfully been changed to '{}'".format(col_right, l_dtype))
                        proceed = True
                except Exception as e:
                    print(e)
                    print("Data conversion did not work, find another solution ...")
            
        if proceed:
        
            len_l = len(left)
            len_r = len(right)
            
            uni_l = left[left_cols].nunique().values[0]
            uni_r = right[right_cols].nunique().values[0]
            
            len_inner = len(left.merge(right, how='inner', left_on=left_cols, right_on=right_cols))
            
            outer = left.merge(right, how='outer', left_on=left_cols, right_on=right_cols)
            
            len_nomatch_l = len(outer[outer[right_cols[0]].isna()])
            len_nomatch_r = len(outer[outer[left_cols[0]].isna()])
            
            print("\n")
            print("Length Left \t\t {}".format(len_l))
            print("Length Right \t\t {}".format(len_r))
            print("\n")
            print("Uniques Left \t\t {}".format(uni_l))
            print("Uniques Right \t\t {}".format(uni_r))
            print("\n")
            print("Inner Join Matches \t {}".format(len_inner))
            print("Left No Match \t\t {}".format(len_nomatch_l))
            print("Right No Match \t\t {}".format(len_nomatch_r))

            return left.merge(right, how=how, left_on=left_cols, right_on=right_cols)

#manpower = SQL.get_df("SELECT PickerId, Team as TeamPicker FROM OS.dbo.ManpowerAll", server='BEGENTN714\sql1')
#prc = SQL.get_df("SELECT PickerNo, Customer, District, Orderno, PRC FROM [OS].[dbo].[Q_ClaimAndReportsJoin]", server='BEGENTN714\sql1')
#
#prc['PickerNo'] = prc['PickerNo'].astype('int64')
#
#manpower.merge(prc, how='inner', left_on=['PickerId'], right_on=['PickerNo'])
#
#merge_with_metrics(manpower, prc, ['PickerId'], ['PickerNo'], 'left')
