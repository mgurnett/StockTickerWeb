import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from data_clean import remove_zeros


json_data = pd.read_json (r'covid_data.json', orient="index")# <class 'pandas.core.frame.DataFrame'>
data = remove_zeros (json_data)
# print (data.describe())
# plt.title ('the latest number is {} on {} and the high was {}'.format(current_covid, current_covid_date, max_covid))
plt.xlabel('Dates')
plt.ylabel('Cases')
plt.plot (data, label='raw')


# Test train split for supervised training
# print (data.index, data['cases'])
X_train, X_test, y_train, y_test = train_test_split(data.index, data['cases'])

# plt.scatter (X_train, y_train, label='Training data', color='r', alpha=.7)
# plt.scatter (X_test, y_test, label='Testing data', color='g', alpha=.7)
# plt.legend(loc=2)
# plt.show()

# Create linear model and train it
LR = LinearRegression()
LR.fit(X_train.values.reshape(-1,1), y_train.values)

#Use model to predict on TEST data
prediction = LR.predict(X_test.values.reshape(-1,1))

#plot prediction line against actual test data
plt.plot(X_test, prediction, label="Linear Regression", color='p')
plt.scatter(X_test, y_test, label="Actual Test Data", color="y", alpha=.7)
plt.legend(loc=2)
plt.show()