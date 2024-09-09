import json
import requests
from datetime import datetime
import time
import argparse
import secret
import pandas as pd
import urllib3

startTime = time.time()

secretVersion = input('To edit production server, enter secret filename: ')
if secretVersion != '':
    try:
        secret = __import__(secretVersion)
        print('Editing Production')
    except ImportError:
        print('Editing Development')
else:
    print('Editing Development')

# import secret
baseURL = secret.baseURL
user = secret.user
password = secret.password
repo = secret.repository
verify = secret.verify

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='filename to retrieve')
args = parser.parse_args()

if args.file:
    filename = args.file
else:
    filename = input('Enter file name as filename.csv: ')

s = requests.Session()

# authenticate
auth = s.post(baseURL+'/users/'+user+'/login?password='+password, verify=verify).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session': session,
           'Content_Type': 'application/json'}

df = pd.read_csv(filename)
total_count = len(df)

log = []
for count, row in df.iterrows():
    row = row
    itemLog = row
    uri = row['uri']
    csv_title = row['title']
    ao_link = baseURL+uri
    try:
        ao_object = s.get(ao_link, headers=headers, verify=verify).json()
    except requests.exceptions.RequestException as e:
        itemLog['error'] = e
        print(e)
        log.append(itemLog)
        continue
    title = ao_object['title']
    print('Item {} retrieved, number {} of {}'.format(uri, count+1, total_count))
    if csv_title == title:
        linked_agents = ao_object['linked_agents']
        print('Title verified')
    else:
        title_error = 'Incorrect title {}'.format(title)
        print(title_error)
        itemLog['error'] = title_error
        log.append(itemLog)
        continue
    if not linked_agents:
        csv_agents = row['linked_agents']
        csv_agents = csv_agents.split('||')
        new_agents = []
        for agent in csv_agents:
            agent_parts = agent.split(';;')
            role = agent_parts[0]
            ref = agent_parts[1]
            new_agent = {'role': role,
                         'ref': ref}
            new_agents.append(new_agent)
    else:
        error = 'Linked agents already exist.'
        print(error)
        itemLog['error'] = error
        itemLog['api_agents'] = linked_agents
        log.append(itemLog)
        continue
    ao_object['linked_agents'] = new_agents
    ao_object = json.dumps(ao_object)
    try:
        post = s.post(ao_link, headers=headers, verify=verify, data=ao_object).json()
    except requests.exceptions.RequestException as e:
        itemLog['error'] = e
        print(e)
    status = post['status']
    itemLog['post_status'] = status
    print(status)
    log.append(itemLog)

log = pd.DataFrame.from_dict(log)
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
log.to_csv('logOfUpdatedAO_'+dt+'.csv', index=False)

# Show script runtime
elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Post complete.  Total script run time: ', '%d:%02d:%02d' % (h, m, s))