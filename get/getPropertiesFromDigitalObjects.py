import requests
import secret
import pandas as pd
import argparse
from datetime import datetime

secretVersion = input('To edit production server, enter the name of the secret file: ')
if secretVersion != '':
    try:
        secret = __import__(secretVersion)
        print('Editing Production')
    except ImportError:
        print('Editing Development')
else:
    print('Editing Development')

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='file_name to retrieve')
args = parser.parse_args()

if args.file:
    filename = args.file
else:
    filename = input('Enter file name as filename.csv: ')

baseURL = secret.baseURL
user = secret.user
password = secret.password
repository = secret.repository

df_1 = pd.read_csv(filename)
itemList = df_1.digital.to_list()


def collect_property(dictionary, do_property, name=None):
    if dictionary is not None:
        value = dictionary.get(do_property)
        if value is not None:
            if name:
                tiny_dict[name] = value
            else:
                tiny_dict[do_property] = value


auth = requests.post(baseURL + '/users/' + user + '/login?password=' + password).json()
session = auth['session']
print(auth)
print(session)
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}
all_items = []
for count, item in enumerate(itemList):
    tiny_dict = {}
    print(count)
    print(baseURL + item)
    output = requests.get(baseURL + item, headers=headers).json()
    collect_property(output, 'uri')
    collect_property(output, 'digital_object_id')
    files = output.get('file_versions')
    for file in files:
        collect_property(file, 'file_uri')
    all_items.append(tiny_dict)

df = pd.DataFrame.from_dict(all_items)
print(df.head)
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
df.to_csv('digitalObjects_' + dt + '.csv', index=False)