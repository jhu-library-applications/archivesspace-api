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
parser.add_argument('-f', '--file', help='filename to retrieve')
args = parser.parse_args()

if args.file:
    filename = args.file
else:
    filename = input('Enter filename: ')

startTime = time.time()

base_url = secret.base_url
user = secret.user
password = secret.password
repository = secret.repository
repository = str(repository)
auth = requests.post(base_url+'/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}


df = pd.read_csv(filename)

log = []
for count, row in df.iterrows():
    archival_id = row['archival_id']
    archival_id = str(archival_id)
    endpoint = '/repositories/'+repository+'/archival_objects/'+archival_id+'/children'
    print(endpoint)
    output = requests.get(base_url+endpoint, headers=headers).json()
    total_objects = len(output)
    for object_count, child in enumerate(output):
        object_log = {}
        print('{} of {}'.format(object_count+1, total_objects))
        parent = child['parent']['ref']
        title = child['title']
        uri = child['uri']
        object_log = {'parent': parent, 'title': title, 'uri': uri}
        log.append(object_log)

df = pd.DataFrame.from_records(log)
print(df.head)
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
df.to_csv('archival_objects_'+dt+'.csv', index=False)
