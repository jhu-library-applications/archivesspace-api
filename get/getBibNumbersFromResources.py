import requests
import secret
import time
import pandas as pd
from datetime import datetime

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

base_url = secret.base_url
user = secret.user
password = secret.password
repository = secret.repository

auth = requests.post(base_url+'/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session': session,
           'Content_Type': 'application/json'}

repository = str(repository)
endpoint = '/repositories/'+repository+'/resources?all_ids=true'
ids = requests.get(base_url+endpoint, headers=headers).json()

total = len(ids)
all_items = []
for r_id in ids:
    print('a_id', r_id, total, 'resources remaining')
    total -= 1
    endpoint = '/repositories/'+repository+'/resources/'+str(id)
    output = requests.get(base_url+endpoint, headers=headers).json()
    id_dict = {}
    title = output['title']
    id_dict['title'] = title
    uri = output['uri']
    id_dict['uri'] = uri
    date_modified = output['user_mtime']
    publish = output['publish']
    suppressed = output['suppressed']
    id_dict['date_modified'] = date_modified
    id_dict['publish'] = publish
    id_dict['suppressed'] = suppressed
    user_defined = output.get('user_defined')
    if user_defined:
        bib_number = user_defined.get('real_1')
        id_dict['bib'] = bib_number
    else:
        pass
    all_items.append(id_dict)

df = pd.DataFrame.from_records(all_items)
print(df.head(15))
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
df.to_csv('aspaceResourcesBib_'+dt+'.csv', index=False)


elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))
