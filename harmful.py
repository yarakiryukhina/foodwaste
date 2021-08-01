import json

from conf import df


df = df[['age', 'country', 'harmful']].copy().dropna()

p = df.groupby(['harmful']).agg(amount=('harmful', 'count')) / df.groupby(['harmful']).agg(amount=('harmful', 'count')).sum() * 100

print(p)