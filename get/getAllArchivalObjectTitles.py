import requests
import secrets
import time
import pandas as pd
from datetime import datetime

secretsVersion = input('To edit production server, enter the name of the secrets file: ')
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

auth = requests.post(baseURL + '/users/' + user + '/login?password=' + password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}
print('authenticated')

endpoint = '/repositories/' + repository + '/archival_objects?all_ids=true'

ids = requests.get(baseURL + endpoint, headers=headers).json()
print(len(ids))

allItems = []
for r_id in ids:
    print(r_id)
    endpoint = '/repositories/' + repository + '/archival_objects/' + str(id)
    output = requests.get(baseURL + endpoint, headers=headers).json()
    title = output.get('title')
    uri = output.get('uri')
    print(title, uri)
    idDict = {'uri': uri, 'title': title}
    allItems.append(idDict)

df = pd.DataFrame.from_dict(allItems)
print(df.head(15))
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
df.to_csv('aspaceResourcesBib_' + dt + '.csv', index=False)

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))