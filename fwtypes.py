import json

from conf import df


df = df[['age', 'country', 'fwtype']].copy().dropna()

ages = df.query('fwtype != "None"').groupby(['age', 'country', 'fwtype']).agg(amount=('fwtype', 'count'))

fwtypes = ages.reset_index().groupby('fwtype').amount.sum()

print(ages)
print(fwtypes)