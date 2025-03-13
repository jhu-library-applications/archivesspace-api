import requests
import secret
import argparse
import pandas as pd
from datetime import datetime
import time

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--entity',
                    help='options: people, corporate_entities, families')
args = parser.parse_args()

if args.entity:
    type_entity = args.entity
    print(type_entity)
else:
    type_entity = input('options: people, corporate_entities, families')

startTime = time.time()

baseURL = secret.baseURL
user = secret.user
password = secret.password
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
all_items = []
for e_id in ids:
    print('a_id', e_id, total, 'records remaining')
    total -= 1
    endpoint = '/agents/'+type_entity+'/'+str(e_id)
    output = requests.get(baseURL + endpoint, headers=headers).json()
    id_dict = {}
    uri = output['uri']
    id_dict['uri'] = uri
    zeroName = output['names'][0]
    name = zeroName['sort_name'].strip()
    id_dict['name'] = name
    create_time = output['create_time']
    id_dict['create_time'] = create_time
    created_by = output.get('created_by')
    id_dict['created_by'] = created_by
    rules = zeroName.get('rules')
    id_dict['rules'] = rules
    publish = output.get('publish')
    if publish is False:
        id_dict['publish'] = publish
        all_items.append(id_dict)

df = pd.DataFrame.from_records(all_items)
print(df.head(15))
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
df.to_csv('notPublished'+type_entity+'_'+dt+'.csv', index=False)


elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))
