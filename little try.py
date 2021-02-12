import datetime

def purchase_shares( **kwargs):
    price = kwargs.get("historical_price", 500)
    p_date  = kwargs.get("historical_date", str(datetime.datetime.now()))#raw_datetime.replace(microsecond=0) 
    print (p_date)
    p = '%Y-%m-%d %H:%M:%S'
    epoch = datetime.datetime(1970, 1, 1)
    print((datetime.datetime.strptime(p_date, p) - epoch).total_seconds())
    
    print ('The price will be {} as sold on {}'.format(price, ps_date))
    
    

    
    
#     for key, value in kwargs.items():
#         print (str(key) + str(value))
#         
#         if  key == "historical_price":
#             price = value
#             print ('price = {}'.format(price))
#         else:
#             price=500
#             print ('price = {}'.format(price))
#         if  key == "historical_date":
#             p = '%Y-%m-%d %H:%M:%S'
#             epoch = datetime.datetime(1970, 1, 1)
#             print((datetime.datetime.strptime(value, p) - epoch).total_seconds())
#         else:
#             ps_date = datetime.datetime.now().strftime('%s')
            
        
    return price

now_price = purchase_shares (historical_price=25)
print (now_price)

now_price = purchase_shares ()
print (now_price)
#https://realpython.com/python-kwargs-and-args/

# def testFunc( **kwargs ):
#     options = {
#             'option1' : 'default_value1',
#             'option2' : 'default_value2',
#             'option3' : 'default_value3', }
# 
#     options.update(kwargs)
#     print (options)
# 
# testFunc( option1='new_value1', option3='new_value3' )
# # {'option2': 'default_value2', 'option3': 'new_value3', 'option1': 'new_value1'}
# 
# testFunc( option2='new_value2' )
# # {'option1': 'default_value1', 'option3': 'default_value3', 'option2': 'new_value2'}
# 
# attribute = kwargs.get('name', default_value)