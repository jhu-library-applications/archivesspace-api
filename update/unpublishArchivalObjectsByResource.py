import json
import requests
import secret
import time
import csv
from datetime import datetime

secretVersion = input('To edit production server, enter secret filename: ')
if secretVersion != '':
    try:
        secret = __import__(secretVersion)
        print('Editing Production')
    except ImportError:
        print('Editing Development')
else:
    print('Editing Development')

startTime = time.time()


def find_key(d, key):
    if key in d:
        yield d[key]
    for k in d:
        if isinstance(d[k], list) and k == 'children':
            for i in d[k]:
                for j in find_key(i, key):
                    yield j


baseURL = secret.baseURL
user = secret.user
password = secret.password
repository = secret.repository

auth = requests.post(baseURL+'/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}

resource_id = input('Enter resource ID: ')

treeEndpoint = '/repositories/'+repository+'/resources/'+str(resource_id)+'/tree'

output = requests.get(baseURL + treeEndpoint, headers=headers).json()
archivalObjects = []
for value in find_key(output, 'record_uri'):
    if 'archival_objects' in value:
        archivalObjects.append(value)
print(archivalObjects)

dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')

f = csv.writer(open('unpublishedAOs_'+dt+'.csv', 'w'))
f.writerow(['uri']+['post'])

for archivalObject in archivalObjects:
    output = requests.get(baseURL+archivalObject, headers=headers).json()
    output['publish'] = False
    asRecord = json.dumps(output)
    post = requests.post(baseURL+archivalObject, headers=headers,
                         data=asRecord).json()
    post = json.dumps(post)
    print(post)
    f.writerow([archivalObject]+[post])

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))