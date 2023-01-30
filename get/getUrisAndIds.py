import requests
import secret
import pandas as pd
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

baseURL = secret.baseURL
user = secret.user
password = secret.password
repository = secret.repository

auth = requests.post(baseURL+'/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session': session, 'Content_Type': 'application/json'}

recordType = input('Enter either \'resources\' or \'accessions\': ')

endpoint = '/repositories/'+repository+'/'+recordType+'?all_ids=true'

ids = requests.get(baseURL+endpoint, headers=headers).json()

total = len(ids)
allItems = []
for id in ids:
    print('a_id', id, total, recordType, ' remaining')
    total = total - 1
    idDict = {}
    endpoint = '/repositories/'+repository+'/'+recordType+'/'+str(id)
    idDict['uri'] = endpoint
    output = requests.get(baseURL + endpoint, headers=headers).json()
    id_0 = output.get('id_0')
    id_1 = output.get('id_1')
    id_2 = output.get('id_2')
    id_3 = output.get('id_3')
    if id_0 and id_1 and id_2 and id_3:
        ConCatID = id_0+'.'+id_1+'.'+id_2+'.'+id_3
        idDict['ConCatID'] = ConCatID
    idDict['id_0'] = id_0
    idDict['id_1'] = id_1
    idDict['id_2'] = id_3
    idDict['id_3'] = id_3
    allItems.append(idDict)

df = pd.DataFrame.from_dict(allItems)
print(df.head(15))
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
df.to_csv(recordType+'_'+dt+'UrisAndIds.csv', index=False)


elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))