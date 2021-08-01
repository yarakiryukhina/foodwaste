import pandas as pd
import json

sheet_id = 'Insert_sheet_id_here'
sheet_name = 'Sheet1'

url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

df = pd.read_csv(url, usecols=range(9))

if __name__ == '__main__':
    with open('output/food_waste.js', 'w', encoding='utf-8') as f:
        f.write('var food_waste =\n' + json.dumps(df.to_dict(orient='records'), ensure_ascii=False) + ';\n')
