import pytz
from datetime import datetime

def fix_time (api_dt): 
    # print (f'api_dt {api_dt} of {type(api_dt)}')
    datetime_object = datetime.strptime(api_dt, '%Y-%m-%dT%H:%M:%SZ')
    UTC_time = pytz.timezone("UTC").localize(datetime_object)
    d = UTC_time.astimezone()
    # Edmonton_time = d.strftime("%d %b %Y (%I:%M %p) %Z") #Print it with a directive of choich
    Edmonton_time = d.strftime("%Y-%m-%dT%H:%M:%SZ") #Print it with a directive of choich
    return (Edmonton_time)


date_fixed = fix_time ("2021-03-26T23:00:00Z")
print (date_fixed)