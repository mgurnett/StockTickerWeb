import datetime

p = '%Y-%m-%d %H:%M:%S'

# mytime = "2009-03-08T00:27:31.807Z"
mytime = '2021-02-11 00:00:00'
epoch = datetime.datetime(1970, 1, 1)
ps_date = (datetime.datetime.strptime(mytime, p) - epoch).total_seconds()

print(ps_date)