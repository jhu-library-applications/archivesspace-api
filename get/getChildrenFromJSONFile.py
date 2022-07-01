import pandas as pd
import json
import argparse
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='filename to retrieve')
args = parser.parse_args()

if args.file:
    filename = args.file
else:
    filename = input('Enter file name as filename.json: ')

with open(filename) as f:
    data = json.load(f)
    series = data['children']
    child_dict = {}
    for child in series:
        for k, v in child.items():
            if k == 'a_id':
                if v == 151002:
                    child_dict.update(child)
    children = child_dict.get('children')
    print(children)


df_1 = pd.DataFrame.from_dict(children)
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
df_1.to_csv(path_or_buf='calculateChildren_'+dt+'.csv', index=False)