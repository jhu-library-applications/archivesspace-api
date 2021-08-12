import requests
import secrets
import argparse
import pandas as pd
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--entity', help='options: people, corporate_entites, families')
args = parser.parse_args()

if args.entity:
    type_entity = args.entity
    print(type_entity)
else:
    type_entity = input('options: people, corporate_entites, families: ')

baseURL = secrets.baseURL
user = secrets.user
password = secrets.password
print(baseURL + '/users/'+user)
auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
print(auth)
session = auth["session"]
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}
print('authenticated')

endpoint = '/agents/'+type_entity+'?all_ids=true'
print(endpoint)

ids = requests.get(baseURL + endpoint, headers=headers).json()

total = len(ids)
allItems = []
for id in ids:
    print('id', id, total, 'records remaining')
    total = total - 1
    endpoint = '/agents/'+type_entity+'/'+str(id)
    output = requests.get(baseURL + endpoint, headers=headers).json()
    idDict = {}
    uri = output['uri']
    idDict['uri'] = uri
    zeroName = output['names'][0]
    name = zeroName['sort_name'].strip()
    idDict['name'] = name
    create_time = output['create_time']
    idDict['create_time'] = create_time
    created_by = output.get('created_by')
    idDict['created_by'] = created_by
    rules = zeroName.get('rules')
    idDict['rules'] = rules
    publish = output.get('publish')
    if publish is False:
        idDict['publish'] = publish
        allItems.append(idDict)

df = pd.DataFrame.from_dict(allItems)
print(df.head(15))
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
df.to_csv('notPublished'+type_entity+'_'+dt+'.csv', index=False)


elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))
