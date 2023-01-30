import json
import requests
import secret
import time

secretVersion = input('To edit production server, enter the name of the secret file: ')
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

auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}
print('authenticated')

endpoint = '/repositories/'+repository+'/accessions?all_ids=true'

ids = requests.get(baseURL + endpoint, headers=headers).json()

records = []
for a_id in ids:
    endpoint = '/repositories/'+repository+'/accessions/'+str(a_id)
    output = requests.get(baseURL + endpoint, headers=headers).json()
    records.append(output)

f = open('accessions.json', 'w')
json.dump(records, f)
f.close()

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))