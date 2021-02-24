import pandas as pd
columns = ['Team', 'Games Played', 'Win', 'Loss', 'OT Loss', 'SO Loss', 'Points', 'Division']
dummy = [['', 0, 0, 0, 0, 0, 0, '']]
df = pd.DataFrame(columns=columns, data=dummy)

data = [['Calgary Flames',            19,    9,     9,       1,        0,      19,      'Scotia North'],
        ['Edmonton Oilers',            20,   12,     8,        0,        0,      24,      'Scotia North'],
        ['Colorado Avalanche',            15,    9,     5,        1,        0,      19,        'Honda West']]

for d in data:
    a_series = pd.Series(d, index = df.columns)
    df = df.append(a_series, ignore_index=True)
print (df)
df = df.drop(0)
print (df)