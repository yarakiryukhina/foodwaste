import json

from conf import df


df = df[['age', 'country', 'covid', 'habits']].copy()

covid = df.groupby(['covid']).agg(amount=('covid', 'count'))

# Split multiple answers
df['hab'] = df.habits.str.split(';')

# Only multiple answers
multi = df.hab.apply(lambda x: len(x) > 1)

# New DataFrame with single answer
df_new = df[~multi].reset_index(drop=True).copy()

df_new.info()

del df_new['hab']

# Update new DataFrame
for i, r in df[multi].iterrows():
    for h in r.hab:
        df_new.loc[len(df_new)] = [r.age, r.country, r.covid, h]

question = 'How have your food waste habits changed since the start of the Covid-19 pandemic if at all?'


tree = {
    'name': question,
    #'parent': 'null',
    'children': []
}


for ans, num in df_new.groupby(['covid']).agg(amount=('covid', 'count')).reset_index().values:
    children = list()

    for ans2, num2 in df_new.query('covid == @ans').groupby(['habits']).agg(amount=('habits', 'count')).reset_index().values:
        children.append({
            'name': ans2,
            #'parent': ans,
            'count': num2
        })

    tree['children'].append({
        'name': ans,
        #'parent': question,
        'count': num,
        'children': children
    })


if __name__ == '__main__':
    with open('output/tree.js', 'w', encoding='utf-8') as f:
        f.write('var tree_graph =\n' + json.dumps(tree, ensure_ascii=False) + ';\n')