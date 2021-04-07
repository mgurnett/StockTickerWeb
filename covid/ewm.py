import pandas as pd
import numpy as np

df = pd.DataFrame({"B": [0, 1, 2, np.nan, 4]})
ewm_df = df.ewm(com=0.5).mean()
print (ewm_df)