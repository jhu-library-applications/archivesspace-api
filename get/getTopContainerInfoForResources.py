import requests
import secret
import pandas as pd
import argparse
from datetime import datetime
from helpingscripts import collect_value

secretVersion = input('To edit production server, enter secret file name: ')
if secretVersion != '':
    try:
        secret = __import__(secretVersion)
        print('Editing Production')
    except ImportError:
        print('Editing Development')
else:
    print('Editing Development')

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file')
args = parser.parse_args()

if args.file:
    filename = args.file
else:
    filename = input('Enter file name as filename.csv: ')

base_url = secret.base_url
user = secret.user
password = secret.password
repository = secret.repository

df_1 = pd.read_csv(filename)
container = df_1.top_container.dropna()
itemList = container.unique()
itemList = list(itemList)
print(itemList)


auth = requests.post(base_url+'/users/'+user+'/login?password='+password).json()
session = auth['session']
print(session)
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}

all_items = []
for count, item in enumerate(itemList):
    tiny_dict = {}
    print(base_url+item)
    print(count)
    output = requests.get(base_url+item, headers=headers).json()
    collect_value(output, 'barcode', tiny_dict)
    collect_value(output, 'entity_type', tiny_dict)
    collect_value(output, 'indicator', tiny_dict)
    collect_value(output, 'display_string', tiny_dict)
    collect_value(output, 'uri', tiny_dict)
    all_items.append(tiny_dict)


df = pd.DataFrame.from_records(all_items)
print(df.head)
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
df.to_csv('top_containers_'+dt+'.csv', index=False)
