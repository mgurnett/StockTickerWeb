import datetime

TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'
DISPLAY_FORMAT = "%a, %e %b %Y -%l:%M %p"

current_date_e = int(datetime.datetime.now().timestamp())
tz_string = datetime.datetime.now(datetime.timezone.utc).astimezone().tzname()
print (tz_string)
    
# print ('Timezone {}'.format (datetime.now.strftime("%Z %z")))

def timestamp_str_from_e (date_time):
    dt = datetime.datetime.fromtimestamp(date_time)
    return str(dt)

def timestamp_str_to_e (date_time):
    epoch = datetime.datetime(1970, 1, 1)
    tz_string = datetime.datetime.now(datetime.timezone.utc).astimezone().tzname()
    if tz_string == 'MST':
        tz_comp = 25200
    else:
        tz_comp = 28800
    epoch_time = (datetime.datetime.strptime(date_time, TIMESTAMP_FORMAT) - epoch).total_seconds() + tz_comp
    return int(epoch_time)  
    

print ('current_date_e {}'.format (current_date_e))

current_date_s = datetime.datetime.fromtimestamp(current_date_e);
print ('local convert - current_date_s {}'.format (current_date_s))

current_date_s = timestamp_str_from_e(current_date_e);
print ('local convert - current_date_s {}'.format (current_date_s))

current_date_e = timestamp_str_to_e(current_date_s);
print ('local convert - current_date_s {}'.format (current_date_e))