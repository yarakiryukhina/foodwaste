import pandas as pd

sheet_id = 'Insert_sheet_id_here'
sheet_name = 'Food%20waste%20project_Goldsmiths-4'

url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

df = pd.read_csv(
        url,
        header = 0,
        parse_dates = True,
        names = [
            'date' ,'age', 'country', 'attitude', 'assoc', 'harmful', 'unwanted', 'thrown_bags',
            'reason', 'fwtype', 'covid', 'habits', 'auth', 'done'
        ]
    )
