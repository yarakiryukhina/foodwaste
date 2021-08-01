import json

from conf import df


df = df[['age', 'country', 'thrown_bags']].copy().dropna()

df['thrown_bags'] = df.thrown_bags.str.strip().replace('-', 'None')

df_bags = df.groupby(['age', 'country', 'thrown_bags']).agg(amount=('thrown_bags', 'count')).reset_index()
df_bags_pivot = df_bags.groupby(['age','thrown_bags']).sum().reset_index().pivot(columns='age', values='amount', index='thrown_bags').fillna(0)

ages = df_bags_pivot.iloc[0] + df_bags_pivot.iloc[1]*2 + df_bags_pivot.iloc[2]*3 + df_bags_pivot.iloc[4]*0.5 + df_bags_pivot.iloc[5]*4

bags = df_bags_pivot.iloc[[0, 1, 2, 4, 5]].sum().sum()
compost = df_bags_pivot.iloc[3].sum()
no_bags = df_bags_pivot.iloc[6].sum()
total = df_bags_pivot.sum().sum()

print('Responses')

print(bags, round(bags / total * 100, 1))
print(compost, round(compost / total * 100, 1))
print(no_bags, round(no_bags / total * 100, 1))


if __name__ == '__main__':
    with open('output/bags_thrown.js', 'w', encoding='utf-8') as f:
        f.write('var bags_thrown =\n' + json.dumps(ages.round(1).to_dict(), ensure_ascii=False) + ';\n')