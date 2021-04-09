from datetime import datetime
import pytz

local_tz = pytz.timezone('America/Edmonton')

def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)

api_dt = '2021-05-11T23:00:00Z'
datetime_object = datetime.strptime(api_dt, '%Y-%m-%dT%H:%M:%SZ')
print(api_dt)
newtime = utc_to_local(datetime_object)
print (newtime.tzinfo)