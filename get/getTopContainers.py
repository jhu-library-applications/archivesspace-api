import json
import requests
import secret
import time

secretVersion = input('To edit production server, enter secret file name: ')
if secretVersion != '':
    try:
        secret = __import__(secretVersion)
        print('Editing Production')
    except ImportError:
        print('Editing Development')
else:
    print('Editing Development')

startTime = time.time()

baseURL = secret.baseURL
user = secret.user
password = secret.password
repository = secret.repository

auth = requests.post(baseURL+'/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}
print('authenticated')

endpoint = '/repositories/'+repository+'/top_containers?all_ids=true'

ids = requests.get(baseURL + endpoint, headers=headers).json()
print(len(ids))

records = []
for tc_id in ids:
    print(id)
    endpoint = '/repositories/'+repository+'/top_containers/'+str(tc_id)
    output = requests.get(baseURL + endpoint, headers=headers).json()
    records.append(output)

f = open('topContainers.json', 'w')
json.dump(records, f)
f.close()

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))