import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import numpy as np

from sklearn import datasets
import pandas as pd

iris = datasets.load_iris()
df = pd.DataFrame(iris.data, columns = iris.feature_names)
df ['Species'] = iris.target
df
print (df.info())
print (df.describe())
