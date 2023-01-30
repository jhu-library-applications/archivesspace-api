import json
import requests
import time
import csv
import secret
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

baseURL = secret.baseURL
user = secret.user
password = secret.password
repository = secret.repository

targetFile = input('Enter file name: ')

auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
session = auth['session']
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}

f = csv.writer(open('postNewPersonalAgents'+datetime.now().strftime('%Y-%m-%d %H.%M.%S')+'.csv', 'w'))
f.writerow(['sortName']+['uri'])

csvfile = csv.DictReader(open(targetFile))

for row in csvfile:
    agentRecord = {}
    names = []
    name = {'primary_name': row['primaryName'], 'name_order': 'inverted', 'jsonmodel_type': 'name_person',
            'rules': 'rda', 'sort_name': row['sortName']}
    try:
        name['authority_id'] = row['authorityID']
        name['source'] = 'viaf'
    except KeyError:
        pass
    try:
        name['rest_of_name'] = row['restOfName']
    except KeyError:
        name['name_order'] = 'direct'
    try:
        name['fuller_form'] = row['fullerForm']
    except KeyError:
        pass
    try:
        name['title'] = row['title']
    except KeyError:
        pass
    try:
        name['prefix'] = row['prefix']
    except KeyError:
        pass
    try:
        name['suffix'] = row['suffix']
    except KeyError:
        pass
    try:
        name['dates'] = row['date']
    except KeyError:
        pass
    names.append(name)

    if row['date'] != '':
        dates = []
        date = {'label': 'existence', 'jsonmodel_type': 'date'}
        if row['expression'] != '':
            date['expression'] = row['expression']
            date['date_type'] = 'single'
        elif row['begin'] != '' and row['end'] != '':
            date['begin'] = row['begin']
            date['end'] = row['end']
            date['date_type'] = 'range'
        elif row['begin'] != '':
            date['begin'] = row['begin']
            date['date_type'] = 'single'
        elif row['end'] != '':
            date['end'] = row['end']
            date['date_type'] = 'single'
        dates.append(date)
        agentRecord['dates_of_existence'] = dates
        print(dates)
    agentRecord['names'] = names
    agentRecord['publish'] = True
    agentRecord['jsonmodel_type'] = 'agent_person'
    agentRecord = json.dumps(agentRecord)
    print(agentRecord)
    post = requests.post(baseURL + '/agents/people', headers=headers, data=agentRecord).json()
    print(json.dumps(post))
    uri = post['uri']
    f.writerow([row['sortName']]+[uri])

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))