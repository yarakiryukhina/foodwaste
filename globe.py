import pandas as pd
import json

sheet_id = '1lLDjY_I8PgjsKpWsQi125SRzESjFqUkDMsXehlwVy0E'
url = 'https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}'

df = pd.read_csv(url.format(sheet_id, 'Sheet1'), usecols=range(10))
un = pd.read_csv(url.format(sheet_id, 'Sheet2'), usecols=range(20))

if __name__ == '__main__':
    with open('output/globe.js', 'w', encoding='utf-8') as f:
        f.write('var food_waste =\n' + json.dumps(
            df.to_dict(orient='records'),
            ensure_ascii=False) + ';\n')

        f.write('var undernourishment =\n' + json.dumps(
            un.drop(columns='country').set_index('iso3').to_dict(orient='index'),
            ensure_ascii=False) + ';\n')