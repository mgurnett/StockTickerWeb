import pandas as pd
import matplotlib.pyplot as plt
from data_clean import remove_zeros

data = pd.read_json (r'covid_data.json', orient="index")# <class 'pandas.core.frame.DataFrame'>
# print (data.head(20).index.tolist())

data_cleaned = remove_zeros (data)

# plt.title ('the latest number is {} on {} and the high was {}'.format(current_covid, current_covid_date, max_covid))
plt.xlabel('Dates')
plt.ylabel('Cases')
plt.plot (data, label='raw')
plt.legend(loc=2)
plt.show()

