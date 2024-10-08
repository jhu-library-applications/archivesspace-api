import json
import requests
import secret
import csv
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

endpoint = '/agents/people?all_ids=true'

ids = requests.get(baseURL + endpoint, headers=headers).json()

records = []
for agent_id in ids:
    endpoint = '/agents/people/'+str(agent_id)
    output = requests.get(baseURL + endpoint, headers=headers).json()
    records.append(output)

f = csv.writer(open('asArrayResults.csv', 'w'))
f.writerow(['uri']+['begin']+['end']+['expression'])
for i in range(0, len(records)):
    for j in range(0, len(records[i]['dates_of_existence'])):
        uri = records[i]['uri']
        beginDate = records[i]['dates_of_existence'][j].get('begin', 'none')
        endDate = records[i]['dates_of_existence'][j].get('end', 'none')
        expressionDate = records[i]['dates_of_existence'][j].get('expression', 'none')
        f.writerow([uri]+[beginDate]+[endDate]+[expressionDate])

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))