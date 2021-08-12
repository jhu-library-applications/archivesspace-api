import requests
import secrets
import time
import pandas as pd
from datetime import datetime

secretsVersion = input('To edit production server, enter secrets file name: ')
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

auth = requests.post(baseURL+'/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session': session,
           'Content_Type': 'application/json'}

endpoint = '/repositories/'+repository+'/resources?all_ids=true'
ids = requests.get(baseURL + endpoint, headers=headers).json()

total = len(ids)
allItems = []
for id in ids:
    print('id', id, total, 'resources remaining')
    total = total - 1
    endpoint = '/repositories/'+repository+'/resources/'+str(id)
    output = requests.get(baseURL + endpoint, headers=headers).json()
    idDict = {}
    title = output['title']
    idDict['title'] = title
    uri = output['uri']
    idDict['uri'] = uri
    date_modified = output['user_mtime']
    publish = output['publish']
    suppresed = output['suppressed']
    idDict['date_modified'] = date_modified
    idDict['publish'] = publish
    idDict['supressed'] = suppresed
    user_defined = output.get('user_defined')
    if user_defined:
        bibnum = user_defined.get('real_1')
        idDict['bib'] = bibnum
    else:
        pass
    allItems.append(idDict)

df = pd.DataFrame.from_dict(allItems)
print(df.head(15))
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
df.to_csv('aspaceResourcesBib_'+dt+'.csv', index=False)


elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))
