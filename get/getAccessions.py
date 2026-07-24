"""Retrieves all accessions from a particular repository into a JSON file.
"""

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

base_url = secret.base_url
user = secret.user
password = secret.password
repository = secret.repository

auth = requests.post(base_url + '/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}
print('authenticated')

repository = str(repository)
endpoint = '/repositories/'+repository+'/accessions?all_ids=true'

accession_ids = requests.get(base_url+endpoint, headers=headers).json()

records = []
for accession in accession_ids:
    endpoint = '/repositories/'+repository+'/accessions/'+str(accession)
    output = requests.get(base_url + endpoint, headers=headers).json()
    records.append(output)

f = open('accessions.json', 'w')
json.dump(records, f)
f.close()

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))
