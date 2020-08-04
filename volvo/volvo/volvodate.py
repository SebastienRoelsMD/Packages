import datetime
import pandas as pd
import numpy as np

###############################################################################
###############################################################################	
                    ### DATE AND TIME FUNCTIONS ###
###############################################################################
###############################################################################

def weeknumber(x):
    return x.isocalendar()[1]

def daynumber(x):
    return x.isocalendar()[2]

def to_date(x):
    return datetime.datetime.strptime(x, '%Y-%m-%d').date()

def to_datetime(x):
    return datetime.datetime.strptime(x, '%Y-%m-%d')

def volvoweek(x):
    return "W" + str(x.year)[-2:] + add_zero(weeknumber(x))

def lastdayscounter(x):
    return (datetime.datetime.now().date() - x).days

def todaydate():
	return datetime.datetime.now().date()
	
def todaydatetime():
	return datetime.datetime.now()
	
def thisweek():
	return weeknumber(datetime.datetime.now().date())
	
def dayofweek():
	return daynumber(datetime.datetime.now().date())


### --------------------------------------------------------------------------
### GET TIME DIFFERENCE IN HOURS BETWEEN TWO DATETIME OBJECT ###
### INPUT TYPES: min_date: datetime.datetime, max_date: datetime.datetime
### --------------------------------------------------------------------------
    
def get_time_difference_in_hours(min_date, max_date):
    
    ## Check for NaN's ##
    if (pd.isna(min_date)) | (pd.isna(max_date)):
        return np.nan
    
    else:
        ## Get total difference (as timedelta) ##
        dif = (max_date - min_date)

        ## Get total difference in days ##
        dif_days = dif.days

        ## Total diff in hours ##
        dif = dif.total_seconds() / 3600

        ## Get holidays and remove from dif ##
        bus_days = np.busday_count(min_date.date(), max_date.date())
        ## If time part of max date is smaller than time part of min date
        ## then deduct 24 hours (by removing one business day)
        if (min_date.hour > max_date.hour) or ((min_date.hour == max_date.hour) and (min_date.minute > max_date.minute)):
             bus_days -= 1
            
        dif -= (dif_days - bus_days) * 24

        ## Remove holidays ## 
        from workalendar.europe import Belgium
        cal = Belgium()

        hol_cnt = 0

        for d in cal.holidays(datetime.datetime.now().year):
            ## Avoid double count when holiday is weekend day ##
            if d[0].strftime('%A') not in ['Sunday', 'Saturday']:
                ## Check if holiday is in between min and max date ##
                if min_date.date() <= d[0] <= max_date.date():
                    hol_cnt += 24

        dif -= hol_cnt

        ## Return dif in hours ##
        return dif

###############################################################################
###############################################################################	
                        ### HELPER FUNCTIONS ###
###############################################################################
###############################################################################

def add_zero(x):
    if x < 10:
        return "0" + str(x)
    else:
        return str(x)