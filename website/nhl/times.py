from datetime import datetime
import pytz

ED_tz = pytz.timezone("America/Edmonton")

date_data = '2021-01-17T00:07:44Z'
datetime_object = datetime.strptime(date_data, '%Y-%m-%dT%H:%M:%SZ')
d = pytz.UTC.localize(datetime_object) #make it UTC
print (f'd         {d}')
d.astimezone(ED_tz)

print (f'd         {d}')



# print (f'datetime_object {datetime_object}')
# # MT_time = datetime_object.astimezone(pytz.timezone("America/Edmonton"))
# print (f'our_time         {our_time}')



'''

# print (datetime_object)

date_time = timezone.localize(datetime_object)
# date_time.tzinfo
print (date_time.tzinfo)


#2021-01-17 00:07:44



'''