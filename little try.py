import datetime

def purchase_shares( **kwargs):
    for key, value in kwargs.items():
        print (str(key) + str(value))
        if  key == "historical_price":
            price = value
        else:
            price=500
            
        if  key == "historical_date":
            p = '%Y-%m-%d %H:%M:%S'
            epoch = datetime.datetime(1970, 1, 1)
            print((datetime.datetime.strptime(value, p) - epoch).total_seconds())
        else:
            ps_date = datetime.datetime.now().strftime('%s')
            
        print ('The price will be {} as sold on {}'.format(price, ps_date))
    return price


now_price = purchase_shares (historical_price=25)
print (now_price)

now_price = purchase_shares ()
print (now_price)
#https://realpython.com/python-kwargs-and-args/