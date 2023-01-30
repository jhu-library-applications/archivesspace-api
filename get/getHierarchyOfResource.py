import requests
import secret
import time
import argparse
import pandas as pd
from datetime import datetime

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
parser.add_argument('-i', '--a_id', help='resourceID of the child_dict to retrieve.')

args = parser.parse_args()

if args.id:
    resourceID = args.id
else:
    resourceID = input('Enter resource ID: ')

startTime = time.time()

baseURL = secret.baseURL
user = secret.user
password = secret.password
repository = secret.repository

auth = requests.post(baseURL + '/users/' + user + '/login?password=' + password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}


def find_key(d, key):
    if key in d:
        yield d[key]
    for k in d:
        if isinstance(d[k], list) and k == 'children':
            for i in d[k]:
                for j in find_key(i, key):
                    yield j


endpoint = '/repositories/' + repository + '/resources/' + resourceID + '/tree'
print(endpoint)
output = requests.get(baseURL + endpoint, headers=headers).json()
archivalObjects = []
for value in find_key(output, 'record_uri'):
    archivalObjects.append(value)


def add_to_dict(arc_dict, value):
    try:
        row_value = output[value]
        if row_value:
            arc_dict[value] = row_value
    except KeyError:
        arc_dict[value] = ''


def add_to_dictnest1(arc_dict, value):
    try:
        row_value = output[value]
        if isinstance(row_value, dict):
            row_keys = list(row_value.keys())
            dict_value = row_value.get(row_keys[0])
            arc_dict[value] = dict_value
    except KeyError:
        arc_dict[value] = ''


arcList = []
for archivalObject in archivalObjects:
    output = requests.get(baseURL + archivalObject, headers=headers).json()
    arc_dict = {}
    add_to_dict(arc_dict, 'title')
    add_to_dict(arc_dict, 'uri')
    add_to_dict(arc_dict, 'level')
    add_to_dict(arc_dict, 'jsonmodel_type')
    add_to_dict(arc_dict, 'publish')
    add_to_dictnest1(arc_dict, 'resource')
    add_to_dictnest1(arc_dict, 'parent')
    arcList.append(arc_dict)

print('Archival child_dict information collected')

df = pd.DataFrame.from_dict(arcList)
df_titles = df[['title', 'uri', 'parent']].copy()
df = df.rename(columns={'parent': 'level1'})
number = 4
for p in range(1, number):
    parentL1 = 'level' + str(p)
    parentL2 = 'level' + str(p + 1)
    df = df.merge(df_titles, how='left', left_on=parentL1, right_on='uri')
    df = df.rename(columns={'uri_x': 'uri', 'title_y': parentL1 + 'Title',
                            'parent': parentL2})
    del df['uri_y']
    print(df.head(10))

print(df.head(15))
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
df.to_csv('hierarchyForResource' + resourceID + '_' + dt + '.csv', index=False)

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))