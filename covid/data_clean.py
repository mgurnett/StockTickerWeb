import pandas as pd

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

def remove_zeros (data):
    starts = []; ends =[]; prev_value = 0
    for index, row in data.iterrows():
        print (row)
        if prev_value > 0 and row['cases'] == 0:
            prev_value = 0
            starts.append(index)
        if prev_value == 0 and row['cases'] > 0:
            prev_value = row['cases']
            ends.append(index)
    ends.pop(0) #remove the first one as it is the end of the initial zeros.
    print (f'starts {len(starts)} and ends {len(ends)}')

    return data

if __name__ == '__main__':
    json_data = pd.read_json (r'covid_data.json', orient="index")# <class 'pandas.core.frame.DataFrame'>
    cleaned_data = remove_zeros (json_data)