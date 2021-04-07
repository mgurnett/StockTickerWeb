import pandas as pd

def fill_zeros (data, first, last):
    for x in range (len(first)):
        num_of_days = ((last[x] - first[x]).days) + 1
        total_date = last[x]
        total_amount = data.at[total_date,'cases']
        amount = int (total_amount / num_of_days)
        print (f'first zero {first[x]} and ends at {total_date} or {num_of_days} days and the total is {total_amount} amount {amount}')
        for y in range (number_of_days+1)
    return (data)

def remove_zeros (data):
    starts = []; ends =[]; prev_value = 0
    for index, row in data.iterrows():
        # print (row)
        if prev_value > 0 and row['cases'] == 0:
            prev_value = 0
            starts.append(index)
        if prev_value == 0 and row['cases'] > 0:
            prev_value = row['cases']
            ends.append(index)
    ends.pop(0) #remove the first one as it is the end of the initial zeros.
    data = fill_zeros (data, starts, ends)
    return data

if __name__ == '__main__':
    json_data = pd.read_json (r'covid_data.json', orient="index")# <class 'pandas.core.frame.DataFrame'>
    cleaned_data = remove_zeros (json_data)