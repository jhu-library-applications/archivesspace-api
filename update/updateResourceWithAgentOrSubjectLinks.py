import json
import requests
import secrets
import time
import csv
import argparse
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

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--type', help='Type of link ("subject" or "agent")')
args = parser.parse_args()

if args.type:
    entity_type = args.type
else:
    entity_type = input('Enter the type of links to create ("subject" or "agent"): ')


def add_uri_link(key, value_source):
    uri = '/repositories/'+repository+'/resources/'+row['ResourceUri']
    value = row[value_source]
    print(value)
    as_record = requests.get(baseURL+uri, headers=headers).json()
    updated_record = as_record
    if key == 'subjects':
        subjects = updated_record['subjects']
        subject = {'ref': value}
        if subject not in subjects:
            subjects.append(subject)
            updated_record['subjects'] = subjects
            print(updated_record['subjects'])
            updated_record = json.dumps(updated_record)
            link = baseURL+uri
            print(link)
            post = requests.post(link, headers=headers,
                                 data=updated_record).json()
            print(post)
            f.writerow([uri]+[subjects]+[post])
        else:
            print('no update')
            f.writerow([uri]+['no update']+[])
    elif key == 'linked_agents':
        agents = updated_record['linked_agents']
        print('originalAgents')
        print(agents)
        agent = {'terms': [], 'ref': value}
        if row['tag'].startswith('1'):
            agent['role'] = 'creator'
        elif row['tag'].startswith('7'):
            agent['role'] = 'creator'
        elif row['tag'].startswith('6'):
            agent['role'] = 'subject'
        else:
            print('error')
            f.writerow([uri]+['tag error']+[])
        if agent not in agents:
            agents.append(agent)
            print('updatedAgents')
            print(agents)
            updated_record['linked_agents'] = agents
            updated_record = json.dumps(updated_record)
            print(baseURL + uri)
            post = requests.post(baseURL+uri, headers=headers, data=updated_record).json()
            print(post)
            f.writerow([uri]+[agents]+[post])
        else:
            print('no update')
            print(agent)
            f.writerow([uri]+['no update']+[])
    else:
        print('error')
        f.writerow([uri]+['error']+[])


startTime = time.time()

baseURL = secrets.baseURL
user = secrets.user
password = secrets.password
repository = secrets.repository

auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}

filename = input('Enter filename (including \'.csv\'): ')

dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')

f = csv.writer(open(filename+'Post'+dt+'.csv', 'w'))
f.writerow(['uri']+['links']+['post'])

with open(filename) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if entity_type == 'agent':
            add_uri_link('linked_agents', 'agentUri')
        elif entity_type == 'subject':
            add_uri_link('subjects', 'subjectUri')
        else:
            f.writerow(['error - invalid type entered (should be "subject" or "agent")']+[]+[])
            print('error - invalid type entered (should be "subject" or "agent")')
            break

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))