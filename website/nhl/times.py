import pytz
from datetime import datetime

def fix_time (dt_object): 
    print (f'dt_object {dt_object} of {type(dt_object)}')
    UTC_time = pytz.timezone("UTC").localize(dt_object)
    d = UTC_time.astimezone()
    Edmonton_time = d.strftime("%d %b %Y (%I:%M:%S:%f %p) %Z") #Print it with a directive of choich
    return (Edmonton_time)


            date_fixed = fix_time (datetime_object)