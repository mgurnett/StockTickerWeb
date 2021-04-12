import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta

url="https://api.opencovid.ca/timeseries?stat=cases&loc=AB"

def get_data (u):
    url_data = pd.read_json(u)
    url_data = pd.json_normalize(url_data['cases'])
    
    url_data['date_fixed'] = pd.to_datetime(url_data['date_report'], format="%d-%m-%Y")
    data_new = url_data.set_index ('date_fixed')
    data_new = data_new.drop ('province', axis='columns')
    data_new = data_new.drop ('cumulative_cases', axis='columns')
    data_new = data_new.drop ('date_report', axis='columns')
    # result = data_new.to_json(r'covid_data.json',orient="index")
    return data_new

def fill_zeros (data, first, last):
    #get the full data dataframe, and a list of all the first zeros and a list of the total amounts at the end.
    #55, 0, 0, 150, 60   The list gives #1 for start and #3 for last.  Div 150 by 3 and put it in the 2 0s and the 150
    #now 55, 50, 50, 50, 60
    for x in range (len(first)): #loop though the list of firsts.  The lasts will have the same number
        num_of_days = ((last[x] - first[x]).days) #find number of days in question
        total_date = last[x] # figure out which date has the total (150)
        total_amount = data.at[total_date,'cases'] #find the total amount (150)
        amount = int (total_amount / (num_of_days + 1)) #figure out the 50s
        day_to_fix = first[x].date() # copy the first date
        for y in range (num_of_days): #loop through the number of effected days BUT NOT the final day
            data.loc[str(day_to_fix), 'cases'] = amount #make the cell now have the 50
            day_to_fix = day_to_fix + timedelta(days=1) #increase the date by one day
        data.loc[str(total_date.date()), 'cases'] = amount #put the 50 in the place of the 150
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
    json_data = get_data (url) #<class 'pandas.core.frame.DataFrame'>
    # json_data = pd.read_json (r'covid_data.json', orient="index")# <class 'pandas.core.frame.DataFrame'>
    cleaned_data = remove_zeros (json_data)
    ewm_data = cleaned_data.iloc[:,0].ewm(span=20,adjust=False).mean()
    cleaned_data.insert(1, 'ewm', ewm_data)
    sma3_data = cleaned_data.iloc[:,1].rolling(window=3).mean()
    cleaned_data.insert(1, 'sma3', sma3_data)
    sma10_data = cleaned_data.iloc[:,1].rolling(window=10).mean()
    cleaned_data.insert(1, 'sma10', sma10_data)

    max_cases = int(cleaned_data["cases"].describe().max())
    last_day = cleaned_data.index[-1].date()
    latest_cases = cleaned_data["cases"].iloc[-1]

    # one of the characters {'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'}, 
    # which are short-hand notations for shades of blue, green, red, cyan, magenta, yellow, black, and white
    plt.figure (figsize=(18,10))
    plt.title (f'the latest number is {latest_cases} on {last_day} and the high was {max_cases}')
    plt.xlabel('Dates')
    plt.ylabel('Cases')
    plt.plot(cleaned_data['cases'], label="Raw data", color='k')
    plt.plot(cleaned_data['ewm'], label="EWM average", color='g')
    plt.plot(cleaned_data['sma3'], label="SMA 3 average", color='b')
    plt.plot(cleaned_data['sma10'], label="SMA 10 average", color='r')
    plt.legend(loc=2)
    plt.show()