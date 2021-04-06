#!/usr/bin/env python3
# https://opencovid.ca/api/#summary
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
from datetime import datetime
pd.options.mode.chained_assignment = None  # default='warn'

url="https://api.opencovid.ca/timeseries?stat=cases&loc=AB"
#https://github.com/ishaberry/Covid19Canada/blob/master/timeseries_prov/cases_timeseries_prov.csv

def get_data (u):
    url_data = pd.read_json(u)
    url_data = pd.json_normalize(url_data['cases'])
    return url_data

def findStartZero (x):
#     print ('X in findStartZero:', x)
    max = len(cases.index)

    while cases[x] > 0:

#         print ('X in findStartZero - while loop:', x)

        if x >= max-1:
#             print ('Len of cases.index', max, 'AND X is', x)
            return max
        x += 1
#     print ('X returned from findStartZero:', x)
    return (x)

def findEndZero (x):
    # print ('X sent in:', x)
    if x >= len(cases.index):
#         print ('falling out')
        return (x)
    while cases[x] == 0:
        x += 1
#         print ('X in while loop:', x)
    if x > len(cases.index): #this prevents running over the end.
        x = len(cases.index)-1
#     print ('X after if:', x)
    return (x)

def data_fill (first, last):
#     print('=============', first)
#     print ('first -1', first-1, cases[first-1])
#     print ('first',  first, cases[first])
#     print ('first+1',  first+1, cases[first+1])
#     print ('first+2',  first+2, cases[first+2])
#     print ('last',  last, cases[last])
    if last == len(cases.index):
        return
    run = last-first + 1
#     print ('run', run)

    fill_amount = cases[last] / run
    for fill in range ( first, last + 1 ):
        cases[fill] = fill_amount
    return

#===============================
data = get_data (url) #<class 'pandas.core.frame.DataFrame'>
data['date_fixed'] = pd.to_datetime(data['date_report'], format="%d-%m-%Y")
data_new = data.set_index ('date_fixed')
data_new = data_new.drop ('province', axis='columns')
data_new = data_new.drop ('cumulative_cases', axis='columns')
data_new = data_new.drop ('date_report', axis='columns')
result = data_new.to_json(r'covid_data.json',orient="index")

data_P = data
data_T = data

cases = data.get('cases') #this makes a local copy
date = data.get('date_report')

for i in range (0,data.shape[0]-2):
    data.loc[data.index[i+2],'SMA_3'] = np.round(((data.iloc[i,1]+ data.iloc[i+1,1] +data.iloc[i+2,1])/3),1)
    
data_P['pandas_SMA_3'] = data.iloc[:,1].rolling(window=3).mean()

data_T['EMA'] = data.iloc[:,0].ewm(span=20,adjust=False).mean()

index_number = 43 #start of good data
spotE = 0 #this is the index of the end of a string of zeros

# print ('last row', len(cases.index))
while spotE < (len(cases.index)):
#     print ('=====================')
#     print ('spotE', spotE)
    spotS = findStartZero (index_number)
    spotE = findEndZero (spotS)
    data_fill (spotS, spotE)
    index_number = spotE

values = np.asarray(cases)
time = np.asarray(date)
max_covid = np.amax(values)
current_covid = values[ -1]
current_covid_date = time[-1]
# print ('the latest number is {} on {} and the high was {}'.format(current_covid, current_covid_date, max_covid))
plt.title ('the latest number is {} on {} and the high was {}'.format(current_covid, current_covid_date, max_covid))
plt.xlabel('Dates')
plt.ylabel('Cases')
plt.plot (time, values,label='raw')
# plt.plot (data_P['pandas_SMA_3'],label='pandas_SMA_3')
plt.plot (data_T['EMA'],label='EMA')

plt.legend(loc=2)
plt.show()
# print (data)