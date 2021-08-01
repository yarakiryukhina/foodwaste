import json

from conf import df


df = df[['age', 'country', 'attitude']].copy().dropna()

# Split multiple answers
df['att'] = df.attitude.str.split(';')

# Only multiple answers
multi = df.att.apply(lambda x: len(x) > 1)

# New DataFrame with single answer
df_new = df[~multi].reset_index(drop=True).copy()

df_new.info()

del df_new['att']

# Update new DataFrame
for i, r in df[multi].iterrows():
    for a in r.att:
        df_new.loc[len(df_new)] = [r.age, r.country, a]


# Pivot table and percentage
df2 = df_new.groupby(['age', 'attitude']).agg(amount=('attitude', 'count'))
df2['pct'] = df2 / df2.groupby('age').sum() * 100

dfp = df2.reset_index()[['age','attitude','pct']].pivot(columns='attitude', index='age', values='pct')


if __name__ == '__main__':
    with open('output/attitude.js', 'w', encoding='utf-8') as f:
        f.write('var attitude =\n' + json.dumps(dfp.round(1).to_dict('split'), ensure_ascii=False) + ';\n')