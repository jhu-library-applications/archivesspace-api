import json
import requests
import csv
import secrets
import time
from datetime import datetime

secretsVersion = input('To edit production server, enter secrets filename: ')
if secretsVersion != '':
    try:
        secrets = __import__(secretsVersion)
        print('Editing Production')
    except ImportError:
        print('Editing Development')
else:
    print('Editing Development')

startTime = time.time()

baseURL = secrets.baseURL
user = secrets.user
password = secrets.password
repository = secrets.repository

targetFile = input('Enter file name: ')

auth = requests.post(baseURL+'/users/'+user+'/login?password='+password).json()
session = auth['session']
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}

dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')

f = csv.writer(open('postNewCorporateAgents_'+dt+'.csv', 'w'))
f.writerow(['sortName']+['uri'])

csvfile = csv.DictReader(open(targetFile))

for row in csvfile:
    agentRecord = {}
    names = []
    name = {'primary_name': row['primary'], 'sort_name': row['sortName'], 'jsonmodel_type': 'name_corporate_entity',
            'name_order': 'direct', 'rules': 'rda'}
    try:
        name['subordinate_name_1'] = row['subordinate_1']
    except KeyError:
        pass
    try:
        name['subordinate_name_2'] = row['subordinate_2']
    except KeyError:
        pass
    try:
        name['authority_id'] = row['authorityID']
        name['source'] = 'viaf'
    except KeyError:
        pass
    names.append(name)
    agentRecord['names'] = names
    agentRecord['publish'] = True
    agentRecord['jsonmodel_type'] = 'agent_corporate_entity'
    agentRecord = json.dumps(agentRecord)
    post = requests.post(baseURL+'/agents/corporate_entities', headers=headers,
                         data=agentRecord).json()
    print(json.dumps(post))
    uri = post['uri']
    f.writerow([row['sortName']]+[uri])

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))