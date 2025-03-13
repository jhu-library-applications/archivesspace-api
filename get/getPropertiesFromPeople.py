import requests
import secret
import pandas as pd
from datetime import datetime
import time

secretVersion = input('To edit production server, enter secret file name: ')
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
print('authenticated')

endpoint = '/agents/people?all_ids=true'

ids = requests.get(baseURL+endpoint, headers=headers).json()
print(len(ids))

all_items = []
for a_id in ids:
    print(a_id)
    endpoint = '/agents/people/'+str(a_id)
    output = requests.get(baseURL+endpoint, headers=headers).json()
    id_dict = {}
    uri = output['uri']
    sort_name = output['names'][0]['sort_name']
    authority_id = output['names'][0].get('authority_id', '')
    id_dict['uri'] = uri
    id_dict['sort_name'] = sort_name
    id_dict['authority_id'] = authority_id
    all_items.append(id_dict)

df = pd.DataFrame.from_records(all_items)
print(df.head(15))
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
df.to_csv('peopleProperties_'+dt+'.csv', index=False)

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))
