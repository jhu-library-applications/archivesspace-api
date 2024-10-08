import json
import requests
import secret
import time
import csv

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

auth = requests.post(baseURL+'/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}

f = csv.writer(open('resourceProperties.csv', 'w'))
f.writerow(['title']+['uri']+['bibnum']+['entity_type']+['value'])

resource_id = input('Enter resource ID: ')
endpoint = '/repositories/3/resources/' + resource_id
output = requests.get(baseURL + endpoint, headers=headers).json()
print(json.dumps(output))

title = output['title']
uri = output['uri']
try:
    bibnum = output['user_defined']['real_1']
except:
    bibnum = ''
try:
    agents = output['linked_agents']
    for agent in agents:
        agentUri = agent['ref']
        agentOutput = requests.get(baseURL + agentUri, headers=headers).json()
        agentName = agentOutput['title']
        f.writerow([title]+[uri]+[bibnum]+['name']+[agentName])
except:
    pass
try:
    subjects = output['subjects']
    for subject in subjects:
        subjectUri = subject['ref']
        subjectOutput = requests.get(baseURL + subjectUri, headers=headers).json()
        subjectName = subjectOutput['title']
        f.writerow([title]+[uri]+[bibnum]+['subject']+[subjectName])
except:
    pass
for note in output['notes']:
    abstract = ''
    scopecontent = ''
    acqinfo = ''
    custodhist = ''
    if note['entity_type'] == 'abstract':
        abstract = note['content'][0]

        f.writerow([title]+[uri]+[bibnum]+['abstract']+[abstract])
    if note['entity_type'] == 'scopecontent':
        scopecontentSubnotes = note['subnotes']
        for subnote in scopecontentSubnotes:
            scopecontent = scopecontent + subnote['content'] + ' '
        f.writerow([title]+[uri]+[bibnum]+['scopecontent']+[scopecontent])
    if note['entity_type'] == 'acqinfo':
        acqinfoSubnotes = note['subnotes']
        for subnote in acqinfoSubnotes:
            acqinfo = acqinfo + subnote['content'] + ' '
        f.writerow([title]+[uri]+[bibnum]+['acqinfo']+[acqinfo])
    if note['entity_type'] == 'custodhist':
        custodhistSubnotes = note['subnotes']
        for subnote in custodhistSubnotes:
            custodhist = custodhist + subnote['content'] + ' '
        f.writerow([title]+[uri]+[bibnum]+['custodhist']+[custodhist])

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))