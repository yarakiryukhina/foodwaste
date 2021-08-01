import json

from conf import df


df = df[['age', 'country', 'unwanted']].copy().dropna()

# Split multiple answers
df['unw'] = df.unwanted.str.split(';')

# Only multiple answers
multi = df.unw.apply(lambda x: len(x) > 1)

# New DataFrame with single answer
df_new = df[~multi].reset_index(drop=True).copy()

df_new.info()

del df_new['unw']

# Update new DataFrame
for i, r in df[multi].iterrows():
    for u in r.unw:
        df_new.loc[len(df_new)] = [r.age, r.country, u]


df_unw = df_new.groupby(['age', 'country', 'unwanted']).agg(amount=('unwanted', 'count')).reset_index()
df_unw_pivot = df_unw.groupby(['age','unwanted']).sum().reset_index().pivot(columns='age', values='amount', index='unwanted')

unw = df_unw_pivot.to_dict('split')

unw['data2'] = []

for i in range(len(unw['index'])):
    b = unw['index'][i]

    cnt = []

    for j in range(len(unw['columns'])):
        a = unw['columns'][j]

        cnt.append(
            df_unw.
                query('(age == @a) & (unwanted == @b)')[['country', 'amount']].
                sort_values(by='amount', ascending=False).
                to_dict('records')
        )

    unw['data2'].append(cnt)

# Output
if __name__ == '__main__':
    with open('output/unwanted.js', 'w', encoding='utf-8') as f:
        f.write('var unwanted_food =\n' + json.dumps(unw, ensure_ascii=False) + ';\n')