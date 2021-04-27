# -*- coding: utf-8 -*-
import io
import json
from datetime import timedelta, datetime
import pandas as pd
import requests
import matplotlib.pyplot as plt
from pretty_html_table import build_table

to_unicode = str

URL="https://services9.arcgis.com/pJENMVYPQqZZe20v/arcgis/rest/services/province_daily_totals/FeatureServer/0/query?where=Province%20%3D%20'ALBERTA'&outFields=Province,Abbreviation,DailyTotals,SummaryDate,DailyDeaths,DailyHospitalized,DailyICU,DailyTested&outSR=4326&f=json"

def make_web (name, df):
    # html_table = build_table(df, 'blue_dark')
    # file_name = ('games_folder/' + name + ".html")
    file_name = (name + ".html")
    # text_file = open(file_name, "w")
    # text_file.write(html_table)
    # text_file.close()
    with open(file_name, 'w') as fo:
        df.to_html(fo)
    print (f'Saved as {file_name}')
        
def get_data ():
    data_loaded = json.loads(requests.get(URL).text)
    url_data_df = pd.json_normalize(data_loaded['features'])
    url_data_df['date_fixed'] = pd.to_datetime(url_data_df['attributes.SummaryDate'], unit='ms')
    data_new = url_data_df.set_index ('date_fixed')
    return data_new

def load_json():
    # Read JSON file
    try:
        with open('alberta_covid_data.json') as data_file:
            data_loaded = json.load(data_file)
        data_df = pd.DataFrame.from_dict(data_loaded, orient="index")
        data_df['date_fixed'] = pd.to_datetime(data_df['attributes.SummaryDate'], unit='ms')
        data_new = data_df.set_index ('date_fixed')
        print ("loaded data from file")
    except Exception:
        data_new = get_data()
        print ("downloaded data from API")
    return data_new

def save_json(data):
    # Write JSON file
    data.to_json (r'alberta_covid_data.json', orient="index")# <class 'pandas.core.frame.DataFrame'>

def fill_zeros (data, first, last):
    #get the full data dataframe, and a list of all the first zeros and a list of the total amounts at the end.
    #55, 0, 0, 150, 60   The list gives #1 for start and #3 for last.  Div 150 by 3 and put it in the 2 0s and the 150
    #now 55, 50, 50, 50, 60
    for x in range (len(first)): #loop though the list of firsts.  The lasts will have the same number
        num_of_days = ((last[x] - first[x]).days) #find number of days in question
        total_date = last[x] # figure out which date has the total (150)
        total_amount = data.at[total_date,'attributes.DailyTotals'] #find the total amount (150)
        amount = int (total_amount / (num_of_days + 1)) #figure out the 50s
        day_to_fix = first[x].date() # copy the first date
        for y in range (num_of_days): #loop through the number of effected days BUT NOT the final day
            data.loc[str(day_to_fix), 'attributes.DailyTotals'] = amount #make the cell now have the 50
            day_to_fix = day_to_fix + timedelta(days=1) #increase the date by one day
        data.loc[str(total_date.date()), 'attributes.DailyTotals'] = amount #put the 50 in the place of the 150
    return (data)

def remove_zeros (data):
    starts = []; ends =[]; prev_value = 0
    for index, row in data.iterrows():
        # print (row)
        if prev_value > 0 and row['attributes.DailyTotals'] == 0:
            prev_value = 0
            starts.append(index)
        if prev_value == 0 and row['attributes.DailyTotals'] > 0:
            prev_value = row['attributes.DailyTotals']
            ends.append(index)
    ends.pop(0) #remove the first one as it is the end of the initial zeros.
    data = fill_zeros (data, starts, ends)
    return data

def find_averages (cleaned_data):
    if 'ewm' in cleaned_data.columns:
        cleaned_data = cleaned_data.drop('ewm', 1)
        cleaned_data = cleaned_data.drop('sma3', 1)
        cleaned_data = cleaned_data.drop('sma10', 1)
    ewm_data = cleaned_data.iloc[:,2].ewm(span=50,adjust=False).mean()
    cleaned_data.insert(1, 'ewm', ewm_data)
    sma3_data = cleaned_data.iloc[:,1].rolling(window=3).mean()
    cleaned_data.insert(1, 'sma3', sma3_data)
    sma10_data = cleaned_data.iloc[:,1].rolling(window=10).mean()
    cleaned_data.insert(1, 'sma10', sma10_data)
    return (cleaned_data)

def manual_data (data):
    # man_date = input ("date (yyyy-mm-dd)")
    timestamp = int(datetime.now().timestamp()) * 1000
    index_date = pd.to_datetime(timestamp, unit='ms')
    man_cases = input ("number of cases")
    man_icu = input ("number of new ICU")
    man_hosp = input ("number of new hospitalizations")
    row = pd.Series ({'attributes.DailyTotals': int(man_cases),
                      'attributes.Province': 'ALBERTA',
                      'attributes.Abbreviation': 'AB', 
                      'attributes.SummaryDate': timestamp,
                      'attributes.DailyDeaths': 0,
                      'attributes.DailyHospitalized': int(man_hosp),
                      'attributes.DailyICU': int(man_icu),
                      'attributes.DailyTested': 0,
                      },name=index_date)
    data = data.append(row)
    make_web ('enterdata', data)
    return (data)

def hosp (cleaned_data):
    if 'current_hosp' in cleaned_data.columns:
        cleaned_data = cleaned_data.drop('current_hosp', 1)
        cleaned_data = cleaned_data.drop('current_icu', 1)
    cleaned_data['current_icu'] = cleaned_data['attributes.DailyICU'].cumsum()
    cleaned_data['current_hosp'] = cleaned_data['attributes.DailyHospitalized'].cumsum()
    print (cleaned_data.tail(5))
    plt.figure (figsize=(18,10))
    plt.title (f'Hopitalization and ICU')
    plt.xlabel('Dates')
    plt.ylabel('Cases')
    plt.plot(cleaned_data['current_icu'], label="Current ICU", color='k')
    plt.plot(cleaned_data['current_hosp'], label="Current Hospitalized", color='r')
    plt.legend(loc=2)
    plt.show()

def cases (json_data):
    zero_data = remove_zeros (json_data)
    cleaned_data = find_averages (zero_data)
    max_cases = int(cleaned_data["attributes.DailyTotals"].describe().max())
    last_day = cleaned_data.index[-1].date()
    latest_cases = cleaned_data["attributes.DailyTotals"].iloc[-1]
    # one of the characters {'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'}, 
    # which are short-hand notations for shades of blue, green, red, cyan, magenta, yellow, black, and white
    plt.figure (figsize=(18,10))
    plt.title (f'the latest number is {latest_cases} on {last_day} and the high was {max_cases}')
    plt.xlabel('Dates')
    plt.ylabel('Cases')
    plt.plot(cleaned_data['attributes.DailyTotals'], label="Raw data", color='k')
    plt.plot(cleaned_data['ewm'], label="EWM average", color='r')
    plt.plot(cleaned_data['sma3'], label="SMA 3 average", color='b')
    plt.plot(cleaned_data['sma10'], label="SMA 10 average", color='g')
    plt.legend(loc=2)
    plt.show()

'''
['attributes.Province', 'attributes.Abbreviation', 'attributes.DailyTotals', 
'attributes.SummaryDate', 'attributes.DailyDeaths', 'attributes.DailyHospitalized', 
'attributes.DailyICU', 'attributes.DailyTested']
'''

if __name__ == '__main__':
    choice = ""; data = None
    while choice != "Q":
        choice = input ("Do you want to: Download new data, Enter more data, Load data, Save data, show New cases, show Icu cases or Quit?")
        if choice == "E" or choice == "e":
            if data is None:
                data = load_json()
            data = manual_data(data)
        elif choice == "L" or choice == "l":
            data = load_json()
        elif choice == "D" or choice == "d":
            data = get_data()
        elif choice == "S" or choice == "s":
            save_json(data)
        elif choice == "N" or choice == "n":
            if data is None:
                data = load_json()
            cases(data)
        elif choice == "I" or choice == "i":
            if data is None:
                data = load_json()
            make_web ('hosp', data)
            hosp(data)
        elif choice == "Q" or choice == "q":
            break
