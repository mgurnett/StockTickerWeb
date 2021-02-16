import datetime

def purchase_shares( **kwargs):
    price = kwargs.get("historical_price", 500)
    cur_datetime = datetime.datetime.now().replace(microsecond=0) 
    p_date  = kwargs.get("historical_date", str(cur_datetime))
    p = '%Y-%m-%d %H:%M:%S'
    epoch = datetime.datetime(1970, 1, 1)
    return price, p_date

now_price, now_date = purchase_shares (historical_price = 25)
print ('The price will be {} as sold on {}'.format(now_price, now_date))

now_price, now_date = purchase_shares ()
print ('The price will be {} as sold on {}'.format(now_price, now_date))

now_price, now_date = purchase_shares (historical_price = 25, historical_date = str('2018-02-12 09:07:56'))
print ('The price will be {} as sold on {}'.format(now_price, now_date))

now_price, now_date = purchase_shares (historical_date = str('2018-02-12 09:07:56'))
print ('The price will be {} as sold on {}'.format(now_price, now_date))

#https://realpython.com/python-kwargs-and-args/